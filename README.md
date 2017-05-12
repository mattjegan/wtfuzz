# wtfuzz - What The Fuzz 
[![PyPI version](https://badge.fury.io/py/wtfuzz.svg)](https://badge.fury.io/py/wtfuzz)

Wtfuzz is a pip-installable tool used for checking the existance of different types of web resources including webpages, files, api endpoints and more.

## Installation
Requires Python 3.5+
```
pip install wtfuzz
```

## Usage
```
wtfuzz http://your-url-here.com myList.txt

404 : http://your-url-here.com/.bash_history
404 : http://your-url-here.com/.bashrc
404 : http://your-url-here.com/.cache
404 : http://your-url-here.com/.config
404 : http://your-url-here.com/.cvs
200 : http://your-url-here.com/.git/HEAD
200 : http://your-url-here.com/index.php
200 : http://your-url-here.com/wp-admin.php
```

## Options
```
usage: wtfuzz [-h] [-w wait_time] [-n num_requests] [-t num_threads]
              [-o output_file] [--only http_status]
              root_url list_file

A CLI tool for finding web resources

positional arguments:
  root_url            the url you want to start the search from
  list_file           an optional list of resources to check

optional arguments:
  -h, --help          show this help message and exit
  -w wait_time        an optional time to wait between the number of requests
                      given by the -n flag. Note: this is per thread.
  -n num_requests     an optional number of requests to make before waiting
                      for the time specified by the -w flag. Note: this is per
                      thread.
  -t num_threads      an optional number of threads to use to send requests.
  -o output_file      an optional file to log output to.
  --only http_status  only show requests that return http_status
```
