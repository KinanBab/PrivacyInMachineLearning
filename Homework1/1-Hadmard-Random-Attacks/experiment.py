import sys
import json

from collections import OrderedDict

import hadamard
import randomQuery
import math

from plot import MyDataPlot, MyLambdaPlot

# Possible parameters
ns = [ 128, 512, 2048, 8192 ]

def ms(n, experiment):
  if experiment == 'hadamard':
    return [ n ]
  if n < 2048:
    return [ int(m * n) for m in [ 1.1, 4.0, 16.0 ] ]
  elif n < 8192:
    return [ int(m * n) for m in [ 1.1, 4.0 ] ]
  else:
    return [ int(m * n) for m in [ 1.1 ] ]

def sigmas(n, experiment):
  max = int(math.log(math.sqrt(32*n), 2.0))
  return [ 1.0/(2**p) for p in range(2, max + 1) ] # max is included


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
    print 'Options: python experiment <command> [<t>]'
    print 'Where:'
    print '<command>:\tHadamard - for the Hadamard attack'
    print '\t\tRandom - for the Random query attack'
    print '\t\tHelp - to see this message'
    print ''
    print '<t>:\t\tis the number of times to repeat the experiement for a single set of parameters to compute average accuracy.'
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
  output = {n: {m: dict() for m in ms(n, experiment) } for n in ns}  

  # run experiments
  visited = set()
  i = 0
  for n, m, sigma in parameters:
    # progress
    print i, '/', len(parameters)
    i += 1

    # when things reach 0, stop decreasing sigma
    if (n, m) in visited:
      continue

    # Perform T Games and get the mean and average deviation
    allTrials = [ Game(n, m, sigma, experiment) for t in range(T) ]
    mean = sum(allTrials) / T
    avgDev = sum([ abs(g - mean) for g in allTrials]) / T
    output[n][m][sigma] = [mean, avgDev]
    result[n][m][sigma] = mean
    if result[n][m][sigma] == 0:
      visited.add( (n, m) )

  # minor clean up result
  if experiment == 'hadamard':
    result = { n: result[n][n] for n in ns } 

    # plot all n and sigma
    MyDataPlot(result, ['n', 'ham/n', 'sigma'], show=True, ctx=lambda plot: plot.title('Fraction of wrong bits vs size (n) and sigma'))

    # plot for single n against bound
    ctx = lambda plot: [ plot.ylim(top=10, bottom=0), plot.title('Bound on Error vs Actual Error') ]
    for n in ns:
      MyLambdaPlot(lambda sigma: 4*sigma*sigma*n, [ i/100.0 for i in range(int(min(result[n].keys())*100), 51, 2)], 'error bound', show=False, ctx=ctx)
      MyDataPlot({ n: result[n] }, [ 'n', 'ham/n', 'sigma' ], show=True)

  else:
    for n in ns:
      MyDataPlot(result[n], ['m', 'ham/n', 'sigma'], show=True, ctx=lambda plot: plot.title('N = ' + str(n)))

  print '***DONE***'
  print ''
  print ''
  print ''
  print "# Values are 2-elements array: [mean, average deviation]"
  print json.dumps(output, indent=2, sort_keys=True)

  

