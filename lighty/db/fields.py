'''All fields described
'''
import lighty.validators


class Field(object):
    '''Base field class
    '''

    def __init__(self, verbose_name=None, primary_key=False, db_index=False, 
                       unique=False, blank=False, null=False, 
                       choices=None, default=None, editable=True,
                       error_messages={}, validators=(),
                       help_text="", db_column=None, db_tablespace=False,
                       unique_for_date=False, 
                       unique_for_month=False, unique_for_year=False):
        """
        """
        self.null 			= null
        self.blank 			= blank
        self.choices 		= choices
        self.default 		= default
        self.editable 		= editable
        self.db_column 		= db_column
        self.db_tablespace 	= db_tablespace
        self.db_index 		= db_index
        self.primary_key 	= primary_key
        self.help_text 		= help_text
        self.verbose_name 	= verbose_name
        self.error_messages = error_messages
        # Add additional choice if needed
        if choices is not None:
            validators += (lighty.validators.ChoicesValidator(choices),)
        self.validators = validators
        # Unique params
        if unique:
            self.unique 		= True
            unique_for_date 	= False
            unique_for_month 	= False
            unique_for_year 	= False
        else:
            self.unique 		= False
            if unique_for_date:
                self.unique_for_date 	= unique_for_date
                self.unique_for_month 	= False
                self.unique_for_year 	= False
            else:
                self.unique_for_date 	= False
                if unique_for_month:
                    self.unique_for_month 	= unique_for_month
                    self.unique_for_year 	= False
                else:
                    self.unique_for_month 	= False
                    self.unique_for_year 	= unique_for_year

    def __config__(self, model_class, field_name):
        """
        """
        self.model = model_class
        self.name  = field_name

    def get_value_for_datastore(self, model):
        """Get value
        """
        return model.__dict__[self.name]

    def make_value_from_datastore(self, value):
        """Create object from value was taken from datastore
        """
        return value



class IntegerField(Field):
    '''An integer. The admin represents this as an <input type="text"> (a 
    single-line input).
    '''

    def __init__(self, **options):
        super(IntegerField, self).__init__(**options)


class PositiveIntegerField(IntegerField):
	'''
	Like an IntegerField, but must be positive.
	'''
	def __init__(self, **options):
		# Add validation
		validators = (lighty.validators.MinValueValidator(1),)
		if 'validators' in options:
			options['validators'] += validators
		else:
			options['validators'] = validators
		# Create IntegerField 
		super(PositiveIntegerField, self).__init__(**options)


class AutoField(IntegerField):
	'''
	An IntegerField that automatically increments according to available IDs. 
	You usually won't need to use this directly; a primary key field will 
	automatically be added to your model if you don't specify otherwise. See 
	Automatic primary key fields.
	'''
	pass


class BigIntegerField(IntegerField):
	'''
	A 64 bit integer, much like an IntegerField except that it is guaranteed to
	fit numbers from -9223372036854775808 to 9223372036854775807. The admin 
	represents this as an <input type="text"> (a single-line input).
	'''
	pass


class SmallIntegerField(IntegerField):
	'''
	Like a IntegerField, but only allows values under a certain (database-
	dependent) point.
	'''
	pass


class PositiveSmallIntegerField(PositiveIntegerField):
	'''
	Like a PositiveIntegerField, but only allows values under a certain 
	(database-dependent) point.
	'''
	pass



class FloatField(Field):
	'''
	A floating-point number represented in Python by a float instance.

	The admin represents this as an <input type="text"> (a single-line input).
	'''

	def __init__(self, **options):
		super(FloatField, self).__init__(**options)



class DecimalField(Field):
	'''
	A fixed-precision decimal number, represented in Python by a Decimal 
	instance.

	The admin represents this as an <input type="text"> (a single-line input).
	'''

	def __init__(self, max_digits=None, **options):
		'''
		Create new fixed-precision decimal number 

		max_digits
			The maximum number of digits allowed in the number

		decimal_places
			The number of decimal places to store with the number
		'''
#TODO write valid max_digits and decimal_places processing
		super(DecimalField, self).__init__(**options)



class BooleanField(Field):
	'''
	A true/false field

	The admin represents this as a checkbox
	'''

	def __init__(self, **options):
		super(BooleanField, self).__init__(**options)


class NullBooleanField(BooleanField):
	'''
	Like a BooleanField, but allows NULL as one of the options. Use this 
	instead of a BooleanField with null=True. The admin represents this as a 
	<select> box with "Unknown", "Yes" and "No" choices.
	'''

	def __init__(self, **options):
		'''
		Create new BooleanField field with null=True
		'''
		options['null'] = True
		super(NullBooleanField, self).__init__(**options)



class CharField(Field):
    '''A string field, for small- to large-sized strings.

    For large amounts of text, use TextField.

    The admin represents this as an <input type="text"> (a single-line input).
    '''

    def __init__(self, max_length=None, **options):
        '''Create new CharField with one extra required argument:

        Arguments:
            max_length: The maximum length (in characters) of the field. 
            The max_length is enforced at the database level and in validation.
        '''
        # Process max_length option
        if max_length is None:
            max_length = 255
        self.max_length = max_length
        # Add MaxLengthValidator
        validators = (lighty.validators.MaxLengthValidator(max_length), )
        if 'validators' in options:
            options['validators'] += validators
        else:
            options['validators'] = validators
        # Then create usual field 
        super(CharField, self).__init__(**options)


