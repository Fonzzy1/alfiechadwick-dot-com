import math
import numpy as np
import matplotlib.pyplot as plt

## Int vector such that [h,x,f(x),f'(x) .... f^n(x)] in a column matrix
vect_initial = np.array([[0.01],[1],[0],[1],[1]])

def adjustment_funtion(vector):
    return vector

## Transformation Matrix
def nonlin_IVP(xmin, xmax, vect_initial):

    #Check for valid input information
    ## Column int Vect?
    if vect_initial.shape[1] != 1 or len(vect_initial.shape) != 2:
        print('Invalid input vector, not a column')
        exit(0)
    ## positive h?
    if vect_initial[0][0] <= 0:
        print('Requires a positive non 0 value for h')
        exit(0)
    ## Valid xmin and xmax?
    if xmax-xmin <= 0:
        print('xmax must be greater than xmin')
        exit(0)

    h = vect_initial[0][0]

    # Build the Stepping matrices
    matix_step_neg = build_matix_step(-h, vect_initial)
    matix_step_pos = build_matix_step(h, vect_initial)

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
        vect =adjustment_funtion(np.matmul(matix_step_pos, vect))

    ## Do the negative steps next
    vect = vect_initial.copy()
    while vect[1][0] > xmin:
        index = int((vect[1][0] - xmin) / h)
        # Index Error commonly caused float size limit for small step size
        try:
            df_output[index] = vect.T
        except IndexError:
            pass
        vect = adjustment_funtion(np.matmul(matix_step_neg, vect))

    ## Plot df_output
    plt.plot(df_output.T[1], df_output.T[2])
    plt.title(str(vect_initial.T))
    plt.show()

    return df_output

def build_matix_step(h, vect_initial):
    base_matrix = np.identity(len(vect_initial))
    base_matrix[1][0] = np.sign(h)
    for i in range(2, len(base_matrix)):
        for j in range(i, len(base_matrix)):
            base_matrix[i][j] = h ** (j - i) / math.factorial(j - i)
    matix_step = base_matrix
    return matix_step

df_output = nonlin_IVP(0,10,vect_initial)

