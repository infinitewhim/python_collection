import time

try:
	f = open('/home/vagrant/Desktop/python/news.txt', 'r')
	# readlines(): read all the lines.   readline(): read one line
	for line in f.readlines():
		print(line)
		time.sleep(0.5)
except IOException:
	print('no such file exists')
finally:
	if f:
		f.close()
