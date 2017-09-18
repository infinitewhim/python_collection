import requests
from bs4 import BeautifulSoup
from collections import Iterator

url = 'https://www.lottery.ie/dbg/results/view?game=euromillions&draws=0'
source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')

f = open('/home/vagrant/Desktop/python/euromilresult.txt', 'a')
odd = 2

#attrs={'name':'form_build_id', 'type':'hidden'}
it = iter(soup.findAll('input', attrs={'name':'picknumber'}))
#print(isinstance(iter(soup.findAll('input', attrs={'name':'picknumber'})),Iterator))


def getDraw():
	counter = 0
	#use the global variable "odd" defined earlier
	global odd
	if(odd%2 == 0):
		draw = []
		while(counter<7):
			value = next(it).get('value')
			draw.append(value)
			counter = counter + 1
		
		print(' '.join(draw))
	else:
		draw = []
		while(counter<5):
			value = next(it).get('value')
			draw.append(value)
			counter = counter + 1
		
		print(' '.join(draw))

	odd = odd + 1

while True:
    try:
        getDraw()

    except StopIteration:
        break
