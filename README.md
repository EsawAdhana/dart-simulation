# dart-simulation

Given a model of how much your aim wobbles, where on a dartboard should you aim? This finds the answer by Monte Carlo'ing many darts around each candidate aim point, computing the expected score, then sweeping the board for the maximum. There's a small Tkinter visualization as you go.

Single Python file: `main.py`. The [Overleaf write-up](https://www.overleaf.com/read/pxsnznvndnbp#a53d8f) has the full derivation and results.

## Setup

```bash
pip install numpy tqdm
python main.py
```

Tkinter ships with Python on macOS and Windows. On most Linux distros you'll need to install it separately (e.g. `sudo apt install python3-tk`).
