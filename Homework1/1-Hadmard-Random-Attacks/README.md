# Hadamard and Random Query attacks

These experiments are setup such that some mechanism publishes averages about selected members of some (random) population/dataset of bits.
Each average corresponds to a query (a row in the matrix) that specifies which members to include in the average.
The two attacks relate to two kinds of queries: queries according to the hadamard matrix, and random queries.
Additionally, the mechanism adds normal noise centered around zero with deviation/scale sigma.

## Run
To run the experiments use
```
python experiment.py <attack> <t>
```

where attack is either 'hadamard' or 'random' according to the desired attack,
and t is the number of times to repeat a single experiment before taking the mean accuracy.

The experiement will produce plots showing the relationship between the size of the dataset n,
the number of queries m, and the standard deviation of the added normal noise sigma, against
the accuracy of the attack (fraction of incorrectly reconstructed bits)

To fine-tune the ranges of n, m, and sigma, modify the heading of experiement.py

## Output
In addition to the plots, the scripts will produce an JSON object on the form:

```json
{
 <n1>: {
  <m1>: {
    <sigma1>: [ <mean>, <average deviation> ],
    <sigma2>: [ <mean>, <average deviation> ],
    <sigma3>: [ <mean>, <average deviation> ]
    ...
  },
  <m2>: {
    <sigma1>: [ <mean>, <average deviation> ],
    <sigma2>: [ <mean>, <average deviation> ],
    <sigma3>: [ <mean>, <average deviation> ]
    ...
  },
  ...
 },
 ...
}

```

## Plots
Some plots are already available at ./plots. These plots show the accuracy (fraction of incorrectly reconstructed bits) 
as a function of n, m, and sigma. They compare the results achieved experimentally with theoretical bounds on the precision.
