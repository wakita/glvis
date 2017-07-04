import json
from pathlib import PurePath, Path
import numpy as np

from sn.io.util import pickle, io_array


class Loader:
    def __init__(self, dataset_dir: PurePath, name: str):
        self.name = name
        self.root = dataset_dir.joinpath(name)
        self.g = io_array(str(self.root.joinpath('graph', 'adjacency.npy')))
        with open(str(self.root.joinpath('misc', 'profile.json'))) as r:
            self.profile = json.load(r)

    def g(self):
        return self.g

    def name(self):
        return self.name

    def size(self):
        return self.profile['graph_size']

    def n_nodes(self):
        return self.profile['graph_size'][0]

    def n_edges(self):
        return self.profile['graph_size'][1]

    def attributes(self):
        return self.profile['attributes']

    def attribute(self, name: str):
        assert name in self.profile['attributes']
        return pickle(self.root.joinpath('graph', 'attribute', name))

    def dim_hd(self):
        return self.profile['dim_hd']

    def layout_hd(self):
        return io_array(self.root.joinpath('layout', 'layout_hd.npy'))

    def eigens(self):
        layout_dir = self.root.joinpath('layout')
        Λ = io_array(layout_dir.joinpath('eigenvalues.npy'))
        E = io_array(layout_dir.joinpath('eigenvectors.npy'))
        return Λ, E

    def centralities(self):
        return self.profile['centrality']

    def centrality_v(self, name) -> np.array:
        assert name in self.centralities()['v']
        return io_array(self.root.joinpath('centrality.npy', 'v', name))

    def centrality_e(self, name) -> np.array:
        assert name in self.centralities()['e']
        return io_array(self.root.joinpath('centrality.npy', 'e', name))


def load(dataset_dir: PurePath, name: str) -> Loader:
    loader = Loader(dataset_dir, name)
    return loader

