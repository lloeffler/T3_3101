#!/usr/bin/python
import numpy as np
test_1 = np.empty(shape=1)
test_2 = np.empty(shape=1)
# To test other qtables, replace 'default' with the name of the file or entered in the application.
with np.load(file='default.npz', allow_pickle=True) as data:
    try:
        test_1 = data['FORWARD']
    except:
        print('FORWARD not found')
    try:
        test_2 = data['BACKWORD']
    except:
        print('BACKWARD not found')

    try:
        print('forward:')
        print(test_1[15, 0, 18])
        print(np.max(test_1))
        print('backward:')
        print(test_2[15, 0, 18])
        print(np.max(test_2))
    except Exception as exception:
        print(exception)
