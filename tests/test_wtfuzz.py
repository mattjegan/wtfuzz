import os

import responses

import wtfuzz.wtfuzz as wtfuzz


def get_path(file):
    path = os.path.join(os.path.dirname(__file__), file)
    return path


def setup_module(module):
    # Setup our good urls
    responses.add(responses.GET, 'http://www.good-example.com/index.html',
                  body='okay',
                  content_type='application/json',
                  status=200,
                  )
    responses.add(responses.GET, 'http://www.good-example.com/home/careers.html',
                  body='okay',
                  content_type='application/json',
                  status=200,
                  )

    # Setup our bad urls
    responses.add(responses.GET, 'http://www.bad-example.com/index.html',
                  body='okay',
                  content_type='application/json',
                  status=200,
                  )
    responses.add(responses.GET, 'http://www.bad-example.com/home/careers.html',
                  body='oops',
                  content_type='application/json',
                  status=404,
                  )


@responses.activate
def test_functional_simple_no_optional_args(capsys):
    """
    Simple functional test to ensure core function
    :return:
    """
    # Our user has just typed in wtfuzz.py with known functioning url and the test_mylist.txt file as arguments.
    wtfuzz.Fuzzer(['www.good-example.com', get_path('test_mylist.txt')]).run()

    # They expect to see a "200" response for every attribute
    expected_out = "Prepending protocol: http://www.good-example.com\n" \
                   "200 : http://www.good-example.com/index.html\n" \
                   "200 : http://www.good-example.com/home/careers.html\n"
    out, err = capsys.readouterr()
    assert out == expected_out

    # However they don't trust our script yet so they run a test against a url
    # they know wont respond to the home/careers.html resource in our list
    wtfuzz.Fuzzer(['www.bad-example.com', get_path('test_mylist.txt')]).run()
    expected_out = "Prepending protocol: http://www.bad-example.com\n" \
                   "200 : http://www.bad-example.com/index.html\n" \
                   "404 : http://www.bad-example.com/home/careers.html\n"
    out, err = capsys.readouterr()
    assert out == expected_out

    # Finally they run the test against a url that doesn't exist.
    wtfuzz.Fuzzer(['http://www.idontexist.com', get_path('test_mylist.txt')]).run()
    expected_out = "Web server does not exist or is unavailable\n" \
                   "Web server does not exist or is unavailable\n"
    out, err = capsys.readouterr()
    assert out == expected_out
