# cnn_conv2D_maxPooling2D.py

import numpy as np

from tensorflow.keras.datasets import mnist, cifar10, cifar100
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout, MaxPooling2D
# Maxpooling: 연산이 아니기때문에 model pkg가 아닌 layers pkg에 삽입, 2D: 이미지
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

path = './_save/'


# 1. data
(x_train, y_train), (x_test, y_test) = mnist.load_data()
'''
x_train.shape: (60000, 28, 28) # 행(28), 열(28), 흑백(1-생략)인 이미지 데이터 60000개
y_train.shape: (60000,) # 이미지에 대한 값을 수치화
'''

# CNN Conv2D 처리하기 위해 4D(Tensor)화
x_train = x_train.reshape(60000, 28, 28, 1)
x_test = x_test.reshape(10000, 28, 28, 1)

'''
# y_train에서 동일한 값의 빈도수 반환
print(np.unique(y_train, return_counts=True))
(array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=uint8), # y_calss
array([5923, 6742, 5958, 6131, 5842, 5421, 5918, 6265, 5851, 5949], dtype=int64) y_class의 개수)
'''


# 2. Model
model = Sequential()
model.add(Conv2D(filters=128,
                 kernel_size=(3, 3),
                 strides=1,
                 padding='same',
                 input_shape=(28, 28, 1),
                 activation='relu'))
'''
padding=valid
output_shape=(26,26,128)
# output shape = input_shape - kernel_size +1 (Not using padding)
padding=same
output_shape=(28,28,128)
'''
model.add(MaxPooling2D())
# output_shape=(14, 14, 128)
# Parameter=0 (연산 X)
model.add(Conv2D(filters=64,
                 kernel_size=(3, 3),
                 padding='same'))
# Sequential Model output->input이므로 입력값 작성 생략
model.add(Conv2D(filters=64,
                 kernel_size=(3, 3),
                 padding='same'))
model.add(MaxPooling2D())
model.add(Conv2D(filters=32,
                 kernel_size=(3, 3),
                 padding='same'))
model.add(Flatten()) # input_dim=7*7*32 (column)
model.add(Dense(32, activation='relu'))
# batch_size(총 훈련 필요 대상)=60000
model.add(Dropout(0.3))
model.add(Dense(10, activation='softmax')) # y_class=10
model.summary()
'''
Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 conv2d (Conv2D)                 (None, 28, 28, 128)       1280

 max_pooling2d (MaxPooling2D)    (None, 14, 14, 128)       0

 conv2d_1 (Conv2D)               (None, 14, 14, 64)        73792

 conv2d_2 (Conv2D)               (None, 14, 14, 64)        36928

 max_pooling2d_1 (MaxPooling2D)  (None, 7, 7, 64)          0

 conv2d_3 (Conv2D)               (None, 7, 7, 32)          18464

 flatten (Flatten)               (None, 1568)              0

 dense (Dense)                   (None, 32)                50208 = 1568*32 + 32

 dropout (Dropout)               (None, 32)                0

 dense_1 (Dense)                 (None, 10)                330

=================================================================
Total params: 181,002
Trainable params: 181,002
Non-trainable params: 0
_________________________________________________________________
'''


# 3. Compile and train
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['acc'])
# one-hot encoding 안했으므로, sparse_categorical_crossentropy

earlyStopping = EarlyStopping(monitor='val_loss', mode='min', patience=32, restore_best_weights=True, verbose=1)


modelCheckPoint = ModelCheckpoint(monitor='val_loss', mode='auto', verbose=1,
                                   save_best_only=True,
                                   filepath='cnn_conv2D_maxPooling2D.hdf5')


model.fit(x_train, y_train, epochs=256, batch_size=128,
                    validation_split=0.2,
                    callbacks=[earlyStopping, modelCheckPoint],
                    verbose=1)

model.save(path+'cnn_conv2D_maxPooling2D_save_model.h5')


# 4. evaluate and predict
result = model.evaluate(x_test, y_test)
print("loss: ", result[0])
print("acc: ", result[1])



'''
Result
loss:  0.049012500792741776
acc:  0.9872999787330627

'''
