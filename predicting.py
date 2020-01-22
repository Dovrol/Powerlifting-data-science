import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np


def predict_total(data):
    if len(data) > 100:
        data = data[['BodyweightKg', 'WeightClassKg', 'TotalKg']]
        data.dropna(inplace = True)
        X = data.drop(columns=['TotalKg', 'WeightClassKg'])
        y = data['TotalKg']

        lr = LinearRegression()
        lr.fit(X, y)

        weight_classes = data['WeightClassKg'].unique()
        weight_classes = [int(x) for x in weight_classes]

        final = np.array(sorted(weight_classes))

        y_predicted = lr.predict(final.reshape(-1,1))
        return y_predicted
    else:
        print('Not enough data to predict')
        return None