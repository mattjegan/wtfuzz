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
  -m http_method      http method to use for requests
  --only http_status  only show requests that return http_status
```

## Contributing

Anyone is welcome to contribute, just head over to [the issues page](https://github.com/mattjegan/wtfuzz/issues) and find an issue you'd like to work on. Check out the discussion and if it seems cool for you to begin working on something, fork the repository, make your changes, and then make a pull request back into this master branch. When making your changes, make sure to add yourself to the AUTHORS file.

### Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/<your-user>/wtfuzz`
3. Go to the project directory: `cd wtfuzz`
4. Install the required packages: `pip3 install -r requirements.txt`
5. Run the code: `python3 wtfuzz/wtfuzz.py http://your-url-here.com myList.txt`
