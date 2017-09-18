import requests
import os
from bs4 import BeautifulSoup

url = 'https://www.irishtimes.com/' 
source = requests.get(url).text
soup = BeautifulSoup(source,'lxml')

f = open('/home/vagrant/Desktop/python/news.txt', 'a')

for link in soup.findAll('span',class_='h2'):
	#strip() can remove whitespace from the beginning and end of a string
	str1 = link.string.encode('utf-8').strip()
	f.write(str1+'\n\n')
f.close()
			
os.system('/usr/local/hadoop/bin/hdfs dfs -put /home/vagrant/Desktop/python/news.txt input')
