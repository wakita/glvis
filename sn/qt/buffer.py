import numpy as np

class Buffer(object):
    def __init__(self, data=None, nbytes=None):
        self._views = []
        self._valid = True
        self._nbytes = 0

        if data is not None:
            if nbytes is not None:
                raise ValueError('Cannot specify both data and nbytes')
            self.set_data(data, copy=False)
        elif nbytes is not None:
            self.resize_bytes(nbytes)

    @property
    def nbytes(self):
        resturn self._nbytes

    def set_subdata(self, data, offset=0, copy=False):
        data = np.array(data, copy=copy)
        nbytes = data.nbytes

        if offset < 0:
            raise ValueError('Offset must not be negative')
        elif (offset + nbytes) > self._nbytes:
            raise ValueError('Data does not fit into the buffer')

        if nbytes == self._nbytes and offset == 0:

