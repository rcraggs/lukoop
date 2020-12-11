import getopt
import csv 
import json 
import os
import sys

path = ''
result_delimiter = '@'

HELP_MESSAGE = """
        lukoop.py 
        -c --command search/columns/list
        -p --path path to folder or file        
        """

def get_columns(csvFilePath, target_row):

    items_array = []

    with open(csvFilePath, encoding='utf-8-sig') as csvf: 
        csvReader = csv.DictReader(csvf) 

        for num, row in enumerate(csvReader):
            if num == target_row:
                for key in row.keys():
                    
                    # Create a script filter item from the array row       
                    item = {}
                    item['uid'] = key
                    item['title'] = key
                    item['subtitle'] = row[key]
                    item['arg'] = row[key]
                    items_array.append(item)                
                break            
    items = {}
    items['items'] = items_array

    print(json.dumps(items, indent = 3))

def search_json(csvFilePath): 
      
    # create the list of items to search
    items_array = []
      
    for root, d, f in os.walk(csvFilePath):
        for file in f:
            if '.csv' in file:
                
                # Open a csv reader called DictReader 
                with open(os.path.join(root, file), encoding='utf-8-sig') as csvf: 
                    csvReader = csv.DictReader(csvf) 

                    row_index = 0

                    # Add each item from the file to an array
                    for row in csvReader: 
                                
                        # Create a script filter item from the array row       
                        item = {}
                        uid = row[list(row.keys())[0]]
                        item['uid'] = uid
                        item['title'] = row[list(row.keys())[1]]
                        item['subtitle'] = ', '.join(str(x) for x in row.values())
                        item['arg'] = os.path.join(root, file) + result_delimiter + str(row_index) # row index?
                        item['match'] = ' '.join(str(x) for x in row.values())
                        items_array.append(item)

                        row_index += 1
  
    items = {}
    items['items'] = items_array

    print(json.dumps(items, indent = 3))

def sheets(csvFilePath): 
      
    # create the list of items to search
    items_array = []
      
    for root, d, f in os.walk(csvFilePath):
        for file in f:
            if '.csv' in file:
                
                item = {}
                uid = file
                item['uid'] = uid
                item['title'] = file
                items_array.append(item)
  
    items = {}
    items['items'] = items_array

    print(json.dumps(items, indent = 3))

folder = ""
command = "search"

try:

    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv, "c:p:h", ["command=", "path=", "help"])
    
except getopt.GetoptError:
    print(HELP_MESSAGE)
    sys.exit(2)
for opt, arg in opts:

    if opt == '-h':
        print(HELP_MESSAGE)
        sys.exit()
    elif opt in ("-p", "--path"):
        path = arg
    elif opt in ("-c", "--command"):
        command = arg
        
if command == "search":
    search_json(path)

elif command == "columns":
    just_path = path.split("@")[0]
    target_row = int(path.split("@")[1])
    get_columns(just_path, target_row)

elif command == "list":
    sheets(path)
