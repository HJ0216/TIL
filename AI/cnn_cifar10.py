# cnn_cifar10.py

import datetime
import numpy as np

from tensorflow.keras.datasets import cifar10, cifar100
# cifar10: 총 10개의 label, label 당 6000개의 이미지로 이뤄진 data set
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout, MaxPooling2D
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

filepath = './_save/MCP/'
filename = '{epoch:04d}-{val_loss:.4f}.hdf5'


# 1. data
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
print(x_train.shape, y_train.shape) # (50000, 32, 32, 3) (50000, 1)
print(x_test.shape, y_test.shape) # (10000, 32, 32, 3) (10000, 1)

# pixel값의 최대 수치인 255로 직접 나눠주어 정규화 scaling
x_train = x_train/255
x_test = x_test/255

print(np.unique(y_train, return_counts=True))
'''
(array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=uint8),
 array([5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000], dtype=int64))
'''


# 2. Model
model = Sequential()
model.add(Conv2D(filters=128,
                 kernel_size=(2, 2),
                 padding='same',
                 input_shape=(32, 32, 3),
                 activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(filters=64,
                 kernel_size=(2, 2),
                 padding='same',
                 activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(filters=64,
                 kernel_size=(2, 2),
                 padding='same',
                 activation='relu'))
model.add(Flatten())
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.5))
# dropout = rate: Float between 0 and 1. Fraction of the input units to drop.
# 사용하지 않을 node의 비율
model.add(Dense(10, activation='softmax'))


# 3. Compile and train
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['acc'])

earlyStopping = EarlyStopping(monitor='val_loss', mode='min', patience=32, restore_best_weights=True, verbose=1)

date = datetime.datetime.now()
date = date.strftime("%m%d_%H%M")

modelCheckPoint = ModelCheckpoint(monitor='val_loss', mode='auto', verbose=1,
                                   save_best_only=True,
                                   filepath=filepath + 'cnn_cifar10_' + date + '_' + filename)

model.fit(x_train, y_train, epochs=256, batch_size=128,
                    validation_split=0.2,
                    callbacks=[earlyStopping, modelCheckPoint],
                    verbose=1)


# 4. evaluate and predict
result = model.evaluate(x_test, y_test)
print("loss: ", result[0])
print("acc: ", result[1])



'''
Result

'''
