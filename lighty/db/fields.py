'''All fields described
'''
import lighty.validators

from .functor import BaseField, NumericField, SequenceField


def add_validator(validator, options):
    '''Helper function for adding validator into the validator's list inside
    options dictionary. Written to make some field types constructor shorter.
    '''
    if 'validators' in options:
        if isinstance(options['validators'], list):
            options['validators'].append(validator)
        else:
            options['validators'] += (validator, )
    else:
        options['validators'] = (validator, )
    return options


class Field(BaseField):
    '''Base field class. Declares basic methods an fields for all the field
    classes and fields

    Args:
        verbose_name:   human readable field name
        primary_key:    is field would be a primary key
        db_index:       is field a part of database index
        unique:         add checking for unique value
        blank:          is field can be empty on model saving
        null:           it field can be None on model saving
        choices:        list of values available for this field
        default:        default value
        editable:       check is value can be changed
        validators:     list of validators used to check field value before
                        store it into database
        help_text:      field description
        db_column:      name of the field inside database
        db_tablespace:  can be used to set additional datastorage parameter
    '''
    __slots__ = ('name', 'model', 'verbose_name', 'primary_key', 'db_index',
                 'unique', 'blank', 'null', 'choices', 'default', 'editable',
                 'validators', 'help_text', 'db_column', 'db_tablespace', )

    def __init__(self, verbose_name=None, primary_key=False, db_index=False,
                       unique=False, blank=False, null=False, choices=None,
                       default=None, editable=True, validators=(),
                       help_text="", db_column=None, db_tablespace=False):
        '''Create new Field instance

        '''
        self.null = null
        self.blank = blank
        self.choices = choices
        self.default = default
        self.editable = editable
        self.unique = unique
        self.db_column = db_column
        self.db_tablespace = db_tablespace
        self.db_index = db_index
        self.primary_key = primary_key
        self.help_text = help_text
        self.verbose_name = verbose_name
        # Add additional validator for choices if needed
        if choices is not None:
            validators += (lighty.validators.ChoicesValidator(choices),)
        self.validators = validators

    def __config__(self, model_name, field_name):
        """Configure field with model-depended paramenters

        Args:
            model_name: model class name
            field_name: name of this field
        """
        self.model = model_name
        self.name = field_name

    def get_value_for_datastore(self, model):
        """Get value prepared for saving in datastore

        Args:
            model:  model instance to take value from
        """
        return model.__dict__[self.name]

    def make_value_from_datastore(self, value):
        """Create object from value was taken from datastore
        """
        return value

    def __str__(self):
        '''Get string representation
        '''
        return self.model + '.' + self.name


class FieldDescriptor(Field):
    '''Field that will be used as a descriptor - on creation creates a field
    '_field_name' to store the name of the attribute of the model class
    instance used to store the field value.
    '''

    def __config__(self, model_name, field_name):
        '''Set default value
        '''
        super(FieldDescriptor, self).__config__(model_name, field_name)
        self._field_name = '_field_%s_value' % field_name

    def __get__(self, instance, owner):
        '''Get field value from instance
        '''
        if instance is None:
            return self
        return getattr(instance, self._field_name)

    def __set__(self, instance, value):
        '''Store field value in instance
        '''
        setattr(instance, self._field_name, value)


class IntegerField(FieldDescriptor, NumericField):
    '''An integer. The admin represents this as an <input type="text"> (a
    single-line input).
    '''

    def __set__(self, instance, value):
        '''Set value as int
        '''
        super(IntegerField, self).__set__(instance, int(value))


class PositiveIntegerField(IntegerField):
    '''Like an IntegerField, but must be positive.
    '''

    def __init__(self, **options):
        '''Create new field. Adds validator that checks value to be greater
        than 0 into the validator's list
        '''
        options = add_validator(lighty.validators.MinValueValidator(1),
                                options)
        super(PositiveIntegerField, self).__init__(**options)


