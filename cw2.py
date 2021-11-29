import json
import matplotlib.pyplot as plt
import pycountry_convert as pc
import pandas as pd

#create a empty list called data
data = []

# empty list for getting countries for task 2
countries = []

browsers = []
#open the json file and call it dataset
dataset = open("testlarge.json", 'r')
Lines = dataset.readlines()

#for every line in the json file
for line in Lines:
    #y = a dictionary of every json object
    dataDict = json.loads(line)
    #add the json objects to the list "data"
    data.append(dataDict)
    
dataset.close()

#doc_uuid = input("Please enter the doc ID")



def display_views_by_country(): 
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

def display_views_by_browser(doc_uuid): 
    for viewer in data:
        try:
            if (viewer['env_doc_id'] == doc_uuid):
                viewer_browser = viewer['visitor_useragent'].split('/')[0]
                
                browsers.append(viewer_browser)
        except Exception:
            pass # do something here for the exception
    
    plt.xlabel('browser')
    plt.ylabel('amount')
    plt.hist(browsers)
    plt.show()

def display_viewtime_by_userid(doc_uuid):
    
    visitor_ids = list(set([visitor['visitor_uuid'] for visitor in data]))
    viewtime = dict([(visitor, 0) for visitor in visitor_ids])
    for id in viewtime:
        for viewer in data:
            try:
                if (id == viewer['visitor_uuid']):
                    temp_readtime = viewer['event_readtime']
                    temp_readtime += viewer['event_readtime']
                    viewtime[id] = temp_readtime
            except Exception:
                pass
    
    time_sorted = list(sorted(viewtime.items(), key=lambda kv: kv[1], reverse=True))[:10]
    users = []
    times = []

    for viewer in time_sorted:
        users.append(viewer[0])
        times.append(viewer[1])

    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('viewer ID')
    plt.ylabel('time spent')
    plt.bar(users, times)
    plt.show()


# testing the functions here
#display_views_by_country(doc_uuid)
#display_views_by_continent()
display_viewtime_by_userid("130927071110-0847713a13bea63d7f359ea012f3538d")
