from pathlib import PurePath
import numpy as np

from sn.io import pickle, io_array


class Loader:
    def __init__(self, dataset_dir: PurePath, name: str):
        self.name = name
        self.root = dataset_dir.joinpath(name)
        self.g = io_array(self.root.joinpath('graph', 'adjacency'))
        self.profile = pickle(self.root.joinpath('misc', 'profile'))

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
        return io_array(self.root.joinpath('layout', 'layout_hd'))

    def eigens(self):
        layout_dir = self.root.joinpath('layout')
        Λ = io_array(layout_dir.joinpath('eigenvalues'))
        E = io_array(layout_dir.joinpath('eigenvectors'))
        return Λ, E

    def centralities(self):
        return self.profile['centrality']

    def centrality_v(self, name) -> np.array:
        assert name in self.centralities()['v']
        return io_array(self.root.joinpath('centrality', 'v', name))

    def centrality_e(self, name) -> np.array:
        assert name in self.centralities()['e']
        return io_array(self.root.joinpath('centrality', 'e', name))


def load(dataset_dir: PurePath, name: str) -> Loader:
    loader = Loader(dataset_dir, name)
    return loader

