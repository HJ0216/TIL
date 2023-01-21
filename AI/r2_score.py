# r2_score.py

import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from sklearn.model_selection import train_test_split


# 1. Data
x = np.array(range(1,21))
y = np.array([1,2,4,3,5,7,9,3,8,12,13,8,14,15,9,6,17,23,21,20])

x_train, x_test, y_train, y_test = train_test_split(
    x,y,
    train_size=0.7,
    shuffle=True,
    random_state=123
)


# 2. Model Construction
model = Sequential()
model.add(Dense(64, input_dim=1))
model.add(Dense(32))
model.add(Dense(16))
model.add(Dense(1))


# 3. compile and train
model.compile(loss='mae', optimizer='adam', metrics=['mse'])
model.fit(x_train, y_train, epochs=128, batch_size=4)


# 4. Evalueate and Predict
loss = model.evaluate(x_test, y_test)
y_predict = model.predict(x_test)


from sklearn.metrics import mean_squared_error, r2_score # ','로 class 다중 삽입 가능


def RMSE (y_test, y_predict):
    return np.sqrt(mean_squared_error(y_test, y_predict))
print("RMSE: ", RMSE(y_test, y_predict))

r2 = r2_score(y_test, y_predict)
print("R: ", r2)



'''
Result for prediction

MAE: 3.0612
MSE: 15.1591
RMSE: 3.8482795786702315
-> loss: 낮을수록 고성능

R: 0.6485608399723322
-> accuracy: 높을수록 고성능

'''
