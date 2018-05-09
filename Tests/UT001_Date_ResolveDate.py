#usr/bin/python
"""
Set of unit tests for regex_lib.Date.py module, function ResolveDate()

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

from regex_lib.Date import ResolveDate

#+ test cases

class Test_ResolveDate(unittest.TestCase):
    """
    Unit tests for the regex_lib.Date.ResolveDate() function.
    
    Version 0.1.20180509
    """
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        
        Version 0.1.20180509
        """
        cls.ExceptionCases = [1, None, 1.0, [1], (1, 2), {1 : 2}, True]
        cls.NonMatchingCases = ['120180509', #too long for compact date
                                '0180509', #too short for compact date
                                '18180509', #compact date outside range
                                '21180509', #compact date outside range
                                '2018d0509', #not a compact date
                                '20181509', #not a compact date (not month)
                                '20180539', #not a compact date (not day)
                                '2018/05#09', #wrong separator
                                '2018a/05/09', #not a digit
                                '201a8/05/09', #not a digit
                                '2018/a05/09', #not a digit
                                '2018/0a5/09', #not a digit
                                '2018/05a/09', #not a digit
                                '2018/05/a09', #not a digit
                                '2018/05/0a9', #not a digit
                                '2018-05-095', #too long day
                                '2018-055-09', #too long month
                                '2018-15-09', #not an ISO date (not month)
                                '2018-05-39', #not an ISO date (not day)
                                '8_5.9', #not a short date (year is wrong)
                                '08_15.9', #not a short date (month is wrong)
                                '08_115.9', #not a short date (month is long)
                                '08_5.39', #not a short date (day is wrong)
                                '08_5.191', #not a short date (day is long)
                                '1 9_5.20187date', #year too long
                                '1 9_5.201date', #year too short
                                '1 29_15.2018date', #month out of range, revers.
                                '1 39_5.2018date', #day out of range, reversed
                                '1 39_35.2018date', #day and month out of range
                                ]
        cls.MatchingCases = [('20180509', '2018-05-09'), #compact date
                            ("MSC00000001_20170502_1448_PROGRAMMING_PASS.xml",
                                "2017-05-02"), #compact date
                                ('a20180509', '2018-05-09'), #compact date
                                ('20180509b', '2018-05-09'), #compact date
                                ('date20180509now', '2018-05-09'), #compact date
                                ('00180509', '2018-05-09'), #compact date
                                ('19180509', '1918-05-09'), #compact date
                                ('1 20180509 1', '2018-05-09'), #compact date
                                ('0018_05_09', '2018-05-09'), #ISO date
                                ('2018_05_09', '2018-05-09'), #ISO date
                                ('2018-05-09', '2018-05-09'), #ISO date
                                ('2018-5-09', '2018-05-09'), #ISO date
                                ('2018-05-9', '2018-05-09'), #ISO date
                                ('2018-5-9', '2018-05-09'), #ISO date
                                ('2018-5-9 23:34:00', '2018-05-09'), #ISO date
                                ('2018/05/09', '2018-05-09'), #ISO date
                                ('2018/05_09', '2018-05-09'), #ISO date
                                ('2018.05.09', '2018-05-09'), #ISO date
                                ('date 2018/05_09 is now', '2018-05-09'), #ISO
                                ('date2018-05-09_is now', '2018-05-09'), #ISO
                                ('1 2018_05_09 1', '2018-05-09'), #ISO date
                                ('1 18_05.09 1', '2018-05-09'), #Short date
                                ('08_05.09', '2008-05-09'), #Short date
                                ('08/5-9', '2008-05-09'), #Short date
                                ('9-5/2018', '2018-05-09'), #reversed date
                                ('1 9_5.2018date', '2018-05-09'), #reversed date
                                ('9-15/2018', '2018-09-15'), #screwed date
                                ('1 9_15.2018date', '2018-09-15'), #screwed date
                                ]
    
    def test_Exception(self):
        """
        Tested function should raise TypeError exception if the passed argument
        is not a string. Uses ExceptionCases attribute as the set of cases.
        
        Version 0.1.20180509
        """
        for gCase in self.ExceptionCases:
            self.assertRaises(TypeError, ResolveDate, gCase)
    
    def test_NotMatches(self):
        """
        Tested function should return None for the non-matching strings. Uses
        NonMatchingCases attribute as the set of cases.
        
        Version 0.1.20180509
        """
        for strCase in self.NonMatchingCases:
            strTest = ResolveDate(strCase)
            self.assertIsNone(strTest, msg = 'Case: {} - {} != None'.format(
                                                            strCase, strTest))
    
    def test_Matches(self):
        """
        Tested function should return the proper date stamp for the matching
        strings. Uses MatchingCases attribute as the set of cases.
        
        Version 0.1.20180509
        """
        for strCase, strResult in self.MatchingCases:
            strTest = ResolveDate(strCase)
            self.assertEqual(strTest, strResult,
                             msg = 'Case: {} - {} != {}'.format(strCase,
                                                            strTest, strResult))

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_ResolveDate)
TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1])

#execution entry point

if __name__ == "__main__":
    sys.stdout.write("Preparing regex_lib.Date.ResolveDate() tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)
    sys.stdout.flush()
