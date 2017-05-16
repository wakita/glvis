
from .graph.load import load as load_dataset
#from .graph.analyse import analyse as analyse_dataset

import importlib.util
print(importlib.util.find_spec('.graph.', 'analyse'))

