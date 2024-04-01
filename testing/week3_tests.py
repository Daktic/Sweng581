import sys
import os
import unittest
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'orangebox')))
from orangebox import Parser



class TestSpecifiedGraphFunctions(unittest.TestCase):

    # Load a file
    parser = Parser.load("BTFL_BLACKBOX_LOG_20240322_235024.BBL")
    header_data = parser.headers
    frame_data = ()
    for frame in parser.frames():
            frame_data = frame.data
            break

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @classmethod
    def setUpClass(cls):
        print("----------------------------------------------------------------------")
        print("TEST: Specified Graph Functions: ")
        print("             toint32, sign_extend_24bit, sign_extend_2bit, _trycast")
        print("----------------------------------------------------------------------")
        cls.result = None

    def setUp(self):
        self.logger = logging.getLogger(self.id())

    def test_header_string(self):
        test_header = 'Blackbox flight data recorder by Nicholas Sherlock'  
        self.assertEqual(self.header_data['Product'], test_header)

    def test_header_float(self):
        test_header = [142, 148, 142.5]
        self.assertEqual(self.header_data['ff_weight'], test_header)
    
    def test_header_hex(self):
        test_header = 1065353216
        self.assertEqual(self.header_data['gyro_scale'], test_header)

    def test_header_int(self):
        test_header = 90
        self.assertEqual(self.header_data['simplified_pitch_d_gain'], test_header)

    def test_frame_2bit(self):
        test_frame = -1
        self.parser.set_log_index(2)
        self.assertEqual(self.frame_data[27], test_frame)

    def test_frame_24bit(self):
        test_frame = -82292728
        self.parser.set_log_index(2)
        self.assertEqual(self.frame_data[1], test_frame)

    def test_frame_int(self):
        test_frame = 39
        self.parser.set_log_index(2)
        self.assertEqual(self.frame_data[37], test_frame)

class LoggingTestResult(unittest.TextTestResult):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def startTest(self, test):
        logging.info(f'Starting test: {test._testMethodName}')
        super().startTest(test)
    
    def addSuccess(self, test):
        logging.info(f'Test passed: {test._testMethodName}\n')
        super().addSuccess(test)
    
    def addError(self, test, err):
        logging.error(f'Test error: {test._testMethodName}\n')
        super().addError(test, err)
    
    def addFailure(self, test, err):
        logging.error(f'Test failed: {test._testMethodName}\n')
        super().addFailure(test, err)

class LoggingTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, resultclass=LoggingTestResult, **kwargs)

    def _makeResult(self):
        return LoggingTestResult(self.stream, self.descriptions, self.verbosity)

if __name__ == '__main__':
    unittest.main(testRunner=LoggingTestRunner())
