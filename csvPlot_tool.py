#!/usr/bin/Python 3

import csv
import matplotlib.pyplot as plt # library for mathematical calc + plotting
from matplotlib.ticker import FormatStrFormatter
import numpy as np # Arrayhandling
import pandas as pd # Data Frames   
import tkinter as tk
from tkinter import Tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
import threading # Multithreading
from threading import Thread as Process
from queue import Queue # Messagehandling
import queue
import sys



class Gui():
    def __init__(self, master, Queue, endCommand):
        self.queue = Queue
        # Set up the GUI
        master.geometry("600x350")
        master.grid_rowconfigure(6, minsize = "20")
        master.grid_rowconfigure(2, minsize = "20")
        master.grid_rowconfigure(14, minsize = "10")
        master.grid_rowconfigure(16, minsize = "10")
        master.grid_rowconfigure(19, minsize = "10")
        master.grid_rowconfigure(21, minsize = "10")
        master.grid_columnconfigure(8, minsize = "10")
        
        # Create style Object
        style = Style()
        
        style.configure('TButton', font =('Helvetica', 10, 'bold'),borderwidth = '3')
        
        # Changes will be reflected
        # by the movement of mouse.
        style.map('TButton', foreground = [('active', 'green')], background = [('active', 'black')])
        
        # *** BUTTONS ***
        self.B1 = Button(master, text = "Choose csv-file to import", command = self.fileOpen)
        self.BExit = Button(master, text = "Exit", command = endCommand)
        self.plotB = Button(master, text = "Plot graph", command = self.plot)    

        

        # *** LABELS ***
        self.l1 = Label(text = "Plotter tool", font=( "Helvetica","16", "bold"))
        self.spacer = Label(text = "")
        self.l2 = Label(text= "Select data column for y-axis")
        self.l3 = Label(text = "[first / second / third / fourth]")
        self.l4 = Label(text= "Select data column for x-axis")
        self.l5 = Label(text = "[first / second / third / fourth]")
        self.l6 = Label(text= "Type name for y-axis label (Optional)")
        self.l7 = Label(text = "Type name for x-axis label (Optional)")
        self.l8 = Label(text = "Please ensure that; \n there is no header row in the .csv file", foreground = "red", font =( "Helvetica",9))
        self.l9 = Label(text = "Type name for graph title (Optional)")

       

        # *** Widgets ***
        self.AxisY = Entry()
        self.AxisX = Entry()
        self.yName = Entry()
        self.xName = Entry() 
        self.title = Entry()
     


        # *** Put widgets and buttons on the screen ***
        self.B1.grid(row ="5", column = "4")

        self.l1.grid(row= "1", column = "4")
      
        self.BExit.grid(row = "25", column = "4")


        self.AxisY.grid(row = "7", column = "4")
        self.l2.grid(row = "7", column = "2")
        self.l3.grid(row = "8", column = "2")

        self.AxisX.grid(row = "10", column = "4")
        self.l4.grid(row = "10", column = "2")
        self.l5.grid(row = "12", column = "2")

        self.yName.grid(row = "13", column = "4")
        self.l6.grid(row = "13", column = "2")

        self.xName.grid(row = "15", column = "4")
        self.l7.grid(row = "15", column = "2")
        self.plotB.grid(row = "20", column = "4")
        self.l8.grid(row = "5", column = "10")
        self.title.grid(row = "17", column = "4")
        self.l9.grid(row = "17", column = "2")

                

        


    def processIncoming(self): # Not used in this gui
        '''Handle all messages currently in the queue'''
  
        while self.queue.qsize():
            try:
                msg = self.queue.get(0) # Check waiting messages
                

            except queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass
            except AttributeError:
                pass

    def fileOpen(self):
        
        try:
            self.fileName = askopenfilename()
            
            
        except FileNotFoundError:
            messagebox.showwarning("File not found", "Please select file first") 

    def plot(self): # If importing csv-file straight from HBM, delete header row 

        choice1 = self.AxisY.get().lower()
        choice2 = self.AxisX.get().lower()   
            

        try: 
            if choice1 == "first":
                yData = self.GetFirstcolumn()
            elif choice1 == "second":
                yData = self.GetSecondcolumn()
            elif choice1 == "third":
                yData = self.GetThirdcolumn()
            elif choice1 == "fourth":
                yData = self.GetFourthcolumn()
            else:
                raise NameError
        except NameError:
            messagebox.showwarning("NameError", "Check spelling when choosing data (columns)")
        except AttributeError:
            messagebox.showwarning("File not found", "Please select file first")  

        try:
            if choice2 == "first":
                xData = self.GetFirstcolumn()
            elif choice2 == "second":
                xData = self.GetSecondcolumn()
            elif choice2 == "third":
                xData = self.GetThirdcolumn()
            elif choice2 == "fourth":
                xData = self.GetFourthcolumn()
            else:
                raise NameError
        except NameError:
            messagebox.showwarning("NameError", "Check spelling when choosing data (columns)")
        except AttributeError:
            messagebox.showwarning("File not found", "Please select file first")  


        try:
            ypoints = np.array(yData) # y-axis data, input right function here
            xpoints = np.array(xData) # x-axis data, input right function here
            fig, ax = plt.subplots()
            ax.plot(xpoints,ypoints)
            ax.xaxis.set_major_formatter(FormatStrFormatter('%1.1f'))
            plt.plot(xpoints,ypoints,'m:', marker = '.')
            plt.xlabel(self.xName.get(), fontsize= 'medium')
            plt.ylabel(self.yName.get(), fontsize= 'medium')
            plt.title(self.title.get(), fontweight= 'semibold', fontsize= 'x-large')
            plt.show()          
        except TypeError:
            messagebox.showwarning("Unhashable type", "Please check csv-file format") 
        except UnboundLocalError:
            messagebox.showerror("Something went wrong", "Please try again")           




    # Get readings from csv and return them // Must be on the first column

    def GetFirstcolumn(self):
        input_file = pd.read_csv(self.fileName, usecols= [0], delimiter= ';', decimal= '.') # Check correct decimal
        df = pd.DataFrame(input_file)
        first = df
        return first

            

    # # Get readings from csv and return them // Must be on the second column

    def GetSecondcolumn(self):
        input_file = pd.read_csv(self.fileName, usecols= [1], delimiter= ';', decimal= '.') # Check correct decimal
        df = pd.DataFrame(input_file)
        second = df
        return second

    # Get readings from csv and return them // Must be on the third column

    def GetThirdcolumn(self):
        input_file = pd.read_csv(self.fileName, usecols= [2], delimiter= ';', decimal= ',', dtype= np.float64)
        df = pd.DataFrame(input_file)
        third = df
        return third

    # Get readings and return them // Must be on the fourth column

    def GetFourthcolumn(self):
        input_file = pd.read_csv(fileName, usecols= [3], delimiter= ';', decimal= ',')
        df = pd.DataFrame(input_file)
        fourth = df
        return fourth

class ThreadedClient(Gui):
    '''
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a same place.
    '''
    def __init__(self, master):
       
        
        '''
        Start the GUI and the asynchronous threads. This is the main 
        thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the workers (I/O).
        '''
        self.master = master

        # Create the queue
        self.queue = Queue()

        # Set up the GUI part
        self.gui = Gui(master, self.queue, self.endApplication)
        
        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target= self.workerThread1)


        

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        '''
        Check every 200 ms if there is something new in the queue.
        '''
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system.
            # Maybe some cleanup before actually shutting it down.

            sys.exit(1)
        self.master.after(200, self.periodicCall)

    def workerThread1(self): 
        pass


    def endApplication(self):
        self.running = 0

    ''' Turns out no multithreading was needed, but functionality is here so it's easier to add in the future'''





if __name__ == "__main__":
    root = tk.Tk()
    client = ThreadedClient(root)
    root.mainloop()