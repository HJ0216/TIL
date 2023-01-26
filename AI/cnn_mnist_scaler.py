# cnn_mnist_scaler.py

import numpy as np

from sklearn.preprocessing import StandardScaler

from tensorflow.keras.datasets import mnist, cifar10, cifar100
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


# 1. data
(x_train, y_train), (x_test, y_test) = mnist.load_data()
# x_train.shape: (60000, 28, 28)
# x_test.shape: (10000, 28, 28)
print(x_train.shape, x_test.shape)
x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)

scaler = StandardScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

'''
ValueError: Found array with dim 4.
StandardScaler expected <= 2.
StandardScaler, MinMaxScaler는 dim=2인 경우에 가능
'''
x_train = x_train.reshape(60000, 28, 28, 1)
x_test = x_test.reshape(10000, 28, 28, 1)
# dimension을 변경했을 경우, 내부적인 수치는 성능에 따라 변경 가능
# (60000, 784) -> (60000, 28, 28, 1) O (60000, 14, 56, 1) O ...


# 2. Model
model = Sequential()
model.add(Conv2D(filters=128,
                 kernel_size=(2, 2),
                 input_shape=(28, 28, 1),
                 activation='relu'))
model.add(Conv2D(filters=64,
                 kernel_size=(2, 2)))
model.add(Conv2D(filters=64,
                 kernel_size=(2, 2)))
model.add(Flatten())
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(10, activation='softmax'))
model.summary()


# 3. Compile and train
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['acc'])

earlyStopping = EarlyStopping(monitor='val_loss', mode='min', patience=32, restore_best_weights=True, verbose=1)

model.fit(x_train, y_train, epochs=128, batch_size=32,
                    validation_split=0.2,
                    callbacks=[earlyStopping],
                    verbose=1)


# 4. evaluate and predict
result = model.evaluate(x_test, y_test)
print("loss: ", result[0])
print("acc: ", result[1])



'''
Result
loss:  0.06953822821378708
acc:  0.9779999852180481

'''
