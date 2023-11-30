# pandas_basic.py

import pandas as pd


# Series
sr = pd.Series([1000, 2000, 3000, 4000],
               index=["일천원", "이천원", "삼천원", "사천원"])
print(sr)
'''
일천원    1000
이천원    2000
삼천원    3000
사천원    4000
dtype: int64
'''
print(format(sr.index)) # Index(['일천원', '이천원', '삼천원', '사천원'], dtype='object')
print(format(sr.values)) # [1000 2000 3000 4000]


# dataFrame
values = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]
index = ['one', 'two', 'three']
columns = ['A', 'B', 'C']

df = pd.DataFrame(values, index=index, columns=columns)
print(df)
'''
       A  B  C
one    1  2  3
two    4  5  6
three  7  8  9
'''
print(format(df.index)) # Index(['one', 'two', 'three'], dtype='object')
print(format(df.columns)) # Index(['A', 'B', 'C'], dtype='object')
print(format(df.values)) # [[1 2 3] [4 5 6] [7 8 9]]

# dataFrame using list
list_data = [
    ['1000', 'Steve', 90.72], 
    ['1001', 'James', 78.09], 
    ['1002', 'Doyeon', 98.43], 
    ['1003', 'Jane', 64.19], 
    ['1004', 'Pilwoong', 81.30],
    ['1005', 'Tony', 99.14],
]
df2 = pd.DataFrame(list_data)
print(df2)
'''
      0         1      2
0  1000     Steve  90.72
1  1001     James  78.09
2  1002    Doyeon  98.43
3  1003      Jane  64.19
4  1004  Pilwoong  81.30
5  1005      Tony  99.14
'''
df2 = pd.DataFrame(list_data, columns=['학번', '이름', '점수']) # col_name 부여
print(df2)
'''
   학번      이름    점수
0  1000     Steve  90.72
1  1001     James  78.09
2  1002    Doyeon  98.43
3  1003      Jane  64.19
4  1004  Pilwoong  81.30
5  1005      Tony  99.14
'''
df2.index=["영", "일", "이", "삼", "사", "오"] # idx_name 부여
print(df2)
'''
     학번     이름    점수
영  1000     Steve  90.72
일  1001     James  78.09
이  1002    Doyeon  98.43
삼  1003      Jane  64.19
사  1004  Pilwoong  81.30
오  1005      Tony  99.14
'''

# dataFrame using dictionary(key-value)
dic_data = {
    '학번' : ['1000', '1001', '1002', '1003', '1004', '1005'],
    '이름' : [ 'Steve', 'James', 'Doyeon', 'Jane', 'Pilwoong', 'Tony'],
    '점수': [90.72, 78.09, 98.43, 64.19, 81.30, 99.14]
    }

df3 = pd.DataFrame(dic_data)
print(df3)
'''
   학번      이름   점수
0  1000     Steve  90.72
1  1001     James  78.09
2  1002    Doyeon  98.43
3  1003      Jane  64.19
4  1004  Pilwoong  81.30
5  1005      Tony  99.14
'''
