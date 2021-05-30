import unittest

from src.utils.string_utils import isEmptyOrNone, isBlankOrNone


class StringUtilsTests(unittest.TestCase):
    EMPTY_STRING = ""
    SPACE_STRING = " "
    BLANK_STRING = SPACE_STRING + SPACE_STRING

    def test_isEmptyOfNone_base_usage(self):
        self.assertEqual(isEmptyOrNone(self.EMPTY_STRING), True)
        self.assertEqual(isEmptyOrNone(None), True)

    def test_isEmptyOfNone_blank_string(self):
        self.assertEqual(isEmptyOrNone(self.BLANK_STRING), False)

    def test_isBlankOrNone_base_usage(self):
        self.assertEqual(isBlankOrNone(self.EMPTY_STRING), True)
        self.assertEqual(isBlankOrNone(None), True)

    def test_isBlankOrNone_blank_string(self):
        self.assertEqual(isBlankOrNone(self.BLANK_STRING), True)


if __name__ == '__main__':
    unittest.main()
