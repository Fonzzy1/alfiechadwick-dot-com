import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


## Varibles to set to define simultaion
def f(x):  ## Only for plotting against estimation
    return

def c(n):  ## C vaules
    if n == 0:
        return 2
    if n == 1:
        return 3
    if n == 2:
        return 3 + math.sin(2) + 3


a = 0  ## Around what point is this estimation
step = 0.1  ## step Size for points
width = 10  ## Range of Estimation
depth = 3  ## Max size of n

## Create List of points
width_mult = 1 / step
new_witdh = int(round(width * width_mult))
ls_points = range(-new_witdh, new_witdh)
ls_points = list(map(lambda x: x * step, ls_points))

## Create List n
ls_n = list(range(0, depth))

## Create List of coefficients
ls_c = list(map(lambda x: c(x), ls_n))


def point_term(x, a, cond, n):
    point = cond / math.factorial(n) * (x - a) ** n
    return point


df = pd.DataFrame(ls_points, columns=['Point'])

## Create A datframe with each collumn being the vaules for a single n
for n in ls_n:
    df[n] = df['Point'].apply(lambda x: point_term(x, a, ls_c[n], n))

df.set_index('Point', inplace=True)

## Sum all the estimations
df_estimation = df.sum(axis=1)

df_estimation.plot(label='Estimation')

if f(a):
    plt.plot(ls_points, list(map(lambda x: f(x), ls_points)), label='Actual', linestyle='dashed', )
plt.legend()

plt.show()