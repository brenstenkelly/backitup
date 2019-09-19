#fastscore.action: unused
#fastscore.schema.0: xgboost_iris_input
#fastscore.schema.1: xgboost_iris_output
#fastscore.module-attached: xgboost

from fastscore.io import Slot
import xgboost
import pickle
import pandas as pd
import time

model = pickle.load(open('xgboost_explicit.pkl', 'rb'))
slot0 = Slot(0)
slot1 = Slot(1)
for df in slot0:
	features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
	df = df[features]
	preds = model.predict_proba(data = df)
	preds = pd.DataFrame(preds, columns = ['A', 'B', 'C'])
	for j in range(len(preds)):
		slot1.write(preds.iloc[j,:].to_dict())



