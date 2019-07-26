#fastscore.action: unused
#fastscore.schema.0: string
#fastscore.schema.1: double
#fastscore.recordsets.1: true
#fastscore.module-attached: tensorflow
#fastscore.module-attached: fastText
#fastscore.module-attached: my_lib
#fastscore.module-attached: h5py
#fastscore.module-attached: boto3

from fastscore.io import Slot
import fastText
import tensorflow as tf
from my_lib import create_model
import numpy as np
import my_lib
import h5py
import pandas as pd
import boto3

filename = Slot(0)
slot1 = Slot(1)
ft_model = fastText.FastText.load_model('/fastscore/artifacts/fasttext_model.bin')
tf_model = my_lib.create_model()
tf_model.load_weights('/fastscore/artifacts/tf_example_checkpoint_small')
data = []

s3 = boto3.client('s3')
content_object = s3.Object('fasttextdata', filename)
inputdata = content_object.get()['Body'].read().decode("utf-8")
inputlist=inputdata.split('\n')

#for s in obj:
#    data.append(s)    

tensors = [list(map(ft_model.get_word_vector, fastText.FastText.tokenize(x))) for x in inputlist]
#Pad with zeros to match dims
for tensor in tensors:
    for j in range(len(tensor), 2**14):
        tensor.append(np.zeros(100))

x_test = np.array(tensors)
#out = tf_model.predict(x_test)[:,0].tolist()
out = pd.Series(tf_model.predict(x_test)[:,0])
slot1.write(out)
