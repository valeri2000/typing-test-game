"""File with tests for methods in utils.py
"""

import unittest

from utils import generate_fixed_length_text
from utils import text_with_fixed_column_size
from utils import total_characters_in_text


class TestUtilsMethods(unittest.TestCase):
    """Tests for methods in utils.py
    """

    def test_generate_fixed_length_text(self):
        """Test for generate_fixed_length_text method
        """

        ten, sixty = 10, 60
        ten_words_text = generate_fixed_length_text(ten)
        sixty_words_text = generate_fixed_length_text(sixty)
        self.assertEqual(len(ten_words_text), ten)
        self.assertEqual(len(sixty_words_text), sixty)

    def test_text_with_fixed_column_size(self):
        """Test for text_with_fixed_column_size method
        """

        text = generate_fixed_length_text(100)
        lim_cols = 15
        text = text_with_fixed_column_size(text, lim_cols)
        for row in text:
            self.assertLessEqual(len(row), lim_cols)

    def test_total_characters_in_text(self):
        """Test for total_characters_in_text method
        """

        text = ['a', 'aaa', 'aa', 'aaaa']
        self.assertEqual(total_characters_in_text(text), 10)


if __name__ == '__main__':
    unittest.main()
