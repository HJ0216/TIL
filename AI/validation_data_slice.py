# validation_data_slice.py

import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


# 1. Data
x = np.array(range(1, 17)) # 1~16
y = np.array(range(1, 17))

x_train = x[:10] # 1~10
y_train = y[:10]
x_test = x[10:13] # 11~13
y_test = y[10:13]
x_validation = x[13:] # 14~16
y_validation = y[13:]
# slicing [초과:이하]


# 2. Model
model = Sequential()
model.add(Dense(32, input_dim=1, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1))


# 3. compile and train
model.compile(loss='mse', optimizer='adam')
model.fit(x_train, y_train, epochs=128, batch_size=32,
          validation_data=(x_validation, y_validation))
# validation_data를 통해서 val_loss 추가
# 훈련 + '검증(Validation)' + 평가 (fit + 'validation'+ evaluate)


# 4. evaluate and predict
loss = model.evaluate(x_test, y_test)

result = model.predict([17])
print("predict [17]: ", result)



'''
Result(slice val_data)
training loss - loss: 0.1758, val_loss: 0.0382
evaluate loss - loss: 0.0025
predict [17] - [16.688446]

'''
