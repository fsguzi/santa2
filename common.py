import pandas as pd
import numpy as np
from sympy import sieve
import time

import solver 

def score(nodes,solution,prime,offset=0,raw=False):
    s = nodes[solution[:-1]]
    e = nodes[solution[1:]]
    out = distance(s,e)
    n = len(s)
    if raw:
        return out
    isten = (np.arange(n)+1+offset)%10==0
    notprime = ~np.isin(solution[:-1],prime)
    isextra = (isten&notprime)*0.1
    out += out*isextra
    return out

def score_(**args):
    return score(**args).sum()

def distance(coor1,coor2):
    return np.sqrt(((coor1-coor2)**2).sum(axis=-1))

class problem:
    def __init__(self, instance_path = './problem/cities.csv', base_path = './solution/base.csv'):
        self.nodes = pd.read_csv(instance_path).iloc[:,1:].values
        self.n = n = len(self.nodes)
        if base_path:
            self.base = pd.read_csv(base_path).values[:,0]
            
        prime_ = sieve.primerange(0,n)
        self.prime = list(prime_)
        prime_ = sieve.primerange(0,n)
        self.prime_set = set(prime_)
    
    def solve(self, *args, **kwargs,):
        self.solution = solver.two_reverse.solve(self.nodes, self.base, self.prime, self.prime_set, *args, **kwargs)
        print(self.score(self.solution))
        
    def score(self, solution, **kwargs):
        return score_(nodes = self.nodes, solution=solution, prime=self.prime,**kwargs)