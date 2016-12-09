from pathlib import PurePath, Path
import json
import re
import sys
from typing import Dict, Tuple

from igraph import Graph
import numpy as np

from sn.io import pickle, io_array
import sn.utils
from sn.utils import time as benchmark

_DEBUG_ = False

sn.utils._VERBOSE_ = True


def read(path: PurePath, *args, **kwds) -> Graph:
    try:
        g = Graph.Read(str(path), *args, **kwds)
        benchmark(message='Reading "{0}"'.format(path))
        try:
            print(path.parent.joinpath(path.stem + '.labels'))
            with open(str(path.parent.joinpath(path.stem + '.labels'))) as r:
                g.vs['label'] = [re.sub(r'\n', '', line) for line in r.readlines()]
        except FileNotFoundError:
            pass
        return g
    except:
        print('Parsing failure:', path)
        e, message, trace = sys.exc_info()
        print(message)
        raise e


def normalize(g: Graph, profile: dict) -> Graph:
    graph_dir = PurePath(profile['root']).joinpath(profile['name'], 'graph')
    print('graph_dir:', graph_dir, 'name:', profile['name'])

    benchmark(message='Starting normalize')
    # Convert to undirected graph
    g.to_undirected()
    assert not g.is_directed()
    benchmark(message='Converted to directed graph')

    # The largest strongly connected component
    g = max(g.decompose(), key=(lambda g: len(g.vs)))
    benchmark(message='Maximum connected component')

    # Remove self-loops
    g.simplify()
    assert not any(g.is_loop())
    benchmark(message='Removed self-loops')

    profile['graph_size'] = [len(g.vs), len(g.es)]

    io_array(graph_dir.joinpath('adjacency'), g.get_adjlist())
    io_array(graph_dir.joinpath('edgelist'),  g.get_edgelist())

    profile['attributes'] = g.vs.attributes()
    attribute_dir = graph_dir.joinpath('attribute')
    for attribute in profile['attributes']:
        pickle(attribute_dir.joinpath(attribute), g.vs[attribute])

    print()

    return g


if __name__ == '__main__' and False:
    def test1():
        g = Graph([(0, 1), (0, 2), (2, 3), (3, 4), (4, 2), (2, 5), (5, 0), (6, 3), (5, 6)])
        g.vs["name"] = ["Alice", "Bob", "Claire", "Dennis", "Esther", "Frank", "George"]
        print(g.vs['name'])
        print(g)
        print(g.vs[0])

    def test2():
        g = Graph([(0, 1), (0, 0), (0, 2), (2, 3), (3, 4), (4, 2), (2, 5), (5, 0), (6, 3), (5, 6),
                   (7, 8), (8, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16)])
        print(g)
        g.to_undirected()
        print(g)
        print(len(g.decompose()))
        print(g.decompose()[0])
        print(g.decompose()[1])
        g = g.decompose(maxcompno=1)[0]
        g.simplify()
        print(g)

    test1()
    test2()


def cmdscale(g: Graph, profile: dict):
    # cmdscale: http://www.nervouscomputer.com/hfs/cmdscale-in-python/

    graph_dir = PurePath(profile['root']).joinpath(profile['name'])
    Λ_path, E_path = Path(graph_dir.joinpath('eigenvalues')), Path(graph_dir.joinpath('eigenvectors'))
    if not profile['force'] and Λ_path.exists() and E_path.exists():
        return io_array(Λ_path), io_array(E_path)

    # Distance matrix (All-pairs shortest path length in numpy array)
    distance_file = graph_dir.joinpath('graph', 'distance')
    try:
        if profile['force']:
            raise FileNotFoundError
        d = io_array(distance_file)
    except FileNotFoundError:
        paths = g.shortest_paths(weights=None)
        d = np.array(paths, dtype=np.int)
        io_array(str(distance_file), d)
        if _DEBUG_ and len(g.vs) < 100:
            print(d)
        benchmark(message='All-pairs shortest path length over the graph')

    # Classical Multi Dimensional Scaling
    N, _ = d.shape
    J = np.eye(N) - np.ones((N, N)) / N      # Centering matrix
    B = - J.dot(d * d).dot(J) / 2.0          # Apply double centering
    Λ, E = np.linalg.eigh(B)

    Λ_positive = Λ > 0                       # Choose positive eigenvalues
    Λ, E = Λ[Λ_positive], E[:, Λ_positive]
    Λ_descending = np.argsort(-Λ)            # Organize in descending order of eigenvalues
    Λ, E = Λ[Λ_descending], E[:, Λ_descending]
    dim_hd = Λ.shape[0]
    layout_hd = E.dot(np.diag(np.sqrt(Λ)))
    profile['dim_hd'] = layout_hd.shape

    if _DEBUG_:
        for i in range(dim_hd):
            v = E[:, i]
            diff = B.dot(v) - Λ[i] * v
            print(diff.dot(diff))
            assert diff.dot(diff) < 1e-10  # Confirm that E are truely eigenvectors

    L = np.eye(N, dim_hd).dot(np.diag(Λ))

    layout_dir = graph_dir.joinpath('layout')
    io_array(layout_dir.joinpath('eigenvalues'),  Λ)
    io_array(layout_dir.joinpath('eigenvectors'), E)
    io_array(layout_dir.joinpath('layout_hd'),    layout_hd)

    benchmark(message='Classical multi dimensional scaling')

    return Λ, E


