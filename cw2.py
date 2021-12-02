import json
from json.decoder import JSONDecodeError
from os import system                                     #import the json library to allow for the use of the dataset
import matplotlib.pyplot as plt                 #import matplotlib library to plot the graphs for tasks 2, 3 and 4
import pycountry_convert as pc                  #import the pycountry_convert library to gain access to a library of country and continent codes for task 3
from collections import Counter                 #import the Counter library to allow for creating a top 10 list for viewer read time and also likes
import graphviz                                 #import graphviz to plot the graph necessary for task 6
import httpagentparser                          #import the httpagentparser library to gain access to a library of browsers by agentparser strings for task 3
import re                                       #import re to allow the use of regular expressions in task 3
from tkinter import *                           #import tkinter to allow the implementation of a graphical user interface for task 7
from tkinter.filedialog import askopenfilename
import argparse                                 #import argparse to create a command line interface


data = []

class DataImport:

    def __init__(self, data_list=[]):
        self.data_list = data_list

    def open_json(self, fname):
        global data
        data = []
        dataDict = []
        self.data_list = []
        dataset = open(fname, 'r', encoding='utf-8')
        Lines = dataset.readlines()
        #for every line in the json file
        for line in Lines:
            try:
                #y = a dictionary of every json object
                dataDict = json.loads(line)
                #add the json objects to the list "data"
                self.data_list.append(dataDict)
            except JSONDecodeError as e:
                print("Error decoding JSON file, please ensure format is correct.")
        dataset.close()
        return self.data_list

#create a global list called data

# Task 2
class Task2:
    #create an empty list called countries accessible by any function within this class
    countries = []

    #initialise the parameters used for the task2 objects
    def __init__(self, doc_uuid, isPressed, list=[]):
        self.isPressed = isPressed
        self.doc_uuid = doc_uuid
        self.countries = list
    
    #-------------------------------------TASK 2A-------------------------------------
    def display_views_by_country(self):
        self.countries = []
        #for every viewer within the dataset
        for viewer in data:
            try:
                #ensure the document the viewer visited has been read
                if (viewer['event_type'] != 'read'):
                    continue
                #if the document id of the viewer matches the inputted document id
                if (viewer['env_doc_id'] == self.doc_uuid):
                    #assign the viewer's country to the ciewer_country variable
                    viewer_country = viewer['visitor_country']
                    #add the viewer's country to the countries list
                    self.countries.append(viewer_country)
            except Exception:
                pass # do something here for the exception
        #if this function was called upon by the press of a button, plot the graph of countries and display it
        if (self.isPressed == True):
            plt.xlabel('country')
            plt.ylabel('amount')
            plt.hist(self.countries)
            plt.show()
        
    #-------------------------------------TASK 2B-------------------------------------
    def display_views_by_continent(self):
        #set the list of countries to empty
        self.countries = []
        #create an empty list of continents
        continents = []
        #set isPressed to False
        self.isPressed = False
        #call the task 2a function to fill the countries list. Since isPressed is false, do not show the countries graph
        self.display_views_by_country()
        #for every country in the countries list
        for i in self.countries:
            try:
                #assign a variable to the continent code of the current country
                temp_continent = pc.country_alpha2_to_continent_code(i)
                #parse the continent code and convert it into the full name of the continent
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
        #plot the continents graph and display it
        plt.xlabel('continents')
        plt.ylabel('amount')
        plt.hist(continents)
        plt.show()
        
