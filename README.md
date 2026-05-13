# dart-simulation

Given a model of how much your aim wobbles, where on a dartboard should you aim? This finds the answer by Monte Carlo'ing many darts around each candidate aim point, computing the expected score, then sweeping the board for the maximum.

Single Python file (`main.py`), run with `python main.py`. The [Overleaf write-up](https://www.overleaf.com/read/pxsnznvndnbp#a53d8f) has the full derivation and results.
