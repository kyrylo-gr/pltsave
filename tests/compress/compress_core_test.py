import unittest
from typing import List

from pltsave import compress


class CompressNumbersTest(unittest.TestCase):
    def test_integers_less_1000(self):
        for i in range(1000):
            self.assertEqual(i, compress.decompress_number(compress.compress_number(i)))

    def test_big_integers(self):
        for i in range(int(1e4), int(1e8), 997):
            self.assertEqual(i, compress.decompress_number(compress.compress_number(i)))

    def test_floats_default_precision(self):
        for i in range(int(1e4), int(1e8), 997):
            number = i / 1000
            result = round(
                compress.decompress_number(compress.compress_number(number)),
                compress.DEFAULT_PRECISION,
            )
            self.assertEqual(number, result)

    def test_floats_precision(self):
        precision = 2
        for i in range(int(1e4), int(1e8), 997):
            number = i / 1000
            result = round(
                compress.decompress_number(compress.compress_number(number, precision=precision)),
                precision,
            )
            self.assertEqual(
                round(number, precision), result, msg=f"number={number}, result={result}"
            )


class CompressArrayTest(unittest.TestCase):
    def compress_and_compare(self, array):
        compressed = compress.compress_array(array)
        decompressed = compress.decompress_array(compressed)
        self.assertEqual(len(array), len(decompressed))
        for i, j in zip(array, decompressed):
            self.assertAlmostEqual(i, j, places=3)

    def test_array(self):
        array: List[float] = list(range(1000))
        self.compress_and_compare(array)

    def test_float(self):
        array: List[float] = [i / 100 for i in range(1000)]
        self.compress_and_compare(array)

    def test_big_array(self):
        array: List[float] = list(range(int(1e4), int(1e8), 957))
        self.compress_and_compare(array)


class CompressDifferentTypesTest(unittest.TestCase):
    def compress_and_compare(self, val):
        compressed = str(compress.compress_elm(val))
        decompressed = compress.decode_elm(compressed)
        self.assertEqual(
            val, decompressed, msg=f"val={val}, compressed={compressed} decompressed={decompressed}"
        )

    def test_int(self):
        self.compress_and_compare(123)

    def test_float(self):
        self.compress_and_compare(123.456)

    def test_string(self):
        self.compress_and_compare("hello")

    def test_hex(self):
        self.compress_and_compare("#1234")

    def test_array(self):
        self.compress_and_compare([1, 2, 3, 4])

    def test_array_float(self):
        self.compress_and_compare([1.1, 2.2, 3.3, 4.4])

    def test_dict(self):
        self.compress_and_compare({"aaa": 1, "bb": 2, "ccc": 3})

    def test_nested_dict(self):
        self.compress_and_compare({"a": 1, "b": {"c": 2, "d": 3}})