class CommaSeparatedIntegerField(CharField):
	'''
	A field of integers separated by commas. As in CharField, the max_length 
	argument is required and the note about database portability mentioned 
	there should be heeded.
	'''

	def __init__(self, max_length=None, **options):
		'''
		Create new CommaSeparatedIntegerField instance
		'''
		# Add additional validators
		validators = (
				lighty.validators.validate_comma_separated_integer_list, )
		if 'validators' in options:
			options['validators'] += validators
		else:
			options['validators'] = validators
		# Create CharField
		super(CommaSeparatedIntegerField, self).__init__(max_length, **options)


class EmailField(CharField):
	'''
	A CharField that checks that the value is a valid e-mail address.
	'''

	def __init__(self, max_length=75, **options):
		'''
		Create CharField that checks that the value is a valid e-mail address.
		'''
		# Add additional validators
		validators = (lighty.validators.validate_email, )
		if 'validators' in options:
			options['validators'] += validators
		else:
			options['validators'] = validators
		# Create CharField
		super(EmailField, self).__init__(max_length, **options)


class URLField(CharField):
	'''
	A CharField for a URL.

	The admin represents this as an <input type="text"> (a single-line input).
	'''

	def __init__(self, verify_exists=True, max_length=200, **options):
		'''
		Create new CharField to store URL

		verify_exists
			If True (the default), the URL given will be checked for existence
			(i.e., the URL actually loads and doesn't give a 404 response).

			Note that when you're using the single-threaded development server,
			validating a URL being served by the same server will hang. This 
			should not be a problem for multithreaded servers.

		max_length
			Like all CharField subclasses, URLField takes the optional 
			max_length, a default of 200 is used.
		'''
		# Add additional validators
		validators = (
			lighty.validators.URLValidator(verify_exists=verify_exists), )
		if 'validators' in options:
			options['validators'] += validators
		else:
			options['validators'] = validators
		# Create char field
		super(URLField, self).__init__(max_length, **options)



class IPAddressField(Field):
	'''
	An IP address, in string format (e.g. "192.0.2.30"). 
	
	The admin represents this as an <input type="text"> (a single-line input).
	'''

	def __init__(self, **options):
		'''
		Create Field with addition validation for store IP address
		'''
		# Add validator 
		validators = (lighty.validators.validate_ipv4_address, )
		if 'validators' in options:
			options['validators'] += validators
		else:
			options['validators'] = validators
		# Create new field
		super(IPAddressField, self).__init__(**options)



class SlugField(CharField):
	'''
	Slug is a newspaper term. A slug is a short label for something, containing
	only letters, numbers, underscores or hyphens. They're generally used in 
	URLs.

	Implies setting Field.db_index to True.

	It is often useful to automatically prepopulate a SlugField based on the 
	value of some other value. You can do this automatically in the admin using
	prepopulated_fields.
	'''

	def __init__(self, max_length=50, **options):
		'''
		Create new CharField field with additional validator for slug
		Like a CharField, you can specify max_length (read the note about 
		database portability and max_length in that section, too). If 
		max_length is not specified, SlugField will use a default length of 50.
		'''
		# Update unique=True
		options['unique'] = True
		# Add additional validator for slug
		validators = (lighty.validators.validate_slug, )
		if 'validators' in options:
			options['validators'] += validators
		else:
			options['validators'] = validators
		# Create char field
		super(SlugField, self).__init__(max_length, **options)



class DateField(Field):
    '''A date, represented in Python by a datetime.date instance. 
    '''

    def __init__(self, auto_now=False, auto_now_add=False, **options):
        '''Create new DateField. Has a few extra, optional arguments

        Args: 
            auto_now: Automatically set the field to now every time the object
            is saved. Useful for "last-modified" timestamps. Note that the 
            current date is always used; it's not just a default value that you
            can override.
            auto_now_add: Automatically set the field to now when the object is
            first created. Useful for creation of timestamps. Note that the 
            current date is always used; it's not just a default value that you 
            can override.
        '''
        self.auto_now 		= auto_now
        self.auto_now_add 	= auto_now_add
        super(DateField, self).__init__(**options)

    def get_value_for_datastore(self, model):
        if self.auto_now or (self.auto_now_add and not model.is_saved()):
            from datetime import date
            model.__dict__[self.name] = date.today()
        return model.__dict__[self.name].strptime("%Y-%m-%d")

    def make_value_from_datastore(self, value):
        from datetime import date
        return date.strptime(value, "%Y-%m-%d")



class DateTimeField(DateField):
    '''A date and time, represented in Python by a datetime.datetime instance. 
    Takes the same extra arguments as DateField.
    '''

    def get_value_for_datastore(self, model):
        from datetime import datetime
        if self.auto_now or (self.auto_now_add and not model.is_saved()):
            model.__dict__[self.name] = datetime.now()
        return datetime.strftime(model.__dict__[self.name], "%Y-%m-%d %H:%M:%S")

    def make_value_from_datastore(self, value):
        from datetime import datetime
        if isinstance(value, datetime):
            return value
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


class TimeField(DateField):
    '''A time, represented in Python by a datetime.time instance. Accepts the 
    same auto-population options as DateField.
    '''

    def get_value_for_datastore(self, model):
        from time import gmtime, strftime
        if self.auto_now or (self.auto_now_add and not model.is_saved()):
            model.__dict__[self.name] = gmtime()
        return strftime("%H:%M:%S", model.__dict__[self.name])

    def make_value_from_datastore(self, value):
        from time import strptime
        return strptime(value, "%H:%M:%S")


class TextField(Field):
	'''
	A large text field. The admin represents this as a <textarea> (a 
	multi-line input).
	'''
	pass


class XMLField(TextField):
	'''
	A TextField that checks that the value is valid XML that matches a given 
	schema. Takes one required argument:

	schema_path
		The filesystem path to a RelaxNG schema against which to validate the 
		field.
	'''
#TODO: write valid code here
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
