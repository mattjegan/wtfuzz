
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time

import crayons
import requests

class Fuzzer(object):
    def __init__(self):
        parser = argparse.ArgumentParser(description='A CLI tool for finding web resources')
        parser.add_argument('-w', metavar='wait_time', required=False, type=int, default=0, help='an optional time to wait between the number of requests given by the -n flag. Note: this is per thread')
        parser.add_argument('-n', metavar='num_requests', required=False, type=int, default=0, help='an optional number of requests to make before waiting for the time specified by the -w flag. Note: this is per thread')
        parser.add_argument('-t', metavar='num_threads', required=False, type=int, default=1, help='an optional number of threads to use to send requests.')
        parser.add_argument('root_url', help='the url you want to start the search from')
        parser.add_argument('list_file', type=str, help='an optional list of resources to check')
        self.args = parser.parse_args()
        self._load_tests()

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

            url = '{}/{}'.format(self.args.root_url, test.lstrip('/'))
            try:
                response = requests.get(url)

                modifier = str
                if response.status_code < 300:
                    modifier = crayons.green
                elif response.status_code >= 400:
                    modifier = crayons.red
                elif response.status_code >= 300:
                    modifier = crayons.yellow

                print(modifier('{} : {}'.format(response.status_code, url)))
            except requests.exceptions.ConnectionError as e:
                print('Web server does not exist or is unavailable')

            num_requests += 1

    def _load_tests(self):
        self.tests = []

        try:
            self.tests.extend([line.strip() for line in open(self.args.list_file, 'r')])
        except:
            print('{} is not a valid file'.format(self.args.list_file))

def main():
    wtfuzz = Fuzzer()
    wtfuzz.run()

if __name__ == '__main__': main()