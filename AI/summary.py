# summary.py

import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


# 1. Data
x = np.array([1,2,3])
y = np.array([1,2,3])


# 2. Model Instruction
model = Sequential()
model.add(Dense(5, input_dim=1))
model.add(Dense(4))
model.add(Dense(3))
model.add(Dense(2))
model.add(Dense(1))

model.summary()



'''
Model: "sequential"
_________________________________________________________________
 Layer (type)         Output Shape(노드의 개수)      Param #
                        - model.add(Dense(*))    parameter (연산): node + bias -> 실질적으로는  node+1이 됨
=================================================================
 dense (Dense)         (None, 5) (data 개수, node 개수) 10 (2*5)
 dense_1 (Dense)       (None, 4)                       24 (6*4)
 dense_2 (Dense)       (None, 3)                       15 (5*3)
 dense_3 (Dense)       (None, 2)                        8 (4*2)
 dense_4 (Dense)       (None, 1)                        3 (3*1)
=================================================================
Total params: 60
Trainable params: 60 -> 훈련이 필요한 나의 model에 대해서는 훈련이 필요
Non-trainable params: 0 -> 이미 훈련된 남의 model에 대해서는 훈련이 따로 필요없으므로 non-trainable에 사용
_________________________________________________________________
'''
