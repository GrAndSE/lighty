'''Module contains base validators that can be used to check the data
'''
import re
import urllib


class ValidationError(Exception):
    '''Error on validation
    '''

    def __init__(self, message, code=None):
        '''Create new validation error instance with specified error message
        '''
        self.message = message
        if code is None:
            self.code = message
        else:
            self.code = code

    def __str__(self):
        '''
        Represent validation error
        '''
        return repr(self.message)


class ChoicesValidator(object):
    '''Validator used to validate choices list
    '''

    def __init__(self, choices, message=None, code=None):
        '''Create new ChoicesValidator with specified choices.

        choices
            An iterable (e.g., a list or tuple) of 2-tuples to use as choices
            for this field.

        message
            The error message used by ValidationError if validation fails.
            Default value: None.

        code
            The error code used by ValidationError if validation fails. If code
            is not specified, "invalid" is used. Default value: None.
        '''
        self.choices = choices
        self.message = message
        if code is None:
            self.code = "invalid"
        else:
            self.code = code

    def __call__(self, value):
        '''Check is value argument inside of choices
        '''
        for choice in self.choices:
            if value in choice or (hasattr(choice[1], '__iter__') and
                                   value in choice[1]):
                return
        # Generate a message
        if self.message is None:
            message = '%s is not in choices list' % value
        else:
            message = self.message
        raise ValidationError(message, self.code)


class RegexValidator(object):
    '''Validator used to check is value matches regular expression
    '''

    def __init__(self, regex, message=None, code=None):
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

        code
            The error code used by ValidationError if validation fails. If code
            is not specified, "invalid" is used. Default value: None.
        '''
        if isinstance(regex, str):
            regex = re.compile(regex)
        self.regex = regex
        if message is None:
            self.message = "Enter a valid value"
        else:
            self.message = message
        if code is None:
            self.code = "invalid"
        else:
            self.code = code

    def __call__(self, value):
        '''
        Check is value mathes pattern
        '''
        if self.regex.match(value) is None:
            raise ValidationError(self.message, self.code)

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
        super(URLValidator, self).__init__(URL_REGEX, "Invalid URL format",
                                           "invalid")
        self.verify_exists = verify_exists
        self.validator_user_agent = validator_user_agent

    def __call__(self, url):
        '''Check is url valid
        '''
        super(URLValidator, self).__call__(url)
        if self.verify_exists:
            urlhandle = urllib.urlopen(url)
            if urlhandle.getcode() >= 400:
                raise ValidationError("Invalid link", "invalid_link")

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


class MaxValueValidator:
    '''Raises a ValidationError with a code of 'max_value' if value is greater
    than max_value.
    '''

    def __init__(self, max_value):
        '''Create new MaxValueValidator with specified max_value
        '''
        self.max_value = max_value

    def __call__(self, value):
        if value > self.max_value:
            raise ValidationError("Not allowed value", 'max_value')


class MinValueValidator:
    '''Raises a ValidationError with a code of 'min_value' if value is less
    than min_value.
    '''

    def __init__(self, min_value):
        '''Create new MinValueValidator with specified min_value
        '''
        self.min_value = min_value

    def __call__(self, value):
        if value < self.min_value:
            raise ValidationError("Not allowed value", 'min_value')


class MaxLengthValidator:
    '''Raises a ValidationError with a code of 'max_length' if length of value
    is greater than max_value.
    '''

    def __init__(self, max_length):
        '''
        Create new MaxLengthValidator with specified max_value
        '''
        self.max_length = max_length

    def __call__(self, value):
        if len(value) > self.max_length:
            raise ValidationError("Not allowed length", 'max_length')


class MinLengthValidator:
    '''Raises a ValidationError with a code of 'min_length' if length of value
    is less than min_length.
    '''

    def __init__(self, min_length):
        '''Create new MinValueValidator with specified min_value
        '''
        self.min_length = min_length

    def __call__(self, value):
        if len(value) < self.min_length:
            raise ValidationError("Not allowed length", 'min_length')
