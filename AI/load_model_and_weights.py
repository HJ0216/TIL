# load_model_and_weights.py

import numpy as np

from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.layers import Dense, Input

# saved model path
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

# scaler = StandardScaler()
scaler = MinMaxScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)


# 2. Model(Function)
model = load_model(path+'save_model1.h5')
# save_model1.h5와 동일한 모델 구성 반환
# Model Construction 생략 가능

# model.load_weights(path + 'save_weights1.h5')
# weight를 가져왔으므로 fit 필요없으나 훈련 전 weights 무의미


# 3. compile and train
model = load_model(path + 'save_model2.h5')
# save_model2.h5와 동일한 모델 구성 및 가중치 반환
# Model construction, compile and train 생략 가능

# model.load_weights(path + 'save_weights2.h5')
# RuntimeError: You must compile your model before training/testing. Use `model.compile(optimizer, loss)`.
# weights만 저장 -> 모델 구성 후 compile 필요


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
RMSE:  4.122959900727362
R2:  0.7896919500228364

'''
