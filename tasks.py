import sys                                      #import the sys library to allow for command line usage        
import matplotlib.pyplot as plt                 #import matplotlib library to plot the graphs for tasks 2, 3 and 4
import pycountry_convert as pc                  #import the pycountry_convert library to gain access to a library of country and continent codes for task 3
from collections import Counter                 #import the Counter library to allow for creating a top 10 list for viewer read time and also likes
import graphviz                                 #import graphviz to plot the graph necessary for task 6
import httpagentparser                          #import the httpagentparser library to gain access to a library of browsers by agentparser strings for task 3
import re                                       #import re to allow the use of regular expressions in task 3
from tkinter import *                           #import tkinter to allow the implementation of a graphical user interface for task 7
from tkinter import messagebox                  #import messagebox to show errors to the user



# Task 2
class Task2:
    #create an empty list called countries accessible by any function within this class
    countries = []

    #initialise the parameters used for the task2 objects
    def __init__(self, doc_uuid, isPressed, data, list=[]):
        self.isPressed = isPressed
        self.doc_uuid = doc_uuid
        self.countries = list
        self.data = data
    
    #-------------------------------------TASK 2A-------------------------------------
    def display_views_by_country(self):
        self.countries = []
        #for every viewer within the dataset
        for viewer in self.data:
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
            except Exception as e:
                messagebox.showerror(title="Error", message=str(e))
        #if this function was called upon by the press of a button, plot the graph of countries and display it
        if len(self.countries) == 0:
            if len(sys.argv) == 1:
                messagebox.showerror(title="Error", message="No countries found for this document ID. Please ensure you provided a valid document ID.")
            else:
                print("No countries found for this document ID. Please ensure you provided a valid document ID.")
        else:
            if (self.isPressed == True):
                plt.figure(1)
                #add title
                plt.title("Display Views by Country")
                #add grid lines
                plt.grid(axis='y', alpha=0.75)
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
            except Exception as e:
                messagebox.showerror(title="Error", message=str(e))
            except:
                print("error")
        if len(self.countries) != 0:
            plt.figure(2)
            #add title
            plt.title("Display Views by Continent")
            #add grid lines
            plt.grid(axis='y', alpha=0.75)
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
    def __init__(self, data, list=[]):
        self.browsers = list
        self.data = data
        
    #-------------------------------------TASK 3A-------------------------------------
    def display_views_by_browser_part_a(self):
        #ensure that the browsers list is empty
        self.browsers = []
        #create a list called already viewed that is set to empty
        already_viewed = []
        #for every viewer in the dataset
        for viewer in self.data:
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
                    
            except Exception as e:
                messagebox.showerror(title="Error", message=str(e))
        # displaying the info
        plt.figure(3)
        counter = Counter(self.browsers)
        #add title
        plt.title("Display Browser Usage")
        #add grid lines
        plt.grid(axis='y', alpha=0.75)
        #plot the browsers and show the graph
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
        for viewer in self.data:
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
            except Exception as e:
                messagebox.showerror(title="Error", message=str(e))
            except:
                print("error")
        #using the "Counter" function, count each time a browser has been added to the list and assign that browser an integer value
        counter = Counter(self.browsers)
        plt.figure(4)
        #add title
        plt.title("Display Browser Usage")
        #add grid lines
        plt.grid(axis='y', alpha=0.75)
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
        for viewer in self.data:
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
                    
            except Exception as e:
                messagebox.showerror(title="Error", message=str(e))
            except:
                print("error")
        # displaying the info
        counter = Counter(self.browsers)
        plt.figure(5)
        #add title
        plt.title("Display Browser Usage")
        #add grid lines
        plt.grid(axis='y', alpha=0.75)
        #plot the browsers and show the graph
        plt.xlabel('Browser')
        plt.ylabel('Amount')
        plt.bar(counter.keys(), counter.values())
        plt.show()

