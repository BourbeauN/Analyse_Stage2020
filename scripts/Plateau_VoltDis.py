import pdb
import numpy as np
import os
import argparse
import pandas as pd

def discharge_time_index(voltage, time, dv, dk):
    
    for k in range(dk, len(time)) :
        if (voltage[k-dk] - voltage[k]) > dv:
            index = k - dk
            end = time[index]
            voltage_dis = voltage[index]
                        
            return end,voltage_dis
        
    return float("nan"),float("nan")

def load_data(filename):

    #loading data    
    Results = pd.read_csv(filename, skiprows = 10)
    
    #creating arrays for time, voltage and current
    time = Results["TIME"]
    voltage = Results["CH1"]
    current = Results["CH2"]
    
    return time, voltage, current 

def Plateau_Discharge(path, dv, dk):
    
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    progress = 0
    
    # RESULTS
    PLATEAU_TABLE = []
    VOLT_DIS_TABLE = []
    # cycle through all files 
    for i,f in enumerate(files) :
        
        time, voltage, current = load_data(os.path.join(path,f))
        
        end, volt_dis = discharge_time_index(voltage, time, dv, dk)
        
        PLATEAU_TABLE.append([f,end])
        VOLT_DIS_TABLE.append([f,volt_dis])
        
        progress +=1
        
        if progress%50 == 0:
            print(progress, end)
        
    return np.asarray(PLATEAU_TABLE),np.asarray(VOLT_DIS_TABLE)

def main():
    
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFOLDER', help = 'file folder corresponding to experimental set with discharge infos')
    parser.add_argument('-dv',type = int,  dest = 'VOLTAGE_THRESHOLD', help = 'pick a value for voltage threshold')
    parser.add_argument('-dk',type = int,  dest = 'INDEX_THRESHOLD', help = 'pick a value for time threshold')
    args = parser.parse_args()
    outfile = args.INFOLDER.split('/')[-1] 
    PLATEAU, VOLT_DIS = Plateau_Discharge(args.INFOLDER,args.VOLTAGE_THRESHOLD,args.INDEX_THRESHOLD)

    print("Finished appending, saving tables...")
    
    pd.DataFrame(PLATEAU, columns = ['Filename', 'Plateau']).to_csv(os.path.join('OUT_TABLES',"PLATEAU_{}_{}dv_{}dk.csv".format(outfile,args.VOLTAGE_THRESHOLD,args.INDEX_THRESHOLD)))
    pd.DataFrame(VOLT_DIS, columns = ['Filename','Voltage']).to_csv(os.path.join('OUT_TABLES',"VOLT_DIS_{}_{}dv_{}dk.csv".format(outfile,args.VOLTAGE_THRESHOLD,args.INDEX_THRESHOLD)))

#update
main()
