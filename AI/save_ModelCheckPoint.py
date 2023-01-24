# save_ModelCheckPoint.py

import numpy as np

from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

path = './_save/'


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
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)


# 2. Model(Function)
input1 = Input(shape=(13,))
dense1 = Dense(64, activation='relu')(input1)
dense2 = Dense(64, activation='sigmoid')(dense1)
dense3 = Dense(32, activation='relu')(dense2)
dense4 = Dense(32, activation='linear')(dense3)
output1 = Dense(1, activation='linear')(dense4)
model = Model(inputs=input1, outputs=output1)


# 3. compile and train
model.compile(loss='mse', optimizer='adam', metrics=['mae'])

earlyStopping = EarlyStopping(monitor='val_loss', mode='min', patience=32, restore_best_weights=True, verbose=1)

modelCheckPoint = ModelCheckpoint(monitor='val_loss', mode='auto', verbose=1,
                                   save_best_only=True,
                                   filepath=path+'MCP/save_ModelCheckPoint.hdf5') # MCP/ = MCP파일 하단
# 가중치 및 모델 저장 확장자: h5
# ModelCheckPoint 저장 확장자: hdf5

model.fit(x_train, y_train,
   epochs=512,
   batch_size=16,
   validation_split=0.2,
   callbacks=[earlyStopping, modelCheckPoint],
   verbose=1)

'''
epochs=512
Epoch 00001: val_loss improved from inf to 481.11652, saving model to ./_save/MCP\save_ModelCheckPoint1.hdf5
-> 처음 훈련은 최상의 결과값이므로 저장
Epoch 00002: val_loss improved from 481.11652 to 273.11346, saving model to ./_save/MCP\save_ModelCheckPoint1.hdf5
-> 2번째 훈련 개선 -> 덮어쓰기
-> 반복
Epoch 00024: val_loss did not improve from 10.37429
-> 개선되지 않을 경우 저장 X
-> 개선되지 않은 결과가 20번 반복될 경우, EarlyStopping = 가장 성능이 좋은 ModelCheckPoint 지점
Epoch 67/512
14/18 [======================>.......] - ETA: 0s - loss: 5.7881 - mae: 1.6581
Restoring model weights from the end of the best epoch: 35.

MCP 저장
MSE:  4.433804789382322
R2:  0.7567847452094035

EarlyStopping: 최적의 weight가 갱신이 안되면 훈련을 끊어주는 역할
ModelCheckPoint: 최적의 weight가 갱신될 때마다 저장해주는 역할

'''


# 4. evaluate and predict
loss = model.evaluate(x_test, y_test)
y_predict = model.predict(x_test)

def RMSE (y_test, y_predict):
    return np.sqrt(mean_squared_error(y_test, y_predict))
print("RMSE: ", RMSE(y_test, y_predict))

r2 = r2_score(y_test, y_predict)
print("R2: ", r2)



'''
Result
MSE:  4.433804789382322
R2:  0.7567847452094035

'''
