import numpy as np

qtable = np.ndarray(shape=(60, 36, 36, 21, 20), dtype=float)

for q in qtable:
    q = 0.1

print(qtable.nbytes)

x = input()
