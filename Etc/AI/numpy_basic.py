# numpy_basic.py

import numpy as np


# 1차원 배열
vec = np.array([1, 2, 3, 4, 5])
print(vec) # [1 2 3 4 5]

# 2차원 배열
mat = np.array([[10, 20, 30], [60, 70, 80]]) 
print(mat) # [[10 20 30] [60 70 80]]

# np.arange(i, j, k): i부터 j-1까지 k씩 증가하는 배열 생성
n = 2
range_n_step_vec = np.arange(1, 10, n)
print(range_n_step_vec) # [1 3 5 7 9]

# np.reshape(): 내부 데이터 변경없이 배열의 구조 변경
originshape_mat = np.array(np.arange(30))
print(originshape_mat) # [0 1 2 ... 28 29]
reshape_mat = np.array(np.arange(30)).reshape((5,6))
print(reshape_mat)
'''
[[ 0  1  2  3  4  5]
 [ 6  7  8  9 10 11]
 [12 13 14 15 16 17]
 [18 19 20 21 22 23]
 [24 25 26 27 28 29]]
'''

# numpy slicing
mat2 = np.array([[1, 2, 3], [4, 5, 6]])
print(mat2) # [[1, 2, 3] [4, 5, 6]]
# 첫번째 행 출력
slicing_mat = mat[0, :]
print(slicing_mat) # [1 2 3]
# 두번째 열 출력
slicing_mat = mat[:, 1]
print(slicing_mat) # [2 5]

# numpy indexing
mat3 = np.array([[1, 2], [4, 5], [7, 8]])
print(mat3) # [[1, 2] [4, 5] [7, 8]]
# 특정 위치 원소 1개 반환
print(mat3[1, 0]) # 4
# 특정 위치 원소 2개 반환 -> 배열 생성
indexing_mat = mat3[[2, 1],[0, 1]] # mat3[[2행, 1행], [0열, 1열]]
print(indexing_mat) # [7 5]
