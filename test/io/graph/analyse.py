from pathlib import PurePath, Path
import logging
import unittest
import time

import sn.io.graph.analyse as analyse

logging.getLogger().setLevel(logging.INFO)

data = PurePath('/Users/wakita/Dropbox/work/glvis/data')
root = data.joinpath('dataset')

dataset_large = data.joinpath('large')
dataset_takami = data.joinpath('takami-svf')

profile = dict(force=True, root=str(root))

class Test(unittest.TestCase):

    def test_lesmis(self):
        logging.info('Les Miserable')
        t_begin = time.time()
        analyse.analyse(root, dataset_takami.joinpath('lesmis.gml'),
                dict(profile, name='lesmis'))
        logging.info('time: {}'.format(time.time() - t_begin))
        return True

    def test_math(self):
        logging.info('Math@Wikipedia.JP')
        t_begin = time.time()
        analyse.analyse(root, dataset_takami.joinpath('math.wikipedia', 'math.graphml'),
                dict(profile, name='math'))
        logging.info('time: {}'.format(time.time() - t_begin))
        return True

    def test_internet_routers(self):
        logging.info('internet routers')
        t_begin = time.time()
        analyse.analyse(root, dataset_large.joinpath('internet_routers-22july06.gml'),
                dict(profile, name='internet_routers'))
        logging.info('time: {}'.format(time.time() - t_begin))
        return True

    def Test_enron(self):
        logging.info('enron')
        dataset_dir = data.joinpath('takami-svf')
        t_begin = time.time()
        analyse.analyse(root, dataset_takami.joinpath('enron.edgelist'),
                dict(profile, name='enron'))
        logging.info('time: {}'.format(time.time() - t_begin))
        return True

if __name__ == '__main__':
    unittest.main()
