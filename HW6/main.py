# Group Members: Lily Kendall, Lacey Eckert, Brody Pinto
import unittest

if __name__ == "__main__":

    # Discover and run all test files in the current directory
    # code from ChatGPT with prompt: for python unittests, how do I run every test from every file in main?
    loader = unittest.TestLoader()
    suite = loader.discover('.')
    runner = unittest.TextTestRunner()
    runner.run(suite)


