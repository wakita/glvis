import logging
from pathlib import PurePath
import unittest

import sn.sn_logging
import sn.io.graph.analyse as analyse

class Test(unittest.TestCase):
    def test_load(self):
        logging.getLogger().setLevel(logging.INFO)

        profile = dict(force=True,
                       root='/Users/wakita/Dropbox/work/glvis/data/dataset',
                       name='enron')
        root = PurePath(profile['root'])
        dataset_dir = PurePath('/Users/wakita/Dropbox/work/glvis/data/takami-svf')

        path = dataset_dir.joinpath('enron.edgelist')
        g = analyse.read(path)
        logging.info('#V = {}, #E = {}'.format(len(g.vs), len(g.es)))
        g = analyse.normalize(g, profile)
        logging.info('#V = {}, #E = {}'.format(len(g.vs), len(g.es)))
        for v in g.vs:
            logging.info('{}'.format(v))


if __name__ == '__main__':
    unittest.main()
