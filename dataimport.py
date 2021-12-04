#Import the data file
import json
from json.decoder import JSONDecodeError
from os import system
from tkinter import messagebox 
import sys

class DataImport:
    #initialise the parameters used for the dataimport objects
    def __init__(self, fname, data_list=[]):
        self.data_list = data_list
        self.fname = fname

    def open_json(self):
        
        #set data to empty
        self.data = []
        #create an empty list called dataDict
        dataDict = []
        #set self.data_list to empty
        self.data_list = []
        
            #set "dataset" to the inputted data file
        dataset = open(self.fname, 'r', encoding='utf-8')
    
        #Set a variable called Lines to every line in the file
        Lines = dataset.readlines()
        #for every line in the json file
        for line in Lines:
            try:
                #y = a dictionary of every json object
                dataDict = json.loads(line)
                #add the json objects to the list "data"
                self.data_list.append(dataDict)
            #error handling
            except JSONDecodeError:
                if len(sys.argv) == 1 or '-t 7' in sys.flags:
                    messagebox.showerror(title="Error", message="Error decoding JSON file, please ensure format is correct.")
                    raise
                else:
                    print("Error decoding JSON file, please ensure format is correct.")
                    raise
        dataset.close()
        
        return self.data_list