# -*- coding: utf-8 -*-
from sklearn import datasets
# サンプルデータ読み込み
iris = datasets.load_iris()
# 学習
clf = svm.SVC()
clf.fit(iris.data, iris.target)

# setosaの特徴量を与えてちゃんと分類してくれるか試します
test_data = [[ 5.1,  3.5,  1.4,  0.2]]
print(clf.predict(test_data))
