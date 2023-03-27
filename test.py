#!/usr/bin/python
import numpy as np

with np.load(file='default.npz', allow_pickle=True) as data:
    test_1 = data['FORWARD']
    # test_2 = data['BACKWORD']
    print(test_1.view())
    print(test_1[15, 0, 18])
    print(np.max(test_1))