class AutoField(IntegerField):
    '''An IntegerField that automatically increments according to available
    IDs. You usually won't need to use this directly; a primary key field will
    automatically be added to your model if you don't specify otherwise. See
    Automatic primary key fields.
    '''


class FloatField(FieldDescriptor, NumericField):
    '''A floating-point number represented in Python by a float instance.

    The admin represents this as an <input type="text"> (a single-line input).
    '''

    def __set__(self, instance, value):
        '''Set value as int
        '''
        super(IntegerField, self).__set__(instance, float(value))


class DecimalField(Field, NumericField):
    '''A fixed-precision decimal number, represented in Python by a Decimal
    instance.

    The admin represents this as an <input type="text"> (a single-line input).
    '''

    def __init__(self, max_digits=None, decimal_places=None, **options):
        '''Create new fixed-precision decimal number

        Args:
            max_digits:     The maximum number of digits allowed in the number
            decimal_places: The number of decimal places to store with the
                number
        '''
        self.max_digits = max_digits
        self.decimal_places = decimal_places
        super(DecimalField, self).__init__(**options)


class BooleanField(FieldDescriptor):
    '''A true/false field

    The admin represents this as a checkbox
    '''
    def __set__(self, instance, value):
        '''Convert value to boolean
        '''
        from ..utils import string_types
        if isinstance(value, string_types):
            value = value == 'True' or value == 'true' or value == 'TRUE'
        elif not isinstance(value, bool):
            value = bool(value)
        super(BooleanField, self).__set__(instance, value)


class NullBooleanField(BooleanField):
    '''Like a BooleanField, but allows NULL as one of the options. Use this
    instead of a BooleanField with null=True. The admin represents this as a
    <select> box with "Unknown", "Yes" and "No" choices.
    '''

    def __init__(self, **options):
        '''Create new BooleanField field with null=True
        '''
        options['null'] = True
        super(NullBooleanField, self).__init__(**options)


class CharField(Field, SequenceField):
    '''A string field, for small- to large-sized strings.

    For large amounts of text, use TextField.

    The admin represents this as an <input type="text"> (a single-line input).
    '''

    def __init__(self, max_length=None, **options):
        '''Create new CharField with one extra required argument:

        Args:
            max_length: The maximum length (in characters) of the field.
            The max_length is enforced at the database level and in validation.
        '''
        # Process max_length option
        if max_length is None:
            max_length = 255
        self.max_length = max_length
        # Add MaxLengthValidator
        options = add_validator(
                    lighty.validators.MaxLengthValidator(max_length), options)
        # Then create usual field
        super(CharField, self).__init__(**options)


class EmailField(CharField):
    '''A CharField that checks that the value is a valid e-mail address.
    '''

    def __init__(self, max_length=75, **options):
        '''Create CharField that checks that the value is a valid e-mail
        address.
        '''
        options = add_validator(lighty.validators.validate_email, options)
        super(EmailField, self).__init__(max_length, **options)


class URLField(CharField):
    '''A CharField for a URL.

    The admin represents this as an <input type="text"> (a single-line input).
    '''

    def __init__(self, verify_exists=True, max_length=200, **options):
        '''Create new CharField to store URL

        Args:
            verify_exists:  If True (the default), the URL given will be
            checked for existence (i.e., the URL actually loads and doesn't
            give a 404 response).

            Note that when you're using the single-threaded development server,
            validating a URL being served by the same server will hang. This
            should not be a problem for multithreaded servers.

            max_length:     Like all CharField subclasses, URLField takes the
            optional max_length, a default of 200 is used.
        '''
        options = add_validator(
                lighty.validators.URLValidator(verify_exists=verify_exists),
                options)
        super(URLField, self).__init__(max_length, **options)


class IPAddressField(Field):
    '''An IP address, in string format (e.g. "192.0.2.30").

    The admin represents this as an <input type="text"> (a single-line input).
    '''

    def __init__(self, **options):
        '''Create Field with addition validation for store IP address
        '''
        options = add_validator(lighty.validators.validate_ipv4_address,
                                options)
        super(IPAddressField, self).__init__(**options)


