"""
Class for doing model selection for BNMTF, maximising the BIC, AIC, or log likelihood.
Instead of trying an entire grid, we do an optimised search:
- Say we just tried values K,L.
- Let K' and L' be the next values in our grid.
- We then try a model with K,L', another with K',L, and a final one with K',L'.
- We update our values to the best of these two models - or if they are worse
  than K,L, we terminate and say K,L is the best.

We expect the following arguments:
- values_K      - a list of values for K
- values_L      - a list of values for L
- R             - the dataset
- M             - the mask matrix
- prior         - the prior values for BNMF. This should be a dictionary of the form:
                    { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF, 'lambdaS':lambdaS, 'lambdaG':lambdaG }
                  where lambdaF, lambdaS, and lambdaG are a single value.
- initFG        - the initialisation of F and G - 'kmeans', 'exp' or 'random'
- initS        - the initialisation of S - 'exp' or 'random'
- iterations    - number of iterations to run 

The greedy grid search can be started by running search(search_metric), where 
we stop searching after our specified metric's performance drops.

After that, the values for each metric ('BIC','AIC','loglikelihood') can be
obtained using all_values(metric), and the best value of K and L can be 
returned using best_value(metric).

all_values(metric) returns a list of tuples detailing the performances: (K,L,metric).

We use the optimised Variational Bayes algorithm for BNMTF.
"""

project_location = "/home/tab43/Documents/Projects/libraries/"
import sys
sys.path.append(project_location)

from BNMTF.code.bnmtf_vb_optimised import bnmtf_vb_optimised
import numpy

metrics = ['BIC','AIC','loglikelihood','MSE']

class GreedySearch:
    def __init__(self,values_K,values_L,R,M,priors,initS,initFG,iterations):
        self.values_K = values_K
        self.values_L = values_L
        self.R = R
        self.M = M
        (self.I,self.J) = self.R.shape
        self.priors = priors
        self.initS = initS
        self.initFG = initFG
        self.iterations = iterations
        
        self.all_performances = {
            metric : []
            for metric in metrics
        }
    
    
    def search(self,search_metric):
        assert search_metric in metrics, "Unrecognised metric name: %s." % search_metric    
        
        def try_KL(K,L):
            # First see if we already tried this combination     
            existing = self.find_KL(search_metric,K,L)
            if existing:
                print "Running line search for BNMF. Already tried K = %s, L = %s." % (K,L)         
                return existing[0][2]
            
            # Otherwise, we try it
            print "Running line search for BNMF. Trying K = %s, L = %s." % (K,L)
            
            priors = self.priors.copy()
            priors['lambdaF'] = self.priors['lambdaF']*numpy.ones((self.I,K))
            priors['lambdaS'] = self.priors['lambdaS']*numpy.ones((K,L))
            priors['lambdaG'] = self.priors['lambdaG']*numpy.ones((self.J,L))
            
            BNMF = bnmtf_vb_optimised(self.R,self.M,K,L,priors)
            BNMF.initialise(init_S=self.initS,init_FG=self.initFG)
            BNMF.run(iterations=self.iterations)
            
            for metric in metrics:
                quality = BNMF.quality(metric)
                self.all_performances[metric].append((K,L,quality))
            return self.all_performances[search_metric][-1][2] # return the quality of the last appended value
            
        # Get the initial starting point
        ik, il = 0, 0 #current indices for values of K and L
        current_K, current_L = self.values_K[ik], self.values_L[il]
        performance_so_far = try_KL(current_K,current_L)
        
        while ik < len(self.values_K)-1 and il < len(self.values_L)-1: 
            print "Currently at K = %s, L = %s." % (current_K,current_L)
            new_K, new_L = self.values_K[ik+1], self.values_L[il+1]
            performance_new_K = try_KL(new_K,current_L)
            performance_new_L = try_KL(current_K,new_L)
            performance_new_KL = try_KL(new_K,new_L)
            
            if performance_so_far > max(performance_new_K,performance_new_L,performance_new_KL):
                break
            else:
                if performance_new_K > performance_new_L and performance_new_K > performance_new_KL:
                    print "(%s,%s) -> (%s,%s)" % (current_K,current_L,new_K,current_L)
                    ik += 1
                    current_K = new_K
                    performance_so_far = performance_new_K
                elif performance_new_L > performance_new_KL:
                    print "(%s,%s) -> (%s,%s)" % (current_K,current_L,current_K,new_L)
                    il += 1
                    current_L = new_L
                    performance_so_far = performance_new_L
                else:
                    print "(%s,%s) -> (%s,%s)" % (current_K,current_L,new_K,new_L)
                    ik += 1
                    il += 1
                    current_K,current_L = new_K,new_L
                    performance_so_far = performance_new_KL
        
        # If we reached the edge of the grid (so ik == len(self.values_K)-1 or 
        # il == len(self.values_L)-1) we keep the search going in the L or K direction (resp)
        if ik == len(self.values_K)-1:
            while il < len(self.values_L)-1:
                print "Currently at K = %s, L = %s." % (current_K,current_L)
                new_L = self.values_L[il+1]
                performance_new_L = try_KL(current_K,new_L)
                if performance_so_far > performance_new_L:
                    break
                else:
                    print "(%s,%s) -> (%s,%s)" % (current_K,current_L,current_K,new_L)
                    il += 1
                    current_L = new_L
                    performance_so_far = performance_new_L
                    
        elif il == len(self.values_L)-1:
            while ik < len(self.values_K)-1:
                print "Currently at K = %s, L = %s." % (current_K,current_L)
                new_K = self.values_K[ik+1]
                performance_new_K = try_KL(new_K,current_L)
                if performance_so_far > performance_new_K:
                    break
                else:
                    print "(%s,%s) -> (%s,%s)" % (current_K,current_L,new_K,current_L)
                    ik += 1
                    current_K = new_K     
                    performance_so_far = performance_new_L
                
        print "Finished running line search for BNMF."
    
    
    def all_values(self,metric):
        assert metric in metrics, "Unrecognised metric name: %s." % metric
        return self.all_performances[metric]
        
    
    def find_KL(self,metric,K,L):
        # See if we have already tried this K and L - if so, return the performance
        return filter(lambda x: (x[0],x[1]) == (K,L), self.all_values(metric))
    
    
    def best_value(self,metric):
        assert metric in metrics, "Unrecognised metric name: %s." % metric
        performances_metric = self.all_performances[metric] # This is a list of (K,L,metric) tuples
        (best_K,best_L,best_metric) = max(performances_metric,key=lambda x: x[2])
        return (best_K,best_L)