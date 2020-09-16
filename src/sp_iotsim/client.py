"""
WebSockets client

This program receives simulated data for multiple rooms, with multiple sensors per room.

The default behavior is to only access the computer itself by parameter "localhost"
so that no firewall edits are needed.

The port number is arbitrary, as long as the server and client are on the same port all is well.

Naturally, the server must be started before this client attempts to connect.
"""

import websockets
import zlib
from pathlib import Path
import argparse
import asyncio
import sys
import json
import statistics
import pandas as pd
import os
from datetime import datetime
import typing as T
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss


async def main(port: int, addr: str, max_packets: int, log_file: Path = None):
    """

    Parameters
    ----------

    port: int
        the network port to use (arbitrary, must match server)
    addr: str
        the address of the server (localhost if on same computer)
    max_packets: int
        to avoid using all the hard drive if the client is left running,
        we set a maximum number of packets before shutting the client down
    log_file: pathlib.Path
        where to store the data received (student must add code for this)
    """

    uri = f"ws://{addr}:{port}"

    async with websockets.connect(uri) as websocket:
        qb = await websocket.recv()
        if isinstance(qb, bytes):
            print(zlib.decompress(qb).decode("utf8"))
        else:
            print(qb)

        if log_file:
            log_file = Path(log_file).expanduser()
            #raise NotImplementedError("The code to open the file should be here.")

        for _ in range(max_packets):
            data = await websocket.recv()
            #print(data)
            print_stdout = sys.stdout               #Redirects printed JSON data

            with open(log_file, "a") as f:          #Opens/creates file to append JSON string
                sys.stdout = f 
                print(data)                         #Prints JSON data to file
                sys.stdout = print_stdout           #Reverts output back to terminal
           

def cli():
    p = argparse.ArgumentParser(description="WebSocket client")
    p.add_argument("-l", "--log", help="file to log JSON data")
    p.add_argument("-host", help="Host address", default="localhost")
    p.add_argument("-port", help="network port", type=int, default=8765)
    p.add_argument(
        "-max_packets",
        help="shut down program after total packages received",
        type=int,
        default=100000,
    )
    P = p.parse_args()


    try:
        asyncio.run(main(P.port, P.host, P.max_packets, P.log))
    except KeyboardInterrupt:
        print(P.log)
        
        temperature = {}                            #At keyboard interrupt, creates dicts for each variable
        occupancy = {}
        co2 = {}
        times = []
        
        with open(P.log, "r") as stuff:             #Open file with JSON data to read into
            for line in stuff:
                r = json.loads(line)                #Loops through every line in file
                roomkeys = list(r.keys())[0]        #Creates "keys" to use as index for dicts
                time = datetime.fromisoformat(r[roomkeys]["time"])
                
                temperature[time] = {roomkeys: r[roomkeys]["temperature"][0]}       #Dict with data of each variable 
                occupancy[time] = {roomkeys: r[roomkeys]["occupancy"][0]}
                co2[time] = {roomkeys: r[roomkeys]["co2"][0]}
                times.append(time)

      
        
        chooseroom = input("Please choose a room: office, lab1, class1\n")          #User chooses room
        print("\n")
        
        #print("Now Displaying Temperature...")
        temp = pd.DataFrame.from_dict(temperature, "index").sort_index()            #Load dict into panda dataframe
        x1 = temp[chooseroom].dropna()                                              #Remove any NaN from dataframe
        #print(temp[chooseroom].dropna())   
        #print("\n")
        
        print("Temperature Variance is...")
        print(temp[chooseroom].dropna().var())                                      #Print variance of data
        print("\n")
        
        print("Temperature Median is...")
        print(temp[chooseroom].dropna().median())                                   #Print median of data
        print("\n")
        
        
        
        
        #print("Now Displaying Occupancy...")
        occu = pd.DataFrame.from_dict(occupancy, "index").sort_index()              #Load dict into panda dataframe
        x2 = occu[chooseroom].dropna()                                              #Remove any NaN from dataframe
        #print(occu[chooseroom].dropna())
        #print("\n")
        
        print("Occupancy Variance is...")
        print(occu[chooseroom].dropna().var())                                      #Print variance of data
        print("\n")
        
        print("Occupancy Median is...")
        print(occu[chooseroom].dropna().median())                                   #Print median of data
        print("\n")
        
       
        
        
        #print("Now Displaying CO2...")
        carb = pd.DataFrame.from_dict(co2, "index").sort_index()                    #Load dict into panda dataframe
        x3 = carb[chooseroom].dropna()                                              #Remove any NaN from dataframe
        #print(carb[chooseroom].dropna())
        
        
        
        
        
        plt.figure(1)                                                               #Create histogram plot of data
        x1.hist(bins = 100)
        plt.xlabel("Temperature")
        plt.ylabel("Occurance")
        plt.title("Frequency of Temperatures")
        
        plt.figure(2)                                                               #Create histogram plot of data
        x2.hist()
        plt.xlabel("People")
        plt.ylabel("Occurance")
        plt.title("Frequency of the Number of People")
        
        plt.figure(3)                                                               #Create histogram plot of data
        x3.hist()
        plt.xlabel("CO2 Levels")
        plt.ylabel("Occurance")
        plt.title("Frequency of CO2 Levels")
        

        times = temp.index                                                          #Creates index for time data

        plt.figure(4)                                                               #Create plot for time intervals
        plt.hist(np.diff(times.values).astype(np.int64) // 1000000000, bins = 100)
        plt.xlabel("Time (seconds)")
        plt.ylabel("Occurrences")
        plt.title("Time Intervals between Sensor Readings")
        
        timeint = np.diff(times.values).astype(np.int64) / 1000000000               #Creates list for time intervals  
        
        timeintvar = np.var(timeint)                                                #Calculate and print variance of time interval
        print("Time Interval Variance is...")
        print(timeintvar)
        print("\n")
        
        timeintmean = np.mean(timeint)                                              #Calculate and print mean of time interval
        print("Time Interval Mean is...")
        print(timeintmean)
        print("\n")
    
        plt.show()
        
        #os.remove("data.txt")


if __name__ == "__main__":
    cli()
