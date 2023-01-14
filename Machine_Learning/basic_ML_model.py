# basic_ML_model.py


import numpy as np
# numpy import 및 약칭 np 지정


# 1. Refined Deta
x = np.array([1, 2, 3]) # numpy 타입의 array(배열)
y = np.array([1, 2, 3])


# 2. Model Construction
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential() # 순차적 모델 구성
model.add(Dense(1, input_dim=1)) # Dense layer 추가
# Dense(y_col, input_dim=x_col)


# 3. compile and training for best weight, minimum loss
model.compile(loss='mae', optimizer='adam')
# mae: min absolute error
# adam: loss 최적화

model.fit(x, y, epochs=10)
# training
# fit(x_train_data, y_train_data, epochs=훈련 횟수)
# 초기 weight가 랜덤값이므로 실행 시 마다 훈련 결과가 달라짐


# 4. Evaluation and Prediction
result1 = model.predict([4])
print('result1: ', result1)
# print('문자 인식', 실제 출력 값)


# 5. ect
model.fit(x, y, epochs=1000)
result2 = model.predict([4])
print('result2: ', result2)

model.fit(x, y, epochs=3000)
# epochs가 과하게 높을 경우, 과적합(Overfitting) 문제가 발생할 수 있음
result3 = model.predict([4])
print('result3: ', result3)



'''
result1
Epoch 100/100
Result1:  [[4.001488]]

result2
Epoch 1000/1000
Result2:  [[3.9903853]]


result3
Epoch 3000/3000
Result3:  [[4.000531]]

'''
