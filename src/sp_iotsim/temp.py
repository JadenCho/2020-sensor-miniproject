import argparse
#from sp_iotsim.fileio import load_data
import pandas as pd
import numpy as np
import json
from datetime import datetime


parser = argparse.ArgumentParser()
parser.add_argument('filepath', help='file read in to analyze')
args = parser.parse_args()
filepath = args.filepath

#data = load_data(filepath)
#print(data)
temperature = {}
with open(filepath, "r") as stuff:
    for line in stuff:
        r = json.loads(line)
        roomkeys = list(r.keys())[0]
        time = datetime.fromisoformat(r[roomkeys]["time"])
                
        temperature[time] = {roomkeys: r[roomkeys]["temperature"][0]}

temp = pd.DataFrame.from_dict(temperature, "index").sort_index()

chooseroom = input("Please choose a room: office, lab1, class1\n")
print("\n")
    
temp_values = temp[chooseroom].dropna()

temp_std = np.std(temp_values)   #standard deviation of temperature values
temp_mean_original = np.mean(temp_values) # mean of temperature values (before taking out outlier points)

totaltempvals = len(temp_values) #total number of temperature data points
tempoutliers = 0                 #initialize counter for number of "bad" data points

for k in temp_values:                   #index through all temperature data points. if a data point is an outlier, the counter is incremented and the value is removed.
    if ((temp_values[k] > (temp_std + temp_mean_original)) or (temp_values[k] < (temp_mean_original - temp_std))):     #conditional for removing outliers (within one standard dev of mean)        
        remove(temp_values[k])
        tempoutliers = tempoutliers + 1
        
percentage = tempoutliers/totaltempvals                         #percentage of bad points/total
print("The percent of bad data points is ", percentage)

tempmean = temp_values.mean()                                   #mean of temperature values with outlier points removed
print("The mean of the temperature values is ", tempmean)

tempvar = temp_values.var()                                     #variance of temperature values with outlier points removed
print("The variance of the temperature values is ", tempvar)    
    
