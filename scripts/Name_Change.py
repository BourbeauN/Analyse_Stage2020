import numpy as np
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-f', dest = 'INFOLDER', help = 'file folder corresponding to experimental set with discharge infos')
args = parser.parse_args()

Results = pd.read_csv(args.INFOLDER, skiprows = 10)

def change_name(fname):
    fname.replace("um","").replace("tung","Tungsten_")
    
    return fname

gap = change_name(args.INFOLDER)

pd.DataFrame(Results).to_csv('Audren/Distance_Data/{}.csv'.format(gap))