#Task 3
class Task3:
    #create an empty list called browsers accessible by any function within this class
    browsers = []

    #initialise the parameters used for the task3 objects
    def __init__(self, list=[]):
        self.browsers = list
        
    #-------------------------------------TASK 3A-------------------------------------
    def display_views_by_browser_part_a(self):
        #ensure that the browsers list is empty
        self.browsers = []
        #create a list called already viewed that is set to empty
        already_viewed = []
        #for every viewer in the dataset
        for viewer in data:
            try:
                #ensure the document the viewer visited has been read
                if (viewer['event_type'] != 'read'):
                    continue
                #remove duplicate entries
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
        #plot the browsers and show the graph
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Browser')
        plt.ylabel('Amount')
        plt.bar(counter.keys(), counter.values())
        plt.show()

    #-------------------------------------TASK 3B: Method 1-------------------------------------
    def display_views_by_browser_short_a(self):
        #ensure the browsers list is empty
        self.browsers = []
        #create a list of visitors and make it empty
        vislist = []
        #for every viewer in the dataset
        for viewer in data:
            try:
                #ensure the document the viewer visited has been read
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
        
    #-------------------------------------TASK 3B: Method 2-------------------------------------
    def display_views_by_browser_short_b(self):
        #ensure that the browsers list is empty
        self.browsers = []
        #create a list called already viewed that is set to empty
        already_viewed = []
        #for every viewer in the dataset
        for viewer in data:
            try:
                #ensure the document the viewer visited has been read
                if (viewer['event_type'] != 'read'):
                    continue
                #remove duplicate entries
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
        #plot the browsers and show the graph
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Browser')
        plt.ylabel('Amount')
        plt.bar(counter.keys(), counter.values())
        plt.show()

#Task 4
class Task4:
    #initialise the parameters used for the task4 objects (None are required so simply return)
    def __init__(self):
        return
    
    #-------------------------------------TASK 4-------------------------------------
    def display_viewtime_by_userid():
        #create a variable called total_readtime
        total_readtime = 0
        #create a set (so that users aren't duplicated) of every unique visitor id within the dataset
        visitor_ids = list(set([visitor['visitor_uuid'] for visitor in data]))
        #create a dicionary called viewtime and add every unique visitor id to the key
        viewtime = dict([(visitor, 0) for visitor in visitor_ids])
        
        # O(N) time complexity solution found
        # faster than O(N^2)
        #for every viewer in the dataset
        for viewer in data:
            try:
                #assign the current viewer's "event_readtime" to total_time
                total_readtime = viewer['event_readtime']
                #for the current viewer's key in the viewtime dictionary, add the total_readtime to it's current value
                viewtime[viewer['visitor_uuid']] += total_readtime
            except Exception:
                pass
        #create a list of the top ten viewers sorted by viewtime
        time_sorted = list(sorted(viewtime.items(), key=lambda kv: kv[1], reverse=True))[:10]
        #create two empty lists, users and times
        users = []
        times = []
        #for every viewer in the top 10 viewers list
        for viewer in time_sorted:
            #add the current viewer to the users and times list respectively
            users.append(viewer[0])
            times.append(viewer[1])
        #plot the data and show the graph
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('viewer ID')
        plt.ylabel('time spent')
        plt.bar(users, times)
        current_values = plt.gca().get_yticks()
        plt.gca().set_yticklabels(['{:.0f}'.format(x) for x in current_values])
        plt.show()

