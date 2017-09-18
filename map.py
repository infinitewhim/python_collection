def f(x):
	return x*x

#result of map is an Iterator
#Iterator is lazy-computation
#so we use list to calculate the final result
print(list(map(f,[1,2,3,4])))
