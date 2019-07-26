# fastscore.input: tagged_mse
# fastscore.module-attached: influxdb

from influxdb import InfluxDBClient
from datetime import datetime
from time import sleep



def begin():
    global influx, FLUSH_DELTA, BATCH_SIZE, BATCH, N, MSE
    FLUSH_DELTA = 0.05
    BATCH_SIZE = 10
    BATCH = []
    influx = InfluxDBClient('influxdb', '8086', 'admin', 'scorefast', 'fastscore')

def gen_point(name, actual, prediction, MSE, timestamp):
    point = {
        "measurement": name,
        "time": timestamp,
        "fields": {
            "Predicted": prediction,
            "value": actual,
            "MSE": MSE,
            "timestamp": timestamp
        }
    }
    return point

def action(datum):
    global BATCH
    N = 1
    MSE = 0
    name = datum['name']
    actual = datum['actual']
    predicted = datum['value']
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    MSE = (1/N)*(N*MSE+(predicted - actual) ** 2)
    N = N + 1

    BATCH.append(gen_point(name, actual, predicted, MSE, timestamp))
    if BATCH_SIZE == len(BATCH):
        influx.write_points(BATCH)
        print(BATCH)
        BATCH = []
        sleep(FLUSH_DELTA)
    yield {"name": "score", "predicted": predicted,"actual": actual, "MSE": MSE}

