from pathlib import PurePath, Path
from glob import glob
import pickle
import sys
import traceback

import networkx as nx
import numpy as np

_DEBUG_ = True

_extensions = 'adjlist, multiline_adjlist, edgelist, gexf, gml, graph6, graphml, leda, pajek, shp, yaml'.split(', ')

_reader = dict(zip(_extensions,
                   [eval('nx.read_' + type) for type in _extensions]))

##
# Todo
# SparseGraph6 => graph6, GIS Shapefile => shp
# D3-style .json?


def read(path, *args, type=None, **keywords):
    p = PurePath(path)
    dir, stem, suffix = p.parent, p.stem, p.suffix
    if type == None and suffix[1:] in _reader.keys(): type = suffix[1:]
    if type in _reader.keys():
        try:
            # label_path = dir.joinpath(stem + '.labels')
            # print(path)
            # print(label_path)
            if type == 'gml':
                keywords['label'] = 'id'
            elif type == 'graphml':
                keywords['node_type'] = int
            g = _reader[type](path, *args, **keywords)
            return g
        except:
            print('Parsing failure')
            e, message, trace = sys.exc_info()
            print(message)
            #traceback.print_tb(trace)
            return None


centrality = dict(
    v=dict(
        degree=nx.degree_centrality,
        closeness=nx.closeness_centrality,
        betweenness=nx.betweenness_centrality,
        eigenverctor=nx.eigenvector_centrality,
        katz=nx.katz_centrality),

    e=dict(
        betweenness=nx.edge_betweenness_centrality))

#def process(G):
if __name__ == '__main__':
    profile = dict()

    dataset_root = PurePath('/Users/wakita/Dropbox (smartnova)/work/glvis/data/dataset')

    for path in [
        #'/Users/wakita/Dropbox (smartnova)/work/glvis/data/takami-svf/math.wikipedia/math.graphml',
        #'/Users/wakita/Dropbox (smartnova)/work/glvis/data/takami-svf/sengoku/sengoku.graphml',
        '/Users/wakita/Dropbox (smartnova)/work/glvis/data/takami-svf/dolphins.gml']:

        G = read(path)

        p = PurePath(path)
        dataset = dataset_root.joinpath(p.stem)
        Path(dataset).mkdir(exist_ok=True)

        labels = None
        label_path = Path(p.parent.joinpath(p.stem + '.labels'))
        if _DEBUG_: print(label_path)
        if label_path.is_file():
            labels = label_path.read_text(encoding='utf8')

        original_nodes = G.nodes()
        if _DEBUG_: print(original_nodes)

        # Remove self loops (if any)
        for v in G.nodes_with_selfloops():
            G.remove_edge(v, v)
        assert G.number_of_selfloops() == 0

        # Convert to undirected graph (if necessary)
        if nx.is_directed(G): G = G.to_undirected()

        # Find the largest connected component
        G = max(nx.connected_component_subgraphs(G), key=len)

        # Relabel the node labels
        mapping = dict(zip(G.nodes(), range(0, G.number_of_nodes())))
        G = nx.convert_node_labels_to_integers(G)

        # Save the graph and adjacency-list format
        graph = dataset.joinpath('graph')
        Path(graph).mkdir(exist_ok=True)
        nx.write_adjlist(G, str(graph.joinpath('graph.adjlist')))

        if labels:
            revmap = dict(zip(range(0, G.number_of_nodes()), G.nodes()))
            relabels = [ 0 for i in range(len(G.nodes()))]
            for i in G.nodes():
                relabels[i] = labels[revmap[i]]
            labels = relabels
            with open(str(graph.joinpath('labels.p')), 'wb') as w:
                pickle.dump(labels, w)


        nodes, edges = nx.nodes(G), nx.edges(G)
        profile['#nodes'] = len(G.nodes())
        profile['#edges'] = len(G.edges())

        if _DEBUG_:
            print(profile)
            print(G.nodes())
            print()

        # Distance matrix (All-pairs shortest path length in numpy array)
        distance_file = graph.joinpath('distance.npy')
        if Path(distance_file).is_file():
            D = np.load(str(distance_file))
        else:
            D = np.array([list(row.values()) for row in nx.all_pairs_shortest_path_length(G).values()], dtype=np.int)
            np.save(str(distance_file), D)
            if G.number_of_nodes() < 100:
                print(D)

        # Classical Multi Dimensional Scaling
        N, _ = D.shape
        D2 = D * D
        J = np.eye(N) - np.ones((N, N)) / N # Centering matrix
        B = - J.dot(D).dot(J) / 2.0 # Apply double centering
        Λ, E = np.linalg.eigh(B)

        # Organize eigenvalues in descending order of their eigenvalues
        positive_ev = Λ > 0
        Λ, E = Λ[positive_ev], E[:,positive_ev]
        descending = np.argsort(-Λ)
        Λ, E = Λ[descending], E[:,descending]
        print(Λ.shape, E.shape)
        dim_hd = Λ.shape[0]

        if _DEBUG_:
            for i in range(dim_hd):
                v = E[:, i]
                diff = B.dot(v) - v * Λ[i]
                print(diff.dot(diff))
                assert diff.dot(diff) < 1e-10 # Confirm that E are truely eigenvectors

        layout = dataset.joinpath('layout')
        Path(layout).mkdir(exist_ok=True)
        np.save(str(layout.joinpath('eigenvalues')), Λ)
        np.save(str(layout.joinpath('eigenvectors')), E)


if __name__ == '__main__' and False:
    for path in glob('/Users/wakita/Dropbox (smartnova)/work/glvis/data/takami-svf/**/*', recursive=True):
        g = read(path)
        if g: print(path, g.order())