import itertools
import pandas as pd
import numpy as np


from scipy import optimize
n = 3
spend_per_fortnight = 70
drinks_per_fortnight = 24 

def probability(dice_number, sides, target):
    rollAmount = sides**dice_number
    targetAmount = len([comb for comb in itertools.product(range(1, sides+1), repeat=dice_number) if sum(comb) == target])
    odds = targetAmount / rollAmount
    return odds



outcomes = np.arange(n,n*6+1,1)
pr = np.zeros(len(outcomes))

for value in outcomes:
    prob  = probability(n,6,value)
    index = np.where(outcomes == value)
    pr[index] = prob


whiskeys = pd.read_csv('./current.csv')

whiskeys['cpg'] = whiskeys.apply(lambda row: row['value']/row['vol'] * 40, axis=1)



price = whiskeys['cpg']

A = np.array([price.T, np.zeros(len(whiskeys))+1])

b = np.array([[spend_per_fortnight],[drinks_per_fortnight]])


def f(x):
    return np.linalg.norm(np.matmul(A,x) - b.T)

sol = optimize.least_squares(f, np.zeros(len(whiskeys))+1, bounds=[0,np.inf])

whiskeys['drinks'] = sol.x

whiskeys['probability'] = whiskeys['drinks'].apply(lambda x:x/drinks_per_fortnight)
whiskeys['Rolls'] = ''
whiskeys['roll_prob'] = 0.0
whiskeys.sort_values(by = ['probability'], inplace= True, ascending=False)

dice_rolls = pd.DataFrame(np.array([outcomes, pr]).T)


while len(dice_rolls) > 0:
    for (ind, whiskey) in whiskeys.iterrows():
        try:
            probs = whiskey['probability']
            closest_ind = (np.abs(dice_rolls[1] - probs)).argmin()
            val = np.array(dice_rolls[0])[closest_ind]
            dice_prob = np.array(dice_rolls[1])[closest_ind]
            if abs(probs - dice_prob) <  probs:
                probs -= dice_prob
                whiskeys['roll_prob'][ind] += dice_prob
                whiskeys['Rolls'][ind] = str(whiskeys['Rolls'][ind]) + str(int(val)) + ','
                dice_rolls = dice_rolls[dice_rolls[0] != val].reset_index(drop=True)
        except:
            pass
print(whiskeys)
