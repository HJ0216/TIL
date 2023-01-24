# save_model_and_weight.py

import numpy as np

from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.callbacks import EarlyStopping

# Model save
path = './_save/' # ./ 현재(STUDY) dir
# path = '../_save/' # ../ 상위 dir
# path = 'c:/study/_save/' # 경로 대소문자 구분 X


# 1. Data
dataset = load_boston()
x = dataset.data # for training
y = dataset.target # for predict

x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    train_size=0.7,
    random_state=123
)

scaler = MinMaxScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)


# 2. Model(Function)
input1 = Input(shape=(13,))
dense1 = Dense(64, activation='relu')(input1)
dense2 = Dense(32, activation='relu')(dense1)
output1 = Dense(1, activation='linear')(dense2)
model = Model(inputs=input1, outputs=output1)

# save model before training
model.save(path+'save_model1.h5')
# save weights before training(훈련이 되지 않은 가중치이므로 사용X)
model.save_weights(path +'save_weights1.h5')

# 3. compile and train
model.compile(loss='mse', optimizer='adam', metrics=['mae'])
earlyStopping = EarlyStopping(monitor='val_loss', mode='min', patience=32, restore_best_weights=True, verbose=1)
hist = model.fit(x_train, y_train,
          epochs=512,
          batch_size=16,
          validation_split=0.2,
          callbacks=[earlyStopping],
          verbose=1)

# save model and weight after training
model.save(path+'save_model2.h5')
# save weights after training
model.save_weights(path+'save_weights2.h5')


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
RMSE:  4.60305594170595
R2:  0.7378618798976347

'''
