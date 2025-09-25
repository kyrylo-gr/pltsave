import typing as _t
from math import log2

# from .encoding_maps import DECODING_MAP, ENCODING_MAP
from .encoding_maps_v1 import DECODING_MAP, ENCODING_MAP

BASE = min(16, int(log2(len(ENCODING_MAP))))
BASE_MAX = (1 << BASE) - 1

DEFAULT_PRECISION = 3
DEFAULT_PRECISION_SHIFT = 0


def compress_int(x: int) -> str:
    x = int(x)
    res = ""
    x = ~(x << 1) if x < 0 else x << 1

    while x > BASE_MAX:
        xx = x & BASE_MAX
        res = ENCODING_MAP[xx] + res
        x = x >> BASE
    res = ENCODING_MAP[x] + res

    return res


def decompress_int(code: str) -> int:
    x = 0
    for i, symbol in enumerate(code[::-1]):
        x += DECODING_MAP[symbol] << (BASE * i)
    # x = x >> 1
    x = ~x >> 1 if x & 0b1 else x >> 1
    return x


def reverse_number(x: int, precision: int) -> int:
    x_str = str(x)[::-1]
    return int(x_str + "0" * (precision - len(x_str)))


def compress_remainder(x: float, precision: int) -> _t.Optional[str]:
    x = int(round(x * 10**precision))
    if x == 0:
        return None
    x = reverse_number(x, precision)
    return compress_int(x)


def decompress_remainder(code: _t.Optional[str]) -> int:
    if code is None:
        return 0
    x = decompress_int(code)
    x_str = str(x)[::-1]
    return int(x_str) / 10 ** len(x_str)


def compress_number(x: _t.Union[float, int], precision: _t.Optional[int] = None) -> str:
    if precision is None:
        precision = DEFAULT_PRECISION
    x = round(x, precision)
    modulo = int(x)
    remainder = abs(x) % 1
    if remainder == 0:
        return compress_int(modulo)

    remainder_encoded = compress_remainder(remainder, precision)
    if remainder_encoded is None:
        return compress_int(modulo)
    else:
        return compress_int(modulo) + "." + remainder_encoded


def decompress_number(code: str) -> float:
    if "." not in code:
        return decompress_int(code)

    modulo, remainder = code.split(".")
    modulo = decompress_int(modulo)
    remainder = decompress_remainder(remainder)
    return modulo + remainder


def compress_number_with_len(x: _t.Union[float, int], precision: _t.Optional[int] = None):
    comp = compress_number(x, precision)
    if len(comp) == 1:
        return comp
    # here we are limiting the length to 5.
    # Which is 2**(16 * 3 + 15) = 2**63
    # number_len = len(comp)
    return str(len(comp)) + comp


def compress_number_with_len_and_reps(
    x: _t.Union[float, int],
    precision: _t.Optional[int] = None,
    count: int = 1,
):
    res_num = compress_number_with_len(x, precision)
    if (count - 1) * len(res_num) - 2 > 0:
        res = ""
        one_digit_max = BASE_MAX >> 1
        while count > one_digit_max:
            res += "#" + compress_int(one_digit_max) + res_num
            count -= one_digit_max
        return res + "#" + compress_int(count) + res_num
    return res_num * count


def compress_array(
    array: _t.List[_t.Union[float, int]],
    precision: _t.Optional[int] = None,
    precision_shift: _t.Optional[int] = None,
):
    if precision is None:
        precision = DEFAULT_PRECISION
    if precision_shift is None:
        precision_shift = DEFAULT_PRECISION_SHIFT

    diff = [array[0]] + [array[i] - array[i - 1] for i in range(1, len(array))]
    if precision_shift > 0:
        diff = [x * 10**precision_shift for x in diff]
    res = ""
    last_x = diff[0]
    count = 1
    for x in diff[1:]:
        if round(x, precision) != round(last_x, precision):
            # print(last_x, count, x, diff)
            res += compress_number_with_len_and_reps(last_x, precision, count)
            last_x = x
            count = 1
        else:
            count += 1

    # print(last_x, count, x, diff)

    res += compress_number_with_len_and_reps(last_x, precision, count)

    return res


def decompress_elm_in_array(
    code: str,
    index: int,
):
    first_symbol = code[index]
    if first_symbol == "#":
        reps = decompress_int(code[index + 1])
        elm, index_shift, _ = decompress_elm_in_array(code, index + 2)
        return elm, index_shift + 2, reps

    if 48 < ord(first_symbol) < 58:  # 48 is "0", 57 is "9"
        length = int(first_symbol)
        return decompress_number(code[index + 1 : index + length + 1]), length + 1, 1

    return decompress_number(first_symbol), 1, 1


def decompress_array(
    code: str,
    precision_shift: _t.Optional[int] = None,
) -> _t.List[float]:
    if precision_shift is None:
        precision_shift = DEFAULT_PRECISION_SHIFT

    index: int = 0
    arr: _t.List[float] = []
    last_element: float = 0
    while index < len(code):
        elm, index_shift, reps = decompress_elm_in_array(code, index)
        # print(elm, index_shift, reps)

        index += index_shift
        for _ in range(reps):
            last_element += elm
            arr.append(last_element)

    if precision_shift > 0:
        arr = [x / 10**precision_shift for x in arr]
    return arr
