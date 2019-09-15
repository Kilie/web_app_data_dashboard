## Web App: World Bank Data Dashboard
This repository contains the back- and front-end files for building a web app for a data dashboard to show the land use of the top 10 world economies, including the change of arable land (hectares per person) from 1990 to 2015, the fertilizer consumption (kilograms per hectare of arable land) in 2015, the rural population (% of total population) in 2015, and the change in forest land (% of land area) from 1990 to 2015. 

The origincal data for these graphs was obtained from the [World Bank Open Data](https://data.worldbank.org/) API. 

This web app was deployed to Heroku and can be viewed [here](https://jing-worldbankdata-dashboard.herokuapp.com/).

## Installation
> Python 3:
>> pandas, NumPy, Plotly, Flask, Gunicorn, Jinja2, requests, PySpark

A detailed list of the packages for this web app is shown in the requirements.txt file.

## File Description
There are files for both the back-end and front-end as well as for deploying the web app to [Heroku](https://www.heroku.com).

1. The worldbank.py file is for getting the web app started. When you have all the front- and back-end files ready, you just need to run the worldbank.py in your terminal to start the app.

2. The worldbankapp folder several including an \__init__.py file, a routes.py file, and a templates folder containing the index.html which is responsible for the front-end.

3. The wrangling_scripts folder has data.py file with code for fetching data from the World Bank Open Data API, wrangling the data, and making graphs using these data. 

4. The Procfile and requirements.txt are for deploying the web app to Heroku. The requirement.txt file lists out all the pacakages needed for making this web app.

## Contribution
Anyone is very welcome to contribute to this repository by either adding more features to the front-end or adding more inspiring graphs to the dashboard et cetera.
