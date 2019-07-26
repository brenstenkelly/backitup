#fastscore.action: unused
#fastscore.schema.0: xgboost_iris_input_backtest
#fastscore.slot.1: in-use
#fastscore.recordsets.$all: true
#fastscore.module-attached: xgboost

from fastscore.io import Slot
import xgboost
import pickle
import pandas as pd
from sklearn.metrics import confusion_matrix

slot0 = Slot(0)
slot1 = Slot(1)
model = pickle.load(open('xgboost_explicit.pkl', 'rb'))
df = slot0.read()

features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
df['prediction'] = model.predict(df.loc[:,features])

cm = confusion_matrix(y_pred=df.prediction, y_true=df.target)
cm = pd.DataFrame(cm)

slot1.write(cm)


