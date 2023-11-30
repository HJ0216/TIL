# split_train_test1.py

import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


# 1. Data
x = np.array([1,2,3,4,5,6,7,8,9,10])
y = np.array(range(10)) # [0,1,2,3,4,5,6,7,8,9]

x_train = np.array([1, 2, 3, 4, 5, 6, 7])
x_test = np.array([8, 9, 10])

y_train = np.array(range(7))
y_test = np.array(range(7, 10))


# 2. Model Construction
model = Sequential()
model.add(Dense(64, input_dim=1))
model.add(Dense(64))
model.add(Dense(16))
model.add(Dense(16))
model.add(Dense(1))


# 3. Compile and train
model.compile(loss='mae', optimizer='adam')
model.fit(x_train, y_train, epochs=256, batch_size=5)


# 4. evaluate and predict
loss = model.evaluate(x_test, y_test)
print("Loss: ", loss)

result = model.predict([11])
print("Result: ", result)


'''
# Result

Epoch 256/256
2/2 [==============================] - 0s 5ms/step - loss: 0.0557
1/1 [==============================] - 0s 288ms/step - loss: 0.0259
Loss:  0.02594725228846073
Result:  [[10.031645]]

'''
