#fastscore.slot.0: in-use
#fastscore.slot.1: in-use
#fastscore.recordsets.0: true

import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import ElasticNetCV, LassoCV, RidgeCV
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
import datetime as dt

def begin():
    global ridge_model, train_encoded_columns
    ridge_model = pickle.load(open("ridge_model.pickle", "rb"))
   
    train_encoded_columns = pickle.load(open("train_encoded_columns.pickle", "rb"))

def action(data):

    missing_cols = set(train_encoded_columns) - set(data.columns)
    for c in missing_cols:
        data[c] = 0

    data = data[train_encoded_columns]

    log_predictions = ridge_model.predict(data)
    predictions = np.expm1(log_predictions)

    predictions = pd.DataFrame(predictions.reshape(-1,1))
    yield predictions