#Task 4
class Task4:
    #initialise the parameters used for the task4 objects (None are required so simply return)
    def __init__(self, data):
        self.data = data
    
    #-------------------------------------TASK 4-------------------------------------
    def display_viewtime_by_userid(self):
        #create a variable called total_readtime
        total_readtime = 0
        #create a set (so that users aren't duplicated) of every unique visitor id within the dataset
        visitor_ids = list(set([visitor['visitor_uuid'] for visitor in self.data]))
        #create a dicionary called viewtime and add every unique visitor id to the key
        viewtime = dict([(visitor, 0) for visitor in visitor_ids])
        
        # O(N) time complexity solution found
        # faster than O(N^2)
        #for every viewer in the dataset
        
        for viewer in self.data:
            try:
                #assign the current viewer's "event_readtime" to total_time
                total_readtime = viewer['event_readtime']
                #for the current viewer's key in the viewtime dictionary, add the total_readtime to it's current value
                viewtime[viewer['visitor_uuid']] += total_readtime
            except Exception:
                pass
            except:
                print("error")
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
        plt.figure(6)
        #add title
        plt.title("Display Most Avid Users")
        #add grid lines
        plt.grid(axis='y', alpha=0.75)
        #plot the data and show the graph
        plt.xlabel('viewer ID')
        plt.ylabel('time spent')
        plt.bar(users, times)
        current_values = plt.gca().get_yticks()
        plt.gca().set_yticklabels(['{:.0f}'.format(x) for x in current_values])
        plt.show()

# Task 5
class Task5:
    #initialise the parameters used for the task5 objects
    def __init__(self, doc_uuid, data, visitor_uuid=None):
        self.doc_uuid = doc_uuid
        self.visitor_uuid = visitor_uuid
        self.data = data
        
    #-------------------------------------TASK 5A-------------------------------------
    def return_visitors_by_docid(self, temp):
        #create a set called viewerIDList
        viewerIDList = set()
        #for every viewer in the dataset
        for viewer in self.data:
            try:
                #ensure the document the viewer visited has been read
                if (viewer['event_type'] != 'read'):
                    continue
                #if the subject_doc_id of the current viewer is the same as the inputted document,
                #add the current viewer to the viewerIDList
                if (viewer['subject_doc_id'] == temp):
                    viewerID = viewer['visitor_uuid']
                    viewerIDList.add(viewerID)
            except Exception as e:
                messagebox.showerror(title="Error", message=str(e))
            except:
                print("error")
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
        for docs in self.data:
            try:
                #ensure the document the viewer visited has been read
                if (docs['event_type'] != 'read'):
                    continue
                #if the viewer id of the current document is the same as the inputted viewer,
                #add the current document to the docs_list
                if (docs['visitor_uuid'] == temp):
                    temp_doc = docs['subject_doc_id']
                    docs_list.add(temp_doc)
            except Exception as e:
                messagebox.showerror(title="Error", message=str(e))
            except:
                print("error")
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
            try:
                also_likes_visitor = self.return_visitors_by_docid(temp)
                #for every visitor in the also_likes_visitor list
                for visitor in also_likes_visitor:
                    #if the list returned by return_docs_by_userid(currentvisitor) is not empty
                    if(self.return_docs_by_userid(visitor) != None):
                        #extend the list by the list returned
                        also_likes_docs.extend(self.return_docs_by_userid(visitor))
            except:
                raise
        #if there is an inputted visitor id
        else:
            #extend the also_likes_docs by the list returned by return_docs_by_userid(visitor)
            also_likes_docs.extend(self.return_docs_by_userid(temp2))
        #sort the documents
        sort = sorted(also_likes_docs, key=lambda kv: kv[1], reverse=True)
        sort = list(sort)
        #return the also_likes_docs list
        return sort

    #-------------------------------------TASK 5D-------------------------------------
    def also_likes_top_10 (self, temp, temp2=None):
        #assign a list called top10docs the value of the list returned by the also_likes function
        top10docs = []
        try:
            top10docs = self.also_likes(temp, temp2)
        except:
            print("Invalid document/visitor ID provided, please re-enter with a valid ID.")
        #create a Counter called counter of the top10docs list (counts the amount of times that a document has been entered into the list and assigns that key a value)
        counter = Counter(top10docs)
        #create a new list that counts the top 10 most occuring documents and the inputted document
        top10docsarranged = counter.most_common(11)
        #print a key into the console
        if len(top10docs) > 0:
            print("also likes (document ID : Number of reads):")
            #for every document in the top10docsarranged list, print the document id and the amount of times it has occured
            for doc in top10docsarranged:
                print(str(doc[0]) + " : " + str(doc[1]))
        #return the top10documentsarranged list
        return top10docsarranged

