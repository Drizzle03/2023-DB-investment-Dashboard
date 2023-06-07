import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

yf.pdr_override()

# Define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']



# Add your service account file
creds = ServiceAccountCredentials.from_json_keyfile_name('db-investment-1c34891f7025.json', scope)

# Authorize the clientsheet 
client = gspread.authorize(creds)

# Get the instance of the Spreadsheet
sheet = client.open('DB-Dashboard') 
# List of your tickers
tickers = ['^KS11', '^KQ11', '^GSPC', '^STOXX50E', '^N225', '000300.SS', '^TNX', 'LQD', 'BNDX', 'GLD', 'CL=F', 'SHY']

# Define date range
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Get data and upload to Google Sheets
for ticker in tickers:
    data = pdr.get_data_yahoo(ticker, start_date, end_date)
    # Create a new worksheet with the name of today's date
    date_today = datetime.today().strftime("%Y.%m.%d")
    worksheet = sheet.add_worksheet(title=date_today, rows="100", cols="20")
    # Get the data and transpose it to columns
    data_to_upload = data['Close'].transpose()
    # Use the .set method and the list of lists variable to update the sheet
    worksheet.insert_rows(data_to_upload.values.tolist(), row=1)