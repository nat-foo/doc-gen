import re

def capitalise_first_only(string):
    """
    Returns string - only change is first letter, which is capitalised.

    This was made because .capitalise function returns string with first letter uppercase and rest lowercase.

    This is NO GOOD for camel case. So I have written this function which just does the first letter.
    """

    first_letter = string[0].upper()

    rest_of_word = string[1:]

    new_string = first_letter + rest_of_word

    return new_string

def lower_first_only(string):
    """
    Returns string - only change is first letter, which is lower-cased.

    Python library functions don't handle this well,
    
    so I have written this function which just does the first letter.
    """

    first_letter = string[0].lower()

    rest_of_word = string[1:]

    new_string = first_letter + rest_of_word

    return new_string

def to_upper(string):
    # Converts the given string from camelCase into upper underscore case.
    new_string = re.sub('([A-Z])([A-Z][a-z])', r'\1_\2', string[1:])
    new_string = re.sub('([a-z])([A-Z])', r'\1_\2', new_string)
    new_string = re.sub('([0-9])', r'_\1', new_string)
    new_string = string[0] + new_string
    new_string = new_string.upper()
    return new_string

def to_underscore(string):
    # Converts the given string from camelCase into lower underscore case.
    new_string = re.sub('([A-Z])([A-Z][a-z])', r'\1_\2', string[1:])
    new_string = re.sub('([a-z])([A-Z])', r'\1_\2', new_string)
    new_string = string[0] + new_string
    new_string = new_string.lower()
    return new_string