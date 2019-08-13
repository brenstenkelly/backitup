# fastscore.schema.0: hp_input
# fastscore.schema.1: hp_input
# fastscore.module-attached: streamstats
# fastscore.module-attached: influxdb


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
            "EWMV": datum['EWMV'],
            "Elapsed Time": datum['Elapsed Time'],
            "Number of Records": datum['Number of Records']
        }
    }
    return point


def begin():
    
    # define your cases
    
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
	FLUSH_DELTA = 0.1 
	BATCH_SIZE = 1 
	BATCH = []
	influx = InfluxDBClient(host='influxdb', port='8086', username='admin', password='scorefast', database='fastscore')



def action(datum):
	global bundle
	global start_time
	global num_of_recs
	global BATCH
	name = "hp_input_monitor"

	timestamp = dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
	num_of_recs += 1
	if num_of_recs == 1:
		start_time = dt.datetime.now().timestamp()
	current_time = dt.datetime.now().timestamp()
	elapsed_time = current_time - start_time
	TotalBsmtSF = datum["TotalBsmtSF"]	
	bundle.update(x=TotalBsmtSF) 
	
	report = vals_to_dict(bundle) 
	
	report['Elapsed Time'] = float(elapsed_time)
	report["Number of Records"] = float(num_of_recs)
	BATCH.append(gen_point(name, report, timestamp))
	if BATCH_SIZE == len(BATCH):
		influx.write_points(BATCH)
		BATCH = []
		sleep(FLUSH_DELTA)

	yield datum

