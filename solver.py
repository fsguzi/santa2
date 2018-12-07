import pandas as pd
import numpy as np
import time

import common 

class two_reverse:
    
    @classmethod
    def solve(cls, nodes, solution, prime, prime_set, run_through=None, max_iter=5, start_at=1):
        solution = solution.copy()
        start = time.time()
        
        i=1
        if run_through == None:
            run_through = len(nodes)-1
        
        asd = nodes[solution]
        df = pd.DataFrame(asd)
        df.to_csv('asd.csv')
        solution_nodes = pd.read_csv('asd.csv').iloc[:,1:].values
        
        cls.nodes = nodes
        cls.solution = solution
        cls.prime = prime
        cls.prime_set = prime_set
        cls.solution_nodes = solution_nodes
        
        while i <= max_iter:
            print('Start iteration %s'%i)
            
            iter_start = time.time()
            best = []
            did = 0

            reverse_dist, old_dist, roller = cls.calc_basis(start_at)
            left = 1
            #for left in range(start_at, run_through):
            while left>=1 and left<run_through:
                node_before_a, node_a = solution[left-1:left+1]
                
                middle, reverse_dist = cls.calc_middle(reverse_dist, left)
                to_d, from_a, roller =  cls.calc_connector(roller, left, node_before_a, node_a)
                place, saving, old_dist = cls.calc_save(from_a,to_d,middle,old_dist)

                if saving<0:
                    best.append(saving)
                    did += saving
                    target = place+1+left

                    #execute swap
                    cls.excute_swap(left,place)
                    print('a: %s | saving: %.3f | cumsave: %.3f'%(left, saving, did))

                    #reset infos
                    #reverse_dist, old_dist, roller = cls.calc_basis(left+1)
                    reverse_dist, old_dist, roller = cls.calc_basis(left)
                    left-=1
                left += 1
            print('iter %s done, total swap %s, saves %.3f, time %.1f'%(i,len(best),did,time.time()-iter_start))
            print(common.score(nodes,solution,prime).sum())
            print('####################################')
            i+=1
            if len(best) == 0:
                print('zero')
                break
        return solution
    
    @classmethod
    def calc_reverse(cls,left):
        r_solution = cls.solution[left:-1][::-1]
        reverse_dist = []
        for offset in range(10):
            reverse_dist.append(np.cumsum(common.score(cls.nodes,r_solution,cls.prime,offset)[::-1])[::-1])
        reverse_dist = np.array(reverse_dist)
        return reverse_dist
    
    @classmethod
    def calc_old_dist(cls, from_node):
        offset = from_node%10
        return np.cumsum(common.score(cls.nodes, cls.solution[from_node:],cls.prime, offset=offset))
    
    @classmethod
    def calc_middle(cls, reverse_dist, left):
        middle = np.zeros(shape=(reverse_dist.shape[1]))
        offset = left%10

        for o in range(10):
            order = (offset-o)%10
            using_reverse = reverse_dist[order]
            middle[o::10] = using_reverse[o::10]

        reverse_dist[:,:-1] -= reverse_dist[:,-1:]
        reverse_dist = reverse_dist[:,:-1]
        return middle[::-1], reverse_dist
    
    @classmethod
    def calc_connector(cls, roller, left, node_before_a, node_a):
        to_d = roller[:-1].copy()
        offset = left%10
        if node_before_a not in cls.prime_set and offset == 0:
            to_d *= 1.1

        roller = common.distance(cls.nodes[node_a], cls.solution_nodes[left+2:])
        if node_a in cls.prime_set:
            return to_d, roller, roller  
        else:
            start_leg = (10-left-2)%10
            from_a = roller.copy()
            from_a[start_leg::10] *= 1.1
            return to_d, from_a, roller
    
    @classmethod
    def calc_save(cls, from_a,to_d,middle,old_dist):
        save = from_a+to_d-old_dist[2:]+middle
        old_dist[1:] -= old_dist[0]
        old_dist = old_dist[1:]

        place = np.argmin(save)
        saving = save[place]
        return place, saving, old_dist
    
    @classmethod
    def calc_basis(cls, start_at):
        reverse_dist = cls.calc_reverse(start_at)
        old_dist = cls.calc_old_dist(from_node=start_at-1)
        roller = common.distance(cls.nodes[cls.solution[start_at-1]], cls.solution_nodes[start_at-1+2:])

        return reverse_dist, old_dist, roller
    
    @classmethod
    def excute_swap(cls,left,place):
        target = place+1+left
        cls.solution[left:target+1] = cls.solution[target:left-1:-1]
        cls.solution_nodes[left:target+1] = cls.solution_nodes[target:left-1:-1]
