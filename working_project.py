#importing all the dependencies
import os
import os.path
import csv
import re
import API_KEY
import tkinter as tk
from tkinter import filedialog as fd
from mindee import Client, documents
from contextlib import redirect_stdout


#cleaning out.txt in preparation for the rest of code
with open('out.txt', 'w') as f:
    pass

#creating database that will containg all the records
header = ['Invoice Number', 'Invoice Date', 'Invoice Due Date', 'Supplier Name', 'Tax Amount', 'Total Amount', 'Currency']
if os.path.exists('Invoice_Data.csv'):
    pass
else:
    with open('Invoice_Data.csv', 'w', newline='', encoding='UTF8') as f:
      writer = csv.writer(f)
      writer.writerow(header)

#function tied to a button, selects a file and checks which button was pressed with a global variable
def Select_file():
   with open('selected_file.txt', 'w') as f:
        with redirect_stdout(f):
            print(fd.askopenfilename())
   global Button_clicked
   Button_clicked = 0
   
#function tied to a button, selects a dir and checks which button was pressed using a global variable            
def Select_dir():
    with open('selected_directory.txt', 'w') as f:
        user_input_file = fd.askdirectory()
        with redirect_stdout(f):
            print(user_input_file)
    global Button_clicked
    Button_clicked = 1

#if directory was chosen this iterates through it and using Data.extractor() and two txt files for output and input
def Directory():
    mindee_client = Client(str(API_KEY.KEY))
    i=0
    
    with open('selected_directory.txt', 'r') as f:
        user_input_dir = f.read()
        user_input_dir = user_input_dir.strip('\n')
        user_input_dir = str(user_input_dir)
        
    for filename in os.listdir(user_input_dir):
        f = os.path.join(str(user_input_dir), filename)
        if i > 0:
            Data_extractor()
        if os.path.isfile(f):
            input_file = os.path.join(str(user_input_dir), filename)
            input_doc = mindee_client.doc_from_path(input_file)
            api_response = input_doc.parse(documents.TypeInvoiceV4)
            with open('out.txt', 'w') as f:
                with redirect_stdout(f):
                    print(api_response.document)
                    i=+1


#if file was chosen this takes file path as input, with help of two txt files. Outputs into out.txt    
def One_File():
    mindee_client = Client(str(API_KEY.KEY))
    with open('selected_file.txt', 'r+') as f:
        user_input_file = f.read()
        user_input_file = user_input_file.strip('\n')
    input_doc = mindee_client.doc_from_path(str(user_input_file))
    api_response = input_doc.parse(documents.TypeInvoiceV4)
    with open('out.txt', 'w') as f:
        with redirect_stdout(f):
            print(api_response.document)
            
            
#reads the Invoice by line and extracts information out of it. Uses out.txt
def Data_extractor():
    data = []
    count = 0
    with open('out.txt', 'r') as f:
        Lines = f.readlines()
        for line in Lines:
            count += 1
                
            if 'Invoice number' in line:
                Invoice_number = line.strip('Invoice number: \n')
                data.append(Invoice_number)
                
            elif 'Supplier name' in line:
                Supplier_name = line.strip('Supplier name: \n')
                data.append(Supplier_name)
                
            elif 'Total amount including taxes' in line:
                Total_amount = line.strip('Total amount including taxes: \n')
                data.append(Total_amount)
            
            elif 'Total taxes' in line:
                Total_taxes = line.strip('Total taxes: \n')
                data.append(Total_taxes)
            
            elif 'Invoice date' in line:
                Invoice_date = line.strip('Invoice date: \n')
                data.append(Invoice_date)
                
            elif 'Invoice due date' in line:
                Due_date = line.strip('Invoice due date: \n')
                data.append(Due_date)
                
            elif 'Locale' in line:
                Currency = re.findall(pattern = '[A-Z]{3}', string = line)
                #Currency = Currency.search(line)
                data.append(Currency[0])
                
            
        print(data)
        with open('Invoice_data.csv', 'a+', newline = '', encoding = 'UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(data)
            data.clear()
            

#this part of code is responsible for the GUI
root = tk.Tk()
 
#size of the window
root.geometry("400x200")
#window title
root.title("Inovice Program")
 
#Textbox and its size
T = tk.Text(root, height = 5, width = 52)
 
#Window's label
l = tk.Label(root, text = "Inovoice Information Extractor")
l.config(font =("Courier", 14))
 
#text that will be inside the textbox
Info = """You can either choose one Invoice in pdf or image format for processing or can choose directory to process multiple Invoices at the same time. After selecting file click EXIT / RUN CODE"""
 
#button frame that will allow to place them on 2d plane
buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=1)
buttonframe.columnconfigure(1, weight=1)
buttonframe.columnconfigure(2, weight=1)

#all three buttons and their functions, and placements
b1 = tk.Button(buttonframe, text = "Choose One File",
               command = Select_file)
b1.grid(row=0, column=0)

b2 = tk.Button(buttonframe, text = "Choose a Directory", 
               command = Select_dir)
b2.grid(row=0, column=2)

b3 = tk.Button(buttonframe, text = "EXIT / RUN CODE",
               command = root.destroy)
b3.grid(row=1, column=1)
 
#putting everything on the actual window
l.pack()
T.pack()
buttonframe.pack(fill='x')
T.insert(tk.END, Info)
 
#infinite loop that holds the window open, cancelled by root.destroy
tk.mainloop()

#checking which button was clicked and calling Data_extractor() for a single file and Directory() that contains Data_extractor()
#responsible for data pulling after pressing a button
if Button_clicked == 0:
    One_File()
    Data_extractor()
else:
    Directory()