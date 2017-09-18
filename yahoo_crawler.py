import urllib2
from bs4 import BeautifulSoup

symbolslist = ['SAP','MSFT','ORCL','IBM','AMZN','GOOG','FB']

i = 0
while i<len(symbolslist):
	url = 'https://finance.yahoo.com/quote/' + symbolslist[i] + '?p='+ symbolslist[i]
	source = urllib2.urlopen(url).read()
	soup = BeautifulSoup(source,'lxml')
	
	price = soup.find('span',class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')
	
	if len(symbolslist[i])==4:
		print('the price of '+symbolslist[i]+' is: '+ price.text)
	if len(symbolslist[i])==3:
		print('the price of '+symbolslist[i]+'  is: '+ price.text)
	if len(symbolslist[i])==2:
		print('the price of '+symbolslist[i]+'   is: '+ price.text)
	i+=1
	