# Task 5
class Task5:
    #initialise the parameters used for the task4 objects
    def __init__(self, doc_uuid, visitor_uuid=None):
        self.doc_uuid = doc_uuid
        self.visitor_uuid = visitor_uuid
        
    #-------------------------------------TASK 5A-------------------------------------
    def return_visitors_by_docid(self, temp):
        #create a set called viewerIDList
        viewerIDList = set()
        #for every viewer in the dataset
        for viewer in data:
            try:
                #ensure the document the viewer visited has been read
                if (viewer['event_type'] != 'read'):
                    continue
                #if the subject_doc_id of the current viewer is the same as the inputted document,
                #add the current viewer to the viewerIDList
                if (viewer['subject_doc_id'] == temp):
                    viewerID = viewer['visitor_uuid']
                    viewerIDList.add(viewerID)
            except Exception:
                pass # do something here for the exception
        #if the length of the list is 1, return nothing
        #if the length exceeds 1, return viewerIDList
        if(len(viewerIDList) < 2):
            return
        return list(viewerIDList)

    #-------------------------------------TASK 5B-------------------------------------
    def return_docs_by_userid(self, temp):
        #create a set called docs_list
        docs_list = set()
        #for every document in the dataset
        for docs in data:
            try:
                #ensure the document the viewer visited has been read
                if (docs['event_type'] != 'read'):
                    continue
                #if the viewer id of the current document is the same as the inputted viewer,
                #add the current document to the docs_list
                if (docs['visitor_uuid'] == temp):
                    temp_doc = docs['subject_doc_id']
                    docs_list.add(temp_doc)
            except Exception:
                pass
        #if the length of the list is 1, return nothing
        #if the length exceeds 1, return docs_list
        if(len(docs_list) < 2):
            return
        return list(docs_list)

    #-------------------------------------TASK 5C-------------------------------------
    def also_likes(self, temp, temp2=None):
        #create an empty list called also_likes_docs
        also_likes_docs = []
        #create an empty list called also_likes_visitor
        also_likes_visitor = []
        #if there is no inputted visitor id
        if self.visitor_uuid is None:
            #set the value of the also_likes_visitor list to the list returned by return_visitors_by_docid
            also_likes_visitor = self.return_visitors_by_docid(temp)
            #for every visitor in the also_likes_visitor list
            for visitor in also_likes_visitor:
                #if the list returned by return_docs_by_userid(currentvisitor) is not empty
                if(self.return_docs_by_userid(visitor) != None):
                    #extend the list by the list returned
                    also_likes_docs.extend(self.return_docs_by_userid(visitor))
        #if there is an inputted visitor id
        else:
            #extend the also_likes_docs by the list returned by return_docs_by_userid(visitor)
            also_likes_docs.extend(self.return_docs_by_userid(temp2))
        #sort the documents
        also_likes_docs.sort()
        #return the also_likes_docs list
        return also_likes_docs

    #-------------------------------------TASK 5D-------------------------------------
    def also_likes_top_10 (self, temp, temp2=None):
        #assign a list called top10docs the value of the list returned by the also_likes function
        top10docs = self.also_likes(temp, temp2)
        #create a Counter called counter of the top10docs list (counts the amount of times that a document has been entered into the list and assigns that key a value)
        counter = Counter(top10docs)
        #create a new list that counts the top 10 most occuring documents and the inputted document
        top10docsarranged = counter.most_common(11)
        #print a key into the console
        print("also likes (document ID : Number of reads):")
        #for every document in the top10docsarranged list, print the document id and the amount of times it has occured
        for doc in top10docsarranged:
            print(str(doc[0]) + " : " + str(doc[1]))
        #return the top10documentsarranged list
        return top10docsarranged

