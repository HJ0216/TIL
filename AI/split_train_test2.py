# split_train_test2.py

import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


# 1. Data
x = np.array([1,2,3,4,5,6,7,8,9,10])
y = np.array(range(10)) # [0,1,2,3,4,5,6,7,8,9]

x_train = x[:7] # 시작 생략 가능
x_test = x[7:] # 생략 시 끝 값 가져오기 가능
y_train = y[:7]
y_test = y[7:]
print(x_train, x_test, y_train, y_test)
# [1 2 3 4 5 6 7] [ 8  9 10] [0 1 2 3 4 5 6] [7 8 9]

# -로 위치 표현하는 방법
x_train2 = x[:-3]
x_test2 = x[-3:]
print(x_train2, x_test2)
# [1 2 3 4 5 6 7] [ 8  9 10]

# 2. Model Construction
model = Sequential()
model.add(Dense(64, input_dim=1))
model.add(Dense(64))
model.add(Dense(32))
model.add(Dense(16))
model.add(Dense(1))


# 3. Compile and train
model.compile(loss='mae', optimizer='adam')
model.fit(x_train, y_train, epochs=128, batch_size=2)


# 4. evaluate and predict
loss = model.evaluate(x_test, y_test)
print("Loss: ", loss)

result = model.predict([11])
print("Result: ", result)



'''
# Result

Epoch 128/128
4/4 [==============================] - 0s 2ms/step - loss: 0.0481
1/1 [==============================] - 0s 283ms/step - loss: 0.0506
Loss:  0.050618648529052734
Result:  [[9.937546]]

'''
