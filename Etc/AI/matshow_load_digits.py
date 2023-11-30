# matshow_load_digits.py

import matplotlib.pyplot as plt

from sklearn.datasets import load_digits
# 손글씨로 쓴 숫자를 분류하는 datasets


datasets = load_digits()
# print(datasets.shape) # numpy.shape, datasets=scikit learn

plt.gray() # 이미지의 기본색조: 회색조
plt.matshow(datasets.images[0]) # 훈련용 데이터 손글씨 0
plt.matshow(datasets.images[1]) # 훈련용 데이터 손글씨 1
# plt.matshow(): array -> image로 반환
plt.show()
