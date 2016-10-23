from time import time as _time

_t = _time()

_VERBOSE_ = False


def setVerbose(verbose=False):
    _VERBOSE_ = verbose


def time(message=None):
    global _t

    current = _time()
    t = current - _t
    _t = current
    if _VERBOSE_ and message is not None:
        print('{0}: {1:4.2f} secs'.format(message, t))
    return t