#Task 6
class Task6:
    #initialise the parameters used for the task6 objects
    def __init__(self, doc_uuid, data, visitor_uuid=None):
        self.doc_uuid = doc_uuid
        self.visitor_uuid = visitor_uuid
        self.data = data
    #-------------------------------------TASK 6-------------------------------------
    def alsolikesgraph (self):
        #create an object called task 5 for the Task5 class and messagebox.showerror(title="Error", message=str(e)) the
        #doc_uuid and visitor_uuid of this class
        task5 = Task5(self.doc_uuid, self.data, self.visitor_uuid)
        #create a new list and assign it the returned list of return_visitors_by_docid
        visitors = task5.return_visitors_by_docid(self.doc_uuid)
        #create an empty list called docs
        docs = []
        #create a set called top10 and fill it with the contents returned by also_likes_top_10
        top10 = task5.also_likes_top_10(self.doc_uuid, self.visitor_uuid)
        #for every d in top10, add the document ID to the docs list
        for d in top10:
            docs.append(d[0])
        #create an empty list called discarddocs
        discarddocs = []
        #if there is  an inputted user id
        try:
            if(self.visitor_uuid != None):
            #for every doc in return_docs_by_userid
                for doc in task5.return_docs_by_userid(self.visitor_uuid):
                
                    #if the current doc is not equal to the inputted doc_uuid,
                    #add the doc to the discarddocs list
                    if doc != self.doc_uuid:
                        discarddocs = doc
        except:
            if len(sys.argv) == 1:
                messagebox.showerror(title="Error", message="Error completing this request, please ensure the inputted document/visitor ID are correct.")
                raise
            else:
                print("Error completing this request, please ensure the inputted document/visitor ID are correct.")
                raise
        #create a new graph called gV and assign it's name and shape
        gV = graphviz.Digraph('visitor', node_attr={'shape' : 'rectangle'})
        #create a new graph called gD and assign it's name and shape
        gD = graphviz.Digraph('document', node_attr={'shape' : 'circle'})
        #add the rank attributes to each graph
        gD.graph_attr.update(rank='max')
        gV.graph_attr.update(rank='min')
        #for every doc in the docs list
        for doc in docs:
            try:
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
            except:
                print("There was a problem completing this request, please ensure the document/visitor ID are correct.")
        try:
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
                        except Exception as e:
                            messagebox.showerror(title="Error", message=str(e)) # do something here for the exception
                        except:
                            print("Invalid document/visitor ID provided, please re-enter.")
                    else:
                        #add a rectangle node for the current visitor and colour it white
                        gV.node(visitor, str(visitor[-4:]), fillcolor='white', style='filled', shape='rectangle')
                        
                        try:
                            #if the user has inputted a visitor_uuid
                            if self.visitor_uuid != None:
                                #for every doc in the list returned by return_docs_by_userid for the current visitor
                                for doc in task5.return_docs_by_userid(visitor):                          
                                    #if the current doc is not equal to the inputted doc
                                    if (doc != self.doc_uuid):
                                        #add a circular node and colour it white
                                        gD.node(doc, str((doc)[-4:]), fillcolor='white', style='filled', shape='circle')
                                    #add an edge between the current visitor and the current doc
                                    gV.edge(visitor, doc)
                            else:
                                #for every document in the top10 docs list
                                for doc in docs:
                                    #if the document ID is not the same as the inputted document ID
                                    if (doc != self.doc_uuid):
                                        #add a circular node and colour it white
                                        gD.node(doc, str((doc)[-4:]), fillcolor='white', style='filled', shape='circle')
                                    #if the current doc is in the list returned by return_docs_by_userid for the current visitor
                                    if doc in task5.return_docs_by_userid(visitor):
                                        #add an edge between the current visitor and the current doc
                                        gV.edge(visitor, doc)
                        except Exception as e:
                            messagebox.showerror(title="Error", message=str(e)) # do something here for the exception
                        except:
                            print("Invalid document/visitor ID provided, please re-enter.")
        except:
            messagebox.showwarning(title="Error", message="Invalid document/visitor ID provided, please re-enter.")
            raise
        #connect the two graphs
        gV.subgraph(gD)
        #set the outputted graph's format to a png
        gV.format = 'png'
        #render the graphs
        gV.render(directory='doctest-output', view=True)

