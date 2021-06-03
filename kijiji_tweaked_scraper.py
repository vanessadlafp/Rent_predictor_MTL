import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy
import time
from os import path

## url sample 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/page-1/c37l1700281'

url = 'https://www.kijiji.ca/b-a-louer/ville-de-montreal'
baseurl = 'https://www.kijiji.ca'
baseForMontreal = '/c30349001l1700281'
pageNos = '/page-'
apartment = 'v-appartement-condo'
roomRent = 'v-chambres-a-louer-colocataire'
adurl = []
listing = []
urlToSave = []
title = []
prices = []
description = []
location = []
datePosted = []
features = []
linksFromText = []
listingType = []
adId = []
savePoints = [1000,2000,3000,4000,5000,6000,7000]

def getUrls(noPages):
        for i in range(noPages):
                url_final = url+pageNos+str(i)+baseForMontreal
                response = requests.get(url_final)
                soup = BeautifulSoup(response.text, "lxml")
                advtTitles = soup.findAll('div', attrs={'class' : 'title'})
  
                try:
                    for link in advtTitles:
                        adlink = baseurl+link.find('a')['href']
                        adurl.append(adlink)
                except(Exception):
                    print(Exception)
        print(len(adurl))
        
        ## since connection gets closed by the server its better to save the links to a text file
        saveLinks(adurl)
        getDetails(adurl)

def getDetails(urls):

    i =0;
    try:
        for url in adurl:
            print(url)
            listDetails = ""
            listDetailsTwo = []
            apartments_features_cols= ['Stationnement inclus','Durée du bail',"Date d'emménagement",'Animaux acceptés',
                                       'Taille (pieds carrés)','Meublé','Air conditionné','Fumeurs acceptés']
            url = url.rstrip('\n')
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            try:
                adTitle = soup.select_one("h1[class*=title-2323565163]").text
                title.append(adTitle)
                adPrice = soup.select_one("span[class*=currentPrice-2842943473]").text
                prices.append(adPrice)
                adDescription = soup.find_all('div', attrs={'class' : 'descriptionContainer-3261352004'})
                desc_text= [div.find("div").text for div in adDescription]
                description.append(desc_text)
                adLocation = soup.find('span', attrs={'class' : 'address-3617944557'}).text
                location.append(adLocation)
                date = soup.find('time').text   
                datePosted.append(date)
                
                if apartment in url:
                    adfts = soup.find_all('div', attrs={'class' : 'itemAttributeCards-2416600896'})                             
                    for div in adfts:
                        dd= str(div.find_all("dd")).split(",")
                        dd_clean= [dd[i][38:-5] for i in range(len(dd))]
                        listDetails = listDetails + str(dd_clean) 
                    features.append(listDetails)
    
                    listingType.append("apartment")                
                    urlToSave.append(url)
                    adid = getAdId(url)
                    adId.append(adid)
                else:                
                    adfts = soup.find_all('dl', attrs={'class' : 'itemAttribute-1164924913'})
                    for ft in adfts:
                        dd= ft.find('dd').text
                        dt = ft.find('dt').text
                        listDetails = listDetails + str(dt) + " : " + str(dd) + "|"
                    features.append(listDetails)
                    listingType.append("Room")          
                    
                    urlToSave.append(url)
                    adid = getAdId(url)
                    adId.append(adid)
                
                print("Scraping listing : ",str(i))
                response.close()
                i += 1
                if i in savePoints:
                    saveToDisk(i)

                time.sleep(15)
            except Exception as e:
                pass
        saveToDisk(i)
    except Exception as e: 
        print(e)
        pass
    #saveToDisk()

def getAdId(advt):
    advtList = advt.split("/")
    adlen = len(advtList)
    return advtList[adlen-1]


def saveToDisk(i):
    print("saving ***")
    name='kijiji'+str(i)+'.csv'
    d = {'adId':adId, 'Title':title,'Price':prices,'Description':description, 'Location':location,'Ddate Posted':datePosted, 'Location':location, 'Features' : features, 'URL':urlToSave, 'Type' : listingType}
    df = pd.concat([pd.Series(v, name=k) for k, v in d.items()], axis=1)
    df.to_csv(name,index=False)
    resetAll()
    
def saveLinks(liks):
    with open('links.txt', 'w') as f:
        for item in liks:
            f.write("%s\n" % item)

    f.close()

def resetAll():
    print('cleaning')
    adId.clear()
    title.clear()
    prices.clear()
    description.clear()
    datePosted.clear()
    location.clear()
    features.clear()
    urlToSave.clear()
    listingType.clear()
    

# call main methond to start scraping by passing number of pages wanted to scrape  
noPages = 100
getUrls(noPages)