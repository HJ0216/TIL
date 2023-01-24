# hyperParameter_Tuning.py

import numpy as np

from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential


# 1. Data
x = np.array([1,2,3,4,5])
y = np.array([1,2,3,5,4])


# 2. Model(Sequential)
model = Sequential()
model.add(Dense(64, input_dim=1))
model.add(Dense(64)) # 이전 layer의 output이 다음 layer의 input이 되므로 생략 가능
model.add(Dropout(0.3))
model.add(Dense(32))
model.add(Dense(16))
model.add(Dropout(0.2))
model.add(Dense(8))
model.add(Dense(1))
model.summary()
'''
summray
node를 random하게 추출하여 훈련을 수행 -> 과적합 문제 보완
summary는 dropout된 node를 나누지 않음 -> # param에 영향 X
'''

# 3. Complile, training에서의 HyperParameter_Tuning: optimizer, epochs, batch_size
model.compile(loss='mae', optimizer='adam')
model.fit(x, y, epochs=256, batch_size=2)
# Batch_size Default: 32


# 4. Evaluation, Prediction
result = model.predict([6])
print("6의 결과: ", result)



# Hyper-parameter tuning
# Layer, Node, Dropout
# Optimizer
# Epochs
# Batch_size
