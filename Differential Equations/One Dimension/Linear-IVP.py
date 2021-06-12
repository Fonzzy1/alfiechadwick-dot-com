import math
import numpy as np
import matplotlib.pyplot as plt

## Int vector such that [h,x,f(x),f'(x) .... f^n(x)] in a column matrix
vect_initial = np.array([[0.01],[1],[0],[1],[1]])

matrix_transform = np.array([[1,0,0,0,0],
                             [0,1,0,0,0],
                             [0,0,1,0,0],
                             [0,0,0,1,0],
                             [0,0,-1,0,0]])

## Transformation Matrix
def lin_IVP(xmin, xmax, vect_initial, matrix_transform):

    #Check for valid input information
    ## Column int Vect?
    if vect_initial.shape[1] != 1 or len(vect_initial.shape) != 2:
        print('Invalid input vector, not a column')
        exit(0)
    ## positive h?
    if vect_initial[0][0] <= 0:
        print('Requires a positive non 0 value for h')
        exit(0)
    ## Transform Matrix Correct Shape?
    if matrix_transform.shape[0] != matrix_transform.shape[1] or matrix_transform.shape[0] != vect_initial.shape[0] or len(matrix_transform.shape) != 2:
        print('Transformation matrix wrong shape')
        exit(0)
    ## Valid xmin and xmax?
    if xmax-xmin <= 0:
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

def build_matrix_step(h,matrix_transform):
    matrix_base = np.identity(len(matrix_transform))
    matrix_base[1][0] = np.sign(h)
    for i in range(2, len(matrix_base)):
        for j in range(i, len(matrix_base)):
            matrix_base[i][j] = h ** (j - i) / math.factorial(j - i)
    matrix_step = np.matmul(matrix_transform,matrix_base)
    return matrix_step

df_output = lin_IVP(0,10,vect_initial,matrix_transform)





