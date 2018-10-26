# Library regex_lib Release Log

## 2018-10-26 version 0.1.0.0

Switched to another versioning scheme and Markdown documentation.

## Version 0.4.20180516

Implemented functionality is fully tested (see unit tests in the Tests subfolder) and documented.

### Module Date.py

Date stamps resolution and conversion into ISO 'YYYY-MM-DD' format. Supported input formats are:

* {YY}YY-{M}M-{D}D
* YYYYMMDD
* {D}D-{M}M-YYYY
* {M}M-{D}D-YYYY
* any of the '/', '.', '-' or '_' symbols as separators (may be mixed)

### Module Time.py

Time stamps resolution and conversion into ISO 'HH:MM:SS' format. Supported input formats are:

* {H}H:{M}M{:{S}S{.ms}}{AM|PM}
* HHMM{SS}