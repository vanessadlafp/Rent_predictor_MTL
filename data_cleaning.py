# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 15:35:22 2021

@author: Vanessa
"""

import pandas as pd
import unicodedata
import numpy as np

df_1=  pd.read_csv("kijiji_1.csv")
df_2=  pd.read_csv("kijiji_2.csv")

## Data was collected in two batches, we'll concatenate both datasets for its 
## analysis

df= pd.concat([df_1,df_2],ignore_index= True)

#Function to be able to convert values faster regarless of the type
########################################################################
def tryconvert(value, default, *types):
    for t in types:
        try:
            return t(value)
        except (ValueError, TypeError):
            continue
    return default

##########################################################################

## Round to two decimal places

pd.options.display.float_format = '{:.2f}'.format

## adId Parsing  

df['adId'] = df['adId'].apply(lambda x: int(x) if pd.notnull(x) else 0)

## Price parsing, Null values set to -1
df["Price"]= df['Price'].apply(lambda x: unicodedata.normalize("NFKD", x))
df['Price'] = df['Price'].apply(lambda x: x.strip('$').replace(' ','').replace('Surdemande', '-1').replace(",",""))
df['Price'] = df['Price'].apply(lambda x: int(float(x)))

## Date Posted Parsing 

df["days_since"]= df["Ddate Posted"].astype(str).apply(lambda x: x.strip("il y a ").strip(" jours"))
df["days_since"]= df["days_since"].apply(lambda x: tryconvert(x, 1, int))


##Features parsing 

##Room features have a different format

## Sample'Chambres à coucher : Studio|Salles de bain : 1|Meublé : Oui|Animaux acceptés : Non|'
##Variables indicating if room was furnished and it pets were allowed were the most representatives


df['Furnished_room'] = np.where(
    df['Features'].str.contains('Meublé : Oui'), 1, np.where(
    df['Features'].str.contains('Meublé : Non'),0, -1)) 

df['Pets_allowed_room']=  np.where(
    df['Features'].str.contains('Animaux acceptés : Oui'), 1, np.where(
    df['Features'].str.contains('Animaux acceptés : Non'),0, -1)) 

##Apartment features that are separated by 
apartment_features= df['Features'].apply(lambda x: pd.Series(str(x).split(",")))
apartment_features= apartment_features.drop(apartment_features.iloc[:,-4:], axis=1)

apt_cols=['Parking','Lease_term',"moving_date",'pets_allowed_apt','size (sq.ft.)', 'furnished_apt','AC']
apartment_features.columns= apt_cols

apartment_features['Parking'] = np.where(
    apartment_features['Parking'].str.contains('0'), 0, np.where(
    apartment_features['Parking'].str.contains('1'),1,np.where(
    apartment_features['Parking'].str.contains('2'),2 ,-1))) 

apartment_features['moving_date'] = apartment_features['moving_date'].astype(str).apply(lambda x:  x[8:-8])

apartment_features['pets_allowed_apt'] = np.where(
    apartment_features['pets_allowed_apt'].str.contains('Non'), 0, np.where(
    apartment_features['pets_allowed_apt'].str.contains('Oui'),1,np.where(
    apartment_features['pets_allowed_apt'].str.contains('Limité'),1 ,-1))) 



apartment_features['size (sq.ft.)']= apartment_features['size (sq.ft.)'].astype(str).apply(lambda x: unicodedata.normalize("NFKD", x))
apartment_features['size (sq.ft.)'] = apartment_features['size (sq.ft.)'].apply(lambda x: x.replace('Non disponible', '-1').replace('Oui', "-1").replace('Non',"-1").replace("\\xa0","").replace("nan","-1").replace(" '", "").replace("'",""))
apartment_features['size (sq.ft.)'] = apartment_features['size (sq.ft.)'].apply(lambda x: int(float(x)))

apartment_features['furnished_apt'] = np.where(
    apartment_features['furnished_apt'].str.contains('Non'), 0, np.where(
    apartment_features['furnished_apt'].str.contains('Oui'),1 ,-1)) 

apartment_features['AC'] = np.where(
    apartment_features['AC'].str.contains('Non'), 0, np.where(
    apartment_features['AC'].str.contains('Oui'),1 ,-1)) 

###Concatenate apartment features with main dataframe

df_all= pd.concat([df,apartment_features],axis=1 )


df_all['Description']=df_all['Description'].astype(str).apply(lambda x: unicodedata.normalize("NFKD", x))
df_all['Description']=df_all['Description'].apply(lambda x: x.replace("[","").replace("]","").replace("'",""))

## Drop columns that have been cleaned into other ones "Features" "Ddate Posted"

df_clean= df_all.drop(["Features" ,"Ddate Posted"], axis=1)

clean_data= df_clean.to_csv("df_clean.csv")