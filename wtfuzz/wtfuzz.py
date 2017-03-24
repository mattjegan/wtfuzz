
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

import crayons
import requests

class Fuzzer(object):
    def __init__(self):
        parser = argparse.ArgumentParser(description='A CLI tool for finding web resources')
        parser.add_argument('root_url', help='the url you want to start the search from')
        self.args = parser.parse_args()

        self._load_tests()

    def run(self):

        num_threads = 64

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
        for test in bucket:
            url = '{}/{}'.format(self.args.root_url, test)
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

    def _load_tests(self):
        self.tests = []
        for root, dirs, filenames in os.walk('wtfuzz/assets/lists'):
            for filename in filenames:
                self.tests.extend([line.strip() for line in open('wtfuzz/assets/lists/{}'.format(filename), 'r')])

def main():
    wtfuzz = Fuzzer()
    wtfuzz.run()

if __name__ == '__main__': main()