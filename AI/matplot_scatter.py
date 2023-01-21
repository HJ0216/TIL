# matplot_scatter.py

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
model.compile(loss='mae', optimizer='adam')
model.fit(x_train, y_train, epochs=128, batch_size=4)


# 4. Evalueate and Predict
loss = model.evaluate(x_test, y_test) # 예측 전 평가

y_predict = model.predict(x) # training dataset을 predict에 사용
print("Result: ", y_predict)


import matplotlib.pyplot as plt

plt.scatter(x, y) # Scatter: 실제 x, y 데이터
plt.plot(x, y_predict, color="red") # plot: 실제 x, 예측 y 데이터
plt.show() # Scatter와 plot을 통해 시각적으로 예측을 비교, 분석할 수 있음



'''
Result

Epoch 128/128
4/4 [==============================] - 0s 5ms/step - loss: 1.9357

1/1 [==============================] - 0s 313ms/step - loss: 3.1006

Result:
[[ 1.0797057]
 [ 2.1201117]
 [ 3.160518 ]
 [ 4.2009234]
 [ 5.2413287]
 [ 6.2817335]
 [ 7.32214  ]
 [ 8.362547 ]
 [ 9.402951 ]
 [10.443358 ]
 [11.483764 ]
 [12.524168 ]
 [13.564573 ]
 [14.6049795]
 [15.645383 ]
 [16.685793 ]
 [17.7262   ]
 [18.766605 ]
 [19.807007 ]
 [20.847416 ]]
 
'''
