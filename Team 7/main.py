"""
Target Problem:
---------------
* A classifier for the diagnosis of Autism Spectrum Disorder (ASD)

Proposed Solution (Machine Learning Pipeline):
----------------------------------------------
* Constant Feature Elimination -> SelectKBest Algorithm -> PCA -> Decision Tree Classifier

Input to Proposed Solution:
---------------------------
* Directories of training and testing data in csv file format
* These two types of data should be stored in n x m pattern in csv file format.

  Typical Example:
  ----------------
  n x m samples in training csv file (n number of samples, m - 1 number of features, ground truth labels at last column)
  k x s samples in testing csv file (k number of samples, s number of features)

* These data set files are ready by load_data() function.
* For comprehensive information about input format, please check the section
  "Data Sets and Usage Format of Source Codes" in README.md file on github.

Output of Proposed Solution:
----------------------------
* Predictions generated by learning model for testing set
* They are stored in "submission.csv" file.

Code Owner:
-----------
* Copyright © Team 7. All rights reserved.
* Copyright © Istanbul Technical University, Learning From Data Spring 2019. All rights reserved. """


import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2


def load_data(tra_name, test_name):

    """
    The method reads the training and testing data from their csv files.

    Parameters
    ----------
    tra_name:  directory of the training dataset file
    test_name: directory of testing dataset file

    """

    train_data = pd.read_csv(tra_name)
    test_data = pd.read_csv(test_name)
    return train_data, test_data


def preprocessing(train_data, test_data):

    """
    The method at first eliminates constant features.
    Then, it chooses top 100 features by evaluating chi square values of each feature.
    Finally, these 100 features are reduced to 80 features by using principal component analysis.

    Parameters
    ----------
    train_data: training dataset containing features and labels
    test_data: testing dataset containing only features

    """

    train_data = train_data.drop(['X3', 'X31', 'X32', 'X127', 'X128', 'X590'], axis=1)
    train_data = np.asarray(train_data)

    train_x = train_data[:, :train_data.shape[1] - 1]
    train_y = train_data[:, train_data.shape[1] - 1]
    train_y.shape = (np.size(train_y), 1)

    test_data = test_data.drop(['X3', 'X31', 'X32', 'X127', 'X128', 'X590'], axis=1)
    test_data = np.asarray(test_data)

    selector = SelectKBest(score_func=chi2, k=100)
    selector.fit(train_x, train_y)

    train_features = selector.transform(train_x)
    test_features = selector.transform(test_data)

    pca = PCA(n_components=80)
    x_tra_pca = pca.fit_transform(train_features)
    x_test_pca = pca.transform(test_features)

    return x_tra_pca, train_y, x_test_pca

# ********** MAIN PROGRAM ********** #


train_data, test_data = load_data("train.csv", "test.csv")
x_tra_pca, train_y, x_test_pca = preprocessing(train_data, test_data)


clf = DecisionTreeClassifier(random_state=25)
clf.fit(x_tra_pca, train_y)
predictions = clf.predict(x_test_pca)


yt = pd.DataFrame(predictions, dtype='int32')
yt.columns = ["Predicted"]
yt.index += 1
yt.to_csv("./submission.csv", index_label="ID")
