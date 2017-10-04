from collections import defaultdict
from typing import List

from contour import Contour

class PropotionHandler:

    landing_field_proportions = [100, 74.8, 53.25, 35.35, 21.1, 10.52]
    proportion_tolerance = 5 # in percentages

    def __init__(self):
        self.mx = self._create_proportion_table(self.landing_field_proportions)

    def does_cntrs_statisfy_proportions(cntrs: List[Contour]):
        prop_vec = _create_propo


    @staticmethod
    def _create_proportion_table(props: List[float]) -> List[List[float]]:
        """ Creates a matrix where you have all proportions to each other in it. Let me explain it with a example:
        Your Landing field has six circles with the areas [100, 80, 50, 40, 30, 25] from biggest to smallest. If you know
        get a selection of them e.g. [80, 40, 30] and you would like to know if they are possible proportions, you need
        to create a lookup table. This table looks like:
        [1.0, 0.8, 0.5, 0.4, 0.3, 0.25]
        [1.0, 0.625, 0.5, 0.374, 0.3125]
        [1.0, 0.8, 0.6, 0.5],
        [1.0, 0.749, 0.625]
        [1.0, 0.83]
        [1.0]
        You get this table by starting at your biggest area and divide each one of your smaller areas with it.
        like 100 / 100, 80 / 100, 50 / 100, ... this results in the first row. To get the second row you choice the second
        biggest area as your biggest area and you do the same thing again: 80 / 80, 80 / 50, 80 / 40, ... Due to this shift
        the obvious triangular matrix exists
        :param props: vector with the areas of your landing field
        :return: proportion matrix with dimension len(props) x len(props)
        """
        mx = [[] for _ in range(len(props))]
        for i in range(len(props)):
            for j in range(i + 1):
                mx[j].append(props[i]/props[j])
        return mx

    @staticmethod
    def _create_propotion_vec(areas: List[float]) -> List[float]:
        """ Calculates the proportions from the biggest area to all others. e.g. for a given area vector [100, 50, 30] the
        resulting vector would be [100 / 100, 50 / 100, 30 / 100] = [1, 0.5, 0.3]
        :param areas: Vector of area size
        :return: vector of the proportions of all areas to the biggest one
        """
        if not areas:
            raise ValueError("Areas do not have an entry")

        areas_tmp = sorted(areas, reverse=True)
        props = []
        for i in range(len(areas_tmp)):
            props.append(areas_tmp[i] / areas_tmp[0])

        return props

    prop_threashold = 0.05 # in precentages
    @staticmethod
    def _calc_prop_scores(mx, props):
        score = defaultdict(lambda: 0)
        for i in range(len(mx)):
            k = 0
            for j in range(len(mx[i])):
                if mx[i][j] - prop_threashold <= props[k]\
                    <= mx[i][j] + prop_threashold:
                    score[i] += 1
                    k += 1

                    # check if all proportions are already compared
                    if k >= len(props):
                        break

            score[i] -= 1 # it is -1 bc you always have a one value in front (high math)

        return max(score.values())
