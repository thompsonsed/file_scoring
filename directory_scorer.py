import logging
import pathlib as pl
import operator

from file_scorer import FileScorer
from scorer import Scorer


class DirectoryScorer(Scorer):
    """
    Holds the information for a single directory, counting all individual words within the file.

    Example:
        Provide a directory
        ``ds = DirectoryScorer(input_directory="my_directory")``
        Read the files in the directory
        ``ds.read_directory()``
        Calculate the 5 most common words in each file and as a total.
        ``ds.calculate_maximums(n=5)``
        Print out the summary.
        ``print(ds.summary)``
    """

    def __init__(
            self, input_directory: pl.Path = None, logger: logging.Logger = None, logging_level: int = logging.WARNING
    ) -> None:
        """
        Creates the DirectoryScorer object.

        :param pl.Path input_directory: the directory from which to parse files
        :param logging.Logger logger: a logging.Logger object for outputting information
        :param int logging_level: the severity level for logging
        """
        Scorer.__init__(self, logger=logger, logging_level=logging_level)
        self.input_directory = None
        self.set_input_directory(input_directory)
        self.files = []

    def __str__(self) -> str:
        """
        Gets the string representation of the object.

        :return: the name of the object.
        :rtype: str
        """
        return "DirectoryScorer({})".format(self.input_directory)

    def set_input_directory(self, input_directory: pl.Path) -> None:
        """
        Sets the input file.

        If input_file is None, does nothing.

        :param pl.Path input_directory: the file to use for this FileScorer.

        :return: None
        :rtype: None
        """
        if input_directory is not None:
            if not pl.Path.is_dir(input_directory) or not pl.Path.exists(input_directory):
                raise IOError("Path at {} does not exist or is not a directory.".format(input_directory))
            self.input_directory = input_directory

    def read_directory(self, input_directory: pl.Path = None) -> None:
        """
        Reads the files from the given directory, recursively.

        :param pl.Path input_directory: the directory path to parse

        :return: None
        :rtype: None
        """
        self.set_input_directory(input_directory)
        total = self.add_files_in_directory(self.input_directory)
        self.logger.info("Parsing {} files...".format(total))
        self.parse()

    def parse(self) -> None:
        """
        Reads and parses each file in the file list.

        :return: None
        :rtype: None
        """
        self.files = sorted(self.files, key=operator.attrgetter("input_file"))
        for file in self.files:
            file.read_file()

    def add_files_in_directory(self, directory: pl.Path) -> int:
        """
        Adds all the files in the directory, recursively, returning the total number of files.

        :param pl.Path directory: the directory to add files from

        :return: the total number of files in the directory
        :rtype: int
        """
        total = 0
        for each in directory.iterdir():
            if each.is_file():
                total += self.add_file(each)
            else:
                total += self.add_files_in_directory(each)
        return total

    def add_file(self, file: pl.Path) -> int:
        """
        Adds the file to the directory, if it is a text file.

        :param pl.Path file: the file or path to add
        :return: 1 if the file is added, 0 otherwise.
        """
        try:
            self.files.append(FileScorer(input_file=file, logging_level=self.logging_level))
            return 1
        except IOError as ioe:
            self.logger.warning("Skipping {}: {}.".format(file, ioe))
            return 0

    def combine_words(self) -> None:
        """
        Combines the words from across all parsed files into a single dictionary.

        :return: None
        :rtype: None
        """
        for file in self.files:
            for k, v in file.words.items():
                if k in self.words:
                    self.words[k] += v
                else:
                    self.words[k] = v

    def calculate_maximums(self, n: int = 10) -> None:
        """
        Calculates the maximum values for each file in the list.

        :param int n: the number of maximum values to find

        :return: None
        :rtype: None
        """
        self.combine_words()
        for file in self.files:
            file.calculate_maximums(n=n)
        Scorer.calculate_maximums(self, n=n)

    def summarise(self, summarise_total: bool = True) -> str:
        """
        Gets the summaries for each of the files within the directory and then gets the total summary.

        :return: the summary of each file and the sum of all files
        :rtype: str
        """
        output = "Summarising from {}\n".format(self.input_directory)
        for file in self.files:
            output += file.summarise()
        if summarise_total:
            output += Scorer.summarise(self)
        return output
