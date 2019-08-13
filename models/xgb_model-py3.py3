# fastscore.schema.0: hp_input
# fastscore.schema.1: hp_output
# fastscore.recordsets.$all: true
import pickle
import pandas as pd
import sys

def begin():
    global xgb_model
    #train = pd.read_csv('/var/app/anaconda/projects/mm63454/Test/train.csv')
    #with open('train_pickle.pkl', 'rb') as f:
    #    train = pickle.load(f)
    with open('hp_xgb_pickle1.pkl', 'rb') as f:
        xgb_model = pickle.load(f)
    #with open('hp_id_pickle1.pkl', 'rb') as f:
    #    ID = pickle.load(f)
        
def action(testdata):
    features = ['BedroomAbvGr', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtFullBath',
       'BsmtHalfBath', 'BsmtUnfSF', 'EnclosedPorch', 'Fireplaces', 'FullBath',
       'GarageArea', 'GarageCars', 'GarageYrBlt', 'GrLivArea', 'HalfBath',
       'KitchenAbvGr', 'LotArea', 'LotFrontage', 'LowQualFinSF', 'MasVnrArea',
       'MiscVal', 'OpenPorchSF', 'OverallQual', 'PoolArea', 'ScreenPorch',
       'TotRmsAbvGrd', 'TotalBsmtSF', 'WoodDeckSF', 'X1stFlrSF', 'X2ndFlrSF',
       'X3SsnPorch', 'YearBuilt', 'YearRemodAdd']
    testdata = testdata[features]
    print(testdata.columns)
    print(testdata)
    sys.stdout.flush()
   
    X = xgb_model.predict(testdata)
    
    X = pd.DataFrame(X, columns=["SalePrice"])
    
    yield X
