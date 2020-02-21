approved = open('approvedusers.txt','r')

for line in approved: 
	data = approved.readline()
	print(data)