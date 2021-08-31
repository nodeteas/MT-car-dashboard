#!/usr/bin/python

import plotly.express as px
from app import data_preprocess


dataset = data_preprocess()

# figures
# Price to Miles
mil_to_price_fig = px.scatter(dataset,
                              x=dataset["mileage"],
                              y=dataset["price"],
                              color="year",
                              title="Price of Used Cars"
                              )

mil_to_price_fig.update_layout(
    title_x=0.5,
    font_color="#f72585",
    width=750
)

mil_to_price_fig.update_xaxes(title="total mileage (in miles)", showline=True, linewidth=2, linecolor='black')
mil_to_price_fig.update_yaxes(title="price ($)", tickprefix="$", showline=True, linewidth=2, linecolor='black')

# make to volume graph
vol_to_make_fig = px.bar(dataset["make"].value_counts(), title="Volume by Make", orientation='h')
vol_to_make_fig.update_layout(
    title_x=0.5,
    font_color="#f72585",
    showlegend=False
)
vol_to_make_fig.update_traces(marker_color='#6930c3')
vol_to_make_fig.update_xaxes(title="volume", showline=True, linewidth=2, linecolor='black')
vol_to_make_fig.update_yaxes(title="make", showline=True, linewidth=2, linecolor='black')