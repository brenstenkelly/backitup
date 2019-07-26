# fastscore.schema.0: close_price

import numpy as np
import pickle
import time
from sklearn.linear_model import LinearRegression
from random import uniform

def begin():
    global lr
    global window, window_size
    window = []
    window_size = 15
    with open('lr_pickle1.pkl', 'rb') as f:
        lr = pickle.load(f)

def action(x):
    global window, window_size
    x = x['Close']
    #actual = x*uniform(1, 1.5)
    window = window[1-window_size:] + [x]
    if len(window) < window_size:
        yield {"name": "price", "score":x}
    else:
        X = np.array([window])
        y = lr.predict(X)
        yield {"name":"price", "score": y[0,0]}

