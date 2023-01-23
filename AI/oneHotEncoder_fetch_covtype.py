# oneHotEncoder_fetch_covtype.py

import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from sklearn.datasets import fetch_covtype
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score


# 1. Data
datasets = fetch_covtype()
x = datasets.data # (581012, 54)
y = datasets['target'] # (581012,)

y = y.reshape(581012, 1)
# 문제: OneHotEncoder는 Matrix 2차원만 입력받음
# 해결: data(y)를 reshape

ohe = OneHotEncoder()
ohe.fit(y)
y = ohe.transform(y)
y = y.toarray()
# 문제: TypeError: A sparse matrix was passed, but dense data is required.
# 해결: Use X.toarray() to convert to a dense numpy array.

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

model.fit(x_train, y_train, epochs=256, batch_size=128,
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
loss:  0.596627414226532
accuracy:  0.7471494078636169
accuracy_score:  0.7471493851277505

'''
