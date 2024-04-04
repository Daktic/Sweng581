import unittest
import datetime
import sys

from week3_tests import TestSpecifiedGraphFunctions, LoggingTestRunner

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestSpecifiedGraphFunctions))
    return suite

def continuous_run(time_in_hours):
    # capture the time now and calculate how long to run the tests
    time_now = datetime.datetime.now()
    time_end = time_now + datetime.timedelta(hours=time_in_hours)

    iteration = 0 # Initialize the iteration counter

    with open(f"./logs/test_results_for_time_{time_in_hours}.log", "w") as log_file:
        log_file.write(f"Test started at {time_now}\n")
        # Used to capture the logging output to file
        sys.stdout = log_file
        sys.stderr = log_file

        while datetime.datetime.now() < time_end:
            print("\n\n\n" + "=" * 70)
            print(f"\nRunning iteration: {iteration + 1}")
            print(f"TimeStamp: {datetime.datetime.now()}\n")
            print("=" * 70 + "\n")
            runner = LoggingTestRunner()
            runner.run(suite())
            iteration += 1
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


if __name__ == '__main__':
    continuous_run(1)  # Run the tests for 1 hour
    continuous_run(4)  # Run the tests for 4 hour
    continuous_run(12)  # Run the tests for 12 hour
