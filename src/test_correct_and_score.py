import unittest
from correct_and_score import connect_and_score

class TestConnectAndScore(unittest.TestCase):
    def test_same_word(self):
        word = "hell"
        word_dict = {
            4: {"hell": ["file2-2"]}
        }
        result = connect_and_score(word, word_dict)
        expected = [("hell", 8)]  # 4 matching characters * 2 points each
        self.assertEqual(result, expected)

    def test_added_character(self):
        word = "hell"
        word_dict = {
            5: {"hellh": ["file2-3"]}
        }
        result = connect_and_score(word, word_dict)
        expected = [("hellh", 6)]  # -2 for adding a letter, 4 matching characters * 2 points each
        self.assertEqual(result, expected)

    def test_switched_characters(self):
        word = "hell"
        word_dict = {
            4: {"hall": ["file2-4"]}
        }
        result = connect_and_score(word, word_dict)
        expected = [("hall", 2)]  # -5 for replacing 'e' with 'a', 3 matching characters * 2 points each
        self.assertEqual(result, expected)

    def test_deleted_character(self):
        word = "hell"
        word_dict = {
            3: {"hel": ["file2-5"]}
        }
        result = connect_and_score(word, word_dict)
        expected = [("hel", 2)]  # -2 for deleting a character, 3 matching characters * 2 points each
        self.assertEqual(result, expected)

    def test_added_strange_character(self):
        word = "hell"
        word_dict = {
            5: {"hello": ["file2-6"]}
        }
        result = connect_and_score(word, word_dict)
        expected = [("hello", 6)]  # -2 for adding a character, 4 matching characters * 2 points each
        self.assertEqual(result, expected)

    def test_duplicate_words_with_higher_scores(self):
        word = "hell"
        word_dict = {
            4: {"hell": ["file2-2"], "hell": ["file2-7"]},  # Same word appears multiple times
            5: {"hellh": ["file2-3"], "hellh": ["file2-6"]}
        }
        result = connect_and_score(word, word_dict)
        expected = [("hell", 8), ("hellh", 6)]  # Should take the highest score for each duplicate word
        self.assertEqual(result, expected)

    def test_multiple_suggestions(self):
        word = "hell"
        word_dict = {
            4: {"hell": ["file2-2"], "hall": ["file2-4"], "hull": ["file2-5"]},
            5: {"hello": ["file2-6"], "hellh": ["file2-3"]}
        }
        result = connect_and_score(word, word_dict)
        expected = [("hell", 8), ("hellh", 6), ("hello", 6), ("hall", 2), ("hull", 2)]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
