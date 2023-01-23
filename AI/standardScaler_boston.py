# standardScaler_boston.py

import numpy as np

from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping


# 1. Data
dataset = load_boston()
x = dataset.data # for training
y = dataset.target # for predict

x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    train_size=0.7,
    random_state=123
)

scaler = StandardScaler()
# scaler = MinMaxScaler()
scaler.fit(x_train)
# x_train을 기준으로 scaling -> scaler에 훈련된 가중치 저장
x_train = scaler.transform(x_train)
# 가중치가 저장된 scaler로 x_train data를 transform 후 x_train에 저장
x_test = scaler.transform(x_test)
# train data의 가중치가 저장된 scaler로 x_test data를 transform 후 x_test에 저장
# train data로만 fit 후 가중치 저장


# 2. Model
model = Sequential()
model.add(Dense(64, input_dim=13, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))


# 3. compile and train
model.compile(loss='mae', optimizer='adam')
earlyStopping = EarlyStopping(monitor='val_loss', mode='min', patience=32, restore_best_weights=True, verbose=1)
model.fit(x_train, y_train,
          epochs=512,
          batch_size=32,
          validation_split=0.2,
          callbacks=[earlyStopping],
          verbose=1)

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
RMSE:  3.9774667461538487
R2:  0.7499457664401593

'''
