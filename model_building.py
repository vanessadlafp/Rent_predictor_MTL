# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 18:27:57 2021

@author: Vanessa
"""
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 

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

##Verifying the Assumptions of Linear Regression

