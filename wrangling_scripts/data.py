import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.colors
from collections import OrderedDict
import requests


# default list of all countries of interest
country_default = OrderedDict([('Canada', 'CAN'), ('United States', 'USA'), 
  ('Brazil', 'BRA'), ('France', 'FRA'), ('India', 'IND'), ('Italy', 'ITA'), 
  ('Germany', 'DEU'), ('United Kingdom', 'GBR'), ('China', 'CHN'), ('Japan', 'JPN')])


def return_figures(countries=country_default):
  """Creates four plotly visualizations using the World Bank API

  # Example of the World Bank API endpoint:
  # arable land for the United States and Brazil from 1990 to 2015
  # http://api.worldbank.org/v2/countries/usa;bra/indicators/AG.LND.ARBL.HA?date=1990:2015&per_page=1000&format=json

    Args:
        country_default (dict): list of countries for filtering the data

    Returns:
        list (dict): list containing the four plotly visualizations

  """

  # when the countries variable is empty, use the country_default dictionary
  if not bool(countries):
    countries = country_default

  # prepare filter data for World Bank API
  # the API uses ISO-3 country codes separated by ;
  country_filter = list(countries.values())
  country_filter = [x.lower() for x in country_filter]
  country_filter = ';'.join(country_filter)

  # World Bank indicators of interest for pulling data
  indicators = ['AG.LND.ARBL.HA.PC', 'SP.RUR.TOTL.ZS', 'AG.CON.FERT.ZS', 'AG.LND.FRST.ZS']

  data_frames = [] # stores the data frames with the indicator data of interest
  urls = [] # url endpoints for the World Bank API

  # pull data from World Bank API and clean the resulting json
  # results stored in data_frames variable
  for indicator in indicators:
    url = 'http://api.worldbank.org/v2/countries/' + country_filter +\
    '/indicators/' + indicator + '?date=1990:2015&per_page=1000&format=json'
    urls.append(url)

    try:
      r = requests.get(url)
      data = r.json()[1]
    except:
      print('could not load data ', indicator)

    for i, value in enumerate(data):
      value['indicator'] = value['indicator']['value']
      value['country'] = value['country']['value']

    data_frames.append(data)
  
  # first chart plots arable land from 1990 to 2015 in top 10 economies 
  # as a line chart
  graph_one = []
  df_one = pd.DataFrame(data_frames[0])

  # filter and sort values for the visualization
  # filtering plots the countries in decreasing order by their values
  df_one = df_one[(df_one['date'] == '2015') | (df_one['date'] == '1990')]
  df_one.sort_values('value', ascending=False, inplace=True)

  # this  country list is re-used by all the charts to ensure legends have the same
  # order and color
  countrylist = df_one.country.unique().tolist()
  
  for country in countrylist:
      x_val = df_one[df_one['country'] == country].date.tolist()
      y_val =  df_one[df_one['country'] == country].value.tolist()
      graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

  layout_one = dict(title = 'Change in Arable Land (Hectares per Person) <br> from 1990 to 2015',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=1990, dtick=25, showgrid=True),
                yaxis = dict(title = 'Hectares', dtick=0.2, showgrid=True),
                )
  
  # Second bar chart shows rural population vs arable land as percents
  graph_two = []
  df_two = pd.DataFrame(data_frames[2])
  df_two = df_two[(df_two['date'] == '2015')]

  df_two.sort_values('value', ascending=False, inplace=True)

  graph_two.append(
          go.Bar(
          x = df_two.country.tolist(),
          y = df_two.value.tolist(),
          )
      )

  layout_two = dict(title = 'Fertilizer Consumption (Kilograms per Hectare <br> of Arable Land) in 2015',
                xaxis = dict(title = 'Country',),
                yaxis = dict(title = 'Fertilizer Consumption'),
                )

  
  # third chart plots percent of population that is rural from 1990 to 2015
  graph_three = []
  df_three = pd.DataFrame(data_frames[1])
  df_three = df_three[(df_three['date'] == '2015')]

  df_three.sort_values('value', ascending=False, inplace=True)

  graph_three.append(
          go.Bar(
          x = df_three.country.tolist(),
          y = df_three.value.tolist(),
          )
      )

  layout_three = dict(title = 'Rural Population (% of Population) in 2015',
                xaxis = dict(title = 'Country',),
                yaxis = dict(title = 'Percent'),
                )

  # fourth change of forest land area(% of land use) as a line chart
  graph_four = []
  df_four = pd.DataFrame(data_frames[3])

  # filter and sort values for the visualization
  # filtering plots the countries in decreasing order by their values
  df_four = df_four[(df_four['date'] == '2015') | (df_four['date'] == '1990')]
  df_four.sort_values('value', ascending=False, inplace=True)
    
  for country in countrylist:
      x_val = df_four[df_one['country'] == country].date.tolist()
      y_val =  df_four[df_one['country'] == country].value.tolist()
      graph_four.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

  layout_four = dict(title = 'Change in Forest Land (% of Land Area) <br> from 1990 to 2015',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=1990, dtick=25),
                yaxis = dict(title = 'Percent'),
                )  


  # append all charts
  figures = []
  figures.append(dict(data=graph_one, layout=layout_one))
  figures.append(dict(data=graph_two, layout=layout_two))
  figures.append(dict(data=graph_three, layout=layout_three))
  figures.append(dict(data=graph_four, layout=layout_four))

  return figures
