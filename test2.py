x = {"one": "1", "two" : "2"}
y = {"one": "1", "two" : "2", "three" : "3"}

xSet = set(x)
ySet = set(y)
if xSet.issubset(ySet) == True:
	print("Yes!")