# dart-simulation

Monte Carlo simulation of where to aim on a dartboard given variation in your aim.

## Overview

Given a model of aim variance, this project answers: what's the highest-expected-value point to aim for on a standard dartboard? It computes the expected score at a candidate aim point by throwing many simulated darts around it, then sweeps the board to find the maximum. See the [Overleaf write-up](https://www.overleaf.com/read/pxsnznvndnbp#a53d8f) for the full derivation and results.

## Stack

- Python (single-file: `main.py`)

## Getting started

```bash
python main.py
```

## Links

- [Full write-up (Overleaf)](https://www.overleaf.com/read/pxsnznvndnbp#a53d8f)

## Status

Finished writeup.
