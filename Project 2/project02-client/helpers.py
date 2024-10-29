import requests  # calling web service

import logging
import time

TRIES = 3


###################################################################
#
# prompt
#
def prompt():
    """
    Prompts the user and returns the command number

    Parameters
    ----------
    None

    Returns
    -------
    Command number entered by user (0, 1, 2, ...)
    """

    try:
        print()
        print(">> Enter a command:")
        print("   0 => end")
        print("   1 => stats")
        print("   2 => users")
        print("   3 => assets")
        print("   4 => download")
        print("   5 => download and display")
        print("   6 => bucket contents")
        print("   7 => add user")
        print("   8 => upload")

        cmd = int(input())
        return cmd

    except Exception as e:
        print("ERROR")
        print("ERROR: invalid input")
        print("ERROR")
        return -1


###################################################################
#
# web_service
#
def web_service(url, method="GET", data=None):
    """
    Submits the {method} request to a web service at most {TRIES} times,
    since web services can fail to respond e.g. too heavy user or
    internet traffic. If the web service responds with status code 200,
    400 or 500, we consider this a valid response and return the response.
    Otherwise we try again, at most {TRIES} times. After {TRIES} attempts
    the function returns with the last response.

    Parameters
    ----------
    url: url for calling the web service
    method: method we request to the web service
    data: data we pass into the endpoint (in JSON format)

    Returns
    -------
    response received from web service
    """

    try:
        method = method.upper()
        retries = 0
        while True:
            if method == "GET":
                response = requests.get(url)
            elif method == "PUT":
                response = requests.put(url, json=data)
            elif method == "POST":
                response = requests.post(url, json=data)
            else:
                raise ValueError(f"{method} is not supported")

            if response.status_code in [200, 400, 500]:
                # we consider this a successful call and response
                break

            # failed, try again
            retries = retries + 1
            if retries < TRIES:
                # try at most TRIES times
                time.sleep(1)
                continue

            # if get here, we tried 3 times, we give up
            break

        return response

    except Exception as e:
        print("**ERROR**")
        logging.error("web_service_get() failed:")
        logging.error(f"url: {url}")
        logging.error(e)
        return


###################################################################
#
# web_service_get
#
# When calling servers on a network, calls can randomly fail.
# The better approach is to repeat at least N times (typically
# N=3), and then give up after N tries.
#
def web_service_get(url):
    """
    Submits a GET request to a web service at most 3 times, since
    web services can fail to respond e.g. too heavy user or internet
    traffic. If the web service responds with status code 200, 400
    or 500, we consider this a valid response and return the response.
    Otherwise we try again, at most 3 times. After 3 attempts the
    function returns with the last response.

    Parameters
    ----------
    url: url for calling the web service

    Returns
    -------
    response received from web service
    """

    try:
        retries = 0

        while True:
            response = requests.get(url)

            if response.status_code in [200, 400, 500]:
                #
                # we consider this a successful call and response
                #
                break

            #
            # failed, try again?
            #
            retries = retries + 1
            if retries < TRIES:
                # try at most TRIES times
                time.sleep(retries)
                continue

            #
            # if get here, we tried 3 times, we give up:
            #
            break

        return response

    except Exception as e:
        print("**ERROR**")
        logging.error("web_service_get() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return


###################################################################
#
# web_service_put
#
# When calling servers on a network, calls can randomly fail.
# The better approach is to repeat at least N times (typically
# N=3), and then give up after N tries.
#
def web_service_put(url, data):
    """
    Submits a PUT request to a web service at most TRIES times, since
    web services can fail to respond e.g. too heavy user or internet
    traffic. If the web service responds with status code 200, 400
    or 500, we consider this a valid response and return the response.
    Otherwise we try again, at most TRIES times. After TRIES attempts the
    function returns with the last response.

    Parameters
    ----------
    url: url for calling the web service
    data: data we pass into the endpoint (in JSON format)

    Returns
    -------
    response received from web service
    """

    try:
        retries = 0

        while True:
            response = requests.put(url, json=data)

            if response.status_code in [200, 400, 500]:
                # we consider this a successful call and response
                break

            # failed, try again
            retries = retries + 1
            if retries < TRIES:
                # try at most TRIES times
                time.sleep(1)
                continue

            # if get here, we tried { TRIES } times, we give up
            break

        return response

    except Exception as e:
        print("**ERROR**")
        logging.error("web_service_put() failed:")
        logging.error(f"url: {url}")
        logging.error(f"data: {data}")
        logging.error(e)
        return
