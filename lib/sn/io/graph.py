from pathlib import PurePath, Path
from glob import glob
import sys
import traceback

import networkx as nx
import numpy as np

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
            if type == 'gml': keywords['label'] = 'id'
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


if __name__ == '__main__':
    for path in glob('/Users/wakita/Dropbox (smartnova)/work/glvis/data/takami-svf/**/*', recursive=True):
        g = read(path)
        if g: print(path, g.order())