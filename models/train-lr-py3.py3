
import pandas as pd
import json
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression


def action(x):
	with open('/data/close_prices.jsons', 'r') as f:
		inputs = pd.DataFrame([json.loads(line) for line in f])
	close_prices = np.array(inputs['Close'])

	X1, y1 = make_data(close_prices[0:1000])
	lr = LinearRegression()
	lr = lr.fit(X1, y1)
	with open('lr_pickle3.pkl', 'wb') as f:
	pickle.dump(lr, f)

def make_data(inputs, window_size = 15, size = 500):
	X, y = np.vstack( inputs[i:i+window_size] for i in range(0, size) ), np.vstack( inputs[i+window_size: i + window_size + 1] for i in range(0, size) )
	return X, y