#Task 6
class Task6:
    #initialise the parameters used for the task4 objects
    def __init__(self, doc_uuid, visitor_uuid=None):
        self.doc_uuid = doc_uuid
        self.visitor_uuid = visitor_uuid
    #-------------------------------------TASK 6-------------------------------------
    def alsolikesgraph (self):
        #create an object called task 5 for the Task5 class and pass the
        #doc_uuid and visitor_uuid of this class
        task5 = Task5(self.doc_uuid, self.visitor_uuid)
        #create a new list and assign it the returned list of return_visitors_by_docid
        visitors = task5.return_visitors_by_docid(self.doc_uuid)
        #create a new list and assign it the returned list of also_likes
        docs = task5.also_likes(self.doc_uuid, self.visitor_uuid)
        #create an empty list called discarddocs
        discarddocs = []
        #if there is  an inputted user id
        if(self.visitor_uuid != None):
            #for every doc in return_docs_by_userid
            for doc in task5.return_docs_by_userid(self.visitor_uuid):
                #if the current doc is not equal to the inputted doc_uuid,
                #add the doc to the discarddocs list
                if doc != self.doc_uuid:
                    discarddocs = doc
        #create a new graph called gV and assign it's name and shape
        gV = graphviz.Digraph('visitor', node_attr={'shape' : 'rectangle'})
        #create a new graph called gD and assign it's name and shape
        gD = graphviz.Digraph('document', node_attr={'shape' : 'circle'})
        #add the rank attributes to each graph
        gD.graph_attr.update(rank='max')
        gV.graph_attr.update(rank='min')
        #for every doc in the docs list
        for doc in docs:
            #if the current doc equals the inputted document
            if (doc == self.doc_uuid):
                #add a circular node and colour it green
                gD.node(doc, str((doc)[-4:]), fillcolor='green', style='filled', shape='circle')
            else:
                #if the current doc is in the discarddocs list and the docs list, do nothing
                if doc in discarddocs and doc in docs:
                    continue
                #otherwise
                else:
                    #add a circular node and colour it white
                    gD.node(doc, str((doc[-4:])), fillcolor='white', style='filled', shape='circle')
        #for every visitor in the visitors list
        for visitor in visitors:
            #if the list returned by return_docs_by_userid is not empty
            if(task5.return_docs_by_userid(visitor) != None):
                #if the current visitor equals the inputted visitor_uuid
                if(visitor == self.visitor_uuid):
                    #add a rectangle node and colour it green
                    gV.node(visitor, str(visitor[-4:]), fillcolor='green', style='filled', shape='rectangle')
                    try:
                            #add an edge between the current visitor and the inputted document
                            gV.edge(visitor, self.doc_uuid)
                    except Exception:
                        pass # do something here for the exception
                else:
                    #add a rectangle node for the current visitor and colour it white
                    gV.node(visitor, str(visitor[-4:]), fillcolor='white', style='filled', shape='rectangle')
                    #for every doc in the list returned by return_docs_by_userid for the current visitor
                    for  doc in task5.return_docs_by_userid(visitor):
                        try:
                            #if the current doc is not equal to the inputted doc
                            if (doc != self.doc_uuid):
                                #add a circular node and colour it white
                                gD.node(doc, str((doc)[-4:]), fillcolor='white', style='filled', shape='circle')
                            #add an edge between the current visitor and the current doc
                            gV.edge(visitor, doc)
                        except Exception:
                            pass # do something here for the exception
        #connect the two graphs
        gV.subgraph(gD)
        #set the outputted graph's format to a png
        gV.format = 'png'
        #render the graphs
        gV.render(directory='doctest-output', view=True)

  

class Gui:

    def __init__(self):
        return

    def make_gui(self):   
        visitorEmpty = None
        window = Tk()
        window.title("Data Document Tracker")
        window.geometry('900x500')
        window.configure(bg='white')

        doc_uuid_label = Label(window, text="Document UUID:")
        doc_uuid_label.place(x = 3, y = 40)
        doc_uuid_label.configure(bg='white')
        vis_uuid_label = Label(window, text="Visitor UUID:")
        vis_uuid_label.place(x = 25, y = 70)
        vis_uuid_label.configure(bg='white')

        doc_uuid_entry = Entry(window,width=130)
        doc_uuid_entry.place(x = 95, y = 40)
        vis_uuid_entry = Entry(window,width=130)
        vis_uuid_entry.place(x = 95, y = 70)

        btnFile = Button(window, text="Select input data file", bg='white', width = 40, command=lambda: self.changefile(changefile_entry.get()))
        btnFile.place(x = 3, y = 10)
        
        btn2a = Button(window, text="2a. Views by Country", bg='white', width = 30, command=lambda: self.task2a(doc_uuid_entry.get()))
        btn2b = Button(window, text="2b. Views by Continent", bg='white', width = 30, command=lambda: self.task2b(doc_uuid_entry.get()))
        btn3a = Button(window, text="3a. Views by Browser", bg='white', width = 30, command=self.task3a)
        btn3b1 = Button(window, text="3b. Views by Browser Method 1", bg='white', width = 30, command=self.task3b1)
        btn3b2 = Button(window, text="3b. Views by Browser Method 2", bg='white', width = 30, command=self.task3b2)
        btn4 = Button(window, text="4. View Time by User", bg='white', width = 30, command=self.task4)
        btn5 = Button(window, text="5/6. Display Also Likes Graph", bg='white', width = 30, command=lambda: self.task5and6helper(doc_uuid_entry.get(), vis_uuid_entry.get()))

        btn2a.place(x = 660, y = 110)
        btn2b.place(x = 660, y = 140)
        btn3a.place(x = 660, y = 170)
        btn3b1.place(x = 660, y = 200)
        btn3b2.place(x = 660, y = 230)
        btn4.place(x = 660, y = 260)
        btn5.place(x = 660, y = 290)


        window.mainloop()

    def changefile(self, file):
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        jfile = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        global data
        import_data = DataImport()
        data = []
        data = import_data.open_json(jfile)
        print("File has been changed to: " + jfile)
    
    def task2a(self, doc_uuid):
        task2 = Task2(doc_uuid, True)
        task2.display_views_by_country()
    
    def task2b(self, doc_uuid):
        task2 = Task2(doc_uuid, True)
        task2.display_views_by_continent()
    
    def task3a(self):
        task3 = Task3()
        task3.display_views_by_browser_part_a()

    def task3b1(self):
        task3 = Task3()
        task3.display_views_by_browser_short_a()
    
    def task3b2(self):
        task3 = Task3()
        task3.display_views_by_browser_short_b()

    def task4(self):
        Task4.display_viewtime_by_userid()
    
    def task5and6(self, doc_uuid, visitor_uuid=None):
        task6 = Task6(doc_uuid, visitor_uuid)
        task6.alsolikesgraph()

    def task5and6helper(self, doc_uuid, visitor_uuid):
        visEmpty = None
        if (visitor_uuid == ""):
            self.task5and6(doc_uuid, visEmpty)
        else:
            self.task5and6(doc_uuid, visitor_uuid)
    
