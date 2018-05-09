#!/usr/bin/python
"""
Module regex_lib.Time

Date stamps regular expression patterns used in the analysis and parsing of the
files.

Patterns:
    YEAR_PATTERN - four digits representing year either as 00YY or YYYY, for the
        second option the year must be between 1900 and 2099 inclusively
    MONTH_PATTERN - one or two digits representing month in the interval of 1
        to 12 inclusively; value < 10 may be prefixed by 0
    DAY_PATTERN - one or two digits representing day in the interval of 1 to 31
        inclusively; value < 10 may be prefixed by 0
    DATE_SEPARATOR - any standard separator for the date stamp: '-', '_', '/' or
        '.'
    ISO_DATE - year, month, day
    
    REVERSED_DATE - day, month, year; N.B. for both month and day <= 12 may
        result in false positive if the actual stamp is month, day, year
    
    SCREWED_DATE - month, day, year but only for day >= 13

    COMPACT_DATE - year, month, day but without separators and always 8 digits,
        i.e. 'YYYYMMDD', year must be between 1900 and 2099 inclusively, 00YY is
        treated as 20YY
    SHORT_DATE - year, month, day with any standard separator for the date
        stamp: '-', '_', '/' or '.' - but the year is only with two last digits,
        i.e YY instead of 20YY

Compiled patterns:
    C_ISO_DATE, C_REVERSED_DATE, C_SCREWED_DATE, C_COMPACT_DATE, C_SHORT_DATE

Functions:
    ResolveDate()
        str -> str OR None
        
        Extracts and converts allowed formats into the ISO format 'YYYY-MM-DD'

Version 0.3.20180509
"""

__author__ = "Anton Azarov"
__copyright__ = "(c) 2014-2018 Diagnoptics Technologies B.V."
__license__ = "GPL"
__version__ = "0.3.20180509"
__date__ = "09-05-2018"
__status__ = "Production"
__maintainer__ = "a.azarov@diagnoptics.com"

#imports

#+ standard library

import re

#patterns

YEAR_PATTERN = r"(?P<year>((00)|(19)|(20))[0-9]{2})"

MONTH_PATTERN = r"(?P<month>(0?[1-9])|(1[0-2]))"

DAY_PATTERN = r"(?P<day>(0?[1-9])|([1-2][0-9])|(3[0-1]))"

DATE_SEPARATOR = r"((-)|(/)|(_)|(\.))"

#+ ((00)|(YY))YY-M?M-D?D

ISO_DATE = r"".join([r"(.*[^0-9]|^)", YEAR_PATTERN, DATE_SEPARATOR,
                    MONTH_PATTERN, DATE_SEPARATOR, DAY_PATTERN,
                    r"([^0-9].*|$)"])

#+ D?D-M?M-((00)|(YY))YY

REVERSED_DATE = r"".join([r"(.*[^0-9]|^)", DAY_PATTERN, DATE_SEPARATOR,
                        MONTH_PATTERN, DATE_SEPARATOR, YEAR_PATTERN,
                        r"([^0-9].*|$)"])

#+ M?M-D?D-((00)|(YY))YY - only for day >= 13

SCREWED_DATE = r"".join([r"(.*[^0-9]|^)" + MONTH_PATTERN + DATE_SEPARATOR +
                    r"(?P<day>(1[3-9])|(2[0-9])|(3[0-1]))"
                    + DATE_SEPARATOR + YEAR_PATTERN + r"([^0-9].*|$)"])

#+ YYYYMMDD

COMPACT_DATE = r"".join([r"(.*[^0-9]|^)", YEAR_PATTERN,
                            r"(?P<month>(0[1-9])|(1[0-2]))",
                                r"(?P<day>(0[1-9])|([1-2][0-9])|(3[0-1]))",
                                    r"([^0-9].*|$)"])

#+ YY-M?M-D?D

SHORT_DATE = r"".join([r"(.*[^0-9]|^)(?P<year>[0-9]{2})", DATE_SEPARATOR,
                    MONTH_PATTERN, DATE_SEPARATOR, DAY_PATTERN,
                    r"([^0-9].*|$)"])

#compiled patterns

C_ISO_DATE = re.compile(ISO_DATE)

C_REVERSED_DATE = re.compile(REVERSED_DATE)

C_SCREWED_DATE = re.compile(SCREWED_DATE)

C_COMPACT_DATE = re.compile(COMPACT_DATE)

C_SHORT_DATE = re.compile(SHORT_DATE)

#functions

def ResolveDate(strStamp):
    """
    Attempts to resolve the passed date stamp with help of the defined regular
    expression patterns in the following order:
        ISO_DATE, REVERSED_DATE, SCREWED_DATE, SHORT_DATE, COMPACT_DATE
    
    Returns the resolved date stamp as a string in ISO format 'YYYY-MM-DD' or
    None value if none of the patterns is matched.
    
    Raises TypeError if the passed argument is not a string.
    
    Signature:
        str -> str OR None
    
    Version 0.2.20180509
    """
    if not isinstance(strStamp, basestring):
        strError = '{} of {} is not a string'.format(strStamp, type(strStamp))
        raise TypeError(strError)
    for objPattern in [C_ISO_DATE, C_REVERSED_DATE, C_SCREWED_DATE,
                                                C_SHORT_DATE, C_COMPACT_DATE]:
        objMatch = objPattern.match(strStamp)
        if objMatch:
            iYear = int(objMatch.group('year'))
            iMonth = int(objMatch.group('month'))
            iDay = int(objMatch.group('day'))
            if iYear < 100:
                iYear += 2000
            strResult = "{}-{:02}-{:02}".format(iYear, iMonth, iDay)
            break
    else:
        strResult = None
    return strResult