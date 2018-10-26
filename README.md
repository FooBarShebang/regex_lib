# Library regex_lib

## Purpose

Set of regular expression patterns and functions for the aggregated patterns based search / resolution based locale-independend data processing with Python.

## Structure and Documentation

* Module [Date](./Date.py). Documentation [UD001](./Documentation/UD001_Date_Reference.md)
* Module [Time](./Time.py). Documentation [UD002](./Documentation/UD002_Time_Reference.md)

## Usage

### regex_lib.Date

```python
from regex_lib.Date import ResolveDate

strDate = ResolveDate('20180509') # -> '2018-05-09'

ResolveDate("MSC00000001_20170502_1448_PROGRAMMING_PASS.xml") # -> '2017-05-02'

ResolveDate('2018/5_9 23:34:00') # -> '2018-05-09'

ResolveDate('1 18_05.09 1') # -> '2018-05-09'

ResolveDate('0018_05_09') # -> '2018-05-09'

ResolveDate('1 9_5.2018date') # Day, month, year! -> '2018-05-09'

ResolveDate('1 9_15.2018date') # Month, day, year! -> '2018-09-15'

ResolveDate('2018-055-09') # wrong format! -> None

ResolveDate(20180101) # not a string! -> TypeError exception
```

### regex_lib.Time

```python
from regex_lib.Time import ResolveTime

strTime, bDateIncrement = ResolveTime('1448') # -> '14:48:00', False

ResolveTime("MSC00000001_20170502_1448_PROGRAMMING_PASS.xml") # -> '14:48:00', False

ResolveTime('144801') # -> '14:48:01', False

ResolveTime('now23:05:01.499999time') # -> '23:05:01', False

ResolveTime('now23:05:01.500000time') # -> '23:05:02', False

ResolveTime('23:59:59.500000000') # -> '00:00:00', True

ResolveTime('12:50 am') # -> '00:50:00', False

ResolveTime('12:50 A.M.') # -> '00:50:00', False

ResolveTime('12:50aMnow') # -> '00:50:00', False

ResolveTime('10:50:01.5 A.M.') # -> '10:50:02', False

ResolveTime('12:50 P.M.') # -> '12:50:00', False

ResolveTime('10:50:03.4pm') # -> '22:50:03', False

ResolveTime('12:14:60') # wrong format! -> None, False

ResolveTime(121459) # not a string! -> TypeError exception
```