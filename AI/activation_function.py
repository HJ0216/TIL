# activation_function.py

import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


# 1. Data
datasets = load_diabetes()
x = datasets.data
y = datasets.target

x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    train_size=0.7
)


# 2. model
model = Sequential()
model.add(Dense(32, input_dim=10, activation='linear'))
model.add(Dense(16, activation='linear'))
model.add(Dense(1))


# 3. compile and train
model.compile(loss='mse', optimizer='adam')
model.fit(x_train, y_train, epochs=128, batch_size=32)


# 4. evaluate and predict
loss = model.evaluate(x_test, y_test)
y_predict = model.predict(x_test)

def RMSE (y_test, y_predict):
    return np.sqrt(mean_squared_error(y_test, y_predict))
# def 함수_이름(para1, para2):
    # return np.sqrt(mse)
print("RMSE: ", RMSE(y_test, y_predict))

r2 = r2_score(y_test, y_predict)
print("R2: ", r2)



'''
Result with Sigmoid
RMSE:  149.80864055376117
R2:  -2.883800175441581

Result with ReLU
RMSE:  56.906094021920666
R2:  0.41644697806090136

Result with Linear
MSE:  58.45104205742501
R2:  0.43929155713336476

'''
