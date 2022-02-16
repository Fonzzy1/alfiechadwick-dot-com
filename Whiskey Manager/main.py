import itertools
import pandas as pd
import numpy as np
from scipy import optimize

n = 3 

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
whiskeys['rel_cpg'] = whiskeys.apply(lambda row: 1/row['cpg']/sum(1/whiskeys['cpg']), axis=1) 
whiskeys['rolls'] = '                '
whiskeys['roll_prob'] = 0

while len(pr) != 0:
    whiskeys['rem'] = whiskeys.apply(lambda row: row['rel_cpg']-row['roll_prob'], axis=1)
    whiskeys.sort_values('rem', ascending = False, inplace = True, ignore_index = True )
    index = np.argmin(abs(whiskeys['rem'][0]-pr))
    whiskeys.loc[0,'roll_prob']  += pr[index]
    whiskeys.loc[0,'rolls'] += str(outcomes[index]) + ', '
    pr =np.delete(pr,index)
    outcomes =np.delete(outcomes,index)

print(whiskeys)
    
    


