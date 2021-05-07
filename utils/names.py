# Contains functions for managing input data.
from .strings import capitalise_first_only, lower_first_only, to_upper, to_underscore

def parse_names(raw_name):
    name = raw_name
    Name = capitalise_first_only(raw_name)
    NAME = to_upper(raw_name)
    _name = to_underscore(raw_name)

    return (
        name, Name, NAME, _name
    )

def parse_dict_properties(dictionary):
    """
        Parse every key and value of the given dictionary into three separate properties: lowercase, Sentence-case, and UPPER_CASE.
        Works recursively to find all nested dictionaries.

        Note: Anything that isn't a list or a dict will be converted into a string. 
        This behaviour can be modified, but it is suitable for API-Gen to do this.
    """

    keys = list(dictionary.keys()).copy()
    for _key in keys:

        # If the value is a dict, go deeper down the rabbit hole.
        val = dictionary[_key]
        if isinstance(val, dict):
            val = parse_dict_properties(val)

        # If the value is a list, check the list for dicts.
        elif isinstance(val, list):
            for v in val:
                if isinstance(v, dict):
                    v = parse_dict_properties(v)

        # If the key is a hidden property, skip it.
        elif _key[0] == "_":
            continue

        # Finally, parse the key and then the value into 3 separate properties.
        # elif isinstance(val, str): # If the value is a string,
        else:
            key, Key, KEY, _key = parse_names(_key)
            val = dictionary[_key]
            val = str(val) # This is where we make all values a string. To revert, comment this line, and uncomment 'elif isinstance'.
            value, Value, VALUE, _value = parse_names(val)
            dictionary[key] = value
            dictionary[Key] = Value
            dictionary[KEY] = VALUE
            dictionary[f'_{key}'] = _value

    return dictionary