# August 13th, 2021
# The game "Move or Die" releases an update with a website to submit a hidden code that can be found in a video.
# Website: https://moveordiegame.com/treasure/
# Video: https://www.youtube.com/watch?v=Jl2u72LzurU

# Noticing that the code is submitted via a REST endpoint, I thought I'd just programmatically try every combination, as
# I am incapable of determining the code from the video after re-watching it several times.

import requests
import socket
import string
import logging as lg
import time


lg.basicConfig(
    format='%(asctime)s - %(name)10s - %(levelname)7s - %(message)s', level=lg.DEBUG
)

requests_logger = lg.getLogger('urllib3')
# requests_logger.setLevel(lg.ERROR)

# Example URL submitting code "1234" = "https://moveordiegame.com/treasure/?a=1&b=2&c=3&d=4"

URI_BASE = "https://moveordiegame.com:{}/treasure/"
DEFAULT_PORT = 443
FULL_URI_FORMAT = URI_BASE + "?a={}&b={}&c={}&d={}"
INCORRECT_RESPONSE = "Seems like those symbols are not the correct ones, you might have to dig deeper and try again..."
IR_MSG_START = -134
IR_MSG_END = -38

TOO_FAST_RESPONSE = "Not so fast, young grasshopper..."

PORTS = [440, 441, 442, 443, 444, 445, 446, 447, 448, 449]

URI_IP = "173.255.252.249"


def test_run():
    test_uri = FULL_URI_FORMAT.format(str(DEFAULT_PORT), "x", "x", "x", "x")

    lg.debug("Test URI = " + test_uri)

    test_r = requests.get(test_uri)
    test_response_text = test_r.text

    # lg.debug("Response HTML text:\n" + test_response_text)

    my_str = """
    <body>
        <div id="main">
            <div id="logo">
                <img src="Logo.png" alt="The lost treasure that was never found"/>
            </div>
            <div id="text">
                <p class="error">Seems like those symbols are not the correct ones, you might have to dig deeper and try again...</p>
            </div>
        </div>
    </body>
    </html>
    """

    my_str_length = len(my_str)

    lg.debug("Incorrect Code Body Length = " + str(my_str_length))
    lg.debug("Response HTML text end:\n" + test_response_text[-134:-38])


def check_ports():
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    for port in PORTS:
        location = (URI_IP, port)
        result_of_check = a_socket.connect_ex(location)

        if result_of_check == 0:
            res = "Open"
        else:
            res = "Not open"

        lg.debug("Port {} - {}".format(str(port), res))

    a_socket.close()


def _current_time_ms():
    return round(time.time() * 1000)


if __name__ == '__main__':

    # char_set = string.ascii_letters
    # lg.debug("Char Set = " + char_set)
    #
    # b = 'x'
    # c = 'x'
    # d = 'x'
    #
    # for i, a_char in enumerate(char_set[:5]):
    #     request_uri = FULL_URI_FORMAT.format(str(PORTS[i % 10]), a_char, b, c, d)
    #
    #     response = requests.get(request_uri)
    #     response_msg = response.text[IR_MSG_START:IR_MSG_END]
    #
    #     is_correct = (response_msg != INCORRECT_RESPONSE)
    #
    #     lg.debug(response_msg)
    #     lg.debug("{} {} {} {} - Correct? {}".format(a_char, b, c, d, str(is_correct)))
    #     time.sleep(5)

    check_ports()
