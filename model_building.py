# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 18:27:57 2021

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
from sklearn.linear_model import LinearRegression
import math
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split


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

# Check the skew of all numerical features
skewed_feats = Features.skew().sort_values(ascending=False)
skewness= pd.DataFrame({'Skew':skewed_feats})

##Regular linear regression will be made as a baseline for other models to 
## properly understand the weight each feature has on the target 

##Create dummy variables
df_dummies= pd.get_dummies(categorical_data, drop_first=True)
df_dum= np.array(df_dummies)


##We first scale the data
scaler= StandardScaler()
scaler.fit(Features)
inputs_scaled= scaler.transform(Features)

predictors= np.concatenate((inputs_scaled,df_dum), axis=1)

##Checking OLS assumptions

#1. Linearity

fig, ax = plt.subplots(1,2, figsize= (15,5))
fig.suptitle(" qq-plot & distribution apartment rent prices ", fontsize= 15)

sm.qqplot(targets, stats.t, distargs=(4,),fit=True, line="45", ax = ax[0])


#sns.histplot(targets, bins= 50)
sns.distplot(targets, hist=True,fit = norm)
plt.title("Distribution of apartment rent Prices", fontsize= 14,
         weight= "bold")
plt.xlabel("Price($)")
plt.ylabel("Number of apartments")
sns.despine()

#We could verify that targets aren't normally distributed so we apply log(targets) to achieve linearity

targets= np.log(targets)

fig, ax = plt.subplots(1,2, figsize= (15,5))
fig.suptitle(" qq-plot & distribution SalePrice ", fontsize= 15)

sm.qqplot(targets, stats.t, distargs=(4,),fit=True, line="45", ax = ax[0])

##train test split 

X_train, X_test, y_train, y_test = train_test_split(predictors, targets, test_size=0.2, random_state=1)

# multiple linear regression 
X_sm =sm.add_constant(X_train)
model = sm.OLS(y_train,X_sm)
model.fit().summary()




##sklearn

reg= LinearRegression()
reg.fit(X_train, y_train)
y_hat= reg.predict(X_train)

plt.scatter(y_train, y_hat)

sns.distplot(y_train- y_hat)

reg.score(X_train, y_train)

reg.intercept_

reg.coef_

features_cols= [c for c in Features.columns.values]
dummies_cols= [c for c in df_dummies.columns.values]
coef_cols= features_cols + dummies_cols

reg_summary= pd.DataFrame(coef_cols, columns= ["Features"])
reg_summary["Weights"]= reg.coef_


sns.set_style("white")
plt.figure(figsize= (40,40))
sns.barplot(x= 'Weights', y='Features', data= reg_summary)
plt.title("Coeficcients OLS", fontsize= 14,
         weight= "bold")
sns.despine()


y_hat_test= reg.predict(X_test)