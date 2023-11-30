# to_categorical_fetch_covtype.py

import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

from sklearn.datasets import fetch_covtype
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Data
datasets = fetch_covtype()
x = datasets.data
y = datasets['target']

y=to_categorical(y)
'''
print(type(y)) # 타입 확인 <class 'numpy.ndarray'>

문제
to_catergorical: class가 0부터 시작하지 않을 때, 앞에 0을 추가 -> 추가된 0만큼의 자원의 낭비가 발생
to_categorical(y): (0,1,2,3,4,5,6,7)
y: (1,2,3,4,5,6,7)

해결
y = np.delete(y, 0, 1)
np.delete(array, idx, axis)
열 -> 축(axis)이 지정되지 않으면 1차원으로 변환된(flatten) array에서 지정한 인덱스 값 제거
np.delete(a, 1, axis=1)과 같이 축을 지정: 축을 따라 지정한 인덱스의 서브어레이를 제거한 어레이를 반환

np.delete 참조: 
numpy_delete.py

'''

y = np.delete(y, 0, axis=1)

x_train, x_test, y_train, y_test = train_test_split(
    x,y,
    shuffle=True,
    random_state=333,
    test_size=0.2,
    stratify=y
)


# 2. Model Construction
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(54, )))
model.add(Dense(64, activation='sigmoid'))
model.add(Dense(32,activation='relu'))
model.add(Dense(16,activation='linear'))
model.add(Dense(7,activation='softmax'))


# 3. Compile and train
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy']
              )

model.fit(x_train, y_train, epochs=100, batch_size=128,
          validation_split=0.2,
          verbose=1)


# 4. evaluate and predict
loss, accuracy = model.evaluate(x_test, y_test)

y_predict = model.predict(x_test)
y_predict = np.argmax(y_predict, axis=1)
y_test = np.argmax(y_test, axis=1)

acc = accuracy_score(y_test, y_predict)
print("accuracy_score: ", acc)



'''
Result
accuracy_score:  0.729817646704474

'''