class Task8:

    def __init__(self, doc_uuid=None, visitor_uuid=None, file_name=None):
        self.doc_uuid = doc_uuid
        self.visitor_uuid = visitor_uuid
        self.file_name = file_name
        # using the argparse library to create an initial parser for command line interface commands
        self.cmd_parser = argparse.ArgumentParser(description= 'Document Tracker interface.')
        # visitor uid is optional: made option with the --uid flag
        self.cmd_parser.add_argument('-u', '--uid', type=str, help='The visitor ID to analyse.')
        # remaining commands are mandatory
        self.cmd_parser.add_argument('-d', type=str, help='The document ID to analyse.')
        self.cmd_parser.add_argument('-t', type=str, help='The specified task to anaylse.')
        self.cmd_parser.add_argument('-f', type=str, help='The path to the JSON file.')
        self.cmd_args = self.cmd_parser.parse_args()

    def cmd_checking(self):
        global data
        import_data = DataImport() 
        if self.cmd_args.uid:
            self.visitor_uuid = self.cmd_args.uid
        if self.cmd_args.t is None:
            print("No task ID provided, please re-enter.")
        if self.cmd_args.t not in ['2a', '2b', '3a', '3b', '4', '5d', '6', '7']:
            print("Invalid task ID provided, please re-enter (options: 2a, 2b, 3a, 3b, 4, 5d, 6, 7).")
        if self.cmd_args.d is None:
            print("No document ID provided, please re-enter.")
        if self.cmd_args.f is None:
            print("No JSON file path provided, please re-enter.")
        self.doc_uuid = self.cmd_args.d
        data = import_data.open_json(self.cmd_args.f)
        self.cmd_execute(self.cmd_args.t)
        
    def cmd_execute(self, id):
        task2 = Task2(self.doc_uuid, True)
        task3 = Task3()
        task5 = Task5(self.doc_uuid, self.visitor_uuid)
        task6 = Task6(self.doc_uuid, self.visitor_uuid)
        task7 = Gui()
        if id == '2a':
            task2.display_views_by_country()
        if id == '2b':
            task2.display_views_by_continent()
        if id == '3a':
            task3.display_views_by_browser_part_a()
        if id == '3b':
            task3.display_views_by_browser_short_a()
        if id == '4':
            Task4.display_viewtime_by_userid()
        if id == '5d':
            task5.also_likes_top_10(self.doc_uuid, self.visitor_uuid)
        if id == '6':
            task6.alsolikesgraph()
        if id == '7':
            task7.make_gui()

            

#task8 = Task8()
#task8.cmd_checking()



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

gui = Gui()
gui.make_gui()
