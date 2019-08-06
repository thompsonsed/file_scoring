import argparse
import logging
import pathlib

from directory_scorer import DirectoryScorer


class FileScoring:
    """Runs the file scoring utility, counting the most common words in a list of files or directories."""

    def __init__(self) -> None:
        self.summarise = True
        self.input = []
        self.logging_level = logging.ERROR
        self.scorer = None
        self.n = 0

        self.parse_arguments()

    def parse_arguments(self) -> None:
        """
        Parse the command-line arguments provided by the user.

        :rtype: None
        :return: None
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("input", nargs="+", help="the source file or directories", action="store")
        parser.add_argument(
            "-s",
            dest="summarise",
            action="store_true",
            required=False,
            default=True,
            help="summarise the results from across all files.",
        )
        parser.add_argument(
            "-v",
            dest="verbose",
            action="store_true",
            default=False,
            help="output more information for scanning files and directories.",
        )
        parser.add_argument(
            "-n",
            dest="n",
            action="store",
            type=int,
            default=10,
            required=False,
            help="the number of the most common words to get.",
        )
        arguments = parser.parse_args()
        self.summarise = arguments.summarise
        self.directory = arguments.input
        if arguments.verbose:
            self.logging_level = logging.INFO
        self.scorer = DirectoryScorer(logging_level=self.logging_level)
        self.n = arguments.n
        for each in arguments.input:
            self.input.append(pathlib.Path(each))

    def add_files_and_parse(self) -> None:
        """
        Adds the files to the DirectoryScorer object and parses.

        :return: None
        :rtype: None
        """
        for fd in self.input:
            if fd.is_file():
                self.scorer.add_file(fd)
            elif fd.is_dir():
                self.scorer.add_files_in_directory(fd)
        self.scorer.parse()
        self.scorer.calculate_maximums(n=self.n)

    def output_summary(self) -> None:
        """
        Prints the summary to the command line, if summarise is True.

        :return: None
        :rtype: None
        """
        self.scorer.input_directory = [str(x) for x in self.input]
        print(self.scorer.summarise(summarise_total=self.summarise))


if __name__ == "__main__":
    fso = FileScoring()
    fso.add_files_and_parse()
    fso.output_summary()
