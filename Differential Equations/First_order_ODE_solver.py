import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def c(a, cond, n):
    if n == 0:
        return cond;
    if n == 1:
        return a * math.sin(cond)

    return cond


int_x = 0
int_y = 2
# 2
depth = 2
step = 0.001
d_min = -3
d_max = 3

# 2.1 Set up output space
d_min_scale = int(round(d_min / step))
d_max_scale = int(round(d_max / step))
ls_points = list(range(d_min_scale, d_max_scale))
ls_points = list(map(lambda x: x * step, ls_points))
df = pd.DataFrame(ls_points, columns=['Point'])
df['Value'] = 0
df.set_index('Point', inplace=True)

# 2.2 Set up n list
ls_n = list(range(0, depth))


# 3
def point(step, vector, ls_n, derivative):
    ls_point_term = []
    for n in ls_n:
        coefficient = c(vector, n + derivative)
        point = coefficient / math.factorial(n) * step ** n
        ls_point_term.append(point)
    point_value = sum(ls_point_term)
    return point_value


a = int_x
cond = int_y
while a <= d_max:
    point_value = point(step, a, cond, ls_n)
    location = df.index.get_loc(a, method='nearest')
    df.iloc[location, 0] = point_value
    cond = point_value
    a += step

a = int_x
cond = int_y

while a >= d_min:
    point_value = point(-step, a, cond, ls_n)
    location = df.index.get_loc(a, method='nearest')
    df.iloc[location, 0] = point_value
    cond = point_value
    a -= step

df.plot()
plt.show()
