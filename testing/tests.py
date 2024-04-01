import sys
import os
import unittest
import logging
from struct import error as StructError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'orangebox')))
from orangebox.tools import toint32, sign_extend_24bit, sign_extend_2bit, _trycast

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class TestToint32(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("----------------------------------------------------------------------")
        print("TEST FUNCTION: toint32")
        print("----------------------------------------------------------------------")
        cls.result = None

    def setUp(self):
        self.logger = logging.getLogger(self.id())

    def test_positive_number(self):
        """Test conversion with a positive number"""
        self.assertEqual(toint32(123), 123)

    def test_negative_number(self):
        """Test that numbers expected to be negative are indeed negative"""
        self.assertTrue(toint32(2147483648) < 0)

    def test_overflow(self):
        """Test integer overflow behavior"""
        # Maximum signed 32-bit int
        self.assertEqual(toint32(2**31 - 1), 2**31 - 1)
        # Just over the maximum, should wrap to negative
        self.assertEqual(toint32(2**31), -(2**31))
        # Maximum unsigned 32-bit int, should wrap to -1
        self.assertEqual(toint32(2**32 - 1), -1)

    def test_zero(self):
        """Test conversion of zero"""
        self.assertEqual(toint32(0), 0)

    def test_with_string(self):
        """Test that passing a string raises a StructError"""
        with self.assertRaises(StructError):
            toint32("string")

    def test_with_float(self):
        """Test that passing a float raises a StructError"""
        with self.assertRaises(StructError):
            toint32(3.14)

    def test_with_none(self):
        """Test that passing None raises a StructError"""
        with self.assertRaises(StructError):
            toint32(None)

class TestSignExtend24Bit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("----------------------------------------------------------------------")
        print("TEST FUNCTION: sign_extend_24bit")
        print("----------------------------------------------------------------------")

    def setUp(self):
        self.logger = logging.getLogger(self.id())

    def test_positive_integer(self):
        """Test with a positive integer within 24-bit range"""
        self.assertEqual(sign_extend_24bit(0x007FFFFF), 0x007FFFFF)
    
    def test_negative_integer(self):
        """Test with a negative integer represented in 24-bit"""
        # 0x00800000 should be sign-extended to negative
        self.assertEqual(sign_extend_24bit(0x00800000), toint32(0xFF800000))
    
    def test_overflow_integer(self):
        """Test with an integer beyond the 24-bit range"""
        self.assertEqual(sign_extend_24bit(0x01FFFFFF), toint32(0xFFFFFFFF))
    
    def test_zero(self):
        """Test with zero"""
        self.assertEqual(sign_extend_24bit(0x00000000), 0x00000000)

    def test_with_string(self):
        """Test that passing a string raises an exception"""
        with self.assertRaises((TypeError, StructError)):
            sign_extend_24bit("string")

    def test_with_float(self):
        """Test that passing a float raises an exception"""
        with self.assertRaises((TypeError, StructError)):
            sign_extend_24bit(3.14)

    def test_with_none(self):
        """Test that passing None raises an exception"""
        with self.assertRaises((TypeError, StructError)):
            sign_extend_24bit(None)

class TestSignExtend2Bit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("----------------------------------------------------------------------")
        print("TEST FUNCTION: sign_extend_2bit")
        print("----------------------------------------------------------------------")

    def setUp(self):
        self.logger = logging.getLogger(self.id())

    def test_positive_integer(self):
        """Test with a positive integer that does not require sign extension"""
        self.assertEqual(sign_extend_2bit(0x01), 0x01)
    
    def test_negative_integer(self):
        """Test with 'negative' integers that require sign extension"""
        # 0x02 should be sign-extended to indicate a negative value in 32-bit
        self.assertEqual(sign_extend_2bit(0x02), -2)
        # 0x03, when sign-extended correctly, represents -1 in a 32-bit signed integer
        self.assertEqual(sign_extend_2bit(0x03), -1)
    
    def test_overflow_integer(self):
        """Test with an integer beyond the 2-bit range"""
        self.assertEqual(sign_extend_2bit(0x0F), toint32(0xFFFFFFFF))
    
    def test_zero(self):
        """Test with zero"""
        self.assertEqual(sign_extend_2bit(0x00), 0x00)

    def test_with_string(self):
        """Test that passing a string raises an exception"""
        with self.assertRaises((TypeError, StructError)):
            sign_extend_2bit("string")

    def test_with_float(self):
        """Test that passing a float raises an exception"""
        with self.assertRaises((TypeError, StructError)):
            sign_extend_2bit(3.14)

    def test_with_none(self):
        """Test that passing None raises an exception"""
        with self.assertRaises((TypeError, StructError)):
            sign_extend_2bit(None)

class TestTryCast(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("----------------------------------------------------------------------")
        print("TEST FUNCTION: _trycast")
        print("----------------------------------------------------------------------")

    def setUp(self):
        self.logger = logging.getLogger(self.id())

    def test_hexadecimal_string(self):
        """Test conversion of hexadecimal string to integer."""
        self.assertEqual(_trycast("0x1a"), 26)
        self.assertEqual(_trycast("0xFF"), 255)

    def test_integer_string(self):
        """Test conversion of integer string to int."""
        self.assertEqual(_trycast("10"), 10)
        self.assertEqual(_trycast("-42"), -42)

    def test_float_string(self):
        """Test conversion of float string to float."""
        self.assertEqual(_trycast("3.14"), 3.14)
        self.assertEqual(_trycast("-0.001"), -0.001)

    def test_non_convertible_string(self):
        """Test with strings that cannot be converted."""
        self.assertEqual(_trycast("abc"), "abc")
        self.assertEqual(_trycast("4.5.6"), "4.5.6")

    def test_edge_cases(self):
        """Test edge cases, including empty strings and strings with spaces."""
        self.assertEqual(_trycast(""), "")
        self.assertEqual(_trycast(" "), " ")
        self.assertEqual(_trycast(" 100 "), 100)
        self.assertEqual(_trycast("+50"), 50)
        self.assertEqual(_trycast("-0.05"), -0.05)
        with self.assertRaises((AttributeError)):
            self.assertEqual(_trycast(None), None)

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