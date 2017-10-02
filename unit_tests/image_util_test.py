import unittest

import main


class ImageUtilTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_proportion_table(self):
        props = [1, 0.8, 0.5, 0.4, 0.3, 0.25]
        mx = main.create_proportion_table()
        print(mx)

if __name__ == '__main__':
    unittest.main(verbosity=2)
