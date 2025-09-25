from .compress_dict import compress_elm, normalize_dict
from .decode_data_funcs import decode_elm

# from .encode_data_funcs import stringify_elm

ALGO_VERSION = 1


def encode_dict(data: dict):
    data = normalize_dict(data)
    # data = compress_dict(data)
    data_str = compress_elm(data)
    if not data_str:
        return ""
    return f"v{ALGO_VERSION}" + data_str


def decode_dict(code: str) -> dict:
    if code[0] == "v":
        version = int(code[1])
        code = code[2:]
    else:
        version = ALGO_VERSION

    return DECODING_ALGO[version](code)


def _decode_dict_v1(code: str) -> dict:
    data = decode_elm(code)
    return data  # type: ignore


DECODING_ALGO = {1: _decode_dict_v1}
