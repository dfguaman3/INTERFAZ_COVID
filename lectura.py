import pandas as pd
import numpy as np
import requests,json,urllib
url1='public/data/owid-covid-data.csv'
url='https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.json'
#data = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv", parse_dates=['date'], index_col='date')

try:
    response = urllib.request.urlopen(url).read().decode()
    datos = json.dumps(response)
    datos2=json.loads(datos)
    
    print(datos2['ALB']['data'][3])
    #print(datos['ALB']['data'][3]['date'])
    
    
    
except Exception as e:
    print(e)