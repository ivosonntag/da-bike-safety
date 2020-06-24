import pandas as pd
from urllib.request import urlopen

dc_crashdata = urlopen('https://prod-hub-indexer.s3.amazonaws.com/files/70392a096a8e431381f1f692aaa06afd/24/full/4326/70392a096a8e431381f1f692aaa06afd_24_full_4326.csv')
df = pd.DataFrame(dc_crashdata)
df.to_csv('DC_accidents.csv')


