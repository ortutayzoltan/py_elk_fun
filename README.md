# py_elk_fun 🏋️‍♂️

A Python project that leverages Elasticsearch to store and analyze workout data, with a focus on visualizing bench press progress over time.

## Features

- Query workout data from Elasticsearch using ESQL
- Generate interactive visualizations of bench press progress using Bokeh
- Track daily workout volume and progress over time
- Export visualizations to HTML for easy sharing

## Prerequisites

- Python 3.x
- Elasticsearch running locally on port 9200
- Required Python packages:
  - elasticsearch
  - bokeh
  - pandas

## Project Structure

- `basic_test.py` - Simple script to test Elasticsearch connectivity and basic queries
- `esql_test.py` - Example of using ESQL (Elasticsearch SQL) for data querying
- `bench_press.py` - Main script that generates an interactive visualization of bench press progress
- `bench_press_progress.html` - Generated visualization output

## Setup & Usage

1. Ensure Elasticsearch is running locally:
```bash
# Elasticsearch should be running on
http://localhost:9200
```

2. Install required Python packages:
```bash
pip install elasticsearch bokeh pandas
```

3. Run the bench press analysis:
```bash
python3 bench_press.py
```

The script will:
- Query workout data from the "fitnotes" index
- Calculate daily total volume (Weight × Reps)
- Generate an interactive plot showing progress over time
- Save the visualization to `bench_press_progress.html`

## Example Query

The project uses ESQL for data querying. Here's an example query used in `bench_press.py`:

```sql
FROM fitnotes 
| WHERE Exercise == "Flat Barbell Bench Press" AND Date > "2021-01-01"
| EVAL Volume = Weight * Reps
| STATS total = SUM(Volume) BY Date
| KEEP Date, total
| SORT Date
| LIMIT 1000
```

## Data Structure

The project expects workout data to be stored in an Elasticsearch index named "fitnotes" with the following fields:
- Date
- Exercise
- Weight
- Reps

## Contributing

Feel free to submit issues and enhancement requests!