import os
import pandas as pd
import itertools
import gspread
from oauth2client.service_account import ServiceAccountCredentials

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\mohanprasath.dhana\Downloads\microservices-377309-b91430eceded.json'

from google.analytics.data import BetaAnalyticsDataClient
from google.oauth2.service_account import Credentials
from google.analytics.data import DateRange, Dimension, Metric, RunReportRequest
import pandas as pd

client = BetaAnalyticsDataClient()

def run_custom_report(property_id,dimensions,metrics):

    credentials_file = r'C:\Users\mohanprasath.dhana\Downloads\microservices-377309-b91430eceded.json'

    # Initialize a Credentials object from the service account JSON key file
    credentials = Credentials.from_service_account_file(credentials_file)

    # Initialize the BetaAnalyticsDataClient
    client = BetaAnalyticsDataClient(credentials=credentials)
dimensions = [
        "date",
        "sessionCampaignName",
        "sessionSource",
        "hostName",
] 

metrics =[
    "sessions",
    "addToCarts",
    "checkouts",
    "transactions",
    "purchaseRevenue"
]


property_id = '372384988'  # Replace with your Google Analytics 4 property ID

# Call the function with dimensions, metrics, and property ID
#run_custom_report(property_id, dimensions, metrics)

df = run_custom_report(property_id,dimensions,metrics)


credentials_file = r'C:\Users\mohanprasath.dhana\Downloads\microservices-377309-b91430eceded.json'

    # Initialize a Credentials object from the service account JSON key file
credentials = Credentials.from_service_account_file(credentials_file)

    # Initialize the BetaAnalyticsDataClient
client = BetaAnalyticsDataClient(credentials=credentials)

    
request = RunReportRequest(
    property=f'properties/{property_id}',
    dimensions=[Dimension(name=dimension) for dimension in dimensions],
    metrics=[Metric(name=metric) for metric in metrics],
    date_ranges=[DateRange(start_date='5daysAgo', end_date='yesterday')]
)
response = client.run_report(request)

session_source_data = []

for row in response.rows:
    if row.dimension_values[2].value == 'sessionSource':
        session_source_data.append(['Source'])
    elif row.dimension_values[2].value.lower() in ['organic', 'direct', 'referral', 'not set']:
        session_source_data.append(['Organic'])
    elif row.dimension_values[2].value.lower() in ['facebook', 'fb']:
        session_source_data.append(['Facebook'])
    elif row.dimension_values[2].value.lower() in ['google']:
        session_source_data.append(['Google'])
    else:
        session_source_data.append(['Other'])

def ga4_result_to_df(response):
    """Original: print_run_report_response: Prints results of a runReport call. v2.1 changed by Bram to create DataFrame"""
    result_dict = {}  
    for dimensionHeader in response.dimension_headers:
        result_dict[dimensionHeader.name] = []
    for metricHeader in response.metric_headers:
        result_dict[metricHeader.name] = []
    for rowIdx, row in enumerate(response.rows):
        for i, dimension_value in enumerate(row.dimension_values):
            dimension_name = response.dimension_headers[i].name
            result_dict[dimension_name].append(dimension_value.value)
        for i, metric_value in enumerate(row.metric_values):
            metric_name = response.metric_headers[i].name
            result_dict[metric_name].append(metric_value.value)
    return pd.DataFrame(result_dict)

df = ga4_result_to_df(response)
df

SPREADSHEET_ID = '17FAhYjfUIESQBi_bWkb2XdU2QJOcxHzs-9iiQpXrHNc'

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE = r'C:\Users\mohanprasath.dhana\Downloads\microservices-377309-b91430eceded.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE, SCOPES)

gc = gspread.service_account(filename=KEY_FILE)
sh = gc.open_by_key(SPREADSHEET_ID)
worksheet = sh.sheet1  # Use the first sheet or specify your sheet name



    # Prepare data for Google Sheets
values = []

    # Extract headers
headers = [header.name for header in response.dimension_headers] + [header.name for header in response.metric_headers]
values.append(headers)

    # Extract rows
for row in response.rows:
  row_values = [dimension.value for dimension in row.dimension_values] + [metric.value for metric in row.metric_values]
  values.append(row_values)

    # Append data to the worksheet
worksheet.update('A1', values)

print("Data loaded into Google Sheet successfully.")



    # Prepare data for Google Sheets
values = []

    # Extract headers
headers = [header.name for header in response.dimension_headers] + [header.name for header in response.metric_headers]
values.append(headers)

    # Extract rows
for row in response.rows:
  row_values = [dimension.value for dimension in row.dimension_values] + [metric.value for metric in row.metric_values]
  values.append(row_values)

    # Append data to the worksheet
worksheet.update('A1', values)

print("Data loaded into Google Sheet successfully.")