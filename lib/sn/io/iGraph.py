from pathlib import PurePath, Path
from glob import glob
import json
import re
import sys

from igraph import Graph
import numpy as np

from sn.io import pickle, io_array
import sn.utils
from sn.utils import time as benchmark

_DEBUG_ = False

sn.utils._VERBOSE_ = True


def read(path, *args, **kwds) -> Graph:
    try:
        g = Graph.Read(path, *args, **kwds)
        benchmark(message='Reading "{0}"'.format(path))
        try:
            p = PurePath(path)
            print(p.parent.joinpath(p.stem + '.labels'))
            with open(str(p.parent.joinpath(p.stem + '.labels'))) as r:
                g.vs['Label'] = [ re.sub(r'\n', '', line) for line in r.readlines()]
        except FileNotFoundError: pass
        return g
    except:
        print('Parsing failure:', path)
        e, message, trace = sys.exc_info()
        print(message)
        raise e


def normalize(g: Graph, profile: dict) -> Graph:
    graph_dir = PurePath(profile['root']).joinpath(profile['name'], 'graph')
    print('graph_dir:', graph_dir)
    Path(graph_dir).mkdir(exist_ok=True, parents=True)

    adj_path = graph_dir.joinpath('edgelist')
    try:
        if not profile['force']: raise FileNotFoundError
        return io_array(adj_path)
    except FileNotFoundError:
        # Convert to undirected graph
        g.to_undirected()
        assert not g.is_directed()

        # The largest strongly connected component
        g = g.decompose(maxcompno=1)[0]
        # ToDo: Check if vertex numbers change after 'decompose'.
        # If they do, we need to reorganize the labels as well.

        # Remove self-loops
        g.simplify()
        assert not any(g.is_loop())

        io_array(adj_path, g.get_edgelist())
        if 'Label' in g.vs.attributes():
            label_path = graph_dir.joinpath('label')
            io_array(label_path, g.vs['Label'])
        return g


if __name__ == '__main__' and False:
    g = Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])
    g.vs["name"] = ["Alice", "Bob", "Claire", "Dennis", "Esther", "Frank", "George"]
    print(g.vs['name'])
    print(g)
    print(g.vs[0])


if __name__ == '__main__' and False:
    g = Graph([(0,1), (0,0), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6),
               (7,8), (8,8), (8,9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17)])
    print(g)
    g.to_undirected()
    print(g)
    print(len(g.decompose()))
    print(g.decompose()[0])
    print(g.decompose()[1])
    g = g.decompose(maxcompno=1)[0]
    g.simplify()
    print(g)


def cmdscale(G, profile, force=False):
    '''cmdscale: http://www.nervouscomputer.com/hfs/cmdscale-in-python/'''
    graph_dir = PurePath(profile['root']).joinpath(profile['name'])
    Λ_path, E_path = Path(graph_dir.joinpath('eigenvalues')), Path(graph_dir.joinpath('eigenvectors'))
    if not force and Λ_path.exists() and E_path.exists():
        return io_array(Λ_path), io_array(E_path)

    # Distance matrix (All-pairs shortest path length in numpy array)
    distance_file = graph_dir.joinpath('graph', 'distance.npy')
    try:
        if not force:
            raise FileNotFoundError
        D = np.load(str(distance_file))
    except FileNotFoundError:
        D = np.array([list(row.values()) for row in nx.all_pairs_shortest_path_length(G).values()], dtype=np.int)
        io_array(str(distance_file), D)
        if _DEBUG_ and G.number_of_nodes() < 100: print(D)
        benchmark(message='All-pairs shortest path length over the graph')

    # Classical Multi Dimensional Scaling
    N, _ = D.shape
    J = np.eye(N) - np.ones((N, N)) / N      # Centering matrix
    B = - J.dot(D * D).dot(J) / 2.0          # Apply double centering
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
            assert diff.dot(diff) < 1e-10 # Confirm that E are truely eigenvectors

    L = np.eye(N, dim_hd).dot(np.diag(Λ))

    layout_dir = graph_dir.joinpath('layout')
    Path(layout_dir).mkdir(exist_ok=True)
    np.save(str(layout_dir.joinpath('eigenvalues')),  Λ)
    np.save(str(layout_dir.joinpath('eigenvectors')), E)
    np.save(str(layout_dir.joinpath('layout_hd')), layout_hd)

    benchmark(message='Classical multi dimensional scaling')

    return Λ, E


def convert(root, path, force=False):
    0


def load(root, name):
    0


def centrality(G):

    # Betweenness centrality
    # API: G.betweenness(vertices, directed=True, cutoff=None, weights=None, nobigint=True)

    # Closeness centrality
    G.closeness(vertices=None, mode=ALL, cutoff=None, weights=None, normalized=True)

    # Clustering coefficient
    G.transitivity_local_undirected(vertices=None, mode="nan", weights=None)

    # Degree distribution
    # API: G.degree(G.vertices, loops=False) -- Degrees of 'vertices' for both incoming&outgoing direction (mode=ALL), ignoring self-loops
    G.degree(loops=False)

    # Eigenvector centrality
    G.eigenvector_centrality(directed=True, scale=True, weights=None, return_eigenvalue=False, arpack_options=None)

    # The Hub score for Kleinberg's HITS model
    G.hub_score(weights=None, scale=True, arpack_options=None, return_eigenvalue=False)

    # PageRank score
    #G.pagerank(self, vertices=None, directed=True, damping=0.85, weights=None, arpack_options=None, implementation='prpack', niter=1000, eps=0.001)
    #Calculates the Google PageRank values of a graph.	source code

    # Personalized PageRank score
    G.personalized_pagerank(vertices=None, directed=True, damping=0.85, reset=None, reset_vertices=None, weights=None, arpack_options=None, implementation="prpack", niter=1000, eps=0.001)


    # Edge betweenness centrality
    G.edge_betweenness(directed=True, cutoff=None, weights=None)


if __name__ == '__main__':
    profile = dict(force=True,
                   root='/Users/wakita/Dropbox (smartnova)/work/glvis/data/dataset')

    dataset = '/Users/wakita/Dropbox (smartnova)/work/glvis/data/takami-svf/'
    testcase = {
        'hypercube-4d': dataset + 'graphs/hypercube-4d.graphml',
        'lesmis': dataset + 'lesmis.gml' }

    for name, path in testcase.items():
        g = normalize(read(path), dict(profile, name=name))
        if 'Label' in g.vs.attributes(): print(g.vs['Label'][0:4])
        else: print('No labels')
