import sys
import json

from collections import OrderedDict

import hadamard
import randomQuery
import math

# Possible parameters
ns = [ 128, 512, 2048, 8192 ]

def ms(n, experiment):
  if experiment == 'hadamard':
    return [ n ]
  return [ m * n for m in [ 1.1, 4.0, 16.0 ] ]

def sigmas(n, experiment):
  max = int(math.log(math.sqrt(32*n), 2.0))
  return [ 1.0/(2**p) for p in range(1, max + 1) ] # max is included


# Runs the mechanism and attack then compares the result for
# different n, sigma, and m.
def Game(n, m, sigma, experiment='hadamard'):
  module = hadamard
  if experiment == 'random':
    module = randomQuery

  x, a = module.Mechanism(n, m, sigma)
  xHat = module.Attack(a)

  ham = sum([ 1.0 for i in range(len(x)) if x[i] != xHat[i] ])
  return ham / n

# Run the different games
if __name__ == '__main__':
  # Help
  if len(sys.argv) < 2 or sys.argv[1] == 'help':
    print 'Options:'
    print '\tHadamard [ t ]- for the Hadamard attack'
    print '\tRandom [ t ]- for the Random query attack'
    print '\tHelp - to see this message'
    print 'in both commands above, t is the number of times to repeat the experiement for a single set of parameters to compute average accuracy.'
    exit()
    
  T = 20
  if len(sys.argv) >= 3:
    T = int(sys.argv[2])

  # Which experiment was chosen
  experiment = sys.argv[1].lower()
  
  # Run all experiments
  parameters = None
  parameters = [ (n, m, sigma) for n in ns for m in ms(n, experiment) for sigma in sigmas(n, experiment) ]

  # initialize result object object
  result = {n: {m: dict() for m in ms(n, experiment) } for n in ns}  

  # run experiments
  visited = set()
  for n, m, sigma in parameters:
    if (n, m) in visited:
      continue

    result[n][m][sigma] = sum( [ Game(n, m, sigma, experiment) for t in range(T) ]) / T
    if result[n][m][sigma] == 0:
      visited.add( (n, m) )

  # minor clean up result
  if experiment == 'hadamard':
    result = { n: result[n][n] for n in ns }
    
  print json.dumps(result, indent=2, sort_keys=True)
  

