# data_shape.py

import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


# 1. data
a = np.array([1, 2, 3])
b = np.array([[1], [2], [3]])
c = np.array([[1, 2, 3]])
d = np.array([[1, 2],
              [3, 4],
              [5, 6]])
e = np.array([[1, 2, 3, 4],
             [11, 22, 33, 44],
             [111, 222, 333, 444]])
f = np.array([[[1, 2, 3],[4, 5, 6]],
              [[11, 22, 33],[44, 55, 66]],
              [[111, 222, 333],[444, 555, 666]]])
g = np.array([[[1, 2], [3, 4], [5, 6]],
             [[11, 22], [33, 44], [55, 66]]])
h = np.array([[[[1], [2], [3]],[[4], [5], [6]]],
              [[[11], [22], [33]],[[44], [55], [66]]]])
i = np.array([[[[1, 2], [3, 4], [5, 6], [7, 8]],
              [[11, 22], [33, 44], [55, 66], [77, 88]]],
              [[[1, 2], [3, 4], [5, 6], [7, 8]],
              [[11, 22], [33, 44], [55, 66], [77, 88]]]])
j = np.array([[[[1,2]]]])
# z = np.array([[1,2,3][4,5]]) # TypeError

print("a.shape: ", a.shape) # Vector: (3, )
print("b.shape: ", b.shape) # Metrix: (3, 1)
print("c.shape: ", c.shape) # Metirx: (1, 3)
print("d.shape: ", d.shape) # Metrix: (3, 2)
print("e.shape: ", e.shape) # Metrix: (3, 4)
print("f.shape: ", f.shape) # Tensor: (3, 2, 3)
print("g.shape: ", g.shape) # Tensor: (2, 3, 2)
print("h.shape: ", h.shape) # Tensor: (2, 2, 3, 1)
print("i.shape: ", i.shape) # Tensor: (2, 2, 4, 2)
print("j.shape: ", j.shape) # Tensor: (1, 1, 1, 2)
# print("z.shape: ", z.shape)



'''
# Result

a.shape:  (3,)
b.shape:  (3, 1)
c.shape:  (1, 3)
d.shape:  (3, 2)
e.shape:  (3, 4)
f.shape:  (3, 2, 3)
g.shape:  (2, 3, 2)
h.shape:  (2, 2, 3, 1)
i.shape:  (2, 2, 4, 2)
j.shape:  (1, 1, 1, 2)

'''

'''
x = [1. 2. 3]
x.shape #(3, ) = (Scalar, ): 스칼라 3개 → 벡터 1개 (출력이 ,로 끝남)

x = [[1], [2], [3]]
x.shape #(3, 1) = (Vector, Scalar): 벡터 3개, 스칼라 1개 → 행렬 1개

x = [[1,2,3]]
x.shape #(1, 3) = (Vector, Scalar): 벡터 1개, 스칼라 3개 → 행렬 1개

x = [[1,2][3,4]]
x.shape #(2, 2) = (Vector, Scalar): 벡터 1개, 스칼라 3개 → 행렬 1개

x = [[[1,2,3]]]
x.shape #(1, 1, 3) = (Metrix, Vector, Scalar): 행렬 1개, 벡터 1개, 스칼라 3개 → 텐서 1개

x = [[1,2,3], [4,5,6]]
x.shape #(2, 3) = (Vector, Scalar): 벡터 2개, 스칼라 3개 → 행렬 1개

x = [[[1], [2]]]
x.shape #(1, 2, 1) = (Metrix, Vector, Scalar): 행렬 1개, 벡터 2개, 스칼라 1개 → 텐서 1개

x = [[1,2,3], [4,5]]
x.shape #(2, 3) = (Vector, Scalar): 벡터 1개, 스칼라 2개 && 벡터 1개, 스칼라 3개  → 행렬 1개

shape: tensor2 ,tensor1, matrix, vector, scalar
→ 최종 도출되는 차원은 1개일 것이므로 출력이 생략 됨
'''