class SlugField(CharField):
    '''Slug is a newspaper term. A slug is a short label for something,
    containing only letters, numbers, underscores or hyphens. They're generally
    used in URLs.

    Implies setting Field.db_index to True.

    It is often useful to automatically prepopulate a SlugField based on the
    value of some other value. You can do this automatically in the admin using
    prepopulated_fields.
    '''

    def __init__(self, max_length=50, **options):
        '''Create new CharField field with additional validator for slug
        Like a CharField, you can specify max_length (read the note about
        database portability and max_length in that section, too). If
        max_length is not specified, SlugField will use a default length of 50.
        '''
        options['unique'] = True
        options = add_validator(lighty.validators.validate_slug, options)
        super(SlugField, self).__init__(max_length, **options)


class DateField(Field, NumericField):
    '''A date, represented in Python by a datetime.date instance.
    '''

    def __init__(self, auto_now=False, auto_now_add=False, **options):
        '''Create new DateField. Has a few extra, optional arguments

        Args:
            auto_now: Automatically set the field to now every time the object
                is saved. Useful for "last-modified" timestamps. Note that the
                current date is always used; it's not just a default value that
                you can override.
            auto_now_add: Automatically set the field to now when the object is
                first created. Useful for creation of timestamps. Note that the
                current date is always used; it's not just a default value that
                you can override.
        '''
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add
        super(DateField, self).__init__(**options)

    def get_value_for_datastore(self, model):
        if self.auto_now or (self.auto_now_add and not model.is_saved()):
            from datetime import date
            model.__dict__[self.name] = date.today()
        return model.__dict__[self.name].strptime("%Y-%m-%d")

    def make_value_from_datastore(self, value):
        from datetime import date
        return date.strptime(value, "%Y-%m-%d")


class DateTimeField(DateField, NumericField):
    '''A date and time, represented in Python by a datetime.datetime instance.
    Takes the same extra arguments as DateField.
    '''

    def get_value_for_datastore(self, model):
        '''Prepare value to store it into datastore.

        Returns:
            string represents field value in format "%Y-%m-%d %H:%M:%S"
        '''
        from datetime import datetime
        if self.auto_now or (self.auto_now_add and not model.is_saved()):
            model.__dict__[self.name] = datetime.now()
        return datetime.strftime(model.__dict__[self.name],
                                 "%Y-%m-%d %H:%M:%S")

    def make_value_from_datastore(self, value):
        '''Create date from value taken from datastore

        Returns:
            parsed DateTime object
        '''
        from datetime import datetime
        if isinstance(value, datetime):
            return value
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


class TimeField(DateField, NumericField):
    '''A time, represented in Python by a datetime.time instance. Accepts the
    same auto-population options as DateField.
    '''

    def get_value_for_datastore(self, model):
        '''Prepare value to store it into datastore.

        Returns:
            string represents field value in format "%Y-%m-%d %H:%M:%S"
        '''
        from time import gmtime, strftime
        if self.auto_now or (self.auto_now_add and not model.is_saved()):
            model.__dict__[self.name] = gmtime()
        return strftime("%H:%M:%S", model.__dict__[self.name])

    def make_value_from_datastore(self, value):
        '''Create date from value taken from datastore

        Returns:
            parsed Time object
        '''
        from time import strptime
        return strptime(value, "%H:%M:%S")


class TextField(Field, SequenceField):
    '''A large text field. The admin represents this as a <textarea> (a
    multi-line input).
    '''
    pass


#
# TODO:
# 		write code for FileField, FilePathField and ImageField
# 		write code for ForeignKey, ManyToManyField, OneToOneField
#


class ForeignKey(Field):
    """An object field can contains
    """

    def __init__(self, model, **kwargs):
        """
        """
        super(ForeignKey, self).__init__(kwargs)
        self.model = model

    def get_value_for_datastore(self, model):
        """Get object's key
        """
        return model.__dict__[self.name].key()

    def make_value_from_datastore(self, value):
        """Get object for key
        """
        return self.model.get(value)
