import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("Testing numpy, pandas, matplotlib...")
x = np.linspace(0, 10, 100)
y = 2.5 * x + np.random.normal(0, 1, 100)

# Linear Regression via numpy lstsq
A = np.vstack([x, np.ones(len(x))]).T
m, c = np.linalg.lstsq(A, y, rcond=None)[0]

print(f"Fit result: slope={m:.4f}, intercept={c:.4f}")
