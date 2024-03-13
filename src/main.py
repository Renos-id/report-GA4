import os
from datetime import datetime, timedelta
from google.analytics.data_v1beta import BetaAnalyticsDataClient, types
import auth
import api_request
import data_processing
import pandas as pd
from dotenv import load_dotenv
from postgres import send_to_postgres

# Load environment variables from .env file
load_dotenv()

# Set your credentials file path
credentials_path = os.getenv('CREDENTIALS_PATH')

# Authenticate with Google API
credentials = auth.authenticate(credentials_path)

# Set your GA4 property ID
property_id = os.getenv('GA4_PROPERTY_ID')

# Get PostgreSQL table name and schema from environment variable
table_name = os.getenv('POSTGRES_TABLE_NAME')
schema_name = os.getenv('POSTGRES_SCHEMA_NAME')

# Create GA4 client
client = BetaAnalyticsDataClient(credentials=credentials)

# Get start and end dates for data retrieval
start_date = datetime(2023, 10, 1)
end_date = datetime.now()

# Iterate over monthly intervals
while start_date < end_date:
    # Calculate end of current month
    end_of_month = (start_date.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    end_of_month = min(end_of_month, end_date)

    # Construct the API request
    response = api_request.run_report(client, property_id, [types.Dimension(name="yearMonth")],
                                       [types.Metric(name="activeUsers")],
                                       [types.DateRange(start_date=start_date.strftime("%Y-%m-%d"),
                                                        end_date=end_of_month.strftime("%Y-%m-%d"))])

    # Process the response
    df = data_processing.process_response(response)

    # Combine schema and table name
    full_table_name = f'{schema_name}.{table_name}'

    # Send DataFrame to PostgreSQL with schema and table name
    send_to_postgres(df, full_table_name, append=True)

    # Move to next month
    start_date = end_of_month + timedelta(days=1)