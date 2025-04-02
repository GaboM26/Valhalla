

def int_str_to_bytes(int_str, byteorder='little'):
    integer = int(int_str)
    num_bytes = (integer.bit_length() + 7) // 8
    return integer.to_bytes(num_bytes, byteorder=byteorder)

def pretty_print_flat_dict(data):
    """
    Pretty prints a flat dictionary without braces.
    Assumes no nested dictionaries or lists inside.
    :param data: The dictionary to be printed.
    """
    for key, value in data.items():
        print(f"{key}: {value}")

def clean_nested_dict(data):
    """
    Cleans a dictionary by removing the "0:" keys from internal dictionaries.
    Extracts the value associated with the "0:" key.
    :param data: The dictionary to be cleaned.
    :return: A cleaned dictionary.
    """
    cleaned_data = {}
    for key, value in data.items():
        if isinstance(value, dict) and len(value) > 0:
            first_key = next(iter(value))
            cleaned_data[key] = value[first_key]
        else:
            cleaned_data[key] = value  # Keep the value as is if it's not a dict with "0:"
    return cleaned_data