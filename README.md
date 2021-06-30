# Montreal Rent Estimator: Project Overview

* Created a tool that estimates apartment rent prices (MAE ~ $ 0.28) to help data scientists negotiate their income when they get a job.
* Scraped over 1000 rent advertisements from kijiji using BeautifulSoup.
* Engineered features from the text of each listing to quantify the value landlords put on location, apartment size, and amenities included.
* Optimized Linear, Lasso, and Random Forest Regressors using GridsearchCV to reach the best model.

## Code and Resources Used

* Python Version: 3.7
* Packages: pandas, numpy, sklearn,scipy, matplotlib, seaborn, BeautifulSoup.
* [Scraper Github](https://github.com/amald94/kijiji-scraper/blob/master/kijiji.py)
* [Scraper Article](https://medium.com/analytics-vidhya/scraping-kijiji-home-rental-advertisements-using-beautiful-soup-5e286af9d96)

## Web Scraping
Tweaked the web scraper github repo (above) to scrape 1626 listings of apartments and rooms for rent from kijiji.ca. With each listing, we got the following:
*  Id
*  Title
*  Price
*  Description
*  Location
*  URL
*  Type 
*  Date posted
*  Furnished
*  Pets allowed 
*  Parking
*  Lease_term
*  Moving date
*  Size (sq.ft.)
*  AC

## Data Cleaning
The following changes were made to clean the data that was messy, mainly due to the website it came from allows its users to fill in the ads in any format, and created the following variables:

* Parsed numeric data out of price
* Parsed numeric data out date posted columns and convert them all to their equivalence in days since posted.
* Parsed numeric data out of furnished 
* Parsed numeric data out of pets allowed
* Parsed numeric data out of number of parking spots 
* Parsed numeric data out of Size (sq.ft.)
* Parsed numeric data out of AC availability 
* Made columns for type of apartment from title information
* Made columns for moving month out of moving date
* Removed rows for rooms due to they weren't representative against the amount of data provided for apartments.
* Made columns with geographical information extracted from location column:
    * Postal code
    * Longitude
    * Latitude
    * Borough
* Column for description length
* Column for title length


## Exploratory Data Analysis (EDA)
Observed the distributions of the data and the value counts for the various categorical variables and plotted listing prices according to their geographical location. Below are a few highlights from the pivot tables:

![alt text](https://github.com/vanessadlafp/Rent_predictor_MTL/blob/master/price_per_district.png)   
--------------------------------------------------------------------------------------------------------
![alt text](https://github.com/vanessadlafp/Rent_predictor_MTL/blob/master/Geo_modeling/Heat%20Map.png) 
--------------------------------------------------------------------------------------------------------
![alt text](https://github.com/vanessadlafp/Rent_predictor_MTL/blob/master/lease_term.png)              
--------------------------------------------------------------------------------------------------------
![alt text](https://github.com/vanessadlafp/Rent_predictor_MTL/blob/master/correlation.png)             
--------------------------------------------------------------------------------------------------------

## Model Buiding
First, the categorical variables were transformed into dummy variables. I also split the data into train and tests sets with a test size of 20%.   

I tried three different models and evaluated them using Mean Absolute Error. I chose MAE because it is relatively easy to interpret and outliers aren’t particularly bad in for this type of model.   

The target variable didn't follow a linear relation for which a logarithmic transformation was applied:
--------------------------------------------------------------------------------------------------------
![alt text](https://github.com/vanessadlafp/Rent_predictor_MTL/blob/master/qq-plot%20%26%20distribution%20of%20apt%20rent%20prices.png)              
--------------------------------------------------------------------------------------------------------
![alt text](https://github.com/vanessadlafp/Rent_predictor_MTL/blob/master/qq-plot%20%26%20distribution%20of%20apt%20rent%20log(prices).png)             
--------------------------------------------------------------------------------------------------------

Three different models were tried:
*	**Multiple Linear Regression** – Baseline for the model
*	**Lasso Regression and Random Forest** – Because of the sparse data from the many categorical variables.

## Model Performance        
The Random Forest model far outperformed the other approaches on the test and validation sets. 
*	**Random Forest** : MAE = 0.288
*	**Linear Regression**: MAE = 0.286
*	**Lasso Regression**: MAE =  0.316
*	**Ensemble: Linear regression  with random forest**: MAE=  0.27925061278742097
                     