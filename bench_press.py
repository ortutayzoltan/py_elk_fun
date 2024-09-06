#!/usr/bin/python3
from elasticsearch import Elasticsearch
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource
import pandas as pd
from datetime import datetime

es = Elasticsearch("http://localhost:9200")
# Example search query

data = es.esql.query( query="""
FROM fitnotes 
| WHERE Exercise == \"Flat Barbell Bench Press\" AND Date > \"2021-01-01\"
| EVAL Volume = Weight * Reps
| STATS total = SUM(Volume) BY Date
| KEEP Date, total
| SORT Date
| LIMIT 1000""",  format="json")

#print(data)
print("Reading data from elasticsearch is done.")

# Convert the values into a DataFrame
df = pd.DataFrame(data['values'], columns=['Date', 'Volume'])

# Convert Date from string to datetime
df['Date'] = pd.to_datetime(df['Date'])

source = ColumnDataSource(df)

# Create a Bokeh figure
p = figure(x_axis_type="datetime", title="Bench Press Progress", 
           x_axis_label='Date', y_axis_label='Daily Total Volume (kg)',
           width = 1200, height = 627)

# Plot the weight lifted over time
p.line(x='Date', y='Volume', source=source, line_width=2, legend_label="Daily Total Volume (kg)")
p.scatter(x='Date', y='Volume', size=8, source=source, legend_label="Daily Total Volume (kg)", fill_color="white")

# Add tooltips and customize appearance
p.legend.location = "top_left"
p.legend.click_policy="hide"

# Output to file
output_file("bench_press_progress.html")

show(p)
print("Saving the figure is done.")