# Additional features
class AdditionalFeatures:

     #initialise the parameters used for the additionalfeatures objects
    def __init__(self, data, doc_uuid=None, visitor_uuid=None):
        self.doc_uuid = doc_uuid
        self.visitor_uuid = visitor_uuid
        self.data = data
    
    # a method to find any users within a specified JSON file that have the input within their user_uuid
    # for example, someone can search for '45ba' and the file will be searched to see any users with this code in their uuid
    def find_users_with_key(self, visitor_uuid):
        visitor_ids = list(set([visitor['visitor_uuid'] for visitor in self.data]))
        found_visitors = []
        if len(visitor_uuid) < 4:
            print("Too small: please search for more than 4 characters at a time.")
        else:
            for visitor in visitor_ids:
                if visitor_uuid in visitor:
                    found_visitors.append(visitor)

        if len(found_visitors) == 0:
            print('No users were found containing this ID in this file.')
        else:
            print('Users found:')
            for i in found_visitors:   
                print(i)
    
    def find_documents_with_key(self, doc_uuid):
        docs_set = set()
        found_docs = []
        #for every document in the dataset
        for docs in self.data:
            try:
                temp_doc = docs['subject_doc_id']
                docs_set.add(temp_doc)
            except Exception:
                pass
        

        if len(doc_uuid) < 4:
            print("Too small: please search for more than 4 characters at a time.")
        else:
            for doc in docs_set:
                if doc_uuid in doc:
                    found_docs.append(doc)

        if len(found_docs) == 0:
            print('No documents were found containing this ID in this file.')
        else:
            print('Documents found:')
            for i in found_docs:   
                print(i)

    def most_popular_visitor_source(self):
        visitor_source = list(set([source['visitor_source'] for source in self.data]))
        #create a dicionary called source_total and add every unique source to the key
        source_total = dict([(source, 0) for source in visitor_source])
        for visitor in self.data:
                source_total[visitor['visitor_source']] += 1
        
        if len(source_total) == 0:
            print('No sources were found in this file.')
        else:
            #create a list of the top source
            source_sorted = list(sorted(source_total.items(), key=lambda kv: kv[1], reverse=True))
            #create two empty lists, users and times
            source_type = []
            source_count = []
            #for every viewer in the top sources list
            for source in source_sorted:
                #add the current source to the lists
                source_type.append(source[0])
                source_count.append(source[1])
            plt.figure(7)
            #add title
            plt.title("Display Most Popular Sources")
            #add grid lines
            plt.grid(axis='y', alpha=0.75)
            #plot the data and show the graph
            plt.xlabel('Source Type')
            plt.ylabel('Total')
            plt.bar(source_type, source_count)
            current_values = plt.gca().get_yticks()
            plt.gca().set_yticklabels(['{:.0f}'.format(x) for x in current_values])
            plt.show()
    
    def most_popular_visitor_device(self):
        visitor_device = list(set([device['visitor_device'] for device in self.data]))
        device_total = dict([(device, 0) for device in visitor_device])
        for visitor in self.data:
                device_total[visitor['visitor_device']] += 1
        
        if len(device_total) == 0:
            print('No devices were found in this file.')
        else:
            #create a list of the top source
            device_sorted = list(sorted(device_total.items(), key=lambda kv: kv[1], reverse=True))
            #create two empty lists, users and times
            device_type = []
            device_count = []
            #for every viewer in the top sources list
            for source in device_sorted:
                #add the current source to the lists
                device_type.append(source[0])
                device_count.append(source[1])
            plt.figure(8)
            #add title
            plt.title("Display Most Popular Devices")
            #add grid lines
            plt.grid(axis='y', alpha=0.75)
            #plot the data and show the graph
            plt.xlabel('Device Type')
            plt.ylabel('Total')
            plt.bar(device_type, device_count)
            current_values = plt.gca().get_yticks()
            plt.gca().set_yticklabels(['{:.0f}'.format(x) for x in current_values])
            plt.show()

    def most_popular_referrers(self):
        referrers_list = set()
        #for every document in the dataset
        for docs in self.data:
            try:
                temp_doc = docs['visitor_referrer']
                referrers_list.add(temp_doc)
            except Exception:
                pass
        referrer_total = dict([(referrer, 0) for referrer in referrers_list]) 
        try:
            for visitor in self.data: 
                referrer_total[visitor['visitor_referrer']] += 1
        except Exception:
            pass
        if len(referrer_total) == 0:
            print('No referrers were found in this file.')
        else:
            #create a list of the top source
            referrer_sorted = list(sorted(referrer_total.items(), key=lambda kv: kv[1], reverse=True))[:10]
            #create two empty lists, users and times
            referrer_id = []
            referrer_count = []
            #for every viewer in the top sources list
            for source in referrer_sorted:
                #add the current source to the lists
                referrer_id.append(source[0])
                referrer_count.append(source[1])
            plt.figure(9)
            #add title
            plt.title("Display Most Popular Referrers")
            #add grid lines
            plt.grid(axis='y', alpha=0.75)
            #plot the data and show the graph
            plt.xlabel('Referrer ID')
            plt.ylabel('Total')
            plt.bar(referrer_id, referrer_count)
            current_values = plt.gca().get_yticks()
            plt.gca().set_yticklabels(['{:.0f}'.format(x) for x in current_values])
            plt.show()

                