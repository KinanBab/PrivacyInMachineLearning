import sys
import json

from collections import OrderedDict

import noinfo
import guess
import math

from plot import MyDataPlot, MyLambdaPlot

# Possible parameters
experiments = [ 'noinfo', 'guess']
ns = [ 100, 500, 1000, 5000, 10000 ]

# Runs the mechanism and attack then compares the result for the given n
def Game(n, experiment='noinfo'):
  module = noinfo
  if experiment == 'guess':
    module = guess

  x, a = module.Mechanism(n)
  xHat = module.Attack(a)

  ham = sum([ 1.0 for i in range(len(x)) if x[i] != xHat[i] ])
  return ham / n

# Run the different games
if __name__ == '__main__':
  # Help
  if len(sys.argv) < 2 or sys.argv[1] == 'help':
    print 'Options: python experiment [<t>]'
    print 'Where:'
    print '<t>:\t\tis the number of times to repeat the experiement for a single set of parameters to compute average accuracy.'
    exit()

  T = 20
  if len(sys.argv) >= 2:
    T = int(sys.argv[1])

  # Run all experiments
  parameters = None
  parameters = [ (exp, n) for exp in experiments for n in ns ]

  # initialize result object object
  result = {exp: dict() for exp in experiments }
  output = {exp: dict() for exp in experiments }

  # run experiments
  i = 0
  for experiment, n in parameters:
    # Perform T Games and get the mean and average deviation
    allTrials = [ ]
    for t in range(T):
      print i, '/', len(parameters)*T
      i += 1 
      allTrials.append(Game(n, experiment))

    # Compute mean and average deviation
    mean = sum(allTrials) / T
    avgDev = sum([ abs(g - mean) for g in allTrials]) / T
    output[experiment][n] = [mean, avgDev]
    result[experiment][n] = mean

  # plot all n and sigma
  MyDataPlot(result, ['ham/n', 'n'], show=False, ctx=lambda plot: plot.title('Fraction of wrong bits vs size n (lower is better)'))
  MyLambdaPlot(lambda n: 0.333, ns, 'n/3', show=False)
  MyLambdaPlot(lambda n: 0.5, ns, 'n/2', show=True, ctx=lambda plot: plot.ylim(top=1, bottom=0))

  print '***DONE***'
  print ''
  print ''
  print ''
  print "# Values are 2-elements array: [mean, average deviation]"
  print json.dumps(output, indent=2, sort_keys=True)

  

