import pdb
import numpy as np
import os
import argparse
import pandas as pd

def discharge_time_index(voltage_inf, time_inf,current_inf, dv,dk):
    time_inf = np.asarray(time_inf)
    voltage_inf = np.asarray(voltage_inf)

    time = time_inf[(voltage_inf<1e208)&(voltage_inf>-1e208)&(current_inf>-1e208)&(current_inf<1e208)]
    voltage = voltage_inf[(voltage_inf<1e208) & (voltage_inf>-1e208)&(current_inf>-1e208)&(current_inf<1e208)]
    current = current_inf[(voltage_inf<1e208) & (voltage_inf>-1e208)&(current_inf>-1e208)&(current_inf<1e208)]     
    #pdb.set_trace()
    if len(time_inf)-len(time)<20:
        for k in range(dk, len(time)) :
            if np.abs(voltage[k-dk] - voltage[k]) > dv :
                #pdb.set_trace()
                index = k - dk
    
                return index,voltage[index]
                break        

    return float("nan"),float("nan")

def load_data(filename):
    #loading data    
    Results = pd.read_csv(filename, skiprows = 10)
    
    #creating arrays for time, voltage and current
    time = Results["TIME"]
    voltage = Results["CH1"]
    current = Results["CH2"]
    
    return time, voltage, current 

def Plateau_Discharge(path, dv, dk ,tr):
    #pdb.set_trace() 
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    progress = 0

    # RESULTS
    PLATEAU_TABLE = []

    VOLT_DIS_TABLE = []
    # cycle through all files 
    for i,f in enumerate(files) :
        
        time, voltage, current = load_data(os.path.join(path,f))
        
        index, volt_dis = discharge_time_index(voltage, time,current,dv,dk)

        delay = Begin_Trigger(args.TRIGGER,index,time)        

        PLATEAU_TABLE.append([f,delay])
        VOLT_DIS_TABLE.append([f,volt_dis])
        
        progress +=1
        if progress%200 == 0:
            print(progress, end)
            #pdb.set_trace()

    return np.asarray(PLATEAU_TABLE),np.asarray(VOLT_DIS_TABLE)

def Begin_Trigger(tr,index,time):
    begin = time[tr]
    end = time[index]
    delay = end - begin

    return float(delay)

def get_info(fname):
    info = fname.split("/")[1]
    
    return info

def main():
    
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFOLDER', help = 'file folder corresponding to experimental set with discharge infos')
    parser.add_argument('-dv',type = int, dest = 'VOLTAGE_THRESHOLD', help = 'pick a value for voltage threshold')
    parser.add_argument('-dk',type = int, dest = 'INDEX_THRESHOLD', help = 'pick a value for time threshold')
    parser.add_argument('-tr',type = int, dest = 'TRIGGER', help = 'voltage threshold', default = float(0))
    args = parser.parse_args()
    PLATEAU, VOLT_DIS = Plateau_Discharge(args.INFOLDER,args.VOLTAGE_THRESHOLD,args.INDEX_THRESHOLD,args.TRIGGER)
    info = get_info(args.INFOLDER)

    print("Finished appending, saving tables...")
    
    pd.DataFrame(PLATEAU, columns = ['Filename','Plateau']).to_csv('Tian/Analysis/DD/{}.csv'.format(info))
    pd.DataFrame(VOLT_DIS, columns = ['Filename','Voltage']).to_csv("Tian/Analysis/BV/{}.csv".format(info))
   
#update
main()
