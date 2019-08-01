import requests
import time
import sys

def limit(func):
    last_request = sys.maxsize
    rate_limiter = 1.5

    def wrapped(*args, **kwargs):
        nonlocal last_request
        wait = (time.time() - last_request) - rate_limiter
        if max(wait, 0):
            print("YOU ARE TO FÆST MAN")
            time.sleep(wait)
        ret = func(*args, **kwargs)
        last_request = time.time()
        return ret
    return wrapped

@limit
def get(*args, retry=False, **kwargs):
    try:
        r = requests.get(*args, **kwargs)
    except requests.exceptions.RequestException as e:
        print(e)
        if not retry:
            return get(*args, retry=True, **kwargs)  # retry once
    return r