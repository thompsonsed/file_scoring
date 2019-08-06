# A File Scoring Utility

A command-line utility for counting the most common words in a file or directory.

## Requirements
Python >= 3.6	

## Usage

Find all options by running `python file_scoring.py -h`:

```
usage: file_scoring.py [-h] [-s] [-v] [-n N] input [input ...]

positional arguments:
  input       the source file or directories

optional arguments:
  -h, --help  show this help message and exit
  -s          summarise the results from across all files.
  -v          output more information for scanning files and directories.
  -n N        the number of the most common words to get.
```

Provide a list of files or directories to the parser, which will output a summary of the *n* most common words in each file and directory (default n=10, override with `-n`.

```
>> python file_scoring.py tests/sample/dir1 tests/sample/sample.txt -n 2
Summarising from ['tests/sample/dir1', 'tests/sample/sample.txt']
Most common 2 words in FileScorer(tests/sample/dir1/the_adventures_of_sherlock_holmes.txt) are:
 - the (381 occurrences)
 - I (231 occurrences)
Most common 2 words in FileScorer(tests/sample/dir1/ulysses.txt) are:
 - the (305 occurrences)
 - and (181 occurrences)
Most common 2 words in FileScorer(tests/sample/dir1/psmith.txt) are:
 - the (380 occurrences)
 - of (251 occurrences)
Most common 2 words in FileScorer(tests/sample/dir1/the_romance_of_lust.txt) are:
 - and (396 occurrences)
 - the (377 occurrences)
Most common 2 words in FileScorer(tests/sample/dir1/war_and_peace.txt) are:
 - CHAPTER (366 occurrences)
 - the (64 occurrences)
Most common 2 words in FileScorer(tests/sample/dir1/moby_dick.txt) are:
 - the (350 occurrences)
 - of (225 occurrences)
Most common 2 words in FileScorer(tests/sample/dir1/dracula.txt) are:
 - the (559 occurrences)
 - and (358 occurrences)
Most common 2 words in FileScorer(tests/sample/dir1/a_tale_of_two_cities.txt) are:
 - the (536 occurrences)
 - of (298 occurrences)
Most common 2 words in FileScorer(tests/sample/dir1/the_adventures_of_tom_sawyer.txt) are:
 - the (193 occurrences)
 - and (185 occurrences)
Most common 2 words in FileScorer(tests/sample/dir1/the_moon_princess.txt) are:
 - the (568 occurrences)
 - and (368 occurrences)
Most common 2 words in FileScorer(tests/sample/sample.txt) are:
 - test (10 occurrences)
 - a (7 occurrences)
Most common 2 words in DirectoryScorer(['tests/sample/dir1', 'tests/sample/sample.txt']) are:
 - the (3713 occurrences)
 - and (2352 occurrences)
```
##Tests

Run the tests using *test_all.py* in the *tests* directory.

```
>> python test_all.py
..............
----------------------------------------------------------------------
Ran 14 tests in 0.558s

OK
```

##Classes
There are three main classes: `FileScorer`, `DirectoryScorer` and `FileScoring`. 

- `FileScorer`: holds the dictionary of words for a single file. Inherits from `Scorer`.
- `DirectoryScorer`: holds the dictionary of words for a directory, listing each text file within the directory and subdirectories. Inherits from `Scorer`.
- `FileScoring`: controls the command-line options for parsing files and directories.

## Contact
Sam Thompson
thompsonsed@gmail.com
samuel.thompson14@ic.ac.uk