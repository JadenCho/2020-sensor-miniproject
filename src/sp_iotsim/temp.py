import argparse
from sp_iotsim.fileio import load_data

parser = argparse.ArgumentParser()
parser.add_argument('filepath', help='file read in to analyze')
args = parser.parse_args()
file = args.filepath

data = load_data(file)
