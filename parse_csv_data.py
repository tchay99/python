import os
import csv
import datetime
import json

def read_directory(directory): 
    #    This function reads the directory,
    #    gets all the directory files, parses them and returns a dictionary with
    #    filedate as key and filedata as a value
    historical_data = {} # initializing empty dictionary
    files = [] # initializing empty file list
    paths = [] # initializing file paths list - later used to concatenate full paths
    count = 0 # counter used to count how many files we have left to go through
    dir_path = '\\\\machinename\\sharename\\folder' # this is where your UNC path to the share goes
    for file in directory:
        files.append(file)
    while files:
        file = files.pop(0) # we process each item in the directory at a time
        fullpath = os.path.join(dir_path,file) # this is where we create the full path of each csv file
        paths.append(fullpath) # we add the full path of each file in a list
        while paths:
            file = paths.pop(0) # we process each file at a time
            modified_date = datetime.date.fromtimestamp(os.stat(fisier).st_mtime)
            modified_date_normalized = modified_date.strftime('%D')
            data = modified_date_normalized # we use the datetime module to get the file creation date
            with open(file, 'r') as file_handler:
                dailySLAdata = file_handler.readlines()
                statistics = dailySLAdata[1][36:] # with this we strip the part of the file data of no interest to us
                historical_data[data] = [statistics]
                count +=1
                print('%s : Added a set --> %s %s' %(count, data, statistics))
                print(len(files))
    return historical_data                    
   
def export_json(directory):
    historical_data = read_directory(directory)
    with open('historical_data.txt', 'w') as outfile:
        json.dump(historical_data, outfile)

def main():
    directory = os.listdir('\\\\machinename\\sharename\\folder') # this is where your UNC path to the share goes
    export_json(directory)

if __name__ =='__main__':
    main()

