import sys                                      #import the sys library to allow for command line usage
from tkinter import *                           #import tkinter to allow the implementation of a graphical user interface for task 7
from tkinter.filedialog import askopenfilename  #import askopenfilename to allow the gui to change the dataset file
import argparse                                 #import argparse to create a command line interface
from tkinter import messagebox                  #import messagebox to show errors to the user
import dataimport
import tasks

#Task 7
class Gui:
    #initialise the parameters used for the task7 objects
    def __init__(self):
        self.data = []
    
    #-------------------------------------TASK 7-------------------------------------
    def make_gui(self, doc_uuid=None, visitor_uuid=None):
        #set window to Tk()
        window = Tk()
        #configure the window settings
        window.title("Data Document Tracker")
        window.geometry('500x500')
        window.configure(bg='white')
        
        #configure label settings
        doc_uuid_label = Label(window, text="Document UUID:")
        doc_uuid_label.place(x = 3, y = 40)
        doc_uuid_label.configure(bg='white')
        vis_uuid_label = Label(window, text="Visitor UUID:")
        vis_uuid_label.place(x = 25, y = 70)
        vis_uuid_label.configure(bg='white')

        #configure Entries
        doc_uuid_entry = Entry(window,width=65)
        doc_uuid_entry.place(x = 95, y = 40)
        if doc_uuid is not None:
            doc_uuid_entry.insert(0, doc_uuid)
        vis_uuid_entry = Entry(window,width=65)
        vis_uuid_entry.place(x = 95, y = 70)
        if visitor_uuid is not None:
            vis_uuid_entry.insert(0, visitor_uuid)

        #configure the change file button
        btnFile = Button(window, text="Select input data file", bg='white', width = 40, command=lambda: self.changefile())
        btnFile.place(x = 3, y = 10)

        #Configure task buttons
        btn2a = Button(window, text="2a. Views by Country", bg='white', width = 30, command=lambda: self.task2a(doc_uuid_entry.get()))
        btn2b = Button(window, text="2b. Views by Continent", bg='white', width = 30, command=lambda: self.task2b(doc_uuid_entry.get()))
        btn3a = Button(window, text="3a. Views by Browser", bg='white', width = 30, command=self.task3a)
        btn3b1 = Button(window, text="3b. Views by Browser Method 1", bg='white', width = 30, command=self.task3b1)
        btn3b2 = Button(window, text="3b. Views by Browser Method 2", bg='white', width = 30, command=self.task3b2)
        btn4 = Button(window, text="4. View Time by User", bg='white', width = 30, command=self.task4)
        btn5 = Button(window, text="5/6. Display Also Likes Graph", bg='white', width = 30, command=lambda: self.task5and6helper(doc_uuid_entry.get(), vis_uuid_entry.get()))
        btn6 = Button(window, text="AF2. Most Popular Visitor Sources", bg='white', width = 30, command=self.af2)
        btn7 = Button(window, text="AF3. Most Popular Visitor Devices", bg='white', width = 30, command=self.af3)
        btn8 = Button(window, text="AF5. Most Popular Referrers", bg='white', width = 30, command=self.af5)

        #Place task buttons
        btn2a.place(x = 260, y = 110)
        btn2b.place(x = 260, y = 140)
        btn3a.place(x = 260, y = 170)
        btn3b1.place(x = 260, y = 200)
        btn3b2.place(x = 260, y = 230)
        btn4.place(x = 260, y = 260)
        btn5.place(x = 260, y = 290)
        btn6.place(x = 260, y= 320)
        btn7.place(x = 260, y= 350)
        btn8.place(x = 260, y= 380)

        #block execution of anymore code after this line
        window.mainloop()

    #definitions of each task to be called by buttons
    def changefile(self):
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        jfile = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        import_data = dataimport.DataImport(jfile)
        self.data = []
        self.data = import_data.open_json()
        print("File has been changed to: " + jfile)
        
    
    def task2a(self, doc_uuid):
        if (self.data == []):
            messagebox.showerror(title="Error", message="Please choose a data file")
        else:
            if(doc_uuid == ""):
                messagebox.showerror(title="Error", message="Please enter a document ID")
            else:
                task2 = tasks.Task2(doc_uuid, True, self.data)
                task2.display_views_by_country()
    
    
    def task2b(self, doc_uuid):
        if (self.data == []):
            messagebox.showerror(title="Error", message="Please choose a data file")
        else:
            if(doc_uuid == ""):
                messagebox.showerror(title="Error", message="Please enter a document ID")
            else:
                task2 = tasks.Task2(doc_uuid, True, self.data)
                task2.display_views_by_continent()
    
    def task3a(self):
        if (self.data == []):
            messagebox.showerror(title="Error", message="Please choose a data file")
        else:
            task3 = tasks.Task3(self.data)
            task3.display_views_by_browser_part_a()

    def task3b1(self):
        if (self.data == []):
            messagebox.showerror(title="Error", message="Please choose a data file")
        else:
            task3 = tasks.Task3(self.data)
            task3.display_views_by_browser_short_a()
    
    def task3b2(self):
        if (self.data == []):
            messagebox.showerror(title="Error", message="Please choose a data file")
        else:
            task3 = tasks.Task3(self.data)
            task3.display_views_by_browser_short_b()

    def task4(self):
        if (self.data == []):
            messagebox.showerror(title="Error", message="Please choose a data file")
        else:
            task4 = tasks.Task4(self.data)
            task4.display_viewtime_by_userid()
    
    def task5and6(self, doc_uuid, visitor_uuid=None):
        if (self.data == []):
            messagebox.showerror(title="Error", message="Please choose a data file")
        else:
            if(doc_uuid == ""):
                messagebox.showerror(title="Error", message="Please enter a document ID")
            else:
                task6 = tasks.Task6(doc_uuid, self.data, visitor_uuid)
                task6.alsolikesgraph()

    def task5and6helper(self, doc_uuid, visitor_uuid):
        visEmpty = None
        if (self.data == []):
            messagebox.showerror(title="Error", message="Please choose a data file")
        else:
            if (visitor_uuid == ""):
                self.task5and6(doc_uuid, visEmpty)
            else:
                self.task5and6(doc_uuid, visitor_uuid)
    
    def af2(self):
        if (self.data == []):
            messagebox.showerror(title="Error", message="Please choose a data file")
        else:
            af2 = tasks.AdditionalFeatures(self.data)
            af2.most_popular_visitor_source()
    
    def af3(self):
        if (self.data == []):
            messagebox.showerror(title="Error", message="Please choose a data file")
        else:
            af3 = tasks.AdditionalFeatures(self.data)
            af3.most_popular_visitor_device()
    
    def af5(self):
        if (self.data == []):
            messagebox.showerror(title="Error", message="Please choose a data file")
        else:
            af5 = tasks.AdditionalFeatures(self.data)
            af5.most_popular_referrers()


