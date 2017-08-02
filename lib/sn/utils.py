import logging
import time as systime

_t = systime.time()

def time(message=None):
    global _t

    current = systime.time()
    t = current - _t
    _t = current
    if message is not None:
        logging.info('{0}: {1:4.2f} secs'.format(message, t))
    return t
