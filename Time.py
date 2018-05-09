#!/usr/bin/python
"""
Module regex_lib.Time

Time stamps regular expression patterns used in the analysis and parsing of the
files.

Patterns:
    HOUR_PATTERN - one or two digits for hours between 0 and 23 inclusively,
        0 to 9 values may be prefixed by extra zero
    MINUTE_PATTERN - one or two digits for minutes between 0 and 59 inclusively,
        0 to 9 values may be prefixed by extra zero
    SECOND_PATTERN - one or two digits for seconds between 0 and 59 inclusively,
        0 to 9 values may be prefixed by extra zero, optionally followed by '.'
        or ',' and one or more digits
    AM_PM_PATTERN - am / pm modifier pattern, which covers optional whitespace
        followed by 'A' or 'P' followed by optional dot ('.') followed by 'M'
        followed by an optional dot.
    SHORT_TIME_PATTERN - only hours and minutes separated by a column ':',
        possibly with am / pm modifier
    TIME_PATTERN - hours, minutes and seconds each separated by a column ':',
        possibly with am / pm modifier
    COMPACT_TIME_PATTERN - hours, minutes and seconds without separators, i.e
        as 'HHMMDD' - exactly 6 digits
    SHORT_COMPACT_TIME_PATTERN - hours and minutes without separators, i.e as
        'HHMM' - exactly 4 digits

Compiled patterns:
    C_SHORT_TIME_PATTERN, C_TIME_PATTERN, C_COMPACT_TIME_PATTERN,
    C_SHORT_COMPACT_TIME_PATTERN

Main function:
    ResolveTime()
        str -> str OR None, bool
        
        Extracts and converts allowed formats into the ISO 'HH:MM:SS' format

Helper functions:
    ConvertAM_PM()
        re.MatchObject -> int OR None
        
        Extracts and converts hours when required from 12-h into 24-h clock
    
    CorrectRounding()
        int, int, int -> int, int, int, bool
        
        Properly handles seconds, minutes and hours change due to the seconds
        rounding, including date change due to the swinging over zero

Version 0.2.20180509
"""

__author__ = "Anton Azarov"
__copyright__ = "(c) 2014-2018 Diagnoptics Technologies B.V."
__license__ = "GPL"
__version__ = "0.2.20180509"
__date__ = "09-05-2018"
__status__ = "Production"
__maintainer__ = "a.azarov@diagnoptics.com"

#imports

#+ standard library

import re

#patterns

HOUR_PATTERN = r"(?P<hour>(([0-1]?[0-9])|(2[0-3])))"

MINUTE_PATTERN = r"(?P<minute>[0-5]?[0-9])"

SECOND_PATTERN = r"(?P<second>[0-5]?[0-9]((\.|,)[0-9]+)?)"

AM_PM_PATTERN = r" ?(?P<modifier>(A|P)\.?M\.?)?"

#+ H?H:M?M

SHORT_TIME_PATTERN = r"".join([r"(.*[^0-9:]|^)", HOUR_PATTERN, ":",
                                MINUTE_PATTERN, AM_PM_PATTERN ,
                                r"([^0-9:].*|$)"])

#+ H?H:M?M:S?S

TIME_PATTERN = r"".join([r"(.*[^0-9]|^)", HOUR_PATTERN, ":", MINUTE_PATTERN,
                        ":", SECOND_PATTERN, AM_PM_PATTERN, r"([^0-9].*|$)"])

#+ HHMM

SHORT_COMPACT_TIME_PATTERN = "".join([r"(.*[^0-9]|^)",
                                r"(?P<hour>([0-1][0-9])|(2[0-3]))",
                                r"(?P<minute>[0-5][0-9])",
                                r"([^0-9].*|$)"])

#+ HHMMSS

COMPACT_TIME_PATTERN = "".join([r"(.*[^0-9]|^)",
                                r"(?P<hour>([0-1][0-9])|(2[0-3]))",
                                r"(?P<minute>[0-5][0-9])",
                                r"(?P<second>[0-5][0-9])",
                                r"([^0-9].*|$)"])

#compiled patterns

C_SHORT_TIME_PATTERN = re.compile(SHORT_TIME_PATTERN)

C_TIME_PATTERN = re.compile(TIME_PATTERN)

C_COMPACT_TIME_PATTERN = re.compile(COMPACT_TIME_PATTERN)

C_SHORT_COMPACT_TIME_PATTERN = re.compile(SHORT_COMPACT_TIME_PATTERN)

#functions

