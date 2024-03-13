import pandas as pd

def process_response(response):
    data = []
    for row in response.rows:
        year_month = row.dimension_values[0].value
        active_users = row.metric_values[0].value
        data.append({'Year-Month': year_month, 'Active Users': active_users})
    df = pd.DataFrame(data).sort_values(by='Year-Month').reset_index(drop=True)
    return df