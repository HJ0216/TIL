# biDirectional.py

import numpy as np

from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, SimpleRNN, LSTM, GRU, Bidirectional # 양방향 연산
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


# 1. Data
a = np.array(range(1, 101))
x_predict = np.array(range(96, 106))
# 모두 x 데이터이므로 y 데이터를 split 할 필요 X

timesteps = 5 # x: 4개, y: 1개

def split_x(dataset, timesteps):
    data_list = [] # 빈 list 생성
    for i in range(len(dataset) - timesteps + 1):
        # for i in range(3->range(3): 0, 1, 2), range(4->2), range(5->1) : 반환하는 리스트 개수
        subset = dataset[i: (i+timesteps)]
        # dataset[0(이상):5(미만)] [1:6] [2:7]: dataset 위치에 있는 값 반환
        data_list.append(subset)
    return np.array(data_list)

a_split = split_x(a, timesteps)
x_pred_split = split_x(x_predict, timesteps-1)
'''
# timesteps의 변수를 timesteps1, timesteps2로 나눠서 사용할 수 있음
timesteps1 = 5
timesteps2 = 4

a_split = split_x(a, timesteps1) # 5 적용
x_pred_split = split_x(x_predict, timesteps2) # 4 적용

'''

x = a_split[:, :-1] # 모든 행, 시작 ~ -1번째 열
y = a_split[:, -1] # 모든 행, -1번째 열(시작: 0번째 열)
x_predict = x_pred_split[:,:]


'''
print(x, y) # (96, 4) (1, 96)
x: [1 2 3 4] ... [96 97 98 99]
y: [5 6 ... 99 100]

print(x_predict) # (7, 4)
[[ 96  97  98  99]
 [ 97  98  99 100]
 [ 98  99 100 101]
 [ 99 100 101 102]
 [100 101 102 103]
 [101 102 103 104]
 [102 103 104 105]]
'''

x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    test_size=0.2,
    shuffle= True,
    random_state = 333
)

print(x_train.shape, x_test.shape, x_predict.shape) # (76, 4) (20, 4) (7, 4)

x_train = x_train.reshape(76,4,1)
x_test = x_test.reshape(20,4,1)
x_predict = x_predict.reshape(7,4,1)
# train_test_split(): 3차원 이상 작업 불가하므로 split 후 reshape
# x_train, x_test, y_train, y_test = train_test_split()


# 2. Model Construction
model = Sequential()
model.add(Bidirectional(LSTM(units=32, return_sequences=True), input_shape=(4,1)))
# Bidirection은 모델이 아니므로 모델 선택 필요
# return_sequences: output_dim을 input_dim과 동일하게 유지하는 parameter
# RNN model에 들어갈 데이터가 시계열 데이터가 아닐 경우, 성능 저하가 있을 수 있음
# Birectional(LSRM) 후, 시계열 데이터가 반환되는 것이 아니라면 RNN을 연달아 사용하여 반드시 성능이 좋아진다고 할 수 없음
model.add(GRU(32, activation='relu'))
model.add(Flatten())
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1))
model.summary()
# Bidirection: Non-Bidirectional model 연산량의 2배


# 3. Compile and Training
model.compile(loss='mse', optimizer='adam')

earlyStopping = EarlyStopping(monitor='loss', mode='min', patience=32, restore_best_weights=True, verbose=1)

model.fit(x_train, y_train, epochs=128, callbacks=[earlyStopping], batch_size=2)


# 4. Evaluation and Prediction
loss = model.evaluate(x_test, y_test)

result = model.predict(x_predict)
print("Predict[100 ... 106]: ", result)



'''
Result(Non-Bi)
[[ 99.99038 ]
 [100.99039 ]
 [101.99034 ]
 [102.99025 ]
 [103.99007 ]
 [104.98979 ]
 [105.989456]]

Result(Bi)
[[ 99.07903 ]
 [ 99.89542 ]
 [100.68855 ]
 [101.46187 ]
 [102.215195]
 [102.94844 ]
 [103.6616  ]]

'''
