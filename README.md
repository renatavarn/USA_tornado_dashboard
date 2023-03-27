# Tornadoes in the USA – doashboard with Plotly Dash 

Building an interactive dashboard app to visualize historical data of tornadoes for each state in the USA, 1954-2013.

## Data 

The `data.csv` dataset represents tornado tracks in the United States, Puerto Rico, and the U.S. Virgin Islands, from 1954 to 2013. Each row represents an individual tornado event including date, geographical coordinates, magnitude, as well as injuries, fatalities and crop loss caused by the tornado.  

Dataset was obtained from [Kagle](https://www.kaggle.com/datasets/thedevastator/1950-2013-north-america-tornadoes-historical-tra). The [original dataset](https://data.world/dhs/historical-tornado-tracks) was provided by the Homeland Infrastructure Foundation. Data in this repository was filtered for years 1954-2013, due to missing magnitude data between 1950-1953. 


## To run the app 

1. Download `code_dashboard.py` and `data.csv` files
2. Create a project folder with PyCharm with the two files
3. Install libraries below to your environment
4. Click on the generated URL to run the app on browser

```
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
```

Check out the `notebook_data_viz.ipynb` file for how the graphs for the dashboard were created! 


## App demo 
![](demo.gif)
