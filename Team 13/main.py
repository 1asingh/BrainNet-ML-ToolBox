"""
Target Problem:
---------------
* A classifier for the diagnosis of Autism Spectrum Disorder (ASD)

Proposed Solution (Machine Learning Pipeline):
----------------------------------------------
* Coorelation Based Elimination -> SelectKBest Algorithm -> Adaptive Boosting (Base: Decision Tree)

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
* Copyright © Team 13. All rights reserved.
* Copyright © Istanbul Technical University, Learning From Data Spring 2019. All rights reserved. """

import csv
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_selection import SelectKBest, chi2


def load_data():
    """
    The method reads train and test data from data set files.
    Then, it splits train data into features and labels.
    """

    train_data = pd.read_csv('train.csv')
    test_data = pd.read_csv('test.csv')

    x_train = train_data.iloc[:, 0: -1]
    y_train = train_data.iloc[:, -1]
    x_test = test_data.iloc[:, 0:]

    return x_train, y_train, x_test


def preprocessing(x_train, y_train, x_test):

    """
    The method at first chooses top 50 features with highest chi square value by using SelectKBest algorithm.
    Then, those features are sorted, and the features least correlated with labels are eliminated.

    Parameters
    ----------
    x_train: features of training data
    y_train: labels of training data
    x_test: features of testing data
    """

    selector = SelectKBest(score_func=chi2, k=50)

    fit = selector.fit(x_train, y_train)

    df_scores = pd.DataFrame(fit.scores_)
    df_columns = pd.DataFrame(x_train.columns)

    feature_scores = pd.concat([df_columns, df_scores], axis=1)
    feature_scores.columns = ['Specs', 'Score']

    selected_features = feature_scores.sort_values(['Score'], ascending=0).iloc[0:50, :]

    new_x_train = x_train.loc[:, selected_features['Specs']]
    new_x_test = x_test.loc[:, selected_features['Specs']]

    plt.matshow(new_x_train.corr().abs())
    plt.show()

    new_x_train = new_x_train.drop(['X584', 'X579', 'X404', 'X528', 'X318'], axis=1)
    new_x_test = new_x_test.drop(['X584', 'X579', 'X404', 'X528', 'X318'], axis=1)

    return new_x_train, new_x_test


def train_model(x_train, y_train):

    """
    The method creates a learning model and trains it by using training data.

    Parameters
    ----------
    x_train: features of training data
    y_train: labels of training data
    """

    model = AdaBoostClassifier(n_estimators=10)
    model.fit(x_train, y_train)
    return model


def predict(model, x_test):

    """
    The method predicts labels for testing data samples.

    Parameters
    ----------
    model: trained model
    x_test: features of testing data set
    """

    y_pred = model.predict(x_test)
    return y_pred


def write_output(y_pred):

    for i in range(0, len(y_pred) + 1):
        if i == 0:
            with open('submission.csv', 'w') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow(["ID", "Predicted"])
            continue
        row = [i, int(y_pred[i - 1])]
        with open('submission.csv', 'a') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(row)


if __name__ == '__main__':

    x_train, y_train, x_test = load_data()
    x_train, x_test = preprocessing(x_train, y_train, x_test)

    model = train_model(x_train, y_train)
    predictions = predict(model, x_test)
    write_output(predictions)
