import cv2
from collections import defaultdict

from copy import deepcopy
from sklearn.neighbors import NearestNeighbors
from typing import Tuple


def get_centers(cntrs):
    centers = []
    for cntr in cntrs:
        M = cv2.moments(cntr)
        centers.append((cntr, (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))))

    return centers

def create_proportion_table(props):
    mx = [[] for _ in range(len(props))]
    for i in range(len(props)):
        for j in range(i + 1):
            mx[j].append(props[i]/props[j])
    return mx

def create_propotion_vec(areas):
    if not areas:
        raise ValueError("Areas do not have an entry")

    areas_tmp = sorted(areas, reverse=True)
    props = []
    for i in range(len(areas_tmp)):
        props.append(areas_tmp[i] / areas_tmp[0])

    return props

prop_threashold = 0.05 # in precentages
def calc_prop_scores(mx, props):
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



def get_n_neighbours_below_delta(centers: Tuple[int, int], n: int, threashold: float):
    """ Returns all n points which are closer than a threashold to each other
    :param centers: Tuple with x and y value
    :param n: how many points have to be close to statisfy the threashold
    :param threashold:
    :return:
    """
    nbrs = NearestNeighbors(n_neighbors=n).fit([center[1] for center in centers])
    distances, indices = nbrs.kneighbors([center[1] for center in centers])

    threashold = 40;

    possible_candidates = []
    index_matrix = []
    for i in range(len(distances)):
        if sum(distances[i]) <= threashold and not does_matrix_contains(index_matrix, indices[i]):
            possible_candidates.append((sum(distances[i]), indices[i]))

    return possible_candidates

def does_matrix_contains(index_matrix, index_vec_to_check):
    index_vec_to_check = sorted(index_vec_to_check) # it is order independend
    for i in range(len(index_matrix)):
        if are_vectors_equal(index_vec_to_check, index_matrix[i]):
            return True

    index_matrix.append(index_vec_to_check)
    return False, index_matrix

def are_vectors_equal(vec_one, vec_two, order_independent: bool=True):
    if len(vec_one) is not len(vec_two):
        return False

    if order_independent:
        vec_one_tmp = sorted(vec_one)
        vec_two_tmp = sorted(vec_two)

    for i in range(len(vec_one_tmp)):
        if vec_one_tmp[i] is not vec_two_tmp[i]:
            return False

    return True

landing_field_proportions = [100, 74.8, 53.25, 35.35, 21.1, 10.52]
proportion_tolerance = 5 # in percentages

def does_cntrs_statisfy_proportions(cntrs, proportions):
    areas = [(cv2.contourArea(cntr), cntr) for cntr in cntrs]
    areas = sorted(areas)



    return