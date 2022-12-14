from sklearn import gaussian_process as gp
from scipy.stats import norm
import numpy as np

'''
This script runs the Bayesian Optimization within a class, with the 
main method being minimize(), from which all the other functions
are called. This script is called in porebo_plus.py.
'''

class BOMinimizer(object):
    def __init__(self, f, bounds, n_init, n_calls, n_sample=10000, sampler=None, noise=1e-3, kernel="Matern", acq="EI", num_pores = -1, porosity = -1, desired_kappa = 0):
        self.error_count = 0
        self.f = f
        self.num_pores = num_pores
        self.porosity = porosity
        self.bounds = bounds
        self.n_init = n_init
        self.n_calls = n_calls
        self.n_sample = n_sample
        low, high = zip(*self.bounds)
        if sampler is not None:
            self.sampler = sampler
        else:
            self.sampler = lambda n=1: np.random.uniform(low=low, high=high, size=(n, len(bounds)))
        self.acq = acq
        self.Xtrain = np.zeros((n_calls, len(bounds)))
        self.ytrain = np.zeros(n_calls)
        self.Xbest = None
        self.ybest = None
        self.n = 0
        self.kernel = gp.kernels.Matern()
        self.model = gp.GaussianProcessRegressor(kernel=self.kernel, normalize_y=True)
        self.desired_kappa = desired_kappa

    def observe(self, sample):
        '''
        Given a sample set of pore centers, adds the kappa value to the training's y-values
        and the set of centers to the training's x-values. Then, if the kappa value is at a
        minimum, highlight the pore arrangement as the best one.
        '''
        try:
            print('Observing the sample now')
            
            obj = self.f(sample, self.num_pores, self.porosity, desired_kappa = self.desired_kappa)
            self.Xtrain[self.n, :] = sample
            self.ytrain[self.n] = obj
            self.n += 1

            if self.ybest is None:
                self.ybest = obj
                self.Xbest = sample
            
            if obj < self.ybest:
                self.ybest = obj
                self.Xbest = sample

            print("Sample successfully observed")
        
        except RuntimeError as e:
            
            sample.append(self.porosity)
            np.savetxt("errors/error_" + str(self.error_count) + "_X.txt", sample)
            self.error_count += 1
            print("Sample failed to observe\nContinuing with next sample")
            pass

        return None

    def choose(self, X):
        '''
        A helper function for ask, this function finds the expected improvement
        for each set of pore centers and returns the greatest one
        '''
        if self.acq == "EI":
            mu, std = self.model.predict(X, return_std=True)
            Z = (self.ybest - mu) / (std + 1e-3)
            EI = (self.ybest - mu) * norm.cdf(Z) + std * norm.pdf(Z)
            EI = np.where(std != 0, EI, 0)
            idx = np.argmax(EI)
            try:
                idx = int(idx[0])
            except:
                idx = int(idx)
        else:
            raise ValueError("acquisition function must be one of {EI}")
        return idx

    def ask(self):
        '''
        Generates a sample list of sets of pore centers, then sees which one has the
        biggest expected improvement and returns that set of centers to apply f to.
        '''
        Xcand = self.sampler(self.num_pores, self.porosity, self.n_sample)
        idx = self.choose(Xcand)
        return Xcand[idx]

    def relearn(self):
        '''
        Generating a new set of functions that attempt to describe f
        '''
        print("fitting gpr...")
        self.model.fit(self.Xtrain[:self.n, :], self.ytrain[:self.n])

    def minimize(self):
        while self.n < self.n_init:
            self.observe(self.sampler(self.num_pores, self.porosity))
        self.relearn()
        while self.n < self.n_calls:
            cand = self.ask()
            print(f"evaluating X = {cand}...")
            self.observe(cand)
            self.relearn()
        return self.Xbest, self.ybest

