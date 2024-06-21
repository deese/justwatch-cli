# justwatch-cli

This is just a silly app to query justwatch and get some where the show/movie is available and the score in imdb if available.
All the power relies on the libraries used simplejustwatchapi, rich and cinemagoer. All the real credits to the developers of those libs 😃

## Install requirements

Run ```pip install -r requirements.txt```

## Usage

```
usage: jw.py [-h] [--imdb] [--lang LANG] [--country COUNTRY] [--limit LIMIT] [--year YEAR] [--rent] [--verbose] query

JustWatch CLI

positional arguments:
  query              Search query

options:
  -h, --help         show this help message and exit
  --imdb             Use IMDB to get ratings
  --lang LANG        Language to use. Defaults to 'es'
  --country COUNTRY  Country to use. Defaults to 'ES'.
  --limit LIMIT      Limit results to this number
  --year YEAR        Year when you think it was release. It will automatically add +5 and -5 years to the number.
  --rent             Show also renting options
  --verbose          Verbose output
```
