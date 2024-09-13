import unittest

from google_autocomplete_project.src.scoring import calculate_score, top_5


class TestCalculateScore(unittest.TestCase):
    def test_same_word(self):
        word = "hell"
        suggestions = {"hell"}
        result = calculate_score(word, suggestions)
        expected = {"hell": 8}
        self.assertEqual(result, expected)

    def test_added_character(self):
        word = "hell"
        suggestions = {"hellh"}
        result = calculate_score(word, suggestions)
        expected = {"hellh": 6}
        self.assertEqual(result, expected)

    def test_switched_characters(self):
        word = "hell"
        suggestions = {"hall"}
        result = calculate_score(word, suggestions)
        expected = {"hall": 2}
        self.assertEqual(result, expected)

    def test_deleted_character(self):
        word = "hell"
        suggestions = {"hel"}
        result = calculate_score(word, suggestions)
        expected = {"hel": 2}
        self.assertEqual(result, expected)

    def test_added_strange_character(self):
        word = "hell"
        suggestions = {"hello"}
        result = calculate_score(word, suggestions)
        expected = {"hello": 6}
        self.assertEqual(result, expected)

    def test_switched_with_existing_character(self):
        word = "hell"
        suggestions = {"hhll"}
        result = calculate_score(word, suggestions)
        expected = {"hhll": 2}
        self.assertEqual(result, expected)

    def test_all_options(self):
        word = "hell"
        suggestions = {"hell", "hellh", "hall", "hel", "hello", "hhll"}
        result = calculate_score(word, suggestions)
        expected = {"hell": 8, "hellh": 6, "hall": 2, "hel": 2, "hello": 6, "hhll": 2}
        self.assertEqual(result, expected)

class TestTop5(unittest.TestCase):
    def test_top_5_suggestions(self):
        user_word = "hell"
        suggestions = {"hell", "hello", "hel", "hall", "hellh"}
        result = top_5(user_word, suggestions)
        expected = {"hell": 8, "hello": 6, "hellh": 6, "hall": 2, "hel": 2}
        self.assertEqual(result, expected)

    def test_less_than_5_suggestions(self):
        user_word = "hell"
        suggestions = {"hell", "hello", "hel"}
        result = top_5(user_word, suggestions)
        expected = {"hell": 8, "hello": 6, "hel": 2}
        self.assertEqual(result, expected)

    def test_empty_suggestions(self):
        user_word = "hell"
        suggestions = set()
        result = top_5(user_word, suggestions)
        expected = {}
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
