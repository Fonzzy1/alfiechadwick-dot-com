import math
import numpy as np
import itertools as it
import matplotlib.pyplot as plt
import pandas as pd

## Set parameters for approximation
h = 0.001
xmin = -math.pi * 2
xmax = math.pi * 2

## Int vector such that [h,x,f(x),f'(x) .... f^n(x)]
int_list = np.array([h, math.pi / 2, -5 / 3, np.NAN, 15])
int_vect = int_list.reshape(len(int_list), 1)

## Condition Vector
condition_vect = np.array([[h, 0, np.NAN, 5, np.NAN],
                          [h, 2, 0, np.NAN, np.NAN],
                          [h, 0, np.NAN, 0, np.NAN]])
search_min = 1.43
search_max = 1.45
search_step = 0.01

## Find Permutaions
search_permutations = [ *it.permutations(np.arange(search_min, search_max, search_step), np.count_nonzero(np.isnan(int_vect)))]
nan_location = np.argwhere(np.isnan(int_vect))
nan_location = nan_location[nan_location != 0]
poss_int_vect = np.zeros((len(search_permutations), len(int_vect)))
for i in range(0, len(poss_int_vect)):
    poss_int_vect[i] = int_vect.T
    poss_int_vect[i][nan_location] = search_permutations[i]

## Set up matrix for step definition
step_matrix_pos = np.identity(len(int_vect))
step_matrix_neg = np.identity(len(int_vect))

## Set up x stepping system
step_matrix_pos[1][0] = 1
step_matrix_neg[1][0] = -1

## Set up taylor seies h values
for i in range(2, len(step_matrix_pos)):
    for j in range(i, len(step_matrix_pos)):
        step_matrix_pos[i][j] = h ** (j - i) / math.factorial(j - i)

## Set up taylor seies h/n! values
for i in range(2, len(step_matrix_neg)):
    for j in range(i, len(step_matrix_neg)):
        step_matrix_neg[i][j] = ((-h) ** (j - i)) / math.factorial(j - i)


## Swap rows of step_matrix to represent linear ODE
def linear_step_converion(matrix):
    matrix[4] = -9 * matrix[2]
    return matrix


step_matrix_pos = linear_step_converion(step_matrix_pos)
step_matrix_neg = linear_step_converion((step_matrix_neg))


## Create adjusting Function for non linear ODE
def adjustment(vector):
    vector[4] = -9 * vector[2] + math.cos(vector[1])
    return vector


## Run Simulation for all permutations, returning the distance from the condition

ls_distance = []
for int_vect in poss_int_vect:
    ## Create Output Space
    x_list = np.arange(xmin, xmax, h)

    output = np.zeros((len(x_list), len(int_vect)))
    output[0:len(output), 0] = h
    output[0:len(output), 1] = x_list
    ## Set up stepping process

    ## Do the positive steps first
    vect = int_vect.copy()
    while vect[1] <= xmax + h:
        index = int((vect[1] - xmin) / h)
        try:
            output[index] = vect.T
        except IndexError:
            pass
        vect = np.matmul(step_matrix_pos, vect)
        vect = adjustment(vect)

    ## Do the negative steps next
    vect = int_vect.copy()
    while vect[1] > xmin:
        index = int((vect[1] - xmin) / h)
        try:
            output[index] = vect.T
        except IndexError:
            pass
        vect = np.matmul(step_matrix_neg, vect)
        vect = adjustment(vect)

    ## Check condition
    dist_ls = []
    for vect in condition_vect:
        index = int(math.floor((vect[1] - xmin) / h))
        dist = np.linalg.norm(np.nan_to_num(output[index] - vect))
        dist_ls.append(dist)
    dist_sum = sum(dist_ls)
    ls_distance.append(dist_sum)

df_results = pd.DataFrame(poss_int_vect)
df_results['dist'] = ls_distance

best_index = df_results[['dist']].idxmin()

best_int_vect = poss_int_vect[best_index]

## Create Output Space
x_list = np.arange(xmin, xmax, h)

output = np.zeros((len(x_list), len(int_vect)))
output[0:len(output), 0] = h
output[0:len(output), 1] = x_list
## Set up stepping process

## Do the positive steps first
vect = best_int_vect.T.copy()
while vect[1] <= xmax + h:
    index = int((vect[1] - xmin) / h)
    try:
        output[index] = vect.T
    except IndexError:
        pass
    vect = np.matmul(step_matrix_pos, vect)
    vect = adjustment(vect)

## Do the negative steps next
vect = best_int_vect.T.copy()
while vect[1] > xmin:
    index = int((vect[1] - xmin) / h)
    try:
        output[index] = vect.T
    except IndexError:
        pass
    vect = np.matmul(step_matrix_neg, vect)
    vect = adjustment(vect)

dist_ls = []
for vect in condition_vect:
    index = int(math.floor((vect[1] - xmin) / h))
    dist = np.linalg.norm(np.nan_to_num(output[index] - vect))
    dist_ls.append(dist)
dist_sum = sum(dist_ls)

plt.plot(output.T[1], output.T[2])
plt.title(str(best_int_vect))
plt.show()
