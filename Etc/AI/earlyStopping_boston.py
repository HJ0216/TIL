# earlyStopping_boston.py

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping

from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split


# 1. Data
datasets = load_boston()
x = datasets.data # (506, 13)
y = datasets.target # (506, )

x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    test_size=0.2,
    shuffle= True,
    random_state = 333
)


# 2. Model Construction
model = Sequential()
model.add(Dense(64, input_shape=(13,)))
model.add(Dense(32))
model.add(Dense(16))
model.add(Dense(1))


# 3. Compile and train
model.compile(loss='mse', optimizer='adam')

earlyStopping = EarlyStopping(monitor='val_loss', mode='min', patience=16, restore_best_weights=True, verbose=1)
# monitor: val_loss로 earlyStopping 지점 확인
# mode: accuracy-max, loss-min, max인지 min인지 모를 때, auto 사용
# patience=5: 갱신이 되지 않더라도 16번 참음
# restore_best_weight: 훈련이 끊긴 지점이 아닌 최적의 weight 지점을 저장
# verbose를 통해 earlyStopping 지점을 확인할 수 있음: Restoring model weights from the end of the best epoch.

hist = model.fit(x_train, y_train,
          epochs=256,
          batch_size=16,
          validation_split=0.2,
          callbacks=[earlyStopping],
          # 정지된 지점-5: min(val_loss)
          # 문제: 5번 인내 후, 최소가 아닌 val_loss 지점에서의 weight가 아닌 끊긴 지점에서의 weight가 반환
          # 해결: restore_best_weights="True"를 통해 최적의 weight 지점을 반환
          # restore_best_weights="False" Defualt
          # 최적의 weight로 predict 수행(false일 경우, epoch가 마무리된 weight를 기준으로 predict 수행)
          verbose=1
          )


# 4. evaluate and predict
loss = model.evaluate(x_test, y_test)



'''
Result

Epoch 79/256
21/21 [==============================] - 0s 6ms/step - loss: 66.6039 - val_loss: 83.2419
Restoring model weights from the end of the best epoch: 63.
Epoch 00079: early stopping

'''
