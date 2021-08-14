# https://www.datacamp.com/community/tutorials/making-http-requests-in-python

import requests
import logging as lg
import time


lg.basicConfig(
    format='%(asctime)s - %(name)10s - %(levelname)7s - %(message)s', level=lg.DEBUG
)

# Increase threshold for requests module to avoid default debug logs
# requests_logger = lg.getLogger('urllib3')
# requests_logger.setLevel(lg.ERROR)

URI_BASE = "https://moveordiegame.com:{}/treasure/"
DEFAULT_PORT = 443
FULL_URI_FORMAT = URI_BASE + "?a={}&b={}&c={}&d={}"


def test_run():
    test_uri = FULL_URI_FORMAT.format(str(DEFAULT_PORT), "x", "x", "x", "x")

    lg.debug("Test URI = " + test_uri)

    test_r = requests.get(test_uri)
    test_response_text = test_r.text

    lg.debug("Response HTML text:\n" + test_response_text)


def _current_time_ms():
    return round(time.time() * 1000)


if __name__ == '__main__':

    test_run()
