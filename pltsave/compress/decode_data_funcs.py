from ..aliases import KEY_ALIASES_INVERSE
from .compress_numbers import decompress_array, decompress_int, decompress_number


def closing_brackets(data: str, open_bracket: str, close_bracket: str | None = None):
    if close_bracket is None:
        if open_bracket == "{":
            close_bracket = "}"
        if open_bracket == "[":
            close_bracket = "]"
        if open_bracket == "(":
            close_bracket = ")"

    brackets = 0 if data[0] == open_bracket else 1
    for i, c in enumerate(data):
        if c == open_bracket:
            brackets += 1
        if c == close_bracket:
            brackets -= 1
        # print(i, c, brackets)
        if brackets == 0:
            return i
    return -1


def decode_elm(data: str):
    if not data:
        return data

    if data[0] == "{":
        return decode_dict(data)
    if data[0] == "[":
        return decode_array(data)
    if data[0] == "(":
        return data[1:-1]
    if data[0] == "@":
        return decompress_number(data[1:])
    if data[0] == "_":
        return data[1:]
    if data[0] == "+":
        precision_shift = int(data[1])  # ord(data[0]) - 97
        # print(data[1:])
        return decompress_array(data[2:], precision_shift=precision_shift)
    if data[0] == "$":
        return "#" + hex(decompress_int(data[1:]))[2:]

    if data.replace(".", "").isnumeric():
        if "." in data:
            return float(data)
        return int(data)

    return data


def decode_array(data: str):
    if data[0] == "[":
        data = data[1:-1]
    index = 0
    global_index = 0
    res = []
    while index < len(data) and global_index < len(data):
        possible_bracket = data[index]
        if possible_bracket in ["{", "[", "("]:
            closing = closing_brackets(data[index:], possible_bracket)
            value = data[index : index + closing + 1]
            res.append(decode_elm(value))
            index += closing + 2
        else:
            value_end = data.find(",", index)
            if value_end < 0:
                value_end = len(data)
            value = data[index:value_end]
            res.append(decode_elm(value))
            index = value_end + 1
        global_index += 1
    return res


def decode_dict(data: str):
    if data[0] == "{":
        data = data[1:-1]
    index = 0
    global_index = 0
    res = {}
    while index < len(data) and global_index < len(data):
        key_end = data.find(":", index)
        key = data[index:key_end]
        key = KEY_ALIASES_INVERSE.get(key, key)
        possible_bracket = data[key_end + 1]
        if possible_bracket in ["{", "[", "("]:
            closing = closing_brackets(data[key_end + 1 :], possible_bracket)
            value = data[key_end + 1 : key_end + 1 + closing + 1]
            index = key_end + closing + 3
            res[key] = decode_elm(value)
        else:
            value_end = data.find(",", key_end)
            if value_end < 0:
                value_end = len(data)
            value = data[key_end + 1 : value_end]
            res[key] = decode_elm(value)
            index = value_end + 1

        global_index += 1

    return res
