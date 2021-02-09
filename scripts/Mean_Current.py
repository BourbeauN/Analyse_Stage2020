import pdb
import numpy as np
import argparse
import pandas as pd
import os

def Mean_cal(path,data):
    
    mean = np.mean(data)
    
    return mean
def load_data(filename):

    Results = pd.read_csv(filename,skiprows=10)
    current = Results["CH2"]

    return current

def get_info(fname):
    info = fname.split("/")[-1]
    
    return info

def main():
    
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFOLDER', help = 'file folder corresponding to experimental set with discharge infos')
    args = parser.parse_args()

    #pdb.set_trace() 
    # list of discharge files  
    files = sorted(os.listdir(args.INFOLDER))
    
    progress = 0
    
    # RESULTS
    mean_curr = []

    info = get_info(args.INFOLDER)

    # cycle through all files 
    for i,f in enumerate(files) :
        current = load_data(os.path.join(args.INFOLDER,f))  
        mean = Mean_cal(f,current)
        mean_curr.append([f,mean])
        
    mean_curr = np.asarray(mean_curr)        
 
    pd.DataFrame(mean_curr, columns = ['Filename','Mean']).to_csv('Analysis/Mean_Current/{}.csv'.format(info))

main()
