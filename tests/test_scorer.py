import unittest

from scorer import Scorer


class TestScorer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Sets up the TestScorer class by creating a simple Scorer object."""
        cls.scorer = Scorer()
        for word, total in [("word", 10), ("another", 5), ("yet", 2)]:
            for i in range(total):
                cls.scorer.add_word(word)
        cls.scorer.calculate_maximums(2)

    def testGetWordsInLine(self):
        """Tests that lines are properly split into a list of words."""

        expected_words = ["a", "also", "but", "in", "line", "punctuation", "some", "with", "words"]
        actual_words = Scorer.get_words_in_line(line="a line with some words in, but also punctuation!")
        self.assertEqual(expected_words, actual_words)
        for each in [["list of words"], None, 10]:
            with self.assertRaises(TypeError):
                _ = Scorer.get_words_in_line(each)
        expected_words = ["a", "digits", "line", "with"]
        actual_words = Scorer.get_words_in_line(line="a10line10with49digits")
        self.assertEqual(expected_words, actual_words)

    def testAddWord(self):
        """Tests that adding words to the dictionary counter works as expected."""
        fs = Scorer()
        fs.add_word("word")
        expected_dict = {"word": 1}
        self.assertEqual(expected_dict, fs.words)
        fs.add_word("word")
        expected_dict = {"word": 2}
        self.assertEqual(expected_dict, fs.words)

    def testCalculateMaximums(self):
        """Tests that the maximums are correctly calculated."""
        self.assertEqual([("another", 5), ("word", 10)], self.scorer.max_words)
        self.assertEqual(2, self.scorer.n)

    def testCalculateMaximumsGreater(self):
        scorer = Scorer()
        scorer.words = self.scorer.get_words_copy()
        scorer.calculate_maximums(n=1000)
        self.assertEqual(3, len(scorer.max_words))
        self.assertEqual(1000, scorer.n)
        self.assertEqual([("word", 10), ("another", 5), ("yet", 2)], scorer.max_words)

    def testSummary(self):
        """Tests that the summary is correctly generated."""

        expected_str = "Most common 2 words in Scorer are:\n - word (10 occurrences)\n - another (5 occurrences)\n"
        self.assertEqual(expected_str, self.scorer.summarise())

    def testString(self):
        """Tests that the string representation of the object makes sense."""
        expected_str = "Scorer"
        self.assertEqual(expected_str, self.scorer.__str__())
        self.assertEqual(expected_str, str(self.scorer))
