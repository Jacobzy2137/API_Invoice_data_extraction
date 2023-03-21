#importing all the dependencies
import os
import os.path
import csv
import re
import API_KEY
from mindee import Client, documents
from contextlib import redirect_stdout


#cleaning out.txt in preparation for the rest of code
with open('out.txt', 'w') as f:
    pass

file_path = input('Enter file path: ')

#creating database that will containg all the records
header = ['Invoice Number', 'Invoice Date', 'Invoice Due Date', 'Supplier Name', 'Tax Amount', 'Total Amount', 'Currency']
if os.path.exists('Invoice_Data.csv'):
    pass
else:
    with open('Invoice_Data.csv', 'w', newline='', encoding='UTF8') as f:
      writer = csv.writer(f)
      writer.writerow(header)
      
mindee_client = Client(str(API_KEY.KEY))
input_doc = mindee_client.doc_from_path(str(file_path))
api_response = input_doc.parse(documents.TypeInvoiceV4)
with open('out.txt', 'w') as f:
    with redirect_stdout(f):
        print(api_response.document)
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
            data.append(Currency[0])
            
        
    print(data)
    with open('Invoice_data.csv', 'a+', newline = '', encoding = 'UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        data.clear()