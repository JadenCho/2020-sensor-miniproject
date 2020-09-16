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

print(temp)
