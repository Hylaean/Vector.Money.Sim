Project documentation.

## Markets

The ``Market`` class provides a simple trading system that links economic
agents with the bio-physical stocks.  Prices automatically adjust whenever a
stock falls below its ecological limit, modelling scarcity effects.

## Data

The ``data`` package loads input-output tables and ecological inventories using pandas.
It also provides ``normalise_per_capita`` to express indicators per person for
Doughnut Economics style analysis.
