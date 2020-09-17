import pdb
import numpy as np
import scipy.integrate as sc
import os
import argparse
import pandas as pd

def load_data(filename):

    #loading data    
    Results = pd.read_csv(filename, skiprows = 10)
    
    #creating arrays for time, voltage and current
    time = Results["TIME"]
    voltage = Results["CH1"]
    current = Results["CH2"]
    
    return time, voltage, current 

def Trapeze_Integration(ydata,xdata,dx):
    Integrate_Trap = np.trapz(ydata,xdata,dx)
    
    return Integrate_Trap

def Simpson_Integration(ydata,xdata,dx):
    Integrate_Simp = sc.simps(ydata,xdata,dx)
    
    return Integrate_Simp

def Rectangle_Integration(ydata,xdata):
    dx, dy = [], []
    
    for i in range(len(ydata)-1):
        dy.append((ydata[i]+ydata[i+1])/2)
    
    for j in range(len(xdata)-1):
        dx.append(xdata[i+1]-xdata[i])
    
    dx=np.asarray(dx)
    dy=np.asarray(dy)
    
    Integral_Rect = np.dot(dx,dy)
    
    return Integral_Rect
    
def Integration(path,dv,dk):
    
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    CURR_TO_INT, TIME_TO_INT = [], []
    
    TRAP, SIMP, RECT = [], [], []
    
    progress = 0

    for i,f in enumerate(files) :
        
        time, voltage, current = load_data(os.path.join(path,f))
        
        for k in range(dk, len(time)) :
            if (voltage[k-dk] - voltage[k]) > dv:
                index = k
        
        for j in range(index, len(time)) :
            TIME_TO_INT.append(time[j])
            CURR_TO_INT.append(np.abs(current[j]))
        
        #pdb.set_trace()

        TRAP.append([f,Trapeze_Integration(CURR_TO_INT,TIME_TO_INT,1)])
        SIMP.append([f,Simpson_Integration(CURR_TO_INT,TIME_TO_INT,1)])
        RECT.append([f,Rectangle_Integration(CURR_TO_INT,TIME_TO_INT)])
        
        progress += 1
        if progress%50 == 0:
            print(progress)

    print(f)

    return np.asarray(TRAP),np.asarray(SIMP),np.asarray(RECT)

def main():
    
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFOLDER', help = 'file folder corresponding to experimental set with discharge infos')
    parser.add_argument('-dv',type = int,  dest = 'VOLTAGE_THRESHOLD', help = 'pick a value for voltage threshold')
    parser.add_argument('-dk',type = int,  dest = 'INDEX_THRESHOLD', help = 'pick a value for time threshold')
    args = parser.parse_args()
    outfile = args.INFOLDER.split('/')[-1] 
    
    dk = args.INDEX_THRESHOLD
    dv = args.VOLTAGE_THRESHOLD
    
    TRAP_TAB, SIMP_TAB, RECT_TAB = Integration(args.INFOLDER,dv,dk)
    
    print("Finished appending, saving tables...")
    
    pd.DataFrame(TRAP_TAB, columns = ['Filename', 'Integration']).to_csv(os.path.join('Injected_Charges/Trapeze',"{}.csv".format(outfile)))
    pd.DataFrame(SIMP_TAB, columns = ['Filename', 'Integration']).to_csv(os.path.join('Injected_Charges/Simpson',"{}.csv".format(outfile)))
    pd.DataFrame(RECT_TAB, columns = ['Filename', 'Integration']).to_csv(os.path_join('Injected_Charges/Rectangle',"{}.csv".format(outfile)))
    
main()