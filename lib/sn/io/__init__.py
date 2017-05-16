import logging
import importlib.util
import sys

from .graph.load import load as load_dataset
# from .graph.analyse import analyse as analyse_dataset

# import sn.io.graph.analyse if igraph is available
specname = 'igraph'
spec = importlib.util.find_spec(specname) 
if spec is not None:
    specname = 'sn.io.graph.analyse'
    spec = importlib.util.find_spec(specname) 
    logging.info('Importing {}.read as analyse_dataset'.format(specname))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    analyse_dataset = module.read
else:
    logging.info('The sn.io.graph.analyse module is not imported as one of its dependency "igraph" module is missing.')
