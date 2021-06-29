# Montreal Rent Estimator: Project Overview



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


![alt text](https://github.com/vanessadlafp/Rent_predictor_MTL/blob/master/Geo_modeling/Heat%20Map.png)



## Model Buiding


## Model Performance        


## Productionalization  
                                 