def ConvertAM_PM(objMatch):
    """
    Helper function for the conversion of the a.m. / p.m. time representation
    (12-hours clock) into 24-hours representation according to the NIST rules:
        * midnight = 11:59 p.m. -> 12:01 a.m.
        * 12:00 a.m. to 12:59 a.m. == 00:00 to 00:59 in 24-h
        * 1:00 a.m. to 11:59 a.m == 01:00 to 11:59 in 24-h
        * midday / noun = 11:59 a.m. -> 12:01 p.m.
        * 12:00 p.m. to 12:59 p.m. == 12:00 to 12:59 in 24-h
        * 1:00 p.m. to 11:59 p.m == 13:00 to 23:59 in 24-h
    
    Note that this function concerns only hours, which are to be extracted from
    a match object, supposedly for SHORT_TIME_PATTERN or TIME_PATTERN, in any
    case with the defined groups 'hour' and 'modifier'.
    
    Returns hour in 24-h clock, if the representation was correct, or None
    otherwise.
    
    Signature:
        re.MatchObject -> int OR None
    
    Version 0.1.20180509
    """
    iHour = int(objMatch.group('hour'))
    gModifier = objMatch.group('modifier')
    if not (gModifier is None):
        if iHour == 0 or iHour > 12:
            gResult = None # hours are 1 to 12 inclusively with am / pm mod.
        elif gModifier.startswith('P'):
            if iHour < 12:
                gResult = iHour + 12
            else:
                gResult = iHour
        elif iHour == 12:
            gResult = 0
        else:
            gResult = iHour
    else:
        gResult = iHour
    return gResult

def CorrectRounding(iHour, iMinute, iSecond):
    """
    Helper function for the proper rounding of the seconds. I.e. seconds > 59.5
    should be converted into 0, and the minutes should be incremented by 1. If
    the minutes become 60 - they must be replaced by 0, and the hours -
    incremented by one. If hours becomes 24 - they must be replaced by 0, and
    the date should be incremented by 1 day, which is indicated by the returned
    boolean flag (the last element of the unpacked tuple)
    
    Signature:
        int, int, int -> int, int, int, bool
    
    Input:
        iHour - integer, hours, assumed to be in the range 0 - 24 inclusively
        iMinutes - integer, minutes, assumed to be in the range 0 - 60 incl.
        iSeconds - integer, seconds, assumed to be in the range 0 - 60 incl.
    
    Returns an unpacked tuple of 3 integers (as the corrected for the swinging
    over zero hours, minutes and seconds) and a boolean flag if the date should
    be incremented by 1 day.
    
    Version 0.1.20180509
    """
    _iHour = iHour
    _iMinute = iMinute
    _iSecond = iSecond
    bIncrementDate = False
    if _iSecond == 60:
        _iSecond = 0
        _iMinute += 1
        if _iMinute == 60:
            _iMinute = 0
            _iHour += 1
            if _iHour == 24:
                _iHour = 0
                bIncrementDate = True
    return _iHour, _iMinute, _iSecond, bIncrementDate

def ResolveTime(strStamp):
    """
    Attempts to resolve the passed time stamp with help of the defined regular
    expression patterns in the following order:
        TIME_PATTERN, SHORT_TIME_PATTERN, COMPACT_TIME_PATTERN,
            SHORT_COMPACT_TIME_PATTERN
    
    Note that the floating point representation of the seconds is rounded to an
    integer, which may cause swinging over zero of the seconds (60 -> 00) and
    incrementing of the minutes; and so on including the hours.
    
    Returns the resolved time stamp as a string in ISO format 'HH:MM:SS' or
    None value if none of the patterns is matched; and the boolean flag if the
    date must be incremented due to rounding up of the seconds, i.e. 23:59:59.5
    -> 00:00:00 of the next day.
    
    Raises TypeError if the passed argument is not a string.
    
    See also helper functions:
        ConvertAM_PM()
        CorrectRounding()
    
    Signature:
        str -> str OR None, bool
    
    Version 0.2.20180509
    """
    if not isinstance(strStamp, basestring):
        strError = '{} of {} is not a string'.format(strStamp, type(strStamp))
        raise TypeError(strError)
    _strStamp = strStamp.upper()
    objMatch = C_TIME_PATTERN.match(_strStamp)
    bIncrementDate = False
    if objMatch:
        iHour = ConvertAM_PM(objMatch)
        if not (iHour is None):
            iMinute = int(objMatch.group('minute'))
            iSecond = int(round(float(objMatch.group('second').replace(
                                                                    ',', '.'))))
            iHour, iMinute, iSecond, bIncrementDate = CorrectRounding(iHour,
                                                            iMinute, iSecond)
            strResult = "{:02}:{:02}:{:02}".format(iHour, iMinute, iSecond)
        else:
            strResult = None
    else:
        objMatch = C_SHORT_TIME_PATTERN.match(_strStamp)
        if objMatch:
            iHour = ConvertAM_PM(objMatch)
            if not (iHour is None):
                strResult = "{:02}:{:02}:00".format(iHour,
                                                int(objMatch.group('minute')))
            else:
                strResult = None
        else:
            objMatch = C_COMPACT_TIME_PATTERN.match(_strStamp)
            if objMatch:
                strResult = "{}:{}:{}".format(objMatch.group('hour'),
                                                objMatch.group('minute'),
                                                    objMatch.group('second'))
            else:
                objMatch = C_SHORT_COMPACT_TIME_PATTERN.match(_strStamp)
                if objMatch:
                    strResult = "{}:{}:00".format(objMatch.group('hour'),
                                                    objMatch.group('minute'))
                else:
                    strResult = None
    return strResult, bIncrementDate