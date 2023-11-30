# indicator_with_california.py

import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split


# 1. Data
datasets = fetch_california_housing()
x = datasets.data
y = datasets.target

x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    train_size=0.7,
    random_state=123
)


# 2. model
model = Sequential()
model.add(Dense(64, input_dim=8))
model.add(Dense(32))
model.add(Dense(1))


# 3. compile and train
model.compile(loss='mae', optimizer = 'adam', metrics=['mse'])
model.fit(x_train, y_train, epochs=128, batch_size=64)


# 4. evaluate and predict
loss = model.evaluate(x_test, y_test)

y_predict = model.predict(x_test)


from sklearn.metrics import mean_squared_error, r2_score


def RMSE (y_test, y_predict):
    return np.sqrt(mean_squared_error(y_test, y_predict))
print("RMSE: ", RMSE(y_test, y_predict))

r2 = r2_score(y_test, y_predict)
print("R2: ", r2)



'''
Result

MAE: 0.6178
MSE: 0.8000
RMSE: 0.8944244298687739
R2: 0.39499231491934617
'''
