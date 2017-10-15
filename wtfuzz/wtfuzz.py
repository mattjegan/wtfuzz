import signal
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import sys
import crayons
import requests


class Fuzzer(object):
    def __init__(self, args=None):

        self.args = self._check_args(args)

        self.color_override = self._build_color_override_map(self.args.c)
        self.root_url = self._generate_root_url(self.args.root_url)

        self._load_tests()
        self._open_file()

    def _check_args(self, args=None):
        parser = argparse.ArgumentParser(description='A CLI tool for finding web resources')
        parser.add_argument('-w', metavar='wait_time', required=False, type=int, default=0,
                            help='an optional time to wait between the number of requests given by the -n flag. Note: this is per thread.')
        parser.add_argument('-n', metavar='num_requests', required=False, type=int, default=0,
                            help='an optional number of requests to make before waiting for the time specified by the -w flag. Note: this is per thread.')
        parser.add_argument('-t', metavar='num_threads', required=False, type=int, default=1,
                            help='an optional number of threads to use to send requests.')
        parser.add_argument('-o', metavar='output_file', required=False, type=str,
                            help='an optional file to log output to.')
        parser.add_argument('-m', metavar='http_method', required=False, type=str, default='GET',
                            help='http method to use for requests')
        parser.add_argument('-c', metavar=('http_status', 'color'), required=False, action='append', nargs=2,
                            help='customize what color a given http status code will display as. Note: this parameter can be specified multiple times. Available Colors: [red,green,yellow,blue,black,magenta,cyan,white]')
        parser.add_argument('-b', metavar='http_body', required=False, type=str, help='http body to use for requests')
        parser.add_argument('--only', metavar='http_status', required=False, type=int,
                            help='only show requests that return http_status')
        parser.add_argument('root_url', help='the url you want to start the search from')
        parser.add_argument('list_file', type=str, help='an optional list of resources to check')
        return parser.parse_args(args)

    def run(self):
        num_threads = self.args.t if self.args.t >= 1 else 1

        test_buckets = {}
        for i in range(num_threads):
            test_buckets[i] = []

        for e, t in enumerate(self.tests):
            test_buckets[e % num_threads].append(t)

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []

            for key, bucket in test_buckets.items():
                future = executor.submit(self.send_requests, bucket)
                futures.append(future)

            for f in as_completed(futures):
                f.result()

    def send_requests(self, bucket):
        num_requests = 0
        for test in bucket:

            if self.args.n > 0 and num_requests == self.args.n:
                num_requests = 0
                time.sleep(self.args.w)

            url = '{}/{}'.format(self.root_url, test.lstrip('/'))
            try:
                response = self._send_request(self.args.m, url, self.args.b)

                modifier = self._display_modifier(response.status_code)

                if not self.args.only:
                    self._print(modifier('{} : {}'.format(response.status_code, url)))
                elif self.args.only == response.status_code:
                    self._print(modifier('{} : {}'.format(response.status_code, url)))
            except requests.exceptions.ConnectionError as e:
                self._print('Web server does not exist or is unavailable')

            num_requests += 1

    def _build_color_override_map(self, override_list):
        overrides = {}
        if override_list:
            for override in override_list:
                overrides[int(override[0])] = self._get_crayon_color(override[1])

        return overrides

    def _get_crayon_color(self, color):
        return {
            'red': crayons.red,
            'green': crayons.green,
            'yellow': crayons.yellow,
            'blue': crayons.blue,
            'black': crayons.black,
            'magenta': crayons.magenta,
            'cyan': crayons.cyan,
            'white': crayons.white
        }[color.lower()]

    def _display_modifier(self, status_code):
        if status_code in self.color_override:
            return self.color_override[status_code]

        if status_code < 300:
            return crayons.green
        elif status_code >= 400:
            return crayons.red
        elif status_code >= 300:
            return crayons.yellow

        return str

    def _send_request(self, http_method, url, body):
        method = http_method.upper()
        if method == 'GET':
            return requests.get(url)
        elif method == 'POST':
            return requests.post(url, data=body)
        elif method == 'PATCH':
            return requests.patch(url, data=body)
        elif method == 'PUT':
            return requests.put(url, data=body)
        raise ValueError('Invalid argument, http_method: {}'.format(method))

    def _load_tests(self):
        self.tests = []

        try:
            self.tests.extend([line.strip() for line in open(self.args.list_file, 'r')])
        except:
            print('{} is not a valid file'.format(self.args.list_file))

    def _open_file(self):
        if self.args.o:
            self.outfile = open(self.args.o, 'w+')

    def _generate_root_url(self, root_url):
        lowercase_url = root_url.strip().lower()
        if lowercase_url.startswith('http://') or lowercase_url.startswith('https://'):
            return root_url

        self._print('Prepending protocol: http://{}'.format(root_url))
        return 'http://' + root_url

    def _print(self, string):
        if hasattr(self, 'outfile'):
            self.outfile.write('{}\n'.format(string))
        print(string)

        
def handler(signum, frame):
    os.kill(os.getpid(), signal.SIGKILL)

def main():
    signal.signal(signal.SIGINT, handler)
    wtfuzz = Fuzzer(sys.argv[1:])
    wtfuzz.run()


if __name__ == '__main__':
    main()
