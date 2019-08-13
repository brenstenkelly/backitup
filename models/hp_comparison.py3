#fastscore.slot.0: in-use
#fastscore.slot.1: in-use
#fastscore.recordsets.0: true
# fastscore.module-attached: influxdb

import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import ElasticNetCV, LassoCV, RidgeCV
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
from influxdb import InfluxDBClient
import datetime as dt

def begin():
    global xgboost_model, lasso_model, ridge_model, train_encoded_columns, influx, measurement_name
    ridge_model = pickle.load(open("ridge_model.pickle", "rb"))
    lasso_model = pickle.load(open("lasso_model.pickle", "rb"))
    xgboost_model = pickle.load(open("xgboost_model.pickle", "rb"))
   
    train_encoded_columns = pickle.load(open("train_encoded_columns.pickle", "rb"))
    influx = InfluxDBClient(host='influxdb', port='8086', username='admin', password='scorefast', database='fastscore')

    measurement_name = "champion_challenger"

def action(data):

    if 'SalePrice' in data.columns:  # Checking to see if data is labeled
        labeled=True
        actuals = data['SalePrice']  # Saving actuals (Sale prices)
        data.drop('SalePrice', axis=1, inplace=True)
    else:
        labeled=False


    missing_cols = set(train_encoded_columns) - set(data.columns)
    for c in missing_cols:
        data[c] = 0

    data = data[train_encoded_columns]



    models = {'Ridge': ridge_model,
              'Lasso': lasso_model,
              'XGBoost': xgboost_model}


    log_predictions = {}  # # Model was trained on log(SalePrice)
    RMSEs = {}  # Root mean square error

    for name, model in models.items():
        log_predictions[name] = model.predict(data)  # Computing predictions for each model and each record

    adjusted_predictions = {}  
    for name, model in models.items():
        adjusted_predictions[name] = np.expm1(log_predictions[name])
        if labeled:
        #  Computing RMSE if actual data is available
            RMSEs[name] = np.sqrt(mean_squared_error(adjusted_predictions[name], actuals))

    timestamp = dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    influx.write_points([{"time":timestamp, "measurement":measurement_name, "fields":RMSEs}])
    
    yield RMSEs



