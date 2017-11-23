#!/usr/bin/python2.7

import pandas as pd 
import time
import math
import datetime
import pandas_datareader.data as web

start = datetime.datetime(2017, 1, 1)
end = datetime.datetime(2017, 11, 1)

def get_std_deviation(name):

	df = web.DataReader(name, "yahoo", start, end)

	number  = 0
	sum = 0
	for i in df['High']:
		sum = sum + i
		number = 1 + number
	avg = sum/number

	sum_for_variance = 0
	for i in df['High']:
		sum_for_variance = sum_for_variance + (i-avg)**2
	variance = sum_for_variance/number
	std_dev = math.sqrt(variance)

	return std_dev

print(get_std_deviation('SAP'))


