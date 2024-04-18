ENCODING_MAP = {}
DECODING_MAP = {}


def compute_encoding_maps():
    number = 0
    forbidden_symbols = (
        [" ", "?", "=", '"', "'", "&", ";", ",", ".", "_", "#"]
        + ["(", ")", "{", "}", "[", "]"]
        + [str(i) for i in range(10)]
        + [chr(i) for i in range(97, 123)]  # a-z
    )

    forbidden_code = set(ord(symbol) for symbol in forbidden_symbols)
    for i in range(0, 100000):
        if i in forbidden_code:
            continue
        symbol = chr(i)
        if symbol.isprintable():
            # print(i, symbol)
            ENCODING_MAP[number] = symbol
            DECODING_MAP[symbol] = number
            number += 1


compute_encoding_maps()
