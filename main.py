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

#======================================================================
# Load the dataset
fields = ['value', 'perf']
data_attack = pd.read_csv('../data/data.csv', skipinitialspace=True, usecols=fields, sep = ", ", engine='python')
print(data_attack.head())
data_new = data_attack.set_index([data_attack.groupby(c).cumcount() + 1, c]).unstack().sort_index(1, 1)
data_new.columns = data_new.columns.droplevel(0)
#data_new['y'] = np.ones([data_new.shape[0],1])

# remove outliers
for df in data_new.drop(['y'],axis=1):
    q_low = data_new[df].quantile(0.01)
    q_hi  = data_new[df].quantile(0.99)
    data_new = data_new[(data_new[df]< q_hi) & (data_new[df] > q_low)]

# create 3 new features branch miss rate, cache miss rate, spec load
data_new['br_miss_rate']=data_new['armv8_cortex_a72/br_mis_pred/'].truediv(data_new['armv8_cortex_a72/br_pred/'])
data_new['cache_miss_rate']=data_new['cache-misses'].mul(100).truediv(data_new['cache-references'])
data_new['spec_load'] = data_new['ldst_spec'].truediv(data_new['ldst_spec'].max())


# Predict
loaded_model = pickle.load(open(filename, 'rb'))
preds = loaded_model.predict(X_test)
print(preds)

