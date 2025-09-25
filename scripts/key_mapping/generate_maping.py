# https://www.ssec.wisc.edu/~tomw/java/unicode.html
# https://www.compart.com/en/unicode/category
import unicodedata

CURRENT_VERSION = "v1"
EXPECTED_NUMBER_OF_SYMBOLS = 64


def compute_encoding_maps():
    encoding_map_ = {}
    decoding_map_ = {}
    number = 0
    forbidden_symbols = (
        # [" ", "?", "=", '"', "'", "&", ";", ",", ".", "_", "#", "\\"]
        [" ", '"', "'", "&", ",", "\\", "#", ".", "_", "$", "+", ":", "@", "%", "^", "`", "¡", "¢"]
        + ["(", ")", "{", "}", "[", "]"]
        + [str(i) for i in range(10)]
        # + [chr(i) for i in range(97, 123)]  # a-z
    )
    forbidden_categories = {"Mn"}

    forbidden_code = set(ord(symbol) for symbol in forbidden_symbols)
    for i in range(0, 6_000):
        if EXPECTED_NUMBER_OF_SYMBOLS <= number:
            break
        if i in forbidden_code:
            continue
        symbol = chr(i)
        if symbol.isprintable() and unicodedata.category(symbol) not in forbidden_categories:
            # print(i, symbol)
            encoding_map_[number] = symbol
            decoding_map_[symbol] = number
            number += 1

    return encoding_map_, decoding_map_


if __name__ == "__main__":
    encoding_map, decoding_map = compute_encoding_maps()
    python_library_path = f"../../pltsave/compress/encoding_maps_{CURRENT_VERSION}.py"
    ts_library_path = f"../../pltsave_ts/encoding_maps_{CURRENT_VERSION}.ts"

    with open(python_library_path, "w", encoding="utf-8") as f:
        f.write("ENCODING_MAP = {\n")
        for k, v in encoding_map.items():
            f.write(f'    {k}: "{v}",\n')
        f.write("}\n")
        f.write("DECODING_MAP = {\n")
        for k, v in decoding_map.items():
            f.write(f'    "{k}": {v},\n')
        f.write("}\n")

    with open(ts_library_path, "w", encoding="utf-8") as f:
        f.write("export const ENCODING_MAP: Record<number, string> = {\n")
        for k, v in encoding_map.items():
            f.write(f"    {k}: '{v}',\n")
        f.write("};\n")
        f.write("export const DECODING_MAP: Record<string, number> = {\n")
        for k, v in decoding_map.items():
            f.write(f"    '{k}': {v},\n")
        f.write("};\n")
