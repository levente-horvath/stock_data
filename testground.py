import requests
import pandas as pd
import numpy as np
import json




response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=ANET&apikey=I18IBEWALO9VW521")

print(response.status_code)
print(response.text)


#dict
data = json.loads(response.text)

df = pd.DataFrame(data)

#print(df.info())


df.to_csv("output.csv")


