from pathlib import PurePath, Path
import pickle as pcl


def mkdir_parent(path: PurePath):
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def pickle(path: PurePath, data=None):
    path = str(path) + '.pickle'
    if data is None:
        with open(path, 'rb') as r:
            return pcl.load(r)
    else:
        mkdir_parent(path)
        with open(path, 'wb') as w:
            pcl.dump(data, w)


def io_array(path, data=None):
    import numpy as np
    path = str(path) + '.npy'
    if data is None:
        return np.load(path)
    else:
        mkdir_parent(path)
        np.save(path, data)
