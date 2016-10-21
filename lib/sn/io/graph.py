from pathlib import PurePath

import networkx as nx
import numpy as np

_reader = dict(zip(types,
                   [eval('nx.read_' + type) for type in
                    'adjlist, multiline_adjlist, edgelist, gexf, gml, graph6, graphml, leda, pajek, shp, yaml'.split(', ')]))

# SparseGraph6 => graph6, GIS Shapefile => shp
# D3-style .json?

def read(path, *args, type=None):
    suffix = PurePath(path).suffix
    if type == None and suffix[1:] in _reader.keys(): type = suffix[1:]
    print(type)
    if type in _reader.keys():
        return reader[type](path, *args)


er = nx.erdos_renyi_graph(100, 0.15)
ws = nx.watts_strogatz_graph(30, 3, 0.1)
ba = nx.barabasi_albert_graph(100, 5)

networks = [er, ws, ba]

centrality = dict(
    v=dict(
        degree=nx.degree_centrality,
        closeness=nx.closeness_centrality,
        betweenness=nx.betweenness_centrality,
        eigenverctor=nx.eigenvector_centrality,
        katz=nx.katz_centrality),

    e=dict(
        betweenness=nx.edge_betweenness_centrality))

for g in networks:
    cmap = centrality['v']['degree'](g)
    np.save('g', np.array(list(cmap.values())))
