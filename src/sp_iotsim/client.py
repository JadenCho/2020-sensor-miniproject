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

    if log_file:
        log_file = Path(log_file).expanduser()

    uri = f"ws://{addr}:{port}"

    async with websockets.connect(uri) as websocket:
        qb = await websocket.recv()
        if isinstance(qb, bytes):
            print(zlib.decompress(qb).decode("utf8"))
        else:
            print(qb)

        for i in range(max_packets):
            data = await websocket.recv()
            if i % 5 == 0:
                pass
                # print(f"{i} total messages received")
            print(data)
            print_stdout = sys.stdout

            with open("data.txt", "a") as f:
                sys.stdout = f 
                print(data)
                sys.stdout = print_stdout 
                
def load_data(file: Path) -> T.Dict[str, pd.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}

    with open(file, "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])

            temperature[time] = {room: r[room]["temperature"][0]}
            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}

    data = {
        "temperature": pd.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pd.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pd.DataFrame.from_dict(co2, "index").sort_index(),
    }

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
       
        data = load_data("data.txt")
        
        print(data)
        
        
        #temperature = {}
        #occupancy = {}
        #co2 = {}

        #with open("data.txt", "r") as dataj:
        #    for line in dataj:
        #        r = json.loads(line)
        #        roomkeys = list(r.keys())[0]
        #        timeanddate = datetime.fromisoformat(r[roomkeys]["time"])

        #        temperature[timeanddate] = {roomkeys: r[roomkeys]["temperature"][0]}
        #        occupancy[timeanddate] = {roomkeys: r[roomkeys]["occupancy"][0]}
        #        co2[timeanddate] = {roomkeys: r[roomkeys]["co2"][0]}
                
                
        #data = {
        #"temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index()
        #}
        #print(data)


if __name__ == "__main__":
    cli()
