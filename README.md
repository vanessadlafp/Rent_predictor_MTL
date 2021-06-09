# Montreal Rent Estimator: Project Overview

* Created a tool that estimates data science salaries (MAE ~ $ 11K) to help data scientists negotiate their income when they get a job.
* Scraped over 1000 job descriptions from glassdoor using python and selenium
* Engineered features from the text of each job description to quantify the value companies put on python, excel, aws, and spark.
* Optimized Linear, Lasso, and Random Forest Regressors using GridsearchCV to reach the best model.
* Built a client facing API using flask

## Code and Resources Used

* Python Version: 3.7
* Packages: pandas, numpy, sklearn,scipy, matplotlib, seaborn, BeautifulSoup.
* [Scraper Github](https://github.com/amald94/kijiji-scraper/blob/master/kijiji.py)
* [Scraper Article](https://medium.com/analytics-vidhya/scraping-kijiji-home-rental-advertisements-using-beautiful-soup-5e286af9d96)

## Web Scraping



## Data Cleaning


## Exploratory Data Analysis (EDA)

Examined the distributions of the data. Below are a few highlights found:

![](https://github.com/vanessadlafp/tennis_analysis_proj/blob/main/career_length_2011.png) | ![](https://github.com/vanessadlafp/tennis_analysis_proj/blob/main/career_length_2019.png)
-----------------------------------------------------------------------------------------------------------------------------------------|-------


<img src="https://github.com/vanessadlafp/tennis_analysis_proj/blob/main/corr_map_2011.png" width="450" height="450"> | <img src="https://github.com/vanessadlafp/tennis_analysis_proj/blob/main/corr_map_2019.png" width="450" height="450">
-----------------------------------------------------------------------------------------------------------------------------------------|-------

## Model Buiding
First, I transformed the categorical variables into dummy variables. I also split the data into train and tests sets with a test size of 20%.

I tried three different models and evaluated them using Mean Absolute Error. I chose MAE because it is relatively easy to interpret and outliers aren’t particularly bad in for this type of model.

I tried three different models:

* Multiple Linear Regression – Baseline for the model
* Lasso Regression – Because of the sparse data from the many categorical variables, I thought a normalized regression like lasso would be effective.
* Random Forest – Again, with the sparsity associated with the data, I thought that this would be a good fit.


<img src="https://github.com/vanessadlafp/tennis_analysis_proj/blob/main/Cluters_by_PCA_components_2011.png  " width="450" height="450"> | <img src="https://github.com/vanessadlafp/tennis_analysis_proj/blob/main/Cluters_by_PCA_components_2019.png  " width="450" height="450">
-----------------------------------------------------------------------------------------------------------------------------------------|-------

## Model Performance        
The Random Forest model far outperformed the other approaches on the test and validation sets.

* Random Forest : MAE = 11.22
* Linear Regression: MAE = 18.86
* Ridge Regression: MAE = 19.67  

## Productionalization  
In this step, I built a flask API endpoint that was hosted on a local webserver by following along with the TDS tutorial in the reference section above. The API endpoint takes in a request with a list of values from a job listing and returns an estimated salary.                                    