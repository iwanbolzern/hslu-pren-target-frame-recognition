import unittest
from src import image_processing


class ProportionHandlerTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_proportion_table(self):
        props = [1, 0.8, 0.5, 0.4, 0.3, 0.25]
        # This matrix should result with the given proportions
        # [1.0]
        # [0.8, 1.0]
        # [0.5, 0.625, 1.0]
        # [0.4, 0.5, 0.8, 1.0]
        # [0.3, 0.37499999999999994, 0.6, 0.7499999999999999, 1.0]
        # [0.25, 0.3125, 0.5, 0.625, 0.8333333333333334, 1.0]
        mx = image_processing.create_proportion_table(props)

        #first row
        self.assertEquals(mx[0][0], 1.0)

        #second row
        self.assertEquals(mx[1][0], 0.8)
        self.assertEquals(mx[1][1], 1.0)

        #third row
        self.assertEquals(mx[2][0], 0.5)
        self.assertEquals(mx[2][1], 0.625)
        self.assertEquals(mx[2][2], 1.0)

        #fourth row
        self.assertEquals(mx[3][0], 0.4)
        self.assertEquals(mx[3][1], 0.5)
        self.assertEquals(mx[3][2], 0.8)
        self.assertEquals(mx[3][3], 1.0)

        #fiveth row
        self.assertEquals(mx[4][0], 0.3)
        self.assertEquals(mx[4][1], 0.37499999999999994)
        self.assertEquals(mx[4][2], 0.6)
        self.assertEquals(mx[4][3], 0.7499999999999999)
        self.assertEquals(mx[4][4], 1.0)

        #sixth row
        self.assertEquals(mx[5][0], 0.25)
        self.assertEquals(mx[5][1], 0.3125)
        self.assertEquals(mx[5][2], 0.5)
        self.assertEquals(mx[5][3], 0.625)
        self.assertEquals(mx[5][4], 0.8333333333333334)
        self.assertEquals(mx[5][5], 1.0)

    def test_proportion_vector(self):
        areas = [100, 80, 50, 40, 30, 25]
        props = image_processing.create_propotion_vec(areas)
        self.assertEquals(props, [0.8, 0.5, 0.4, 0.3, 0.25])

    def test_proportion_score(self):
        props = [1, 0.8, 0.5, 0.4, 0.3, 0.25]
        areas = [100, 80, 50, 40, 30, 25]

        mx = image_processing.create_proportion_table(props)

        vec = image_processing.create_propotion_vec(areas)
        score = image_processing.calc_prop_scores(mx, vec)
        self.assertEquals(score, 5)

        areas = [100, 80, 40, 25]
        vec = image_processing.create_propotion_vec(areas)
        score = image_processing.calc_prop_scores(mx, vec)
        self.assertEquals(score, 3)

        areas = [80, 50, 30, 25]
        vec = image_processing.create_propotion_vec(areas)
        score = image_processing.calc_prop_scores(mx, vec)
        self.assertEquals(score, 3)

        # has to be defined what happend in this case (there are values which are not present in the props table)
        areas = [100, 80, 75, 70, 40, 25]
        vec = image_processing.create_propotion_vec(areas)
        score = image_processing.calc_prop_scores(mx, vec)
        #self.assertEquals(score, 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