def centrality(g: Graph, profile: dict):

    directory = None

    def save(name: str, c: np.array):
        io_array(directory.joinpath(name), c)
        benchmark(message='{0}.{1}'.format(directory, name))

    directory = PurePath(profile['root']).joinpath(profile['name'], 'centrality', 'v')
    save('betweenness', g.betweenness(directed=False))
    save('closeness', g.closeness())
    save('clustering', g.transitivity_local_undirected(mode='zero'))
    save('degree', g.degree())
    save('eigenvector', g.eigenvector_centrality(directed=False))
    save('hits_hub', g.hub_score())  # The Hub score for Kleinberg's HITS model
    save('pagerank', g.pagerank(directed=False))
    # Personalized PageRank score
    # save('ppagerank', g.personalized_pagerank(*args))

    directory = PurePath(profile['root']).joinpath(profile['name'], 'centrality', 'e')
    save('betweenness', g.edge_betweenness(directed=False))

    profile['centrality'] = {
        'v': 'betweenness closeness clustering degree eigenvector hits_hub pagerank'.split(' '),
        'e': 'betweenness'.split(' ')
    }


def analyse(root: PurePath, path: PurePath, profile: dict) -> Graph:
    g = normalize(read(path), profile)

    Λ, E = cmdscale(g, profile)
    centrality(g, profile)

    pickle(root.joinpath(profile['name'], 'misc', 'profile'), profile)
    print(json.dumps(profile, indent=4))

    return g


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


if __name__ == '__main__':
    def analyse_test():
        profile = dict(force=True,
                       root='/Users/wakita/Dropbox (smartnova)/work/glvis/data/dataset')

        root = PurePath(profile['root'])
        dataset_dir = PurePath('/Users/wakita/Dropbox (smartnova)/work/glvis/data/takami-svf')
        testcase = {
            'hypercube-4d': dataset_dir.joinpath('graphs', 'hypercube-4d.graphml'),
            'lesmis': dataset_dir.joinpath('lesmis.gml'),
            'math': dataset_dir.joinpath('math.wikipedia/math.graphml')
        }
        # 'gdea_conf': dataset_dir.joinpath('gdea_conf_paper_1995_2011.gml')

        for name, path in testcase.items():
            g = analyse(root, path, dict(profile, name=name))
            if all([len(label) > 0 for label in g.vs['label']]):
                print(g.vs['label'][0:4])
            else:
                print('No labels')

    def load_test():
        dataset_dir = PurePath('/Users/wakita/Dropbox (smartnova)/work/glvis/data/dataset')
        g = Loader(dataset_dir, 'lesmis')
        nv, ne = g.size()
        print('#V = {}, #E = {}'.format(nv, ne))
        dim_hd = g.dim_hd()
        print('dim(HD): {}'.format(dim_hd))
        assert dim_hd[0] == nv
        print(g.attributes())
        for a in g.attribute('label'):
            print(a)
        Λ, E = g.eigens()
        print('Shape(Λ): {}, Shape(E): {}'.format(Λ.shape, E.shape))
        layout_hd = g.layout_hd()
        print('Shape(layout_hd): {}'.format(layout_hd.shape))

    analyse_test()
    load_test()