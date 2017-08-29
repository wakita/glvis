from pathlib import PurePath, Path
import json
import logging
import re
import sys
from typing import Callable

from igraph import Graph
import numpy as np

from sn.io.util import pickle, io_array
import sn.utils
from sn.utils import time as benchmark

_DEBUG_ = False


def read(path: PurePath, *args, **kwds) -> Graph:
    try:
        g = Graph.Read(str(path), *args, **kwds)
        benchmark(message='Reading "{0}"'.format(path))
        try:
            logging.info(path.parent.joinpath(path.stem + '.labels'))
            with open(str(path.parent.joinpath(path.stem + '.labels'))) as r:
                g.vs['label'] = [re.sub(r'\n', '', line) for line in r.readlines()]
        except FileNotFoundError:
            pass
        return g
    except:
        logging.critical('Parsing failure: {}'.format(path))
        e, message, trace = sys.exc_info()
        logging.critical(message)
        raise e


def normalize(g: Graph, profile: dict) -> Graph:
    graph_dir = PurePath(profile['root']).joinpath(profile['name'], 'graph')
    logging.info('graph_dir: {}, name: {}', graph_dir, profile['name'])

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

    logging.info('')

    return g


def cmdscale(g: Graph, profile: dict):
    force = profile.get('force', False)

    # cmdscale: http://www.nervouscomputer.com/hfs/cmdscale-in-python/

    graph_dir = PurePath(profile['root']).joinpath(profile['name'])
    layout_dir = graph_dir.joinpath('layout')
    Λ_path, E_path, hd_path = [
            Path(layout_dir.joinpath(name + '.npy'))
            for name in 'eigenvalues eigenvectors layout_hd'.split()]
    if not force and Λ_path.exists() and E_path.exists():
        logging.info('Layout files found and returning')
        return io_array(Λ_path), io_array(E_path)
    logging.debug('Layout files not found: {}'.format(Λ_path))

    # Distance matrix (All-pairs shortest path length in numpy array)
    distance_file = graph_dir.joinpath('graph', 'distance.npy')
    try:
        if force:
            raise FileNotFoundError
        d = io_array(distance_file)
    except FileNotFoundError:
        paths = g.shortest_paths(weights=None)
        #d = np.array(paths, dtype=np.int)
        d = np.array(paths, dtype=np.uint8)
        io_array(distance_file, d)
        if _DEBUG_ and len(g.vs) < 100:
            logging.info(d)
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
    max_eigens = 'max_eigens' in profile and profile['max_eigens'] or 500
    if dim_hd > max_eigens:
        Λ = Λ[0:max_eigens]
        E = E[:, 0:max_eigens]
        dim_hd = Λ.shape[0]
    layout_hd = E.dot(np.diag(np.sqrt(Λ)))
    profile['dim_hd'] = layout_hd.shape

    if _DEBUG_:
        for i in range(dim_hd):
            v = E[:, i]
            diff = B.dot(v) - Λ[i] * v
            logging.info(diff.dot(diff))
            assert diff.dot(diff) < 1e-10  # Confirm that E are truely eigenvectors

    L = np.eye(N, dim_hd).dot(np.diag(Λ))

    io_array(Λ_path,  Λ)
    io_array(E_path,   E)
    io_array(layout_dir.joinpath('layout_hd'),    layout_hd)

    benchmark(message='Classical multi dimensional scaling')

    return Λ, E