#Task 8
class Task8:

     #initialise the parameters used for the task8 objects
    def __init__(self, doc_uuid=None, visitor_uuid=None, file_name=None):
        self.doc_uuid = doc_uuid
        self.visitor_uuid = visitor_uuid
        self.file_name = file_name
        self.data = []
        # using the argparse library to create an initial parser for command line interface commands
        self.cmd_parser = argparse.ArgumentParser(description= 'Document Tracker interface.')
        # visitor uid is optional: made option with the --uid flag
        self.cmd_parser.add_argument('-u', '--uid', type=str, help='The visitor ID to analyse.')
        # remaining commands are mandatory
        self.cmd_parser.add_argument('-d', type=str, help='The document ID to analyse.')
        self.cmd_parser.add_argument('-t', type=str, help='The specified task to anaylse.')
        self.cmd_parser.add_argument('-f', type=str, help='The path to the JSON file.')
        self.cmd_parser.add_argument('-af1', type=str, help="Additional feature: search for users in a file with a specified substring. Use the -u flag to specify a string to search for, eg. -u ")
        self.cmd_parser.add_argument('-af2', type=str, help="Additional feature: search for documents in a file with a specified substring. Use the -d flag to specify a string to search for, eg. -d ad902")
        self.cmd_parser.add_argument('-af3', type=str, help="Additional feature: find the most popular visitor sources in a JSON file.")
        self.cmd_parser.add_argument('-af4', type=str, help="Additional feature: find the most popular devices in a JSON file.")
        self.cmd_parser.add_argument('-af5', type=str, help="Additional feature: find the top 10 most popular referrers in a JSON file.")
       
        self.cmd_args = self.cmd_parser.parse_args()

    def cmd_checking(self):
        # initial checking for errors in the command line interface
        # making sure arguments are provided correctly and only consist of the allowed features
        if self.cmd_args.uid:
            self.visitor_uuid = self.cmd_args.uid
        if self.cmd_args.t is None:
            print("No task ID provided, please re-enter.")
        if self.cmd_args.t not in ['2a', '2b', '3a', '3b', '4', '5d', '6', '7', 'af1', 'af2', 'af3', 'af4', 'af5']:
            print("Invalid task ID provided, please re-enter (options: 2a, 2b, 3a, 3b, 4, 5d, 6, 7, af1, af2, af3, af4, af5).")
        if self.cmd_args.d is None:
            print("No document ID provided, please re-enter.")
        if self.cmd_args.f is None:
            print("No JSON file path provided, please re-enter.")
        self.doc_uuid = self.cmd_args.d
        self.file_name = self.cmd_args.f
        import_data = dataimport.DataImport(self.cmd_args.f) 
        self.data = import_data.open_json()
        self.cmd_execute(self.cmd_args.t)
        
    def cmd_execute(self, id):
        # this is where the commands are executed within the command line
        task2 = tasks.Task2(self.doc_uuid, True, self.data)
        task3 = tasks.Task3(self.data)
        task4 = tasks.Task4(self.data)
        task5 = tasks.Task5(self.doc_uuid, self.data, self.visitor_uuid)
        task6 = tasks.Task6(self.doc_uuid, self.data, self.visitor_uuid)
        task7 = Gui()
        taskA = tasks.AdditionalFeatures(self.data)
        # running the different tasks based on the -t flag
        if id == '2a':
            task2.display_views_by_country()
        if id == '2b':
            task2.display_views_by_continent()
        if id == '3a':
            task3.display_views_by_browser_part_a()
        if id == '3b':
            task3.display_views_by_browser_short_a()
        if id == '4':
            task4.display_viewtime_by_userid()
        if id == '5d':
            task5.also_likes_top_10(self.doc_uuid, self.visitor_uuid)
        if id == '6':
            task6.alsolikesgraph()
        if id == '7':
            # if task 7 is provided, a feature was added to open the GUI with the document ID, file path, and visitor ID provided in the command
            # when the GUI is open, these values are defaulted to their text boxes
            import_data = dataimport.DataImport(self.file_name)
            self.data = []
            self.data = import_data.open_json()
            task7.make_gui(self.doc_uuid, self.visitor_uuid)
        if id == 'af1':
            taskA.find_users_with_key(self.visitor_uuid)
        if id == 'af2':
            taskA.find_documents_with_key(self.doc_uuid)
        if id == 'af3':
            taskA.most_popular_visitor_source()
        if id == 'af4':
            taskA.most_popular_visitor_device()
        if id == 'af5':
            taskA.most_popular_referrers()
        

# final checking for command line
# if more than one argument is specified, then begin the command line interface
# otherwise, open up the GUI
if len(sys.argv) == 1:
    gui = Gui()
    gui.make_gui()
    sys.exit()
else:
    cmd = Task8()
    cmd.cmd_checking()
    sys.exit()
