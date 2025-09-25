import unicodedata


def compute_encoding_maps():
    encoding_map = {}
    decoding_map = {}

    number = 0
    forbidden_symbols = (
        [" ", "?", "=", '"', "'", "&", ";", ",", ".", "_", "#"]
        + ["(", ")", "{", "}", "[", "]"]
        + [str(i) for i in range(10)]
        + [chr(i) for i in range(97, 123)]  # a-z
    )
    forbidden_categories = {"Mn"}

    forbidden_code = set(ord(symbol) for symbol in forbidden_symbols)
    for i in range(0, 100_000):
        if i in forbidden_code:
            continue
        symbol = chr(i)
        if symbol.isprintable() and unicodedata.category(symbol) not in forbidden_categories:
            encoding_map[number] = symbol
            decoding_map[symbol] = number
            number += 1

    return encoding_map, decoding_map


ENCODING_MAP, DECODING_MAP = compute_encoding_maps()
