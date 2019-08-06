import pathlib as pl
import unittest

from directory_scorer import DirectoryScorer


class TestDirectoryScorer(unittest.TestCase):
    """Tests the DirectoryScorer class by using a small set of real documents."""

    @classmethod
    def setUpClass(cls):
        cls.ds1 = DirectoryScorer(input_directory=pl.Path("sample", "dir1"), logging_level=40)
        cls.ds1.read_directory()
        cls.ds1.calculate_maximums(n=10)

    def testSetInputDirectory(self):
        """Tests that the correct errors are raised when setting the input directory."""
        ds = DirectoryScorer(logging_level=40)
        with self.assertRaises(IOError):
            ds.set_input_directory(pl.Path("sample/sample.txt"))
        with self.assertRaises(IOError):
            ds.set_input_directory(pl.Path("not_a/directory/"))
        expected_path = pl.Path("sample")
        ds.set_input_directory(expected_path)
        self.assertEqual(expected_path, ds.input_directory)

    def testAddFilesInDirectory(self):
        """Tests that adding files to a directory functions as intended, including recursively."""
        ds = DirectoryScorer(logging_level=40)
        self.assertEqual([], ds.files)
        ds.add_files_in_directory(pl.Path("sample"))
        self.assertEqual(24, len(ds.files))
        self.assertEqual(10, len(self.ds1.files))

    def testAddFile(self):
        """Tests that a file can be correctly added."""
        ds = DirectoryScorer(logging_level=40)
        total = ds.add_file(pl.Path("sample", "sample.txt"))
        self.assertEqual(1, total)
        self.assertEqual(1, len(ds.files))
        self.assertEqual(0, ds.add_file(pl.Path("sample", "notafile.txt")))
        self.assertEqual(0, ds.add_file(pl.Path("sample", "dir1", "test.json")))

    def testReadDirectory(self):
        """Tests that the files in the directory are correctly read."""
        for each in self.ds1.files:
            self.assertEqual(10, len(each.max_words))
        with open(pl.Path("sample", "exp_summary", "exp_summary1.txt"), "r") as text_file:
            expected_summary = text_file.read()
        self.assertEqual(expected_summary, self.ds1.summarise())

    def testReadDirectoryRecursive(self):
        """Tests that the files in the directory are correctly read, including scanning recursively."""
        ds = DirectoryScorer(input_directory=pl.Path("sample", "dir2"), logging_level=40)
        ds.read_directory()
        ds.calculate_maximums(n=3)
        for each in ds.files:
            self.assertEqual(3, len(each.max_words))
        with open(pl.Path("sample", "exp_summary", "exp_summary2.txt"), "r") as text_file:
            expected_summary = text_file.read()
        self.assertEqual(expected_summary, ds.summarise())
