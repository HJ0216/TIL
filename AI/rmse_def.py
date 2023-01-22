# rmse_def.py

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
model.fit(x_train, y_train, epochs=128, batch_size=5)


# 4. Evalueate and Predict
loss = model.evaluate(x_test, y_test)
print("Loss: ", loss)

y_predict = model.predict(x_test)


from sklearn.metrics import mean_squared_error


def RMSE (y_test, y_predict):
    return np.sqrt(mean_squared_error(y_test, y_predict))
# def function_name(para1, para2):
    # return np.sqrt(mse), root(MSE)

print("RMSE: ", RMSE(y_test, y_predict))



'''
Result

MAE: 2.9459493160247803
MSE: 14.699475288391113
RMSE: 3.8339895717187855


'''
