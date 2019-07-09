y = []
x = set()
for q in range(5):
	print (q)
	y.append(q)
	x.add(q)
	for i in range(7):
		print (i)
		y.append(i)
		x.add(i)

print("Length" + str(len(x)))
print(x)