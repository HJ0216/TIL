# split_train_test3.py

import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split


# 1. Data
x = np.array([1,2,3,4,5,6,7,8,9,10])
y = np.array(range(10)) # [0,1,2,3,4,5,6,7,8,9]

x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    train_size = 0.7,
    shuffle = True,
    random_state=1)
print("x_train, x_test: ", x_train, x_test, "\ny_train, y_test: ", y_train, y_test)
'''
train_test_split(arrays, test_size, train_size, random_state, shuffle, stratify)

parameter
arrays: 분할시킬 Data
test_size: 전체 Data 중 test로 사용할 test set 비율
train_size: 1 - test_size (생략 가능)
random_state: 입력 시, 함수 수행 시 마다 결과가 바뀌지 않음
* 같은 데이터로 계속 훈련을 해줘야하므로 random_state를 입력해줘야 함
shuffle: split 시, raw data 셔플 여부(Default = True)
shuffle 사용 시, 자료의 치우침 방지
stratify: 해당 Data 비율 유지
Ex. data = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
0의 비율: 70%, 1의 비율: 30%
stratify=Y로 설정 시, TestSet과 TrainSet에서 0의 비율과 1의 비율을 Data와 동일하게 유지
data(y)가 분류형 데이터일 경우만 사용 가능(비율 유지 기능이므로)
'''


# 2. Model Construction
model = Sequential()
model.add(Dense(64, input_dim=1))
model.add(Dense(64))
model.add(Dense(32))
model.add(Dense(16))
model.add(Dense(1))


# 3. Compile and train
model.compile(loss='mae', optimizer='adam')
model.fit(x_train, y_train, epochs=128, batch_size=4)


# 4. evaluate and predict
loss = model.evaluate(x_test, y_test)
print("Loss: ", loss)

result = model.predict([11])
print("Result: ", result)


'''
Result

Epoch 128/128
2/2 [==============================] - 0s 10ms/step - loss: 0.1477
1/1 [==============================] - 0s 480ms/step - loss: 0.2799
Loss:  0.27993300557136536
Result:  [[9.541215]]

'''
