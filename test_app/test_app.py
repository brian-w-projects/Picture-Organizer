import unittest
import os
from forgery_py import lorem_ipsum
from random import randint, choice
from shutil import rmtree
from app.picture_organizer import PictureOrganizer


class PictureOrganizerTester(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(PictureOrganizerTester, self).__init__(*args, **kwargs)
        self.extensions = ['.txt', '.jpg', '.bmp', '.doc']
        self.cwd = os.getcwd()
        self.pathways = {
            'outer': os.path.join(self.cwd, 'test_data', 'outer'),
            'inner1': os.path.join(self.cwd, 'test_data', 'outer', 'inner1'),
            'inner2': os.path.join(self.cwd, 'test_data', 'outer', 'inner2'),
            'inner3': os.path.join(self.cwd, 'test_data', 'outer', 'inner3'),
            'inner4': os.path.join(self.cwd, 'test_data', 'outer', 'inner1', 'inner4')
        }

    def setUp(self):
        for pathway in self.pathways.values():
            if not os.path.exists(pathway):
                os.mkdir(pathway)
                os.chdir(pathway)
                for i in range(100):
                    if i < 10:
                        open('.' + lorem_ipsum.words(randint(1, 4)) + choice(self.extensions), 'a').close()
                    else:
                        open(lorem_ipsum.words(randint(1, 4)) + choice(self.extensions), 'a').close()
                os.chdir(self.cwd)

        os.chdir(self.cwd)

    def test_invalid_pathway(self):
        self.assertRaises(ValueError, PictureOrganizer, 'invalid')

    def test_no_recurse(self):
        original_inner1 = os.listdir(self.pathways['inner1'])
        original_inner2 = os.listdir(self.pathways['inner2'])
        original_inner3 = os.listdir(self.pathways['inner3'])
        original_inner4 = os.listdir(self.pathways['inner4'])
        po = PictureOrganizer(self.pathways['outer'], recurse=False)
        po.rename_folders()
        self.assertListEqual(original_inner1, os.listdir(self.pathways['inner1']))
        self.assertListEqual(original_inner2, os.listdir(self.pathways['inner2']))
        self.assertListEqual(original_inner3, os.listdir(self.pathways['inner3']))
        self.assertListEqual(original_inner4, os.listdir(self.pathways['inner4']))

    def test_skip_extensions(self):
        ext_skip = ('txt', 'bmp')
        po = PictureOrganizer(self.pathways['outer'], ext_skip=ext_skip)
        po.rename_folders()

        self.verify_name_change(ext_skip=ext_skip)

    def test_folder_skip(self):
        original_inner1 = os.listdir(self.pathways['inner1'])
        original_inner2 = os.listdir(self.pathways['inner2'])

        po = PictureOrganizer(self.pathways['outer'], folder_skip=['inner1', 'inner2'], recurse=True)
        po.rename_folders()

        self.assertListEqual(original_inner1, os.listdir(self.pathways['inner1']))
        self.assertListEqual(original_inner2, os.listdir(self.pathways['inner2']))

    def test_recurse(self):
        po = PictureOrganizer(self.pathways['outer'], recurse=True)
        po.rename_folders()
        self.verify_name_change()

    def test_simulate(self):
        original_outer = os.listdir(self.pathways['outer'])
        po = PictureOrganizer(self.pathways['outer'], simulate=True)
        po.rename_folders()
        self.assertListEqual(original_outer, os.listdir(self.pathways['outer']))

    def verify_name_change(self, ext_skip=()):
        for folder_name, pathway in self.pathways.items():
            for f in os.listdir(pathway):
                if os.path.isfile(f):
                    if f.startswith('.') or f.endswith(ext_skip):
                        self.assertFalse(f.startswith(folder_name))
                    else:
                        self.assertTrue(f.startswith(folder_name))

    def tearDown(self):
        rmtree(self.pathways['outer'])


if __name__ == '__main__':
    unittest.main()
