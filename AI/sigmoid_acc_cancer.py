# sigmoid_acc_cancer.py

import numpy as np

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


# 1. Data
datasets = load_breast_cancer()

x = datasets['data'] # (569, 30) for training
y = datasets['target'] # (569, ) for predict

x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    test_size=0.2,
    shuffle= True,
    random_state = 123
)


# 2. Model Construction
model = Sequential()
model.add(Dense(64, activation='linear', input_shape=(30,)))
model.add(Dense(32, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(1, activation='sigmoid'))


# 3. Compile and train
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Binary Classification Model Construction
# Last Activation=sigmoid, loss='binary_crossentropy'
# 이진분류에서는 정오 판단이 가능하므로 Accuracy 사용이 용이함

from tensorflow.keras.callbacks import EarlyStopping
earlyStopping = EarlyStopping(monitor='accuracy', mode='auto', patience=5, restore_best_weights=True, verbose=1)

hist = model.fit(x_train, y_train,
          epochs=100, batch_size=16,
          validation_split=0.2,
          callbacks=[earlyStopping],
          verbose=1)

'''
print(hist.history)
: model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy']) 기준으로 출력
-> 'loss', 'metrics-accuracy' 출력

'''


# 4. evaluate and predict
loss, accuracy = model.evaluate(x_test, y_test)
# return 값이 2개 이상일 경우, variable 2개 입력 가능

y_predict = model.predict(x_test) # y_test와 비교
# print(y_predict[:10]) # 10개 출력, 0<sigmoid<1
# print(y_test[:10]) # 10개 출력 y_test = 0 or 1
# 실수와 정수 Type Unmatching Error (ValueError: Classification metrics can't handle a mix of binary and continuous targets)

# Solve: ValueError(Classification metrics can't handle a mix of binary and continuous targets)
pred_class = np.where(y_predict >= 0.5, 1, 0) # 0.5 이상=1, 0.5 미만=0
# 조건에 따라 x or y에서 선택한 요소를 반환


from sklearn.metrics import r2_score, accuracy_score
acc = accuracy_score(y_test, pred_class)
print("accuarcy_score: ", acc)
# accuracy(x_test, pred_class)
# y_predict = model.predict(x_test)
# parameter가 다르므로 accuracy도 차이



'''
Result with converting binary classification from sigmoid
loss:  0.13962924480438232
accuracy:  0.9561403393745422
accuarcy_score:  0.956140350877193
accuracy와 accuarcy_score가 차이나는 이유: y_predict값을 0 또는 1로 변환 하였으므로

'''
