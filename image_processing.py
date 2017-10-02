def get_centers(cntrs):
    centers = []
    for cntr in cntrs:
        M = cv2.moments(cntr)
        centers.append((cntr, (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))))

    return centers

def create_proportion_table(props):
    mx = []
    for i in range(len(props)):
        mx.append([])
        for j in range(len(props)-1):
            mx[i].append(props[j]/props[i])
    return mx

prop_threashold = 5 # in precentages
def get_prop_scores(mx, props):
    score = defaultdict(0)
    for i in range(len(mx)):
        k = 0
        for j in range(len(props)):
            if mx[i][j] - prop_threashold <= props[k]\
                <= mx[i][j] + prop_threashold:
                score[i] += 1
                k += 1

    return s



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