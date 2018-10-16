import sys
import json
from random import randint

from math import sqrt
import numpy as np
import scipy.linalg

from collections import OrderedDict

# Possible parameters
ns = [ 128, 512, 2048, 8192 ]
def ms(n):
  ms = [ 1.1, 4.0, 16.0 ]
  return [ m * n for m in ms ]
def sigmas(n):
  p = 1
  sigma = 0.5**p
  sigmas = []
  while sigma >= 1.0/sqrt(32*n):
    sigmas.append(sigma)
    p += 1
    sigma = 0.5**p
  return sigmas


# Helper: round to 0 or 1
def MyRound(x):
  if x < 0: return 0
  if x > 1: return 1
  return round(x)

# Chooses uniform random x and gaussian Y and releases
# a = 1/n Ax + Y where entries of Y are iid from N(0, sigma^2)
# A is either H: the n x n Hadamard matrix with entire { -1, +1 }
# or B: a random uniform binary matrix of dimensions m x n
# depending on the attack
# m is ignored if attack is Hadamard, otherwise serves
# as the number of rows in A.
def Mechanism(attack, n, sigma, m):
  x = np.array([ randint(0,1) for i in range(0, n) ])
  Y = np.random.normal(0, sigma, n)

  # Our matrix depending on the attack
  B = None
  if attack == 'Hadamard':
    B = scipy.linalg.hadamard(n)
    
  # 1/n * Hx + Y
  a = (1.0/n) * B.dot(x) + Y  
  return x, a

# The Hadamard attack:
# Compute Ha and round to estimate original x
def HadamardAttack(a):
  n = len(a)
  H = scipy.linalg.hadamard(n)
  z = H.dot(a)
  return [ MyRound(x) for x in z ]

# The Random Query Attack:
# Compute argmin over random B and all vectors y using least squares
# and then round to get estimate on x.
def randomQueryAttack():
  return [ 0, 0, 0 ]

# Runs the mechanism and attack then compares the result for
# different n, sigma, and m.
def Game(attack, n, sigma, m):
  x, a = Mechanism(attack, n, sigma, m)
  xHat = None
  if attack == 'Hadamard':
    xHat = HadamardAttack(a)
  else:
    xHat = RandomQueryAttack(a)
  
  count = 0.0
  for i in range(len(x)):
    if x[i] != xHat[i]:
      count += 1

  return count / n

# Run the different games
if __name__ == '__main__':
  attack = 'Hadamard' if len(sys.argv) < 2 else sys.argv[1]
  
  result = dict()
  for n in ns:
    result[n] = dict()
    if attack == "Hadamard":
      for sigma in sigmas(n):
        result[n][sigma] = Game(attack, n, sigma, n)
        if result[n][sigma] == 0:
            break
    else:
      for m in ms(n):
        result[n][m] = dict()
        for sigma in sigmas(n):
          result[n][m][sigma] = Game(attack, n, sigma, m)
          if result[n][m][sigma] == 0:
            break
    
  print json.dumps(result, indent=2, sort_keys=True)
  
  
