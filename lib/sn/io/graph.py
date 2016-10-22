from pathlib import PurePath, Path
from glob import glob

import networkx as nx
import numpy as np

_extensions = 'adjlist, multiline_adjlist, edgelist, gexf, gml, graph6, graphml, leda, pajek, shp, yaml'.split(', ')

_reader = dict(zip(_extensions,
                   [eval('nx.read_' + type) for type in _extensions]))

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
            g = _reader[type](path, *args, label='id', **keywords)
            return g
        except Exception as e:
            print('type:', str(type(e)))
            print('args:', str(e.args))
            print('message:', e.message)
            return None


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

#read('/Users/wakita/Dropbox (smartnova)/work/glvis/data/takami-svf/lesmis.gml', label='id')
#nx.read_gml('/Users/wakita/Dropbox (smartnova)/work/glvis/data/takami-svf/graphs/sierpinski04.gml', label='id')
#nx.read_gml('/Users/wakita/Dropbox (smartnova)/work/glvis/data/takami-svf/gdea_conf_paper_1995_2011-nolabel.gml', label='id')
#nx.read_graphml('/Users/wakita/Dropbox (smartnova)/work/glvis/data/takami-svf/erdos1graph-reduced.463-2.graphml', node_type='str')

for path in glob('/Users/wakita/Dropbox (smartnova)/work/glvis/data/takami-svf/**/*.gml', recursive=True):
    g = read(path)
    if g: print(path, g.order())
    else: print(path, 'Parsing failure')

# failures
# dolphins.gml, erdox1graph-reduced.463.graphml, gdea_conf_paper_1995_2011.gml, karate.am, lesmis.gml, *.graphml