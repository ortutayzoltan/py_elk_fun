#!/usr/bin/python3
from elasticsearch import Elasticsearch, ConnectionError, NotFoundError, RequestError
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource
import pandas as pd
from datetime import datetime
import sys

def connect_to_elasticsearch():
    try:
        es = Elasticsearch("http://localhost:9200")
        # Test the connection
        if not es.ping():
            raise ConnectionError("Could not connect to Elasticsearch")
        return es
    except ConnectionError as e:
        print(f"❌ Failed to connect to Elasticsearch: {str(e)}")
        print("📝 Please check that:")
        print("  - Elasticsearch is running on localhost:9200")
        print("  - You have network connectivity to the Elasticsearch server")
        sys.exit(1)

def fetch_bench_press_data(es):
    try:
        query = """
        FROM fitnotes 
        | WHERE Exercise == "Flat Barbell Bench Press" AND Date > "2021-01-01"
        | EVAL Volume = Weight * Reps
        | STATS total = SUM(Volume) BY Date
        | KEEP Date, total
        | SORT Date
        | LIMIT 1000
        """
        
        data = es.esql.query(query=query, format="json")
        print("✅ Successfully fetched data from Elasticsearch")
        return data
        
    except NotFoundError:
        print("❌ Index 'fitnotes' not found!")
        print("📝 Make sure you have:")
        print("  - Created the 'fitnotes' index in Elasticsearch")
        print("  - Indexed your workout data")
        sys.exit(1)
    except RequestError as e:
        print(f"❌ Error in the ESQL query: {str(e)}")
        print("📝 Common causes:")
        print("  - Missing or incorrect field names")
        print("  - Syntax errors in the ESQL query")
        print("  - Data type mismatches")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error while fetching data: {str(e)}")
        sys.exit(1)

def create_visualization(data):
    try:
        # Convert the values into a DataFrame
        df = pd.DataFrame(data['values'], columns=['Date', 'Volume'])
        
        # Convert Date from string to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        source = ColumnDataSource(df)
        
        # Create a Bokeh figure
        p = figure(x_axis_type="datetime", title="Bench Press Progress", 
                  x_axis_label='Date', y_axis_label='Daily Total Volume (kg)',
                  width=1200, height=627)
        
        # Plot the weight lifted over time
        p.line(x='Date', y='Volume', source=source, line_width=2, 
               legend_label="Daily Total Volume (kg)")
        p.scatter(x='Date', y='Volume', size=8, source=source, 
                 legend_label="Daily Total Volume (kg)", fill_color="white")
        
        # Add tooltips and customize appearance
        p.legend.location = "top_left"
        p.legend.click_policy = "hide"
        
        # Output to file
        output_file("bench_press_progress.html")
        show(p)
        print("✅ Successfully created and saved the visualization")
        
    except Exception as e:
        print(f"❌ Error creating visualization: {str(e)}")
        print("📝 This might be due to:")
        print("  - Invalid data format")
        print("  - Missing required data fields")
        print("  - Permission issues writing the output file")
        sys.exit(1)

def main():
    print("🏋️‍♂️ Starting Bench Press Progress Analysis...")
    
    # Connect to Elasticsearch
    es = connect_to_elasticsearch()
    
    # Fetch the data
    data = fetch_bench_press_data(es)
    
    # Create and save the visualization
    create_visualization(data)
    
    print("✨ Analysis complete! Check bench_press_progress.html for your visualization")

if __name__ == "__main__":
    main()