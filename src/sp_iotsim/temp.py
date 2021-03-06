import argparse
#from sp_iotsim.fileio import load_data
import pandas as pd
import numpy as np
import json
from datetime import datetime
import statistics as ss


parser = argparse.ArgumentParser()
parser.add_argument('filepath', help='file read in to analyze')
args = parser.parse_args()
filepath = args.filepath


temperature = {}                                        #Load temperature data from file
with open(filepath, "r") as stuff:
    for line in stuff:
        r = json.loads(line)
        roomkeys = list(r.keys())[0]
        time = datetime.fromisoformat(r[roomkeys]["time"])
                
        temperature[time] = {roomkeys: r[roomkeys]["temperature"][0]}

temp = pd.DataFrame.from_dict(temperature, "index").sort_index()        #Create panda dataframe for data

chooseroom = input("Please choose a room: office, lab1, class1\n")      #User chooses room
print("\n")
    
temp_values = temp[chooseroom].dropna()                                 #Removes NaN from the dataframe
#print(temp_values)

temp_std = np.std(temp_values)   #standard deviation of temperature values          #Find standard deviation of temperature values
#print("Standard Dev")
#print(temp_std)
temp_mean_original = np.mean(temp_values) # mean of temperature values (before taking out outlier points)           #Find mean of temperature values
#print("Original Mean")
#print(temp_mean_original)

totaltempvals = len(temp_values) #total number of temperature data points              
tempoutliers = 0                 #initialize counter for number of "bad" data points
newtemp_values = []

for k in temp_values:                  #index through all temperature data points. if a data point is an outlier, the counter is incremented and the value is removed.
    if ((k > (temp_std + temp_mean_original)) or (k < (temp_mean_original - temp_std))):     #conditional for removing outliers (within one standard dev of mean)        
        newtemp_values.append(k)
        tempoutliers = tempoutliers + 1
        
percentage = round((tempoutliers/totaltempvals)*100,2)                         #percentage of bad points/total
print("The percent of bad data points is ", percentage,"%")

tempmed = ss.median(newtemp_values)                                   #median of temperature values with outlier points removed
print("The median of the temperature values is ", round(tempmed,2),"C")

tempvar = ss.variance(newtemp_values)                                     #variance of temperature values with outlier points removed
print("The variance of the temperature values is ", round(tempvar,2),"C")    
    
