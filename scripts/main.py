import pdb
import numpy as np
import os
import argparse
import pandas as pd
from scipy.signal import savgol_filter
from Plateau import * 
import Max_Voltage
import Max_Current

def main():
    
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFOLDER', help = 'file folder corresponding to experimental set with discharge infos')
    parser.add_argument('-dv',type = float,  dest = 'VOLTAGE_THRESHOLD', help = 'pick a value for voltage threshold')
    parser.add_argument('-dk',type = int,  dest = 'INDEX_THRESHOLD', help = 'pick a value for time threshold')
    args = parser.parse_args()
    outfile = args.INFOLDER.split('/')[-1] 
    
    ##### COMPUTE PLATEAU LENGTHS ###########
    RESULTS_TABLE = compute_plateaus_on_data(args.INFOLDER,args.VOLTAGE_THRESHOLD,args.INDEX_THRESHOLD)
    print("Finished Plateau computation appending RESULTS_TABLE, saving ...")
    PLATEAUS = pd.DataFrame(RESULTS_TABLE, columns = ['Filename', 'Plateau'])
    
    ##### COMPUTE MAX VOLTAGE ###############
    MAX_TENSION_TAB = Max_Voltage.max_voltage(args.INFOLDER)

    MAX_VOLTAGE = pd.DataFrame(MAX_TENSION_TAB, columns = ['Filename', 'Max Voltage'])

    
    ##### COMPUTE MAX CURRENT ###############
    MAX_CURRENT_TAB = Max_Current.max_current(args.INFOLDER)

    MAX_CURRENT = pd.DataFrame(MAX_CURRENT_TAB, columns = ['Filename', 'Max Current'])
    
    pdb.set_trace()
#update

