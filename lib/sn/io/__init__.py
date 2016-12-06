from pathlib import PurePath, Path
from glob import glob


def pickle(path, data=None):
    import pickle as p
    path = str(path)
    if data is None:
        with open(path, 'rb') as r:
            return pickle.load(r)
    else:
        with open(path, 'wb') as w:
            pickle.dump(data, w)


def io_array(path, data=None):
    import numpy as np
    path = str(path)
    if data is None:
        return np.load(path)
    else:
        np.save(path, data)
