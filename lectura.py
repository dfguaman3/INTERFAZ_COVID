import pandas as pd
import numpy as np
import matplotlib as plt
data = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv", parse_dates=['date'], index_col='date')

print(data.location)
