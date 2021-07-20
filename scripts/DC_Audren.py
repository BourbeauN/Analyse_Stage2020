import pandas as pd
import argparse
import numpy as np
import os
import pdb

##Data loading function

def load_data(filename):    
    
    Results = pd.read_csv(filename, skiprows = 10)

    time = Results['TIME']
    voltage = Results['CH1']
    current = Results['CH2']
    
    return np.array(time), np.array(voltage), np.array(current) 

def max_current(path):
    
    Current_Tab = []    
    count = 0
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    for i, f in enumerate(files) :
        time, voltage, current = load_data(os.path.join(path,f))
        max_value = np.amax(current)
        min_value = np.amin(current)
        
        count += 1

        Current_Tab.append([f,max_value,min_value])
        
    return np.asarray(Current_Tab)

def Peak(Extremums,BV):  
    DC = []
    count = 0
    for i in range(len(BV)):
        #pdb.set_trace()

        if BV[i]>0:
            peak = Extremums[i,1]

        elif BV[i]<0:
            peak = Extremums[i,2]

        elif BV[i]/BV[i]!=1:
            peak = float("nan")

        count+=1
        DC.append([i,peak])

    return np.asarray(DC)


def main ():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFILE', help = 'discharge file')
    parser.add_argument('-b', dest = 'BREAKDOWN', help = 'Breakdown file')
    args = parser.parse_args()
    outfile = args.INFILE.split('/')[-1] 

    MAX_CURRENT_TAB = max_current(args.INFILE)
    
    BV_Data = pd.read_csv(args.BREAKDOWN)
    BV = np.asarray(BV_Data['Voltage'])

    PEAK = Peak(MAX_CURRENT_TAB,BV)

    filename = args.INFILE
    #info = filename.split("/")[1]

    Amp = filename.split("/")[-1]
    Wid = filename.split("/")[-2]
    Pol = filename.split("/")[-3]
    info = "_".join((Amp,Wid,Pol))


    pd.DataFrame(PEAK, columns = ['ID', 'Discharge Current']).to_csv(os.path.join('Tian/Analysis/DC/{}.csv'.format(info))) 

main()
