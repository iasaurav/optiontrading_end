
from datetime import datetime
month = datetime.now().strftime("%b%Y").lower()
print(month)


# Step 1: Download the Nifty 500 list
import requests
url = "https://nsearchives.nseindia.com/content/nsccl/mpl_"+month+".csv"
headers = {'User-Agent': 'Mozilla/5.0'}

# Download and save CSV
response = requests.get(url, headers=headers)
if response.status_code == 200:
    with open("fnostock.csv", "wb") as file:
        file.write(response.content)
else:
    print("Download failed.")
import pandas as pd
df = pd.read_csv("fnostock.csv")


df["segment"]="NFO-OPT"
df["ticker"]=df["UNDERLYING_NAME"]+".NS"

df.rename(columns={
    'UNDERLYING_NAME': 'name',


}, inplace=True)

df=df[['name','segment','ticker']]





tickers = [
    {"name": "NIFTY", "segment": "NFO-OPT"},
    {"name": "FINNIFTY","segment": "NFO-OPT"},
    {"name": "BANKNIFTY","segment": "NFO-OPT"},
    {"name": "SENSEX","segment": "BFO-OPT"},
    {"name": "BANKEX","segment": "BFO-OPT"}
    

]


ticker = pd.DataFrame(tickers)

combo_df = pd.concat([ticker,df])

print(combo_df)
# Save the filtered data
combo_df.to_excel("option.xlsx", index=False)


import os

file_path = "fnostock.csv"

if os.path.exists(file_path):
    os.remove(file_path)
    print("File deleted successfully")
else:
    print("File not found")



import pandas as pd

# Read instrument data
option = pd.read_csv("https://api.kite.trade/instruments").iloc[:, 1:]


# Assuming the column name is 'Name' in both files
filtered_kite_df = option[option['name'].isin(combo_df['name'])&option['segment'].isin(combo_df['segment'])]

print(filtered_kite_df)
