# Library regex_lib Release Log

## Version 0.3.20180509

Implemented functionality is fully tested (see unit tests in the Tests subfolder) and documented.

### Module Date.py

At version 0.3.20180509

Date stamps resolution and conversion into ISO 'YYYY-MM-DD' format. Supported input formats are:

* {YY}YY-{M}M-{D}D
* YYYYMMDD
* {D}D-{M}M-YYYY
* {M}M-{D}D-YYYY
* any of the '/', '.', '-' or '_' symbols as separators (may be mixed)

### Module Time.py

At version 0.2.20180509

Time stamps resolution and conversion into ISO 'HH:MM:SS' format. Supported input formats are:

* {H}H:{M}M{:{S}S{.ms}}{AM|PM}
* HHMM{SS}

