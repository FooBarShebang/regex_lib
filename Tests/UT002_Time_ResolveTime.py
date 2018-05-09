#usr/bin/python
"""
Set of unit tests for regex_lib.Time.py module, function ResolveTime()

Version 0.1.20180509
"""

__author__ = "Anton Azarov"
__copyright__ = "(c) 2014-2018 Diagnoptics Technologies B.V."
__license__ = "GPL"
__version__ = "0.1.20180509"
__date__ = "09-05-2018"
__status__ = "Production"
__maintainer__ = "a.azarov@diagnoptics.com"

#imports

#+ standard libraries

import unittest
import sys
import os

#+ tested module and class / function

sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(__file__),
                                                                '../../..')))

from regex_lib.Time import ResolveTime

#+ test cases

class Test_ResolveTime(unittest.TestCase):
    """
    Unit tests for the regex_lib.Time.ResolveTime() function.
    
    Version 0.1.20180509
    """
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        
        Version 0.1.20180509
        """
        cls.ExceptionCases = [1, None, 1.0, [1], (1, 2), {1 : 2}, True]
        cls.NonMatchingCases = ['144', #too short for any compact time
                                '14444', #neither short compact nor compact
                                '1444444', #too long for compact time
                                '14a44', #not a digit inside
                                '14-44', #wrong separator inside
                                '24:05', #hour out of range
                                '14:60', #minute out of range
                                '14:50AM', #hour out of range
                                '0:50 p.m.', #hour out of range
                                '0:50A.m', #hour out of range
                                '13:50 pM', #hour out of range
                                '14-44:05', #wrong separator inside
                                '24:05:01', #hour out of range
                                '14:60:01', #minute out of range
                                '12:14:60', #second out of range
                                ]
        cls.MatchingCases = [('1448', '14:48:00'), #compact short time
                            ("MSC00000001_20170502_1448_PROGRAMMING_PASS.xml",
                                "14:48:00"), #compact short time
                            ('144801', '14:48:01'), #compact time
                            ('1 144801time', '14:48:01'), #compact time
                            ('14:48', '14:48:00'), #short time
                            ('1 14:48now', '14:48:00'), #short time
                            ('12:50aMnow', '00:50:00'), #short time with mod.
                            ('11:50 p.m', '23:50:00'), #short time with mod.
                            ('12:50 p.m', '12:50:00'), #short time with mod.
                            ('23:05:01', '23:05:01'), #full time pattern
                            ('now23:05:01time', '23:05:01'), #full time pattern
                            ('23:05:01.05', '23:05:01'), #full time pattern
                            ('12:14:50.', '12:14:50'), #full time pattern
                            ('12:14:50,a', '12:14:50'), #full time pattern
                            ('12:14:50.a', '12:14:50'), #full time pattern
                            ('12:14:50,5', '12:14:51'), #full time + round
                            ('23:05:1.50000', '23:05:02'), #full time + round
                            ('23:05:59.50000', '23:06:00'), #full time + round
                            ('23:59:59.50000', '00:00:00'), #full time + round
                            ('23:59:59.500000000', '00:00:00'), #same
                            ('now23:05:01.499999time', '23:05:01'), #full time
                            ('now23:05:01.49999999999time', '23:05:01'), #same
                             ]
        cls.DateIncrement = [('12:14:50,5', False),
                             ('23:05:1.50000', False),
                             ('23:05:59.50000', False),
                             ('now23:59:59.49999999999time', False),
                             ('23:59:59.49999999999', False),
                             ('23:59:59.5', True),
                             ('23:59:59.50000', True),
                             ('23:59:59.500000000', True),
                             ('now23:59:59.50000time', True),
                             ('1448', False),
                                ]
    
    def test_Exception(self):
        """
        Tested function should raise TypeError exception if the passed argument
        is not a string. Uses ExceptionCases attribute as the set of cases.
        
        Version 0.1.20180509
        """
        for gCase in self.ExceptionCases:
            self.assertRaises(TypeError, ResolveTime, gCase)
    
    def test_NotMatches(self):
        """
        Tested function should return None for the non-matching strings. Uses
        NonMatchingCases attribute as the set of cases.
        
        Version 0.1.20180509
        """
        for strCase in self.NonMatchingCases:
            strTest, _ = ResolveTime(strCase)
            self.assertIsNone(strTest, msg = 'Case: {} - {} != None'.format(
                                                            strCase, strTest))
    
    def test_Matches(self):
        """
        Tested function should return the proper date stamp for the matching
        strings. Uses MatchingCases attribute as the set of cases.
        
        Version 0.1.20180509
        """
        for strCase, strResult in self.MatchingCases:
            strTest, _ = ResolveTime(strCase)
            self.assertEqual(strTest, strResult,
                             msg = 'Case: {} - {} != {}'.format(strCase,
                                                            strTest, strResult))
    
    def test_DateIncrement(self):
        """
        Tested function should properly treat date increment due to the seconds
        roundining. Uses DateIncrement attribute as the set of cases.
        
        Version 0.1.20180509
        """
        for strCase, strResult in self.DateIncrement:
            _, strTest = ResolveTime(strCase)
            self.assertEqual(strTest, strResult,
                             msg = 'Case: {} - {} != {}'.format(strCase,
                                                            strTest, strResult))

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_ResolveTime)
TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1])

#execution entry point

if __name__ == "__main__":
    sys.stdout.write("Preparing regex_lib.Date.ResolveTime() tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)
    sys.stdout.flush()