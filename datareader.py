#!/usr/bin/python2.7

import pandas as pd 
import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt 
from matplotlib import style
 
style.use('fivethirtyeight')

start = datetime.datetime(2017,1,1)
end = datetime.datetime(2017,9,10)

df = web.DataReader('SAP','yahoo',start,end)
df['High'].plot()
plt.legend()
plt.show()
