import json
import matplotlib.pyplot as plt
import pycountry_convert as pc
import pandas as pd
from collections import Counter
import graphviz
import httpagentparser
import re
from tkinter import *

#create a empty list called data
data = []

# empty list for getting countries for task 2






#open the json file and call it dataset
dataset = open("tests.json", 'r', encoding='utf-8')
Lines = dataset.readlines()

#for every line in the json file
for line in Lines:
    #y = a dictionary of every json object
    dataDict = json.loads(line)
    #add the json objects to the list "data"
    data.append(dataDict)
    
dataset.close()

#doc_uuid = input("Please enter the doc ID")


# Task 2
class Task2:
    countries = []
    def __init__(self, doc_uuid, isPressed, list=[]):
        self.isPressed = isPressed
        self.doc_uuid = doc_uuid
        self.countries = list

    def display_views_by_country(self): 
        for viewer in data:
            try:
                if (viewer['event_type'] != 'read'):
                    continue
                if (viewer['env_doc_id'] == self.doc_uuid):
                    viewer_country = viewer['visitor_country']
                    self.countries.append(viewer_country)
            except Exception:
                pass # do something here for the exception
        if (self.isPressed == True):
            plt.xlabel('country')
            plt.ylabel('amount')
            plt.hist(self.countries)
            plt.show()
        

    def display_views_by_continent(self):
        self.countries = []
        continents = []
        self.isPressed = False
        self.display_views_by_country()
        for i in self.countries:
            try:
                temp_continent = pc.country_alpha2_to_continent_code(i)
                if (temp_continent == "SA"):
                    continents.append("South America")
                if (temp_continent == "NA"):
                    continents.append("North America")
                if (temp_continent == "AS"):
                    continents.append("Asia")
                if (temp_continent == "OC"):
                    continents.append("Oceania")
                if (temp_continent == "AF"):
                    continents.append("Africa")
                if (temp_continent == "EU"):
                    continents.append("Europe")
                if (temp_continent == "AN"):
                    continents.append("Antartica")
            except Exception:
                pass # another exception
        
        plt.xlabel('continents')
        plt.ylabel('amount')
        plt.hist(continents)
        plt.show()

