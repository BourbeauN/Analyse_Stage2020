import pdb
import numpy as np
import matplotlib.pyplot as plt
import os

def load_data():
    path = "/Users/Naomi/Documents/GitHub/Analyse_Stage2020/Git_5kv_100nspicpic"
    #pdb.set_trace()
    List_Plateau = []
    
    for j in os.listdir(path):
        
        time,voltage,current = np.array(np.loadtxt(j, dtype = float, delimiter = ',', skiprows = 12, unpack = True))
        
        ## Beginning of plateau phase ##
        begin = np.where(voltage == np.ndarray.max(voltage))[0][0]
        
        ## End of plateau phase ##
        
        end = []
        for i in range(begin,len(voltage)):
            if np.abs(voltage[i] - voltage[i-1]) > 100 :
               end = time[i-1]
               break
            
    
        
        plateau = end - begin
        
        List_Plateau.append(plateau)
    
    Num_Discharges = np.linspace(0,len(List_Plateau), len(List_Plateau))    
    plt.figure(1)
    plt.plot(Num_Discharges, List_Plateau,'ko', markersize = 2)
    plt.show()


load_data()
  
## PLOTS ##

# b = np.linspace(0, len(time), len(time))
# plt.plot(b, voltage)
# plt.grid()


# plt.figure(1)
# plt.plot(time*1e7, voltage)
# plt.xlabel(r'Time ($10^{-7 }$ s.')
# plt.ylabel('Voltage')
# plt.grid(which = 'both', axis = 'both')
# plt.title('Evolution of voltage after applying a potential difference to copper electrodes')

# plt.figure(2)
# plt.plot(time*1e-5, current)
# plt.xlabel('Time (s.)')
# plt.ylabel('Current(A.')
# plt.title('Evolution of current after applying a potential difference to copper electrodes')

# plt.show