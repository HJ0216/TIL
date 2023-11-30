# evaluate_and_predict.py

import numpy as np

from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential


# 1. Data
x = np.array([1,2,3,4,5,6])
y = np.array([1,2,3,5,4,6])


# 2. Model
model = Sequential()
model.add(Dense(64, input_dim=1))
model.add(Dense(64))
model.add(Dense(32))
model.add(Dense(16))
model.add(Dense(1))


# 3. Complile, training
model.compile(loss='mae', optimizer='adam')
model.fit(x, y, epochs=128, batch_size=2)


# 4. Evaluation, Prediction
loss = model.evaluate(x,y)
print("loss: ", loss)

result = model.predict([7])
print("predict 7: ", result)



'''
Result

model.fit(x, y, epochs=128, batch_size=2)
poch 128/128
3/3 [==============================] - 0s 4ms/step - loss: 0.3661

loss = model.evaluate(x,y)
1/1 [==============================] - 0s 408ms/step - loss: 0.3958
loss:  0.39582571387290955

result = model.predict([7])
predict 7:  [[6.7003293]]

'''
