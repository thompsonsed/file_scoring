import logging
import re
from collections import OrderedDict
from operator import itemgetter


class Scorer(object):
    """
    Holds the information for a single object, counting all individual words within the file.

    Used as the base class for FileScorer and DirectoryScorer.
    """

    def __init__(self, logger: logging.Logger = None, logging_level: int = logging.WARNING) -> None:
        """
        Creates the Scorer object.

        :param logging.Logger logger: a logging.Logger object for outputting information
        :param int logging_level: the severity level for logging
        """
        self.words = OrderedDict()
        self.max_words = []
        if logger is None:
            logger = logging.getLogger("scorer")
        self.logger = logger
        self.logger.setLevel(logging_level)
        self.logging_level = logging_level
        self.n = 0

    def __str__(self) -> str:
        """
        Gets the string representation of the object.

        :return: the name of the object.
        :rtype: str
        """
        return "Scorer"

    @staticmethod
    def get_words_in_line(line: str) -> list:
        """
        Gets a list of the words in the line, ignoring the punctuation and digits.

        :param str line: the line of characters to parse

        :return: a list of the words in the line
        :rtype: list
        """
        if not isinstance(line, str):
            raise TypeError("Provided line of {} is not a string.".format(line))
        words = re.sub("[^A-z\s]", " ", line).split()
        words.sort()
        return words

    def add_word(self, word: str) -> None:
        """
        Adds a word to the dictionary of words in this file or increments the count if it already exists.

        :param str word: the word to add to the dictionary

        :return: None
        :rtype: None
        """
        if word is not None and len(word) > 0:
            if word not in self.words.keys():
                self.words[word] = 1
            else:
                self.words[word] += 1

    def calculate_maximums(self, n: int = 10) -> None:
        """
        Calculates the maximum words in the file.

        @param int n: the number of maximums to calculate.

        :return: None
        :rtype: None
        """
        if len(self.words) <= n:
            self.max_words = [(k, v) for k, v in self.words.items()]
        else:
            self.max_words = [(k, v) for k, v in sorted(self.words.items(), key=itemgetter(1, 0))[-n:]]
        self.n = n

    def summarise(self) -> str:
        """
        Gets the summary of the maximum words in this file to the terminal.

        :return: string containing the summary info
        :rtype: str
        """

        output = "Most common {} words in {} are:\n".format(self.n, self.__str__())
        for k, v in reversed(self.max_words):
            output += " - {} ({} occurrences)\n".format(k, v)
        return output

    def get_words_copy(self) -> dict:
        """
        Gets a copy of the dictionary of words.

        :return: the dictionary of words
        :rtype: dict
        """
        return self.words.copy()
