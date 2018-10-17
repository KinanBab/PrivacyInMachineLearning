from random import randint, random

import numpy as np
#import scipy.linalg

from helpers import MyRound

# Chooses uniform random binary n-vector x and returns 
#   x, (1/n)Hx + Y
# where:
#
# Y is n-vector with entries i.i.d from N(0, sigma^2)
# H is the n x n Hadamard matrix with entrie { -1, +1 }
#
# m is ignored here.
def Mechanism(n):
  x = np.array([ randint(0,1) for i in range(0, n) ])
  Z = np.array([ randint(0,1) for i in range(0, n) ])

  # accum is the partial sum array starting with 0 up to the current step of reduce
  a = reduce(lambda accum, x: accum + [ accum[-1] + x ], x, [0])
  a.pop(0)
  a = np.array(a)
  a = a + Z

  return x, a

# The Hadamard attack:
# Compute z = Ha and round each entry z_i to nearest 0 or 1 to estimate original x
def Attack(a):
  n = len(a)
  a = reduce(lambda accum, x: accum + [ accum[-1] + x ], a, [0]) # prefix sum of everything with noise
  a = [ a[i] - (i+1)/2.0 for i in range(len(a)) ] # remove expected noise
  a.pop(0)

  # every element in the array i looks like this:
  #   a[i] = SUM_{j=0}^{i} (i-j+1)*x[j] (i included in the sum)
  #
  # e.g:
  #   a[0] = x[0] = (0 - 0 + 1) x[0]
  #   a[1] = x[0] + (x[0]+x[1]) = 2*x[0] + x[1]
  #   a[2] = x[0] + (x[0]+x[1]) + (x[0]+x[1]+x[2]) = 3*x[0] + 2*x[1] + x[2]
  #   ...
  #
  # so we have something like this:
  #                               Ax = a
  # where A =
  # [ [ 1, 0, ...., 0 ],
  #   [ 2, 1, ...., 0 ],
  #   [ 3, 2, 1, ., 0 ],
  #   ...
  # ]
  #
  # This is already a lower triangular matrix, solving this system is very easy.
  # I wont use scipy.linalg.solve_triangular because although it is faster 
  # it still takes far more time to allocate memory and fill in A extra
  # Instead I will write my own optimized in-place solver, that does not need a matrix
  #
  for i in range(len(a)-1, 0, -1):
    a[i] = a[i] - a[i-1]

  # A = [ [ 1 if c <= r else 0 for c in range(n) ] for r in range(n) ]  
  # xHat = scipy.linalg.solve_triangular(A, a, lower=True, overwrite_b=True)

  runningSum = 0
  xHat = []
  for ai in a:
    xHat.append(ai - runningSum)
    runningSum += xHat[-1]

  return [ MyRound(xi) for xi in xHat ]
