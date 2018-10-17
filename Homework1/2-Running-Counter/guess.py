from random import randint, random

import noinfo

neg = lambda x: (x * -1) + 1
coin = lambda p, ch1, ch2: ch1 if random() < p else ch2

# Chooses uniform random binary n-vector x and returns 
#   x, (1/n)Hx + Y
# where:
#
# Y is n-vector with entries i.i.d from N(0, sigma^2)
# H is the n x n Hadamard matrix with entrie { -1, +1 }
#
# m is ignored here.
def Mechanism(n):
  x, a = noinfo.Mechanism(n)
  w = [ coin(2.0/3, xi, neg(xi)) for xi in x ]
  return x, (a, w)

# The Hadamard attack:
# Compute z = Ha and round each entry z_i to nearest 0 or 1 to estimate original x
def Attack(a):
  a, w = a
  
  xHat = noinfo.Attack(a)
  return xHat
