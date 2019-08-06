import logging
import pathlib as pl

from scorer import Scorer


class FileScorer(Scorer):
    """
    Holds the information for a single file.

    Example:
        Provide a file.
        ``fs = FileScorer(input_file="my_file")``
        Read the file.
        ``fs.read_file()``
        Calculate the 5 most common words in the file.
        ``fs.calculate_maximums(n=5)``
        Print out the summary.
        ``print(fs.summary)``
    """

    def __init__(
        self, input_file: pl.Path = None, logger: logging.Logger = None, logging_level: int = logging.WARNING
    ) -> None:
        """
        Creates the FileScorer object.

        :param pl.Path input_file: the file to parse
        :param logging.Logger logger: a logging.Logger object for outputting information
        :param int logging_level: the severity level for logging
        """
        Scorer.__init__(self, logger=logger, logging_level=logging_level)
        self.input_file = None
        self.set_input_file(input_file)

    def __str__(self) -> str:
        """
        Gets the string representation of the object.

        :return: the name of the object.
        :rtype: str
        """
        return "FileScorer({})".format(self.input_file)

    def set_input_file(self, input_file: pl.Path) -> None:
        """
        Sets the input file.

        If input_file is None, does nothing.

        :param pl.Path input_file: the file to use for this FileScorer.

        :return: None
        :rtype: None
        """
        if input_file is not None:
            if not input_file.is_file() or not input_file.exists():
                raise IOError("Path at {} does not exist or is not a file.".format(input_file))
            if not input_file.suffix == ".txt":
                raise IOError("File is not a txt file at {}.".format(input_file))
            self.input_file = input_file

    def read_file(self, input_file: pl.Path = None) -> None:
        """
        Reads the input file and counts the words.

        :param pl.Path input_file: the file to read and count words from.

        :return: None
        :rtype: None
        """
        self.set_input_file(input_file)
        self.logger.info("Reading file {}.".format(self.input_file))
        try:
            with open(self.input_file, "r") as file:
                lines = file.readlines()
        except UnicodeDecodeError as ue:
            self.logger.info("{}".format(ue))
            self.logger.info("Detected binary file at {}, converting.".format(self.input_file))
            with open(self.input_file, "rb") as file:
                lines = [x.decode() for x in file.readlines()]
        for line in lines:
            words = self.get_words_in_line(line)
            for word in words:
                self.add_word(word)
