import numpy as np

from ..aliases import KEY_ALIASES_MAP, TEXT_FORBIDDEN_SYMBOLS
from .compress_numbers import compress_array, compress_number


def normalize_elm(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = normalize_elm(value)
        return data
    if isinstance(data, str) and data and data.replace(".", "").isnumeric():
        if "." in data:
            return float(data)
        return int(data)
    if isinstance(data, np.int_):  # type: ignore
        return int(data)
    if isinstance(data, np.float_):  # type: ignore
        return float(data)
    if hasattr(data, "__iter__") and not isinstance(data, (str, bytes)):
        return [normalize_elm(elm) for elm in data]

    return data


def normalize_dict(data: dict) -> dict:
    return normalize_elm(data)  # type: ignore


def compress_key(key):
    return KEY_ALIASES_MAP.get(key, key)


def compress_elm(data):
    if not isinstance(data, (int, float)) and not data:
        return None
    if isinstance(data, dict):
        return compress_dict(data)
    if isinstance(data, (int, float)):
        if isinstance(data, int) and 0 <= data < 10:
            return str(data)
        return "z" + compress_number(data)

    if hasattr(data, "__iter__") and not isinstance(data, (str, bytes)):
        if isinstance(data[0], (int, float)):
            precision_shift = 3
            precision_code = chr(97 + precision_shift)
            return precision_code + compress_array(data, precision=0, precision_shift=3)
        return [compress_elm(elm) for elm in data]

    if isinstance(data, str) and data[0] == "#":
        number = int(data[1:], 16)
        return "x" + compress_number(number)

    if isinstance(data, str) and any(s in data for s in TEXT_FORBIDDEN_SYMBOLS):
        return f"({data})"

    if isinstance(data, str) and 96 < ord(data[0]) < 123:
        return "_" + data
    return data


def compress_dict(data: dict):
    compressed_dict = {}
    for key, value in data.items():
        compressed_key = compress_key(key)
        compressed_value = compress_elm(value)
        if compressed_value:
            compressed_dict[compressed_key] = compressed_value

    return compressed_dict
