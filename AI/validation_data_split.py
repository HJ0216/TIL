# validation_data_split.py

import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from sklearn.model_selection import train_test_split


# 1. Data
x = np.array(range(1, 17))
y = np.array(range(1, 17))


x_train, x_test_tmp, y_train, y_test_tmp = train_test_split(
    x, y,
    shuffle=False,
    train_size=0.625,
    random_state=123
)

x_test, x_val, y_test, y_val = train_test_split(
    x_test_tmp, y_test_tmp,
    shuffle=False,
    train_size=0.5,
    random_state=123
)


# 2. Model
model = Sequential()
model.add(Dense(32, input_dim=1, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1))


# 3. compile and train
model.compile(loss='mse', optimizer='adam')
model.fit(x_train, y_train, epochs=128, batch_size=32,
          validation_data=(x_val, y_val))
# validation_data를 통해서 val_loss 추가
# 훈련 + '검증(Validation)' + 평가 (fit + 'validation'+ evaluate)


# 4. evaluate and predict
loss = model.evaluate(x_test, y_test)

result = model.predict([17])
print("predict [17]: ", result)



'''
Result(split val_data)
training loss - loss: 0.0505, val_loss: 0.2850
evaluate loss - loss: 0.1105
predict [17] - [16.333452]

'''
