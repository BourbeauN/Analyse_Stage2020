import pdb
import numpy as np
import os
import argparse
import pandas as pd

def discharge_time_index(voltage_inf, time_inf, dv, dk):
    time_inf = np.asarray(time_inf)
    voltage_inf = np.asarray(voltage_inf)

    time = time_inf[voltage_inf<1e208]
    voltage = voltage_inf[voltage_inf<1e208]
    if len(time_inf)-len(time)<20:
        for k in range(dk, len(time)) :
            if (voltage[k-dk] - voltage[k]) > dv :
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
    #pdb.set_trace() 
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    progress = 0
    
    # RESULTS
    PLATEAU_TABLE = []

    VOLT_DIS_TABLE = []
    # cycle through all files 
    for i,f in enumerate(files) :
        
        #print(f)

        time, voltage, current = load_data(os.path.join(path,f))
        
        end, volt_dis = discharge_time_index(voltage, time, dv, dk)
        
        PLATEAU_TABLE.append([f,end])
        VOLT_DIS_TABLE.append([f,volt_dis])
        
        progress +=1
        
        if progress%50 == 0:
            print(progress, end)
        

    return np.asarray(PLATEAU_TABLE),np.asarray(VOLT_DIS_TABLE)

def get_info(fname):
    info = fname.split("/")[-1]
    
    return info

def main():
    
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFOLDER', help = 'file folder corresponding to experimental set with discharge infos')
    parser.add_argument('-dv',type = int,  dest = 'VOLTAGE_THRESHOLD', help = 'pick a value for voltage threshold')
    parser.add_argument('-dk',type = int,  dest = 'INDEX_THRESHOLD', help = 'pick a value for time threshold')
    args = parser.parse_args()
    PLATEAU, VOLT_DIS = Plateau_Discharge(args.INFOLDER,args.VOLTAGE_THRESHOLD,args.INDEX_THRESHOLD)
    info = get_info(args.INFOLDER)

    print("Finished appending, saving tables...")
    
    pd.DataFrame(PLATEAU, columns = ['Filename','Plateau']).to_csv('Audren/Distance_Analysis/Discharge_Delay/{}.csv'.format(info))
    pd.DataFrame(VOLT_DIS, columns = ['Filename','Voltage']).to_csv("Audren/Distance_Analysis/Discharge_Voltage/{}.csv".format(info))
   
#update
main()
