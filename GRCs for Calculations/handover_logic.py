connected_to = 'X'
tres = 1
a = 20 #This variable is changed in real time (when the while loop is running based on the distance of the receiver from the access point A)
b = 15 #This variable is changed in real time (when the while loop is running based on the distance of the receiver from the access point B)


#Inital Connection
if a > b:
	connected_to = 'A'
	tres = 0.8
else:
	connected_to ='B'
	tres = 1.25

#After initial connection is made

while True:
	if connected_to == 'A':
		if A/B > tres:
			connected_to = 'A'
			print('Connection retained with A')
		else:
			connected_to = B
			tres =1.25

	else:
		if A/B < tres:
			connected_to = 'B'
			print('Connection retained with B')
		else:
			connected_to ='A'
			tres = 0.8