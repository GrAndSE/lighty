from ..utils import with_metaclass
from ..monads import NoneMonad
from . import fields, query
from .backend import manager


def get_attr_source(name, cls):
    '''Helper method used to get the class where atribute was defined first
    '''
    for src_cls in cls.mro():
        if name in src_cls.__dict__:
            return src_cls


class ModelBase(type):
    """Metaclass used to ORM class generation from definitions
    """

    def __new__(cls, name, bases, attrs):
        """Process new class used ModelBase as metaclass.


        """
        super_new = super(ModelBase, cls).__new__
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super_new(cls, name, bases, attrs)
        # Get attributers
        new_attrs = {}
        new_attrs['_fields'] = set()
        field_source = {}
        defined = set()
        for parent in parents:
            if hasattr(parent, '_fields'):
                duplicate_field_keys = defined & parent._fields
                for dupe_field_name in duplicate_field_keys:
                    field_source[dupe_field_name] = get_attr_source(
                                dupe_field_name, field_source[dupe_field_name])
                    old_source = field_source[dupe_field_name]
                    new_source = get_attr_source(dupe_field_name, parent)
                    if old_source != new_source:
                        raise AttributeError('Duplicate field, %s, is '
                                    'inherited from both %s and %s.' % (
                                        dupe_field_name, old_source.__name__,
                                        new_source.__name__))
                defined |= parent._fields
                field_source.update(dict.fromkeys(parent._fields, parent))
                new_attrs.update([(field_name, getattr(parent, field_name))
                                  for field_name in parent._fields])

        new_attrs['_key_name'] = '_id'

        for attr_name in attrs.keys():
            attr = attrs[attr_name]
            if isinstance(attr, fields.Field):
                if attr_name in defined:
                    raise AttributeError('Duplicate field: %s. It was defined '
                                'in %s already' % (attr_name,
                                    get_attr_source(attr_name,
                                                    field_source[attr_name])))
                defined.add(attr_name)
                attr.configure(name, attr_name)
            new_attrs[attr_name] = attr

        new_attrs['_fields'] = defined

        # Initialize properties
        new_attrs['_unindexed_properties'] = frozenset(
            new_attrs[field].name for field in new_attrs['_fields']
            if not (new_attrs[field].primary_key or new_attrs[field].db_index))

        # Create class instance
        return super_new(cls, name, bases, new_attrs)


class Model(with_metaclass(ModelBase)):
    """Model is the superclass of all object entities in the datastore.

    The programming model is to declare Python subclasses of the Model class,
    declaring datastore properties as class members of that class.
    So if you want to publish a story with title, body, and created date, you
    would do it like this:

        class Story(db.Model):
            title = db.CharField(max_length=255)
            body = db.TextField()
            created = db.DateTimeField(auto_now_add=True)
    """
    _datastore_name = 'default'
    '''Name of datastore where t put the values'''

    def __init__(self, is_new=True, **kwds):
        """Creates a new instance of this model.

        To create a new entity, you instantiate a model and then call put(),
        which saves the entity to the datastore:

            person = Person()
            person.name = 'Bret'
            person.put()

        You can initialize properties in the model in the constructor with
        keyword arguments:

            person = Person(name='Bret')

        We initialize all other properties to the default value (as defined by
        the properties in the model definition) if they are not provided in the
        constructor.

        Args:
            is_new:     Indicates all the newly created objects.
            kwds:       Keyword arguments mapping to properties of model.
        """
        self._app = None
        self._is_saved = not is_new or self._key_name in kwds
        cls_dict = self.__class__.__dict__
        for field_name in self._fields:
            value = (kwds[field_name] if field_name in kwds
                     else cls_dict[field_name].default)
            setattr(self, field_name, value)
        if self._is_saved:
            setattr(self, self._key_name, kwds[self._key_name])
        self.datastore = self.__class__.datastore()

    @classmethod
    def datastore(cls):
        return manager.get(cls._datastore_name)

    def is_saved(self):
        '''Check is model was saved
        '''
        return self._is_saved

    def key(self):
        """Unique key for this entity.

        This property is only available if this entity is already stored in the
        datastore or if it has a full key, so it is available if this entity
        was fetched returned from a query, or after put() is called the first
        time for new entities, or if a complete key was given when constructed.

        Returns:
            Datastore key of persisted entity.

        Raises:
            AttributeError when entity is not persistent.
        """
        if self._is_saved:
            return self.__dict__[self._key_name]
        raise AttributeError('Key is not set for entity')

    def put(self):
        """Writes this model instance to the datastore.

        If this instance is new, we add an entity to the datastore.
        Otherwise, we update this instance, and the key will remain the same.

        Returns:
            The key of the instance (either the existing key or a new key).
        """
        cls_dict = self.__class__.__dict__
        fields = dict([(field_name,
                        cls_dict[field_name].get_value_for_datastore(self))
                       for field_name in self._fields
                       if self._is_saved or cls_dict[field_name].editable])
        if self._is_saved:
            fields[self._key_name] = self.key()
        setattr(self, self._key_name,
                self.datastore.put(self.__class__, fields))
        self._is_saved = True
        return self
    save = put

    def delete(self):
        """Deletes this entity from the datastore
        """
        return self.datastore.delete(self, **{self._key_name: self.key()})

    @classmethod
    def entity_name(cls):
        '''Get the table name
        '''
        return (hasattr(cls, '_app') and '%s_%s' % (cls._app, cls.__name__) or
                cls.__name__)

    @classmethod
    def get(cls, _key=None, **keys):
        """Fetch instance from the datastore of a specific Model type using
        key.

        We support Key objects and string keys (we convert them to Key objects
        automatically).

        Useful for ensuring that specific instance types are retrieved from the
        datastore.  It also helps that the source code clearly indicates what
        kind of object is being retreived.  Example:

            story = Story.get(story_key)

        Args:
            keys: Key within datastore entity collection to find; or string
            key; or list of Keys or string keys.

        Returns:
            a Model instance associated with key for
            provided class if it exists in the datastore, otherwise NoneMonad;
        """
        if _key:
            keys[cls._key_name] = _key
        for key in keys:
            if isinstance(keys[key], NoneMonad):
                return keys[key]
        if len(keys) == 0:
            return NoneMonad('Item not found')
        item = cls.datastore().get(cls, keys)
        cls_dict = cls.__dict__
        if item:
            kwargs = {}
            for field_name in item:
                if field_name in cls._fields:
                    make_val = cls_dict[field_name].make_value_from_datastore
                    kwargs[field_name] = make_val(item[field_name])
                else:
                    kwargs[field_name] = item[field_name]
            return cls(is_new=False, **kwargs)
        else:
            return (item if isinstance(item, NoneMonad) else
                    NoneMonad('Item not found for: %s' % keys))

    @classmethod
    def all(cls):
        """Returns a query over all instances of this model from the datastore.

        Returns:
            Query that will retrieve all instances from entity collection.
        """
        return query.Query(model=cls)

    @classmethod
    def fields(cls):
        """Get fields list
        """
        return cls._fields
    properties = fields

    @classmethod
    def validators(cls):
        '''Get a dictinary view contains validators for fields
        '''
        return dict([(field_name, getattr(cls, field_name).validators)
                     for field_name in cls._fields])
