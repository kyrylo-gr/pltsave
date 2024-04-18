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
    def test_array(self):
        array: List[float] = list(range(1000))
        compressed = compress.compress_array(array)

        decompressed = compress.decompress_array(compressed)
        self.assertEqual(array, decompressed)

    def test_big_array(self):
        array: List[float] = list(range(int(1e4), int(1e8), 957))
        compressed = compress.compress_array(array)
        decompressed = compress.decompress_array(compressed)
        self.assertEqual(array, decompressed)
