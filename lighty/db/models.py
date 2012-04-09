import fields, query
from backend import datastore


class DuplicateFieldError(Exception):
    '''Error thrown when there are two different fields with the same name
    '''
    pass

class TransactionFailedError(Exception):
    '''Error thrown when datastore transaction failed
    '''
    pass

class NotSavedError(Exception):
    '''Thrown when trying to get key for object was not stored in database
    '''
    pass


class ModelBase(type):
    """Metaclass used to ORM class generation from definitions
    """

    def __new__(cls, name, bases, attrs):
        """
        """
        super_new = super(ModelBase, cls).__new__
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super_new(cls, name, bases, attrs)
        # 
        new_attrs = {}
        new_attrs['_fields'] = set()
        field_source = {}

        def get_attr_source(name, cls):
            for src_cls in cls.mro():
                if name in src_cls.__dict__:
                    return src_cls

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
                        raise DuplicateFieldError('Duplicate field, %s, is '
                                'inherited from both %s and %s.'
                                % (dupe_field_name, old_source.__name__, 
                                new_source.__name__))
                defined |= parent._fields
                field_source.update(dict.fromkeys(parent._fields, parent))
                new_attrs.update(parent._fields)

        new_attrs['_key_name']  = None

        for attr_name in attrs.keys():
            attr = attrs[attr_name]
            if isinstance(attr, fields.Field):
                if attr_name in defined:
                    raise DuplicateFieldError('Duplicate field: %s. It was ' 
                                'defined in %s already' % (attr_name, 
                                get_attr_source(attr_name, 
                                                field_source[attr_name])))
                defined.add(attr_name)
                attr.__config__(name, attr_name)
            new_attrs[attr_name] = attr

        new_attrs['_fields'] = defined

        # Initialize properties
        new_attrs['_unindexed_properties'] = frozenset(
            new_attrs[field].name for field in new_attrs['_fields']
            if not (new_attrs[field].primary_key or new_attrs[field].db_index))

        # Create class instance
        return super_new(cls, name, bases, new_attrs)


class Model(object):
    """Model is the superclass of all object entities in the datastore.

    The programming model is to declare Python subclasses of the Model class,
    declaring datastore properties as class members of that class.  
    So if you want to publish a story with title, body, and created date, you 
    would do it like this:

        class Story(db.Model):
            title   = db.CharField(max_length=255)
            body    = db.TextField()
            created = db.DateTimeField(auto_now_add=True)
    """

    __metaclass__ = ModelBase


    def __init__(self, key_name=None, is_new=True, **kwds):
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
            key_name:   Name for new model instance.
            is_new:     Indicates all the newly created objects.
            kwds:       Keyword arguments mapping to properties of model.  
        """
        self._app       = None
        self._key_name  = key_name or '_id'
        self._is_saved  = not is_new
        # Update value
        self.__dict__.update(kwds)
        # Set the default values for unsetted fields
        cls = self.__class__
        for field_name in self._fields:
            if field_name not in kwds:
                self.__dict__[field_name] = cls.__dict__[field_name].default

    def key(self):
        """Unique key for this entity.

        This property is only available if this entity is already stored in the
        datastore or if it has a full key, so it is available if this entity was
        fetched returned from a query, or after put() is called the first time
        for new entities, or if a complete key was given when constructed.

        Returns:
            Datastore key of persisted entity.

        Raises:
            NotSavedError when entity is not persistent.
        """
        if self._is_saved:
            return self.__dict__[self._key_name]
        raise NotSavedError()

    def put(self):
        """Writes this model instance to the datastore.

        If this instance is new, we add an entity to the datastore.
        Otherwise, we update this instance, and the key will remain the same.

        Returns:
            The key of the instance (either the existing key or a new key).

        Raises:
            TransactionFailedError if the data could not be committed.
        """
        fields = dict([(field, self.__dict__[field]) 
                       for field in self._fields])
        datastore.put(self.__class__, fields)
        return self
    save = put

    def delete(self, **kwargs):
        """Deletes this entity from the datastore.

        Args:
            config: datastore_rpc.Configuration to use for this request.

        Raises:
            TransactionFailedError if the data could not be committed.
        """
        raise NotImplemented

    @classmethod
    def entity_name(cls):
        '''Get the table name
        '''
        return (hasattr(cls, '_app') and '%s_%s' % (cls._app, cls.__name__) or
                cls.__name__)

    @classmethod
    def get(cls, keys):
        """Fetch instance from the datastore of a specific Model type using 
        key.

        We support Key objects and string keys (we convert them to Key objects
        automatically).

        Useful for ensuring that specific instance types are retrieved from the
        datastore.  It also helps that the source code clearly indicates what
        kind of object is being retreived.  Example:

            story = Story.get(story_key)

        Args:
            keys: Key within datastore entity collection to find; or string key;
            or list of Keys or string keys.

        Returns:
            If a single key was given: a Model instance associated with key for 
            provided class if it exists in the datastore, otherwise None; 
            if a list of keys was given: a list whose items are either a Model 
            instance or None.
        """
        raise NotImplemented

    @classmethod
    def all(cls, **kwds):
        """Returns a query over all instances of this model from the datastore.

        Returns:
            Query that will retrieve all instances from entity collection.
        """
        return query.Query(model=cls)

    @classmethod
    def fields(cls):
        """Get fields list"""
        return cls._fields

    @classmethod
    def properties(cls):
        """Alias for fields."""
        return cls.fields()           
