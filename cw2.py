import json

#create a empty list called data
data = []

#open the json file and call it file
file = open("test.json", 'r')
Lines = file.readlines()

#for every line in the json file
for line in Lines:
    #y = a dictionary of every json object
    y = json.loads(line)
    #add the json objects to the list "data"
    data.append(y)
    
file.close()



#for every object "visitor country in data, print it
for x in data:
    print(x["visitor_country"])

