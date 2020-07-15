from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import numpy as np
import pandas as pd
# or: requests.get(url).content

#dates = np.arange(2017,2018)
#dates = np.concatenate((dates, np.array([201800]*12)+np.arange(1,13)))
#dates = np.concatenate((dates, np.array([201900]*12)+np.arange(1,13)))
#dates = np.concatenate((dates, np.array([202000]*5)+np.arange(1,6)))
dates = np.array([201800]*12)+np.arange(1, 13)

df = pd.DataFrame()
for date in dates:
    print(f'Processing {date}')
    resp = urlopen(f"https://s3.amazonaws.com/capitalbikeshare-data/{date}-capitalbikeshare-tripdata.zip")
    zf = ZipFile(BytesIO(resp.read()))
    for file in zf.filelist:
        if 'csv' in file.filename:
            df_token = pd.read_csv(zf.open(file))
            df = df.append(df_token)

df.to_csv('capitalbikeshare.csv')
