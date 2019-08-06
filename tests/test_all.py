import argparse
import unittest
import sys

sys.path.append("../")



def main(verbosity=1):
    """
    Runs all tests.

	:param verbosity: the level of information to display from the unittest module

	.. note:: The working directory is changed to the package install location for the duration of this execution.
	"""
    test_loader = unittest.TestLoader().discover(".")
    unittest.TextTestRunner(verbosity=verbosity).run(test_loader)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test file_scoring module functions correctly")
    parser.add_argument("-v", "--verbose", help="Use verbose mode.", action="store_true", default=False)
    args, unknown = parser.parse_known_args()
    if args.verbose:
        main(2)
    else:
        main()
