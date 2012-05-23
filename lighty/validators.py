'''Module contains base validators that can be used to check the data
'''
import re
import urllib

from . import monads
from . import utils


class ValidationError(monads.ErrorMonad):
    '''Error on validation
    '''


class Validator(object):
    '''Base validator class
    '''

    def __init__(self, message=None):
        self._message = message if message else 'Validation error'

    def message(self, value):
        '''This method can be used to override error message generation
        depending on value provided as argument

        Returns: an error message
        '''
        try:
            message = self._message % value
        except:
            message = self._message
        return message

    def error(self, value):
        '''Method that need to be called when need to return value with error
        message
        '''
        return ValidationError(self.message(value))

    def validate(self, value):
        '''This method called on value validation. Any uncatched exception will
        be equivalent of validation error
        '''
        raise NotImplemented('check is not implemented in %s' %
                             self.__class__.__name__)

    @monads.handle_exception
    def __call__(self, value):
        '''Makes validator like a simple function
        '''
        return self.validate(value)


class ChoicesValidator(Validator):
    '''Validator used to validate choices list

    choices
        An iterable (e.g., a list or tuple) of 2-tuples to use as choices 
        for this field.

    message
        The error message used by ValidationError if validation fails.
        Default value: None.
    '''

    def __init__(self, choices, message=None):
        '''Create new ChoicesValidator with specified choices.
        '''
        self.choices = choices
        super(ChoicesValidator, self).__init__(message if message
                                            else '%s is not in choices list')

    def validate(self, value):
        '''Check is value argument inside of choices
        '''
        for choice in self.choices:
            if value in choice or (hasattr(choice[1], '__iter__') and
                                   value in choice[1]):
                return value
        return self.error(value)


REGEX_TYPE = type(re.compile(''))


class RegexValidator(Validator):
    '''Validator used to check is value matches regular expression
    '''

    def __init__(self, regex, message=None):
        '''
        Create new ChoicesValidator with specified choices.

        regex
            The regular expression pattern to search for the provided value, or
            a pre-compiled regular expression. Raises a ValidationError with
            message and code if no match is found.

        message
            The error message used by ValidationError if validation fails. If
            no message is specified, a generic "Enter a valid value" message is
            used. Default value: None.
        '''
        self.regex = (regex if isinstance(regex, REGEX_TYPE)
                      else re.compile(regex))
        super(RegexValidator, self).__init__(message if message
                                             else "Enter a valid value")

    def validate(self, value):
        '''Check is value mathes pattern
        '''
        return self.error(value) if self.regex.match(value) is None else value

URL_VALIDATOR_USER_AGENT = ""
URL_REGEX = ("(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[a-z]{2}|com|org|net|"
             "edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum)\\b")


class URLValidator(RegexValidator):
    '''A RegexValidator that ensures a value looks like a URL and optionally
    verifies that the URL actually exists (i.e., doesn't return a 404 status
    code). Raises an error code of 'invalid' if it doesn't look like a URL, and
    a code of 'invalid_link' if it doesn't exist.
    '''

    def __init__(self, verify_exists=False,
                validator_user_agent=URL_VALIDATOR_USER_AGENT):
        '''Create new URLValidator

        verify_exists
            Default value: False. If set to True, this validator checks that
            the URL actually exists.

        validator_user_agent
            If verify_exists is True, Django uses the value of validator_user_
            agent as the "User-agent" for the request. This defaults to
            settings.URL_VALIDATOR_USER_AGENT.
        '''
        super(URLValidator, self).__init__(URL_REGEX, "Invalid URL format")
        self.verify_exists = verify_exists
        self.validator_user_agent = validator_user_agent

    def validate(self, url):
        '''Check is url valid
        '''
        result = super(URLValidator, self).validate(url)
        if self.verify_exists and not isinstance(result, monads.ErrorMonad):
            urlhandle = urllib.urlopen(url)
            if urlhandle.getcode() >= 400:
                return self.error(url)
        return result

EMAIL_REGEX = ("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)"
               "*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[a-z]{2}|com|org|"
               "net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum)$")
validate_email = RegexValidator(EMAIL_REGEX)

SLUG_REGEX = "^([\w-]+)$"
validate_slug = RegexValidator(SLUG_REGEX)

IPV4_REGEX = ("^(((25[0-5])|(2[0-4][\d])|([0-1]?\d?\d))(\.((25[0-5])|(2[0-4]"
              "[\d])|([0-1]?\d?\d))){3})$")
validate_ipv4_address = RegexValidator(IPV4_REGEX)

validate_comma_separated_integer_list = RegexValidator("^(([\d]+\,)*[\d]+)$")


class MaxValueValidator(Validator):
    '''Raises a ValidationError with a code of 'max_value' if value is greater
    than max_value.
    '''

    def __init__(self, max_value, message=None):
        self.max_value = max_value
        super(MaxValueValidator, self).__init__(message if message
                                    else "%s greater than " + str(max_value))

    def validate(self, value):
        return self.error(value) if value > self.max_value else value


class MinValueValidator(Validator):
    '''Raises a ValidationError with a code of 'min_value' if value is less
    than min_value.
    '''

    def __init__(self, min_value, message=None):
        self.min_value = min_value
        super(MinValueValidator, self).__init__(message if message
                                    else "%s smaller than " + str(min_value))

    def validate(self, value):
        return self.error(value) if value < self.min_value else value


class MaxLengthValidator(Validator):
    '''Raises a ValidationError with a code of 'max_length' if length of value
    is greater than max_value.
    '''

    def __init__(self, max_length, message=None):
        self.max_length = max_length
        super(MaxLengthValidator, self).__init__(message if message
                                                 else "Not allowed length")

    def validate(self, value):
        return self.error(value) if len(value) > self.max_length else value


class MinLengthValidator(Validator):
    '''Raises a ValidationError with a code of 'min_length' if length of value
    is less than min_length.
    '''

    def __init__(self, min_length, message=None):
        '''Create new MinValueValidator with specified min_value
        '''
        self.min_length = min_length
        super(MinLengthValidator, self).__init__(message if message
                                                 else "Not allowed length")

    def validate(self, value):
        return self.error(value) if len(value) < self.min_length else value


def validate(validators, data, transform=None):
    '''Validate data using validators
    '''
    if not transform:
        transform = {}
    results = {}
    errors_num = 0
    for field in validators.keys():
        if field in transform:
            if isinstance(transform[field], utils.string_types):
                value = data.get(transform[field], monads.NoneMonad(
                            'No data for %s (%s)' % (transform[field], field)))
            else:
                value = transform[field](data)
        else:
            value = data.get(field, monads.NoneMonad('No data for %s' % field))
        result = value
        errors = []
        for validator in validators[field]:
            result = validator(result)
            if isinstance(result, monads.NoneMonad):
                errors.append(result)
                result = value
            else:
                value = result
        if len(errors) > 0:
            results[field] = ValidationError(errors)
            errors_num += 1
        else:
            results[field] = result
    return ValidationError(results) if errors_num > 0 else results
