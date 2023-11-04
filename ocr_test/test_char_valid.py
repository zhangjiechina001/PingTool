from ocr.char_valid import FurnaceNumberValid, IndexValid, LengthValid, BrandValid
import unittest


class CharValidTest(unittest.TestCase):
    def test_furnace_valid(self):
        valid = FurnaceNumberValid()
        assert valid.valid('3030138')
        assert valid.valid('Z')

    def test_index_valid(self):
        valid = IndexValid()
        assert valid.valid('120')

    def test_length_valid(self):
        valid = LengthValid()
        assert valid.valid('6800')
        assert not valid.valid('0068')

    def test_brand_valid(self):
        valid = BrandValid()
        assert valid.valid('20CrMoH')
        assert valid.valid('ABC')
