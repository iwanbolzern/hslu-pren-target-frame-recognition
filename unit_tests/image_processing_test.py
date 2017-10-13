import unittest
from image_processing.image_processing import Tree


class ImageProcessingTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_hierarchy_tree(self):
        """
        Tree should look like:
         _______0      1___
        |   |   |      |   |
        2   3   4      5   6
        |              |
        7              9
        |
        8
        """
        cv2_hierarchy = [
            [1, -1, 2, -1],
            [-1, 1, 5, -1],
            [3, -1, 7, 0],
            [4, 2, -1, 0],
            [-1, 3, -1, 0],
            [6, -1, 9, 1],
            [-1, 5, -1, 1],
            [-1, -1, 8, 2],
            [-1, -1, -1, 7],
            [-1, -1, -1, 5]
        ]

        tree = Tree(cv2_hierarchy)
        print(tree.leaves[0])
        print(tree.roots[0].childes)
        print(tree)

if __name__ == '__main__':
    unittest.main(verbosity=2)