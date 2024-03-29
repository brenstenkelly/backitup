# fastscore.schema.0: close_price
# fastscore.slot.1: in-use
# fastscore.module-attached: streamstats
# fastscore.module-attached: influxdb

import numpy as np
import pickle
import time
from sklearn.linear_model import LinearRegression
from random import uniform
from streamstats import *
import sys
import datetime as dt
from influxdb import InfluxDBClient
from time import sleep

def vals_to_dict(sb):
    vals = sb.values
    mean, var = vals["Moments"]
    vals["Mean"] = mean
    vals["Variance"] = var
    del vals["Moments"]
    ewma, ewmv = vals["EWM"]
    vals["EWMA"] = ewma
    vals["EWMV"] = ewmv
    del vals["EWM"]
    return {**vals}
    
def gen_point(name,datum,timestamp):
    point = {
        "measurement": name,
        "time": timestamp,
        "fields": {
            "Max": datum['Max'],
            "Min": datum['Min'],
            "Mean": datum['Mean'],
            "Variance": datum['Variance'],
            "EWMA": datum['EWMA'],
            #"EWMV": datum['EWMV'],
            "prediction": datum['prediction'],
            "Elapsed Time": datum['Elapsed Time'],
            "Number of Records": datum['Number of Records']
        }
    }
    return point

def begin():
    global lr
    global window, window_size
    window = []
    window_size = 15
    with open('lr_pickle1.pkl', 'rb') as f:
        lr = pickle.load(f)

    global influx, FLUSH_DELTA, BATCH_SIZE, BATCH
    global bundle
    global num_of_recs
    num_of_recs = 0
    
    bundle = StreamingCalcBundle()
    
    # Add the streaming calculations we want to track
    
    bundle + StreamingCalc(update_moments, name='Moments', val=(0.0, 0.0))
    bundle + StreamingCalc(update_ewm, name='EWM', val = (0.0,0.0))
    bundle + StreamingCalc(update_max, name='Max')
    bundle + StreamingCalc(update_min, name='Min')
    FLUSH_DELTA = 1.0 
    BATCH_SIZE = 1 
    BATCH = []
    influx = InfluxDBClient('influxdb', '8086', 'admin', 'scorefast', 'fastscore')

def action(x):
    global window, window_size
    x = x['Close']
    #actual = x*uniform(1, 1.5)
    window = window[1-window_size:] + [x]
    if len(window) < window_size:
        predict = {"name": "price", "score":x}
    else:
        X = np.array([window])
        y = lr.predict(X)
        
        predict = {"name":"price", "score": y[0,0]}

    global bundle
    global start_time
    global num_of_recs
    global BATCH
    name = "monitors"

    timestamp = dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    num_of_recs += 1
    if num_of_recs == 1:
        start_time = dt.datetime.now().timestamp()
    current_time = dt.datetime.now().timestamp()
    elapsed_time = current_time - start_time
    prediction = predict["score"]   
    bundle.update(x=prediction)    
    
    
    report = vals_to_dict(bundle)
    
    
    report['Elapsed Time'] = float(elapsed_time)
    report["Number of Records"] = float(num_of_recs)
    report["prediction"] = prediction
    
    BATCH.append(gen_point(name, report, timestamp))
    if BATCH_SIZE == len(BATCH):
        influx.write_points(BATCH)
        sys.stdout.flush()
        BATCH = []
        sleep(FLUSH_DELTA)
