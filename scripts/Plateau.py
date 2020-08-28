import pdb
import numpy as np
import os
import argparse
import pandas as pd
from scipy.signal import savgol_filter

#def Savitsky_Golay(y):
    #return savgol_filter(y,9,2)

def discharge_time_index(voltage, time, dv, dk):
    for k in range(dk, len(time)) :
        if voltage[k] - voltage[k - dk] < -dv:
	    index = k - dk
	    return index
    return float("nan")

def load_data(filename):
    
    Results = pd.read_csv(filename, skiprows = 10)
    
    time = Results["TIME"]

    voltage = Results["CH1"]

    current = Results["CH2"]

    return time, voltage, current 

def Plateaus_Discharge(path, dv, dk):
    
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    progress = 0
    
    # RESULTS
    PLATEAU_TABLE = []
    VOLT_DIS_TABLE = []
    # cycle through all files 
    for i,f in enumerate(files) :
        
        time, voltage, current = load_data(os.path.join(path,f))
        
	index = discharge_time_index(voltage, time, dv, dk)

	plateau = time[index]

	if plateau_end == plateau_end:
		plateau = plateau_end
	else 
		plateau = "nan"
	
	volt_dis = voltage[index]
        
        PLATEAU_TABLE.append([f,plateau])
	VOLT_DIS_TABLE.append([f,volt_dis])
        
        progress +=1
        
        if progress%50 == 0:
            print(progress, plateau)
        
    return np.asarray(PLATEAU_TABLE),np.asarray(VOLT_DIS_TABLE)

def main():
    
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFOLDER', help = 'file folder corresponding to experimental set with discharge infos')
    parser.add_argument('-dv',type = float,  dest = 'VOLTAGE_THRESHOLD', help = 'pick a value for voltage threshold')
    parser.add_argument('-dk',type = int,  dest = 'INDEX_THRESHOLD', help = 'pick a value for time threshold')
    args = parser.parse_args()
    outfile = args.INFOLDER.split('/')[-1] 
    PLATEAU, VOLT_DIS = compute_plateaus_on_data(args.INFOLDER,args.VOLTAGE_THRESHOLD,args.INDEX_THRESHOLD)

    print("Finished appending RESULTS_TABLE, saving ...")
    
    pd.DataFrame(RESULTS_TABLE, columns = ['Filename', 'Plateau']).to_csv(os.path.join('OUT_TABLES',"PLATEAU_{}_{}dv_{}dk.csv".format(outfile,args.VOLTAGE_THRESHOLD,args.INDEX_THRESHOLD)))
    pd.DataFrame(VOLT_DIS, columns =
    ['Filename','Voltage']).to_csv(os.path.join('OUT_TABLES',"VOLT_DIS_{}_{}dv_{}dk.csv".format(outfile,args.VOLTAGE_THRESHOLD,args.INDEX_THRESHOLD)))

#update
main()
