# fastscore.input: gbm_input
# fastscore.output: gbm_output

import cPickle # unpickle a file
import imp # Load a custom class from the attachment
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline

# GBM model
def begin():
    FeatureTransformer = imp.load_source('FeatureTransformer', 'score_auto_gbm/FeatureTransformer.py')
    global gbmFit
    with open("score_auto_gbm/gbmFit.pkl", "rb") as pickle_file:
        gbmFit = cPickle.load(pickle_file)

def action(datum):
    score = list(gbmFit.predict(pd.DataFrame([datum]).replace("NA", np.nan)))[0]
    yield score
