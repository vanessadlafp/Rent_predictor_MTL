# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 18:05:27 2021

@author: Vanessa
"""
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import statsmodels.api as sm
import scipy.stats as stats
from scipy.stats import norm
import math
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('data_eda.csv')

#Due to imbalance in features provided for rooms with respect to apts, only apartments
# will be considered for further modelling.
df= df[df['Type']=='apartment']

# choose relevant columns 
df_model=df[['Price','days_since', 'Parking', 'Lease_term',
       'moving_date', 'pets_allowed_apt', 'furnished_apt',
       'AC', 'Title_length','District', 'desc_len', 'apt_size']]
     
# rename columns to concise name, all data is related to apt now
cols= ['price', 'days_since', 'parking', 'lease_term',
       'moving_date', 'pets_allowed', 'furnished',
       'AC', 'title_length','district', 'desc_length', 'type']

df_model.columns= cols

df_model = df_model.dropna()

##target separation from data set
targets= df_model['price']
df_model= df_model.drop(['price'], axis=1)

##convert categorical variables:pets_allowed,furnished and AC from numerical
## to object type so they can be interpreted as such
df_model['pets_allowed'] = df_model.pets_allowed.astype(str)
df_model['furnished']= df_model.furnished.astype(str)
df_model['AC']= df_model.AC.astype(str)

#separation of numerical and categorical data
categorical_data= df_model.select_dtypes('object')
Features = df_model.select_dtypes('number')


##Regular linear regression will be made as a baseline for other models to 
## properly understand the weight each feature has on the target 

##Create dummy variables
df_dummies= pd.get_dummies(categorical_data, drop_first=True)

predictors= pd.concat([Features,df_dummies], axis=1)
#targets= np.log(targets) ##for linearity

#Train test split
X_train, X_test, y_train, y_test = train_test_split(predictors, targets, test_size=0.2, random_state=42)

# multiple linear regression 
X_sm = predictors = sm.add_constant(predictors)
model = sm.OLS(targets,X_sm)
model.fit().summary()


##Actual regression
lm = LinearRegression()
lm.fit(X_train, y_train)

np.mean(cross_val_score(lm,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3))

# lasso regression 
lm_l = Lasso(alpha= 1.5)
lm_l.fit(X_train,y_train)
np.mean(cross_val_score(lm_l,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3))


alpha = []
error = []

for i in range(1,100):
    alpha.append(i/10)
    lml = Lasso(alpha=(i/10))
    error.append(np.mean(cross_val_score(lml,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3)))
    
plt.plot(alpha,error)

err = tuple(zip(alpha,error))
df_err = pd.DataFrame(err, columns = ['alpha','error'])
df_err[df_err.error == max(df_err.error)]

# random forest 
rf = RandomForestRegressor()
np.mean(cross_val_score(rf,X_train,y_train,scoring = 'neg_mean_absolute_error', cv= 3))

from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,300,10), 'criterion':('mse','mae'), 'max_features':('auto','sqrt','log2')}
gs = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error',cv=3)
gs.fit(X_train,y_train)

gs.best_score_
gs.best_estimator_

# test ensembles 
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

mean_absolute_error(y_test,tpred_lm)
mean_absolute_error(y_test,tpred_lml)
mean_absolute_error(y_test,tpred_rf)

mean_absolute_error(y_test,(tpred_lm+tpred_rf)/2)


import pickle
pickl = {'model': gs.best_estimator_}
pickle.dump( pickl, open( 'model_file' + ".p", "wb" ) )

file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']

model.predict(np.array(list(X_test.iloc[1,:])).reshape(1,-1))[0]

list(X_test.iloc[1,:])