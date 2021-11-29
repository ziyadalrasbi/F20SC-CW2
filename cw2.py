import json
import matplotlib.pyplot as plt
import pycountry_convert as pc
import pandas as pd

#create a empty list called data
data = []

# empty list for getting countries for task 2
countries = [];
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


##test
#for every object "visitor country in data, print it
for x in data:
    print(x["visitor_country"])

def display_views_by_country(doc_uuid): 
    for viewer in data:
        try:
            if (viewer['env_doc_id'] == doc_uuid):
                viewer_country = viewer['visitor_country']
                countries.append(viewer_country)
        except Exception:
            pass # do something here for the exception
    
    plt.xlabel('country')
    plt.ylabel('amount')
    plt.hist(countries)
    plt.show()

def display_views_by_continent():
    continents = []
    for i in countries:
        try:
            temp_continent = pc.country_alpha2_to_continent_code(i)
            continents.append(temp_continent)
        except Exception:
            pass # another exception
    
    plt.xlabel('continents')
    plt.ylabel('amount')
    plt.hist(continents)
    plt.show()




# testing the functions here
display_views_by_country('140228202800-6ef39a241f35301a9a42cd0ed21e5fb0')
display_views_by_continent()