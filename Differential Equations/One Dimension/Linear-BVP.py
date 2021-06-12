import math
import numpy as np
import matplotlib.pyplot as plt
import itertools as it
import pandas as pd

## Int vector such that [h,x,f(x),f'(x) .... f^n(x)] in a column matrix
vect_initial = np.array([[0.01],[1],[np.NAN], [1], [np.NAN]])
matrix_transform = np.array([[1, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0],
                             [0, 0, 1, 0, 0],
                             [0, 0, 0, 1, 0],
                             [0, 0, -1, 0, 0]])
xmin = 0
xmax = 5
## Condition Vector
condition_vect = np.array([[0.01,1,0,1,0],
                           [0.01,2,1,np.NAN,np.NAN]])
search_min = -1
search_max = 1
search_step = 0.01

def lin_IVP(xmin, xmax, vect_initial, matrix_transform):
    # Check for valid input information
    ## Column int Vect?
    if vect_initial.shape[1] != 1 or len(vect_initial.shape) != 2:
        print('Invalid input vector, not a column')
        exit(0)
    ## positive h?
    if vect_initial[0][0] <= 0:
        print('Requires a positive non 0 value for h')
        exit(0)
    ## Transform Matrix Correct Shape?
    if matrix_transform.shape[0] != matrix_transform.shape[1] or matrix_transform.shape[0] != vect_initial.shape[
        0] or len(matrix_transform.shape) != 2:
        print('Transformation matrix wrong shape')
        exit(0)
    ## Valid xmin and xmax?
    if xmax - xmin <= 0:
        print('xmax must be greater than xmin')
        exit(0)

    h = vect_initial[0][0]

    # Build the Stepping matrices
    matrix_step_neg = build_matrix_step(-h, matrix_transform)
    matrix_step_pos = build_matrix_step(h, matrix_transform)

    ## Create df_output Space
    x_list = np.arange(xmin, xmax, h)

    df_output = np.zeros((len(x_list), len(vect_initial)))
    df_output[0:len(df_output), 0] = h
    df_output[0:len(df_output), 1] = x_list

    ## Do the positive steps first
    vect = vect_initial.copy()
    while vect[1][0] <= xmax + h:
        index = int((vect[1][0] - xmin) / h)
        # Index Error commonly caused float size limit for small step size
        try:
            df_output[index] = vect.T
        except IndexError:
            pass
        vect = np.matmul(matrix_step_pos, vect)

    ## Do the negative steps next
    vect = vect_initial.copy()
    while vect[1][0] > xmin:
        index = int((vect[1][0] - xmin) / h)
        # Index Error commonly caused float size limit for small step size
        try:
            df_output[index] = vect.T
        except IndexError:
            pass
        vect = np.matmul(matrix_step_neg, vect)

    ## Plot df_output
    plt.plot(df_output.T[1], df_output.T[2])
    plt.title(str(vect_initial.T))
    plt.show()

    return df_output
def single_value_lin_IVP(x,vect_initial,matrix_transform):
    # Check for valid input information
    ## Column int Vect?
    if vect_initial.shape[1] != 1 or len(vect_initial.shape) != 2:
        print('Invalid input vector, not a column')
        exit(0)
    ## positive h?
    if vect_initial[0][0] <= 0:
        print('Requires a positive non 0 value for h')
        exit(0)
    ## Transform Matrix Correct Shape?
    if matrix_transform.shape[0] != matrix_transform.shape[1] or matrix_transform.shape[0] != vect_initial.shape[
        0] or len(matrix_transform.shape) != 2:
        print('Transformation matrix wrong shape')
        exit(0)
    ## Valid xmin and xmax?
    if xmax - xmin <= 0:
        print('xmax must be greater than xmin')
        exit(0)

    h = vect_initial[0][0]

    # Build the Stepping matrices
    matrix_step_neg = build_matrix_step(-h, matrix_transform)
    matrix_step_pos = build_matrix_step(h, matrix_transform)

    k = int((x - vect_initial[1])/h)

    if k > 0:
        step_matrix_k = np.linalg.matrix_power(matrix_step_pos,k)
        vect_output =  np.matmul(step_matrix_k,vect_initial)
    if k < 0:
        step_matrix_k = np.linalg.matrix_power(matrix_step_neg,-k)
        vect_output =  np.matmul(step_matrix_k,vect_initial)
    if k == 0:
        vect_output = vect_initial

    return vect_output
def build_matrix_step(h, matrix_transform):
    matrix_base = np.identity(len(matrix_transform))
    matrix_base[1][0] = np.sign(h)
    for i in range(2, len(matrix_base)):
        for j in range(i, len(matrix_base)):
            matrix_base[i][j] = h ** (j - i) / math.factorial(j - i)
    matrix_step = np.matmul(matrix_transform, matrix_base)
    return matrix_step
def find_best_initial(search_min, search_max, search_step, vect_initial, matrix_transform, condition_vect):
    # Find All Possible initial vectors
    search_permutations = [*it.combinations_with_replacement(np.arange(search_min, search_max + search_step, search_step),
                                            np.count_nonzero(np.isnan(vect_initial)))]
    nan_location = np.argwhere(np.isnan(vect_initial))
    nan_location = nan_location[nan_location != 0]
    vect_initial_poss = np.zeros((len(search_permutations), len(vect_initial)))
    for i in range(0, len(search_permutations)):
        vect_initial_poss[i] = vect_initial.T
        vect_initial_poss[i][nan_location] = search_permutations[i]

    ## List of scores
    ls_distance = []

    # Run over range of possible vectors
    for vect_initial in vect_initial_poss:
        ls_distance_single = []
        for vect in condition_vect:
            output = single_value_lin_IVP(vect[1],np.reshape(vect_initial, (len(vect_initial),1)),matrix_transform)
            dist = np.linalg.norm(np.nan_to_num(output - np.reshape(vect, (len(vect),1))))
            ls_distance_single.append(dist)
        ls_distance.append(sum(ls_distance_single))

    df_results = pd.DataFrame(vect_initial_poss)
    df_results['dist'] = ls_distance

    best_index = df_results[['dist']].idxmin()

    best_int_vect = vect_initial_poss[best_index].T
    dist = df_results['dist'][best_index].values
    return (best_int_vect, dist, df_results)

(vector_initial_best, dist, df_results) = find_best_initial(search_min, search_max, search_step, vect_initial, matrix_transform, condition_vect)

df_output = lin_IVP(xmin, xmax, vector_initial_best, matrix_transform)
