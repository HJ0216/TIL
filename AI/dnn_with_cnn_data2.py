# dnn_with_cnn_data2.py

import numpy as np

from tensorflow.keras.datasets import mnist, cifar10, cifar100, fashion_mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout, MaxPooling2D
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

path = './_save/'


# 1. data
(x_train, y_train), (x_test, y_test) = mnist.load_data()
'''
x_train.shape: (60000, 28, 28), x_train.shape: (60000,)
x_test.shape: (10000, 28, 28), x_test.shape: (10000,)
'''

x_train=x_train/255.
x_test=x_test/255.


# 2. Model
model = Sequential()
model.add(Flatten()) # 모델 초반부에 Flatten을 통한 1차원 배열로 변환 input_dim=28*28*1=784 (column)
# 차원: []의 개수
model.add(Dense(128, activation='relu', input_shape=(784,)))
model.add(Dropout(0.3))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(32, activation='linear'))
model.add(Dense(10, activation='softmax'))


# 3. Compile and train
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['acc'])

earlyStopping = EarlyStopping(monitor='val_loss', mode='min', patience=32, restore_best_weights=True, verbose=1)

modelCheckPoint = ModelCheckpoint(monitor='val_loss', mode='auto', verbose=1,
                                   save_best_only=True,
                                   filepath='dnn_with_cnn_data2_MCP.hdf5')

model.fit(x_train, y_train, epochs=256, batch_size=32,
                    validation_split=0.2,
                    callbacks=[earlyStopping, modelCheckPoint],
                    verbose=1)

model.save(path+'dnn_with_cnn_data2_save_model.h5')


# 4. evaluate and predict
result = model.evaluate(x_test, y_test)
print("loss: ", result[0])
print("acc: ", result[1])



'''
Result(CNN)
loss:  0.16121244430541992
acc:  0.9692999720573425

Result(DNN)
loss:  0.08222146332263947
acc:  0.977400004863739

'''
