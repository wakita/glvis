import logging
from pathlib import PurePath
import unittest

import sn.sn_logging
from sn.io import load_dataset


class Test(unittest.TestCase):
    def test_load(self):
        dataset_dir = PurePath('d:/wakita/work/glvis/data/dataset')
        g = load_dataset(dataset_dir, 'lesmis')
        nv, ne = g.size()
        logging.info('#V = {}, #E = {}'.format(nv, ne))
        dim_hd = g.dim_hd()
        logging.info('dim(HD): {}'.format(dim_hd))
        assert dim_hd[0] == nv
        logging.info(g.attributes())
        for a in g.attribute('label'):
            logging.info(a)
        Λ, E = g.eigens()
        logging.info('Shape(Λ): {}, Shape(E): {}'.format(Λ.shape, E.shape))
        layout_hd = g.layout_hd()
        logging.info('Shape(layout_hd): {}'.format(layout_hd.shape))

if __name__ == '__main__':
    unittest.main()