def centrality(g: Graph, profile: dict):
    force = profile.get('force', False)

    directory = None

    def save(name: str, fc: Callable[[], np.array]):
        path_centrality = directory.joinpath(name + '.npy')
        if force or not Path(path_centrality).exists():
            io_array(path_centrality, fc())
            benchmark(message='{0}.{1}'.format(directory, name))

    directory = PurePath(profile['root']).joinpath(profile['name'], 'centrality', 'v')
    save('betweenness', lambda: g.betweenness(directed=False))
    save('closeness',   lambda: g.closeness())
    save('clustering',  lambda: g.transitivity_local_undirected(mode='zero'))
    save('degree',      lambda: g.degree())
    save('eigenvector', lambda: g.eigenvector_centrality(directed=False))
    save('hits_hub',    lambda: g.hub_score())  # The Hub score for Kleinberg's HITS model
    save('pagerank',    lambda: g.pagerank(directed=False))
    # Personalized PageRank score
    # save('ppagerank', lambda: g.personalized_pagerank(*args))

    directory = PurePath(profile['root']).joinpath(profile['name'], 'centrality', 'e')
    save('betweenness', lambda: g.edge_betweenness(directed=False))

    profile['centrality'] = {
        'v': 'betweenness closeness clustering degree eigenvector hits_hub pagerank'.split(' '),
        'e': 'betweenness'.split(' ')
    }


def analyse(root: PurePath, path: PurePath, profile: dict) -> Graph:
    g = normalize(read(path), profile)

    cmdscale(g, profile)
    centrality(g, profile)

    path_profile = Path(root.joinpath(profile['name'], 'misc', 'profile.json'))
    if profile.get('force', False) or not path_profile.exists():
        with open(str(path_profile), 'w') as w:
            json.dump(profile, w, ensure_ascii=False, indent=4)
        logging.info(json.dumps(profile, indent=4))

    return g


if __name__ == '__main__':
    def analyse_test():
        profile = dict(force=True,
                       root='/Users/wakita/Dropbox/work/glvis/data/dataset')

        root = PurePath(profile['root'])
        dataset_dir = PurePath('/Users/wakita/Dropbox/work/glvis/data/takami-svf')
        testcase = {
            # 'hypercube-4d': dataset_dir.joinpath('graphs', 'hypercube-4d.graphml'),
            # 'lesmis': dataset_dir.joinpath('lesmis.gml'),
            'math': dataset_dir.joinpath('math.wikipedia/math.graphml')
            # 'gdea_conf': dataset_dir.joinpath('gdea_conf_paper_1995_2011_nographics.gml'),
            # '4dai': dataset_dir.joinpath('twitter', '4dai_uni_d_nolabel.gml'),
            # 'techchan': dataset_dir.joinpath('twitter', 'techchan_uni_d_nolabel.gml')
        }

        for name, path in testcase.items():
            logging.info(name)
            g = analyse(root, path, dict(profile, name=name))
            if 'label' in g.vs.attribute_names() and all([len(label) > 0 for label in g.vs['label']]):
                logging.info(g.vs['label'][0:4])
            else:
                logging.info('No labels')

        dataset_dir = PurePath('/Users/wakita/Dropbox/work/glvis/data/large')
        logging.info('internet routers')
        g = analyse(root, dataset_dir.joinpath('internet_routers-22july06.gml'),
                dict(profile, force=False, name='internet_routers'))

    from sn.io.graph.load import load as load_dataset

    def load_test():
        dataset_dir = PurePath('/Users/wakita/Dropbox/work/glvis/data/dataset')
        g = load_dataset(dataset_dir, 'internet_routers')
        # g = load_dataset(dataset_dir, 'lesmis')
        nv, ne = g.size()
        logging.info('#V = {}, #E = {}'.format(nv, ne))
        logging.info(g.profile)
        dim_hd = g.dim_hd()
        logging.info('dim(HD): {}'.format(dim_hd))
        assert dim_hd[0] == nv
        logging.info(g.attributes())
        for a in g.attribute('label'):
            logging.info(a)
        Λ, E = g.eigens()
        logging.getLogger().setLevel(logging.INFO)
        logging.info('Shape(Λ): {}, Shape(E): {}'.format(Λ.shape, E.shape))
        layout_hd = g.layout_hd()
        logging.info('Shape(layout_hd): {}'.format(layout_hd.shape))

    # Crash on load bug
    # techchan_uni_ud.gml, 4dai_uni_d.gml, gdea_conf_paper_1995_2011.gml

    analyse_test()
    load_test()
