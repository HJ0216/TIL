# missing_value_handling.py

import pandas as pd

dataset = pd.DataFrame([
    {'id': 1, 'val': None, 'pw': 2},
    {'id': 2, 'val': 21, 'pw': 3},
    {'id': 3, 'val': 19, 'pw': 0},
    {'id': 4, 'val': 24, 'pw': 1},
    {'id': None, 'val': 15, 'pw': 2},
    {'id': 5, 'val': 9, 'pw': 2},
    {'id': 6, 'val': 33, 'pw': 1},
    {'id': None, 'val': 40, 'pw': 2}
])

print(dataset)
'''
    id   val  pw
0  1.0   NaN   2
1  2.0  21.0   3
2  3.0  19.0   0
3  4.0  24.0   1
4  NaN  15.0   2
5  5.0   9.0   2
6  6.0  33.0   1
7  NaN  40.0   2
'''


# 1.1. 행 삭제
dataset_rev1 = dataset.dropna()
print(dataset_rev1)
'''
    id   val  pw
1  2.0  21.0   3
2  3.0  19.0   0
3  4.0  24.0   1
5  5.0   9.0   2
6  6.0  33.0   1
'''

# 1.2. 열 삭제
dataset_rev2 = dataset.dropna(axis='columns')
print(dataset_rev2)
'''
   pw
0   2
1   3
2   0
3   1
4   2
5   2
6   1
7   2
'''

# 2.1. 이전 행 값으로 대체
dataset_rev3 = dataset.fillna(method='pad')
print(dataset_rev3)
'''
    id   val  pw
0  1.0   NaN   2
1  2.0  21.0   3
2  3.0  19.0   0
3  4.0  24.0   1
4  4.0  15.0   2
5  5.0   9.0   2
6  6.0  33.0   1
7  6.0  40.0   2

이전 값이 없는 0번째 행은 NaN값 유지
'''

# 2.2. 다음 행 값으로 대체
dataset_rev4 = dataset.fillna(method='bfill')
print(dataset_rev4)
'''
    id   val  pw
0  1.0  21.0   2
1  2.0  21.0   3
2  3.0  19.0   0
3  4.0  24.0   1
4  5.0  15.0   2
5  5.0   9.0   2
6  6.0  33.0   1
7  NaN  40.0   2

다음 값이 없는 7번째 행은 NaN값 유지
'''

# 2.3. 원하는 값으로 대체
dataset_rev5 = dataset.fillna(0) # 0으로 대체
print(dataset_rev5)
'''
    id   val  pw
0  1.0   0.0   2
1  2.0  21.0   3
2  3.0  19.0   0
3  4.0  24.0   1
4  0.0  15.0   2
5  5.0   9.0   2
6  6.0  33.0   1
7  0.0  40.0   2
'''

# 2.4. 보간법으로 대체
dataset_rev6 = dataset.interpolate(method='linear',limit_direction='forward')
# 선형 비례 방법을 위에서부터 아래로 적용하여 NaN 값 채우기(0번째 행 제외)
dataset_rev6 = dataset.interpolate(method='linear',limit_direction='backward')
# 선형 비례 방법을 위에서부터 아래로 적용하여 NaN 값 채우기(7번째 행 제외)
print(dataset_rev6)
'''
forward
    id   val  pw
0  1.0   NaN   2
1  2.0  21.0   3
2  3.0  19.0   0
3  4.0  24.0   1
4  4.5  15.0   2
5  5.0   9.0   2
6  6.0  33.0   1
7  6.0  40.0   2

backward
    id   val  pw
0  1.0  21.0   2
1  2.0  21.0   3
2  3.0  19.0   0
3  4.0  24.0   1
4  4.5  15.0   2
5  5.0   9.0   2
6  6.0  33.0   1
7  NaN  40.0   2
'''

# 2.5. 결측치 값으로 제외한 평균값으로 대체
dataset_rev7 = dataset.fillna(dataset.mean())
print(dataset_rev7)
'''
    id   val  pw
0  1.0  23.0   2
1  2.0  21.0   3
2  3.0  19.0   0
3  4.0  24.0   1
4  3.5  15.0   2
5  5.0   9.0   2
6  6.0  33.0   1
7  3.5  40.0   2
'''
