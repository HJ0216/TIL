# split_x_with_application_model.py

import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN, LSTM, GRU, Conv2D, Flatten, Dropout


# Prepare Total data
a = np.array(range(1,11)) # 1~10
timesteps = 5

def split_x(dataset, timesteps):
    li = [] # 빈 list 생성
    for i in range(len(dataset) - timesteps + 1):
        # for i in range(3->range(3): 0, 1, 2), range(4->2), range(5->1) : 반환하는 리스트 개수
        subset = dataset[i: (i+timesteps)]
        # dataset[0(이상):3(미만)] [1:4] [2:5]: dataset 위치에 있는 값 반환
        li.append(subset) # append: 추가
    return np.array(li)
'''
timesteps = 5
[[1 2 3 4 5]]

timesteps = 4
[[1 2 3 4]
 [2 3 4 5]]
 
 timesteps = 3
 [[1 2 3]
 [2 3 4]
 [3 4 5]] 
'''

total_Data = split_x(a, timesteps)
print(total_Data)
'''
[[ 1  2  3  4  5]
 [ 2  3  4  5  6]
 [ 3  4  5  6  7]
 [ 4  5  6  7  8]
 [ 5  6  7  8  9]
 [ 6  7  8  9 10]]
'''
print(total_Data.shape) # (6, 5)

# 1-2. make x, y data
x = total_Data[:, :-1] # 모든 행, 시작 ~ -2번째 열
y = total_Data[:, -1] # 모든 행, -1번째 열(시작: 0번째 열)

print(x, y)
'''
x: 
[[1 2 3 4]
 [2 3 4 5]
 [3 4 5 6]
 [4 5 6 7]
 [5 6 7 8]
 [6 7 8 9]]
 
 y:
 [ 5  6  7  8  9 10]
= [5][6][7][8][9][10]

'''


# RNN
x=x.reshape(6,4,1)
# LSTM input_shape=3

model1 = Sequential()
model1.add(LSTM(units=64, input_shape=(4,1)))
# model.add(SimpleRNN(units=64, input_shape=(4,1)))
# model.add(GRU(units=64, input_shape=(4,1)))
model1.add(Dense(32, activation='relu'))
model1.add(Dropout(0.2))
model1.add(Dense(16, activation='relu'))
model1.add(Dropout(0.1))
model1.add(Dense(16, activation='relu'))
model1.add(Dense(1))
model1.summary()

'''
cf.
x = x.reshape(96,2,2)
# data feature가 홀수일 때는 reshape이 불가능하므로, 처음부터 data set을 짝수로 구비하기

model.add(LSTM(units=64, input_shape=(2,2)))
# reshape 시, timesteps*feature가 유지되도록 reshape
'''


# DNN
# Dense input_shape=2이상

model2 = Sequential()
model2.add(Dense(32, activation='relu', input_shape=(4,)))
model2.add(Dense(16, activation='relu'))
model2.add(Dense(16, activation='relu'))
model2.add(Dense(4, activation='relu'))
model2.add(Dense(1))


# Cov2D
x = x.reshape(96,2,2,1)
# Conv2D input_shape=4

model3 = Sequential()
model3.add(Conv2D(32, (2,2), padding='same', activation='relu', input_shape=(2,2,1)))
model3.add(Flatten())
model3.add(Dense(16, activation='relu'))
model3.add(Dense(16, activation='relu'))
model3.add(Dense(4, activation='relu'))
model3.add(Dense(1))
