import pdb
import numpy as np
import argparse
import pandas as pd
import os

def Mean_cal(path,data)
    
    mean = np.mean(data)
    
    return mean

def get_info(fname):
    info = fname.split("/")[-1]
    
    return info

def main():
    
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFOLDER', help = 'file folder corresponding to experimental set with discharge infos')
    args = parser.parse_args()

    #loading data    
    Results = pd.read_csv(filename, skiprows = 10)
    
    #creating arrays for time, voltage and current
    time = Results["TIME"]
    voltage = Results["CH1"]
    current = Results["CH2"]
    
    #pdb.set_trace() 
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    progress = 0
    
    # RESULTS
    mean_curr = []

    info = get_info(args.INFOLDER)

    # cycle through all files 
    for i,f in enumerate(files) :
        
        mean = Mean_cal(f,current)
        mean_curr.append([f,mean])
    
        pd.DataFrame(PLATEAU, columns = ['Filename','Mean']).to_csv('Mean_Current/{}.csv'.format(info))

main()