class Task3:
    browsers = []

    def __init__(self, list=[]):
        self.browsers = list
        

    def display_views_by_browser_part_a(self): 
        self.browsers = []
        already_viewed = []
        for viewer in data:
            try:
                if (viewer['event_type'] != 'read'):
                    continue
                # removing duplicate entries
                if (viewer['visitor_uuid'] not in already_viewed): 
                    already_viewed.append(viewer['visitor_uuid'])
                    viewer_browser = viewer['visitor_useragent']
                    # httpagentparser is a parser used to extract info from a user agent
                    # here it is used to detect the browser from the JSON input and extract the browser names
                    test = httpagentparser.simple_detect(viewer_browser)
                    # some more checking to ensure browser names are calculated correctly
                    if "Chrome" in test[1]:
                        self.browsers.append(test[1])
                    elif "Firefox" in test[1] or "Mozilla" in test[1]:
                        self.browsers.append(test[1])
                    elif "Safari" in test[1]:
                        self.browsers.append(test[1])
                    elif "MicrosoftInternetExplorer" in test[1]:
                        self.browsers.append(test[1])
                    elif "UnknownBrowser" in test[1] and "iOS" in test[0]:
                        self.browsers.append(test[1])
                    else:
                        self.browsers.append("Other")
                    
            except Exception:
                pass # do something here for the exception
        # displaying the info
        counter = Counter(self.browsers)
        
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Browser')
        plt.ylabel('Amount')
        plt.bar(counter.keys(), counter.values())
        plt.show()

    def display_views_by_browser_short_a(self):
        self.browsers = []
        #create a list of visitors and make it empty
        vislist = []
        #for every viewer in the dataset
        for viewer in data:
            try:
                #ensure the document is read
                if (viewer['event_type'] != 'read'):
                    continue
                #assign the visitor variable the value of the current viewer's unique ID
                visitor = viewer['visitor_uuid']
                #if the current visitor is not in the list of visitors (if the visitor is not a duplicate entry)
                if visitor not in vislist:
                    #add the current visitor to the list of visitor
                    vislist.append(visitor)
                    #via unique strings that are only found in each browser's specific "visitor_useragent" codes (found at: https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/1)
                    #add each browser to the browsers list
                    if ") Chrome" in viewer['visitor_useragent']:
                        self.browsers.append("Chrome")
                    elif "CriOS" in viewer['visitor_useragent']:
                        self.browsers.append("Chrome")
                    elif "GSA" in viewer['visitor_useragent']:
                        self.browsers.append("Chrome")
                    elif ") Version" in viewer['visitor_useragent']:
                        self.browsers.append("Safari")
                    elif ") Mobile" in viewer['visitor_useragent']:
                        self.browsers.append("AppleWebKit")
                    elif "MSIE" in viewer['visitor_useragent']:
                        self.browsers.append("Internet Explorer")
                    elif "fox" in viewer['visitor_useragent']:
                        self.browsers.append("Firefox")
                    else:
                        self.browsers.append("Other")
            except Exception:
                pass # do something here for the exception
        #using the "Counter" function, count each time a browser has been added to the list and assign that browser an integer value
        counter = Counter(self.browsers)
        #plot the x and y axis
        plt.xlabel('browser')
        plt.ylabel('amount')
        #plot the bar chart using the browser name and the amount of times it appears in the list
        plt.bar(counter.keys(), counter.values())
        #show the bar chart
        plt.show()
        

    def display_views_by_browser_short_b(self): 
        self.browsers = []
        already_viewed = []
        for viewer in data:
            try:
                if (viewer['event_type'] != 'read'):
                    continue
                # removing duplicate entries
                if (viewer['visitor_uuid'] not in already_viewed): 
                    already_viewed.append(viewer['visitor_uuid'])
                    viewer_browser = viewer['visitor_useragent']
                    # httpagentparser is a parser used to extract info from a user agent
                    # here it is used to detect the browser from the JSON input and extract the browser names
                    test = httpagentparser.simple_detect(viewer_browser)
                    # regex to remove empty spaces, numbers, and dot symbols
                    formatted_string = re.sub(r'\d.*', '', test[1])
                    formatted_string = formatted_string.replace(' ', '')
                    # some more checking to ensure browser names are calculated correctly
                    if "Chrome" in formatted_string:
                        self.browsers.append("Chrome")
                    elif "Firefox" in formatted_string or "Mozilla" in formatted_string:
                        self.browsers.append("Firefox")
                    elif "Safari" in formatted_string:
                        self.browsers.append("Safari")
                    elif "MicrosoftInternetExplorer" in formatted_string:
                        self.browsers.append("MSIE")
                    elif "UnknownBrowser" in formatted_string and "iOS" in test[0]:
                        self.browsers.append("AppleWebKit")
                    else:
                        self.browsers.append("Other")
                    
            except Exception:
                pass # do something here for the exception
        # displaying the info
        counter = Counter(self.browsers)
        
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Browser')
        plt.ylabel('Amount')
        plt.bar(counter.keys(), counter.values())
        plt.show()


    
def display_viewtime_by_userid():
    total_readtime = 0
    visitor_ids = list(set([visitor['visitor_uuid'] for visitor in data]))
    viewtime = dict([(visitor, 0) for visitor in visitor_ids])
    for id in viewtime:
        total_readtime = 0
        for viewer in data:
            try:
                if (id == viewer['visitor_uuid']):
                    temp_readtime = viewer['event_readtime']
                    total_readtime += temp_readtime
                    viewtime[id] = total_readtime
                    print(viewtime)
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
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:.0f}'.format(x) for x in current_values])
    plt.show()


