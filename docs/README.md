# Project Documentation

This directory contains a short description of the main components of the Vector Money Simulation.

## Agents

The simulation defines several economic actors using the [`mesa.Agent`](https://mesa.readthedocs.io/) base class:

- `Household` – accumulates income as wealth and chooses technologies.
- `Firm` – a basic production unit that consumes resources.
- `Government` – collects taxes and modifies resource stocks via policies.
- `FinancialIntermediary` – accrues interest on loans and deposits while affecting resource stocks.

## Bio-Physical Stocks

`BioPhysicalStocks` tracks quantities such as carbon budget, water, biomass and minerals. Each stock can be integrated with [`pysd`](https://github.com/SDXorg/pysd) if available, otherwise a minimal integrator is used.

## Markets

The ``Market`` class provides a simple trading system that links economic
agents with the bio-physical stocks.  Prices automatically adjust whenever a
stock falls below its ecological limit, modelling scarcity effects.

## Data

The ``data`` package loads input-output tables and ecological inventories using pandas.
It also provides ``normalise_per_capita`` to express indicators per person for
Doughnut Economics style analysis.

## Baseline Model

`BaselineModel` in ``src/models/baseline.py`` bundles agents, resource stocks
and the market into a single simulation class.  Default parameters imitate
late-20th-century global conditions.  The :py:meth:`run` method executes the
model for a given number of steps and returns a list of recorded stock levels.

