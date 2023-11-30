# useful_method_from_numpy.py

import numpy as np

x = np.array([[1, 2, 3, 4],
             [2, 3, 4, 5],
             [3, 4, 5, 6]])

print(x.shape) # (3, 4)
print(x.dtype) # int32
print(x.ndim) # 2
print(x.size) # 12

y = np.array([1,2,3])
print(y.ndim) # 1

z = np.array([[[1],[2]],[[11],[22]]])
print(z.ndim) # 3
