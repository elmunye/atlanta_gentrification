# let's create a streamlit app a basic steamlit app
# to show the gentrification index

import streamlit as st
import pandas as pd
import numpy as np
import requests
import censusdis.data as ced
from censusdis import states
import addfips

# Title
st.title('Gentrification Index for Georgia by County')

# Header
st.header('Is your neighborhood gentrifying?')

# Subheader
st.subheader('Check how much your county is gentrifying')

# Load data
download_variables=['NAME', 'B15003_022E', 'B25077_001E']
df_2022 = ced.download(

    # Data set: American Community Survey 5-Year
    dataset='acs/acs5',

    # Vintage: 2022
    vintage=2022,

    # Variable: median household income
    download_variables=download_variables,

    # Geography: Georgia State
    state=states.GA,
    county="*",

    with_geometry=True
)

df_2018 = ced.download(

    # Data set: American Community Survey 5-Year
    dataset='acs/acs5',

    # Vintage: 2018
    vintage=2018,

    # Variable: median household income
    download_variables=download_variables,

    # Geography: Georgia State
    state=states.GA,
    county="*",

    with_geometry=True
)


df_2018['year'] = 2018
df_2022['year'] = 2022

df_2018.rename(columns={'B15003_022E': 'median_bachelor_edu', 'B25077_001E': 'median_home_value'}, inplace=True)
df_2022.rename(columns={'B15003_022E': 'median_bachelor_edu', 'B25077_001E': 'median_home_value'}, inplace=True)

df_2018 = df_2018.sort_values(by='COUNTY')
df_2022 = df_2022.sort_values(by='COUNTY')

df_2022['change_median_bachelor_edu'] = (df_2022['median_bachelor_edu'] - df_2018['median_bachelor_edu']) / df_2018['median_bachelor_edu']
df_2022['change_median_home_value'] = (df_2022['median_home_value'] - df_2018['median_home_value']) / df_2018['median_home_value']

min_value_bachelor_edu = df_2022['change_median_bachelor_edu'].min()
adjusted_min_value = abs(min_value_bachelor_edu) + 1
df_2022['change_median_bachelor_edu'] += adjusted_min_value

min_value_home_value = df_2022['change_median_home_value'].min()
adjusted_min_value_home = abs(min_value_home_value) + 1
df_2022['change_median_home_value'] += adjusted_min_value_home

df_2022['change_median_bachelor_edu'] = df_2022['change_median_bachelor_edu'] / df_2022['change_median_bachelor_edu'].max()
df_2022['change_median_home_value'] = df_2022['change_median_home_value'] / df_2022['change_median_home_value'].max()

df_2022['gentrification_index'] = df_2022['change_median_bachelor_edu'] * df_2022['change_median_home_value']

df_2022 = pd.get_dummies(df_2022, columns=['NAME'])
df_2022.columns = df_2022.columns.str.replace('NAME_', '')


df_2022_copy = df_2022.copy()
df_2022_copy = df_2022_copy.drop(df_2022_copy[df_2022_copy['gentrification_index'] == df_2022_copy['gentrification_index'].max()].index)

#provide now the colum with th ehighest gentrification_index
df_2022_copy[df_2022_copy['gentrification_index'] == df_2022_copy['gentrification_index'].max()]


import censusdis.maps as cem

#let us plot ax which we define below
ax = cem.plot_us(
    df_2022_copy,
    'gentrification_index',

    # Styling with Matplotlib **kwargs
    cmap='hot',
    edgecolor='#333',
    linewidth=0.5,

    legend=True,
    figsize=(12, 6)
)

ax.axis('off')

st.pyplot(ax.figure)







