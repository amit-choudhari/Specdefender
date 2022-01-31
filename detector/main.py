import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import pickle
from sklearn.metrics import accuracy_score

# To disply all col
#pd.set_option('display.max_colwidth', None)
trained_model = 'finalized_model.sav'
#data_file = '../data/data.csv'
data_file = '../data/normal.csv'

#======================================================================
# Load the dataset
fields = ['value', 'perf']
data_attack = pd.read_csv(data_file, skipinitialspace=True, usecols=fields, sep = ", ", engine='python')
print(data_attack.head())

c = 'perf'
data_new = data_attack.set_index([data_attack.groupby(c).cumcount() + 1, c]).unstack().sort_index(1, 1)
data_new.columns = data_new.columns.droplevel(0)
#data_new['y'] = np.ones([data_new.shape[0],1])

# remove outliers
for df in data_new:
    q_low = data_new[df].quantile(0.01)
    q_hi  = data_new[df].quantile(0.99)
    data_new = data_new[(data_new[df]< q_hi) & (data_new[df] > q_low)]

# create 3 new features branch miss rate, cache miss rate, spec load
data_new['br_miss_rate']=data_new['armv8_cortex_a72/br_mis_pred/'].truediv(data_new['armv8_cortex_a72/br_pred/'])
data_new['cache_miss_rate']=data_new['cache-misses'].mul(100).truediv(data_new['cache-references'])
data_new['spec_load'] = data_new['ldst_spec'].truediv(data_new['ldst_spec'].max())

X_test = data_new[['cache_miss_rate','spec_load']]
# Predict
loaded_model = pickle.load(open(trained_model, 'rb'))
preds = loaded_model.predict(X_test)
spectre_prob = preds.mean()
if spectre_prob > 0.70:
    print ("Spectre detected!!")
else:
    print ("safe execution..")

