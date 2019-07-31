# Promotion Report 

## Model Information

### Model Name: hp_xgboost 

Input Schema: string 

Output Schema: array-double 

Attachment: ['hp_comparison.tar.gz'] 

Model Hash: 5b3286ceed37acae38cd09a420e1f909 

Model Code: b'#fastscore.slot.0: in-use\n#fastscore.slot.1: in-use\n#fastscore.recordsets.0: true\n\nimport pandas as pd\nimport pickle\nimport numpy as np\nfrom sklearn.preprocessing import RobustScaler\nfrom sklearn.model_selection import KFold, cross_val_score\nfrom sklearn.linear_model import ElasticNetCV, LassoCV, RidgeCV\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.metrics import mean_squared_error\nimport datetime as dt\n\ndef begin():\n    global xgboost_model, train_encoded_columns\n    xgboost_model = pickle.load(open("xgboost_model.pickle", "rb"))\n   \n    train_encoded_columns = pickle.load(open("train_encoded_columns.pickle", "rb"))\n\ndef action(data):\n\n    missing_cols = set(train_encoded_columns) - set(data.columns)\n    for c in missing_cols:\n        data[c] = 0\n\n    data = data[train_encoded_columns]\n\n    log_predictions = xgboost_model.predict(data)\n    predictions = np.expm1(log_predictions)\n\n    predictions = pd.DataFrame(predictions.reshape(-1,1))\n    yield predictions\n' 


 
Scores:
 [''] 

 
## Event Details

### Model Events
 {"description": "put model: hp_xgboost", "id": 640971, "timestamp": "2019-07-29T19:16:04.806Z", "type": "put model"}
 


### Input Schema Events:
 {"description": "put schema: string", "id": 58746, "timestamp": "2019-07-24T20:41:39.962Z", "type": "put schema"}
 

 
### Output Schema Events:
 {"description": "put schema: array-double", "id": 58497, "timestamp": "2019-07-24T20:41:36.135Z", "type": "put schema"}
