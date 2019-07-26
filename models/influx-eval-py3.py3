# fastscore.slot.0: in-use 
# fastscore.slot.1: unused

# fastscore.module-attached: influxdb

from influxdb import InfluxDBClient
from datetime import datetime
from time import sleep

def begin():
    global influx, FLUSH_DELTA, BATCH_SIZE, BATCH
    FLUSH_DELTA = 1.0 
    BATCH_SIZE = 1 
    BATCH = []
    influx = InfluxDBClient('influxdb', '8086', 'admin', 'scorefast', 'fastscore')

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
            "price": datum['score'],
            #"EWMV": datum['EWMV'],
            "Elapsed Time": datum['Elapsed Time'],
            "Number of Records": datum['Number of Records']
        }
    }
    return point

def action(datum):
    global BATCH
    name = "monitors"
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    BATCH.append(gen_point(name, datum, timestamp))
    if BATCH_SIZE == len(BATCH):
        influx.write_points(BATCH)
        BATCH = []
        sleep(FLUSH_DELTA)


