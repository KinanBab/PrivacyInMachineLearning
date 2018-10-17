from random import randint

from math import sqrt
import numpy as np
import numpy.linalg

from helpers import MyRound

# Chooses uniform random binary n-vector x and returns 
#   x, ((1/n)Bx + Y, B)
# where:
#
# entries of Y are iid from N(0, sigma^2)
# B is a random uniform binary matrix of dimensions m x n
def Mechanism(n, m, sigma):
  x = np.array([ randint(0,1) for i in range(0, n) ])
  Y = np.random.normal(0, sigma, int(m))

  # Uniform binary matrix of dimensions m x n
  B = np.matrix([ [ randint(0,1) for i in range(0, n) ] for i in range(0, int(m)) ])

  # (1/n)Bx + y
  a = (1.0/n) * B.dot(x) + Y
  return x, (a, B)

# The Random Query Attack:
# Compute argmin over random B and all vectors y using least squares
# and then round each resulting entries to nearest 0 or 1 to get estimate on x.
def Attack(inp):
  a, B = inp
  n = B.shape[1]

  x = numpy.linalg.lstsq((1.0/n)*B, np.transpose(a), rcond=None)[0]
  return [ MyRound(xi) for xi in x ]