# Task 5 and 6
class Task5:

    def __init__(self, doc_uuid, visitor_uuid=None):
        self.doc_uuid = doc_uuid
        self.visitor_uuid = visitor_uuid

    def return_visitors_by_docid(self, temp):
        viewerIDList = set()
        for viewer in data:
            try:
                if (viewer['event_type'] != 'read'):
                    continue
                if (viewer['subject_doc_id'] == temp):
                    viewerID = viewer['visitor_uuid']
                    viewerIDList.add(viewerID)
            except Exception:
                pass # do something here for the exception
        if(len(viewerIDList) < 2):
            return
        return list(viewerIDList)

    def return_docs_by_userid(self, temp):
        docs_list = set()
        for docs in data:
            try:
                if (docs['event_type'] != 'read'):
                    continue
                if (docs['visitor_uuid'] == temp):
                    temp_doc = docs['subject_doc_id']
                    docs_list.add(temp_doc)
            except Exception:
                pass
        if(len(docs_list) < 2):
            return
        return list(docs_list)

    def also_likes(self, temp, temp2=None):
        also_likes_docs = []
        also_likes_visitor = []
        if self.visitor_uuid is None:
            also_likes_visitor = self.return_visitors_by_docid(temp)
            for visitor in also_likes_visitor:
                if(self.return_docs_by_userid(visitor) != None):
                    also_likes_docs.extend(self.return_docs_by_userid(visitor))
        else:
            also_likes_docs.extend(self.return_docs_by_userid(temp2))

        also_likes_docs.sort()
        return also_likes_docs

    def also_likes_top_10 (self, temp, temp2=None):
        top10docs = self.also_likes(temp, temp2)
        counter = Counter(top10docs)
        top10docsarranged = counter.most_common(11)
        print("also likes (document ID : Number of reads):")
        for doc in top10docsarranged:
            print(str(doc[0]) + " : " + str(doc[1]))
        return top10docsarranged

class Task6:

    def __init__(self, doc_uuid, visitor_uuid=None):
        self.doc_uuid = doc_uuid
        self.visitor_uuid = visitor_uuid

    def alsolikesgraph (self):
        task5 = Task5(self.doc_uuid, self.visitor_uuid)
        visitors = task5.return_visitors_by_docid(self.doc_uuid)
        docs = task5.also_likes(self.doc_uuid, self.visitor_uuid)
        discarddocs = []
        if(self.visitor_uuid != None):
            for doc in task5.return_docs_by_userid(self.visitor_uuid):
                if doc != self.doc_uuid:
                    discarddocs = doc
        gV = graphviz.Digraph('visitor', node_attr={'shape' : 'rectangle'})
        gD = graphviz.Digraph('document', node_attr={'shape' : 'circle'})
        gD.graph_attr.update(rank='max', shape= 'circle' )
        gV.graph_attr.update(rank='min')
        for doc in docs:
            if (doc == self.doc_uuid):
                gD.node(doc, str((doc)[-4:]), fillcolor='green', style='filled', shape='circle')
            else:
                if doc in discarddocs and doc in docs:
                    continue
                else:
                    gD.node(doc, str((doc[-4:])), fillcolor='white', style='filled', shape='circle')
        for visitor in visitors:
            if(task5.return_docs_by_userid(visitor) != None):
                if(visitor == self.visitor_uuid):
                    gV.node(visitor, str(visitor[-4:]), fillcolor='green', style='filled', shape='rectangle')
                    try:
                            gV.edge(visitor, self.doc_uuid)
                    except Exception:
                        pass # do something here for the exception
                else:
                    gV.node(visitor, str(visitor[-4:]), fillcolor='white', style='filled', shape='rectangle')
                    for  doc in task5.return_docs_by_userid(visitor):
                        try:
                            if (doc != self.doc_uuid):
                                gD.node(doc, str((doc)[-4:]), fillcolor='white', style='filled', shape='circle')
                            gV.edge(visitor, doc)
                        except Exception:
                            pass # do something here for the exception
        print(gV)
        gV.subgraph(gD)
       
        gV.format = 'png'
        gV.render(directory='doctest-output', view=True)

            
            

def make_gui():
    window = Tk()

    window.title("Welcome to LikeGeeks app")

    window.geometry('350x200')

    lbl = Label(window, text="Hello")

    lbl.grid(column=0, row=0)

    btn = Button(window, text="Click Me", command=clicked)

    btn.grid(column=1, row=0)

    window.mainloop()


def clicked():
    Task3.display_views_by_browser_short_a()

    
# testing the functions here
#display_views_by_continent("140310170010-0000000067dc80801f1df696ae52862b")
#display_views_by_continent()
#display_views_by_browser_part_a()

#display_viewtime_by_userid("130927071110-0847713a13bea63d7f359ea012f3538d")


#return_docs_by_userid("50ac35b7a0474b3e")


# task2 = Task2('6140310170010-0000000067dc80801f1df696ae5282b', True)
# task2.display_views_by_country()
# task2.display_views_by_continent()

# task3 = Task3()
# task3.display_views_by_browser_short_b()

task6 = Task6('100806162735-00000000115598650cb8b514246272b5', '00000000deadbeef')

task6.alsolikesgraph()
