# dacon_seoul_ddarung.py
# dacon_seoul_ddarung data: https://dacon.io/competitions/open/235576/data

import numpy as np
import pandas as pd

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


# 1. Data
path = './_data/ddarung/'
# 동일한 경로의 파일을 여러번 당겨올 경우, 변수를 지정해서 사용
# ./ = 현재 폴더
# _data/ = _data 폴더
# ddarung/ = ddarung 폴더

train_csv = pd.read_csv(path+'train.csv', index_col=0)
# path + 'train.csv': ./_data/ddarung/train.csv
# index_col을 입력하지 않을 경우 idx도 데이터로 인식하게 됨 (0번째 column은 data가 아닌 idx임을 안내)
# print(train_csv) [1459 rows x 11 columns] -> [1459 rows x 10 columns]

test_csv = pd.read_csv(path+'test.csv', index_col=0)
submission = pd.read_csv(path+'submission.csv', index_col=0)

print(train_csv.columns) # sklearn.feature_names

print(train_csv.info())
# null 값 제외 출력
# Int64Index: 715 entries, 총 데이터 수
# 결측치: 총 데이터 수 - Non-Null (수집못한 데이터)
print(test_csv.info()) # info -> null이 아닌 값(Non-Null) 출력
print(train_csv.describe()) # sklearn.DESC

# 결측치 처리 - '결측 데이터 제거'
print(train_csv.isnull().sum()) # data_set의 결측치(Null) 값 총계 출력
train_csv = train_csv.dropna() # pandas.dropna(): null 값을 포함한 데이터 행 삭제

x = train_csv.drop(['count'], axis=1)
# count column 삭제
# axis=0: index, axis: columns
print(x.shape) # [1459 rows x 9 columns] -> dropna로 인한 변경

y = train_csv['count']
print(y.shape)


x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    shuffle=True,
    train_size=0.7,
    random_state=1234
)

print(x_train.shape, x_test.shape) #(1021, 9) (438, 9)
print(y_train.shape, y_test.shape) #(1021, ) (438, )


# 2. model
model = Sequential()
model.add(Dense(64, input_dim=9)) # input_dim = 9
model.add(Dense(64))
model.add(Dense(32))
model.add(Dense(16))
model.add(Dense(1)) # output_dim = 1


# 3. compile and train
model.compile(loss='mse', optimizer='adam') # RMSE가 평가지표이므로 유사한 mse 사용
model.fit(x_train, y_train, epochs=128, batch_size=32)


# 4. evaluate and predict
loss = model.evaluate(x_test, y_test)
print("Loss: ", loss)

y_predict = model.predict(x_test)
# test는 y값이 없으므로 train의 test dataset 사용


def RMSE (y_test, y_predict):
    return np.sqrt(mean_squared_error(y_test, y_predict))

rmse = RMSE(y_test, y_predict)
print("RMSE: ", rmse)


# for submission
y_submit = model.predict(test_csv) # predict() return numpy
submission['count'] = y_submit
# pandas(submission['count'])에 numpy(y_submit)를 직접 대입시키면 numpy가 pandas가 됨

submission.to_csv(path+'submission_230121.csv')
