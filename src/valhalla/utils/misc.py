

def int_str_to_bytes(int_str, byteorder='little'):
    integer = int(int_str)
    num_bytes = (integer.bit_length() + 7) // 8
    return integer.to_bytes(num_bytes, byteorder=byteorder)