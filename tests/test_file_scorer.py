import pathlib as pl
import unittest
from collections import OrderedDict

from file_scorer import FileScorer


class TestFileScorer(unittest.TestCase):
    def testSetInput(self):
        """Tests that the input is correctly set and throws the appropriate errors."""
        fs = FileScorer()
        with self.assertRaises(IOError):
            fs.set_input_file(input_file=pl.Path("sample"))
        with self.assertRaises(IOError):
            fs.set_input_file(input_file=pl.Path("sample/sample2.txt"))

    def testReadSmallFile(self):
        """Tests that a small file is correctly read and parsed."""
        fs = FileScorer(input_file=pl.Path("sample", "sample.txt"))
        fs.read_file()
        fs.calculate_maximums()
        expected_dict = OrderedDict(
            {
                "test": 10,
                "and": 3,
                "a": 7,
                "b": 6,
                "c": 6,
                "cat": 5,
                "dog": 4,
                "can": 1,
                "cup": 3,
                "table": 5,
                "chair": 4,
                "chairs": 1,
            }
        )
        self.assertEqual(expected_dict, fs.words)
        expected_maximums = [
            ("and", 3),
            ("cup", 3),
            ("chair", 4),
            ("dog", 4),
            ("cat", 5),
            ("table", 5),
            ("b", 6),
            ("c", 6),
            ("a", 7),
            ("test", 10),
        ]
        self.assertEqual(expected_maximums, fs.max_words)
        self.assertEqual(10, len(fs.max_words))
        expected_maximums = [("c", 6), ("a", 7), ("test", 10)]

        fs.calculate_maximums(n=3)
        self.assertEqual(3, len(fs.max_words))
        self.assertEqual(expected_maximums, fs.max_words)

    def testReadsLargeFile(self):
        """Tests that a large file is correctly read and parsed."""
        fs = FileScorer(input_file=pl.Path("sample", "pride_and_prejudice.txt"))
        fs.read_file()
        fs.calculate_maximums()
        expected_maximums = [
            ("that", 1509),
            ("was", 1841),
            ("in", 1850),
            ("a", 1961),
            ("I", 2066),
            ("her", 2118),
            ("and", 3500),
            ("of", 3706),
            ("to", 4186),
            ("the", 4218),
        ]

        self.assertEqual(10, len(fs.max_words))
        self.assertEqual(expected_maximums, fs.max_words)
