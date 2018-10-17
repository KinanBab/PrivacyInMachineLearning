from random import randint

from math import sqrt
import numpy as np
import scipy.linalg

from helpers import MyRound

# Chooses uniform random binary n-vector x and returns 
#   x, (1/n)Hx + Y
# where:
#
# Y is n-vector with entries i.i.d from N(0, sigma^2)
# H is the n x n Hadamard matrix with entrie { -1, +1 }
#
# m is ignored here.
def Mechanism(n, m, sigma):
  x = np.array([ randint(0,1) for i in range(0, n) ])
  Y = np.random.normal(0, sigma, n)

  # Hadamard matrix with entries in {1, -1}
  H = scipy.linalg.hadamard(n)
    
  # (1/n)Hx + y
  a = (1.0/n) * H.dot(x) + Y  
  return x, a


# The Hadamard attack:
# Compute z = Ha and round each entry z_i to nearest 0 or 1 to estimate original x
def Attack(a):
  n = a.shape[0]
  H = scipy.linalg.hadamard(n)
  z = H.dot(a)
  return [ MyRound(x) for x in z ]
