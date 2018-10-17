# if this import gives issues install python-tk
# sudo apt-get install python-tk
import matplotlib.pyplot as pyplot

''' Get a unique color everytime '''
colorIndex = 0
colors = [ 'r', 'g', 'b', 'k', 'y', 'c', 'm' ]
def newColor(reset=False):
  global colorIndex, colors
  
  if reset:
    colorIndex = 0
    return

  c = colors[colorIndex]
  colorIndex = min(colorIndex + 1, len(colors) - 1)
  return c


''' Get number of layers in an object '''
def depth(obj):
  if isinstance(obj, dict):
    m = 0
    for key in obj:
      m = max(m, depth(obj[key]) + 1)
    return m
  return 0

'''
transform given dict to a list of tuples (keys, val) such that data[key[0]][key[1]]... = val
'''
def expand(data, height, accum=[]):
  if height == 1:
    results = []
    for key in data:
      results.append( (accum + [key], data[key]) )
    return results

  results = []
  for key in data:
    results += expand(data[key], height-1, accum+[key])
  return results
  
'''
  put d at data[keys[0]][keys[1]]...
  make sure that data[keys[0]]..[keys[i]] is initialzed before to avoid assigns values to None
'''
def create_and_assign_dicts(data, keys, d):
  if len(keys) == 1:
    data[keys[0]] = d
    return

  if keys[0] not in data:
    data[keys[0]] = dict()
  create_and_assign_dicts(data[keys[0]], keys[1:], d)

'''
We are given some multi level JSON like object/dict, where currentOrder labels each level with a label class
We want to switch the ordering of these levels so that they follow the ordering at desired order

E.g.:  
calling transform on the following object and currentOrder, desiredOrder = ['k', 'x'], ['x', 'k']:
{
  "k1": {
    "x1": "<obj1>",
    "x2": "<obj2>"
  },
  "k2": {
    "x1": "<obj3>",
    "x2": "<obj4>"
  }
  ...
}
Should return:
{
  "x1": {
    "k1": "<obj1>".
    "k2": "<obj3>"
    ...
  },
  "x2": {
    "k1": "<obj2>",
    "k2": "<obj4>"
    ...
  }
}
'''
def transform(data, desiredOrder=None):
  if desiredOrder == None:
    return data, depth(data)

  
  desiredOrder = [ o - 1 for o in desiredOrder ]
  results = expand(data, len(desiredOrder))
  
  if len(results) == 0:
    return {}

  data = {}
  for keys, d in results:
    create_and_assign_dicts(data, [ keys[i] for i in desiredOrder ], d)

  return data, len(results[0][0])

'''
Plot values provided in data: data is a multi layered dict
Each layer represents a parameter/axis, with the layer before last is the x-axis
and the last layer (i.e. end values) being the y axis. 
Higher layers are used to plot attached data as a seperate function with a label reflecting the layer

for example:
{
  'f1': {
    x1: y1,
    x2: y2'
  },
  'f2': {
    x1: y3,
    x2: y4
  }
}

will plot to functions, f1 and f2 such that f1 passes through (x1, y1), (x2, y2) and f2 passes through (x1, y3), (x2, y4).
In case more level are provided (imagine the above object is located within some other object at key 'g1'), then the function name
become the concatenation of the key with all its parents (e.g. g1:f1 and g1:f2)

In the case where data is available with a different layering order than desired, an order parameter can be provided containing a list
of labels, such that if order=[1, 3, 2] it means that we would like level number 1 to appear first, then 3, then 2.

labelsPerLevel allows control over all the labels, the last two labels in this list are the x and y axis labels displayed in the plot,
the other labels are used in the legend in the plotted function name to better display the concatenation: (e.g. assume the first two 
non-axis labels are 'n','m', and that we have two functions: 1:1, 10:100, then the function labels will show as n=1,m=1 and n=10,m=100 
in the legend)

ctx is a function that takes one input which is the pyplot object, this allows users to perform some custom formatting and such on pyplot
'''
def MyDataPlot(data, labelsPerLevel, order=None, show=True, ctx=None):
  if len(labelsPerLevel) == 0:
    labelsPerLevel = ['x', 'y']
  elif len(labelsPerLevel) == 0:
    labelsPerLevel = [ 'x' ] + labelsPerLevel

  data, depth = transform(data, order)

  # if depth > 1, it means we have (potentially several) level of function labels
  results = [ ([], data) ]
  if depth > 1:
    results = expand(data, depth-1)

  pyplot.xlabel(labelsPerLevel[-1])  
  pyplot.ylabel(labelsPerLevel[-2])


  for labels, data in results:
    lenDiff = len(labels) - (len(labelsPerLevel) - 2)
    concat = lambda i: str(labelsPerLevel[i - lenDiff])+'='+str(labels[i])
    concatIfLabel = lambda i: concat(i) if i >= lenDiff else labels[i]

    label = ','.join([ concatIfLabel(i) for i in range(len(labels)) ])
    color = newColor()

    Xs = sorted(list(data.keys()))
    pyplot.plot(Xs, [ data[x] for x in Xs ], '-o'+color, label=label)

  if ctx is not None:
    ctx(pyplot)

  if show:
    pyplot.legend()
    pyplot.show()
    newColor(reset=True)

def MyLambdaPlot(f, xs, label, show=True, ctx=None):
  color = newColor()
  ys = [ f(x) for x in xs ]
  pyplot.plot(xs, ys, '-'+color, label=label)
  
  if ctx is not None:
    ctx(pyplot)

  if show:
    pyplot.legend()
    pyplot.show()
    newColor(reset=True)
    

if __name__ == '__main__':  
  # Transform
  obj = {
    "k1": {
      "x1": "<obj1>",
      "x2": "<obj2>"
    },
    "k2": {
      "x1": "<obj3>",
      "x2": "<obj4>"
    } 
  }
  print 'Test transform: '
  print transform (obj, [2, 1])
  # End of Transform
  
  # Depth
  print 'Test depth: '
  print depth(obj), 2
  # End of Depth
  
  # create_and_assign_dicts
  obj = {}
  create_and_assign_dicts(obj, ['k1', 'x1'], 'v1')
  create_and_assign_dicts(obj, ['k1', 'x2'], 'v2')
  create_and_assign_dicts(obj, ['k2', 'x1'], 'v3')
  create_and_assign_dicts(obj, ['k2', 'x2'], 'v4')
  print 'Test create_and_assign_dicts: '
  print obj
  
  





