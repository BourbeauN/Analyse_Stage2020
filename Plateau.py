import pdb
import numpy as np
import matplotlib.pyplot as plt
import os

def find_plateau(voltage, time,thresh):
        ## Beginning of plateau phase ##
        
        begin = np.where(voltage == np.ndarray.max(voltage))[0][0] ### to be validated ( tested on 10 )

        ## End of plateau phase ##
        for i in range(begin, len(voltage)):
            dist = 5
            if np.abs(voltage[i] - voltage[i-dist]) > thresh:
                if (i + begin )  < len(voltage):
                    return time[begin], time[i + begin]
        

def load_data(thresh):
    leo_path = '5kv_100nspicpic'
    # nao_path = "/Users/Naomi/Documents/GitHub/Analyse_Stage2020/Git_5kv_100nspicpic"
    path = leo_path
    #pdb.set_trace()
    List_Plateau = []
    No_Plateau = 0 
    
    for j in sorted(os.listdir(path)):
        time,voltage,current = np.array(np.loadtxt(os.path.join(path, j), dtype = float, delimiter = ',', skiprows = 12, unpack = True))
        
        print(j) 
        try :  
            begin, end = find_plateau(voltage, time, thresh)    
        except TypeError: 
            print ('unable to find plateau')
            No_Plateau += 1
            begin, end  = float('nan'), float('nan')

        plateau = end - begin
        
        List_Plateau.append(plateau)
     
    print(No_Plateau)
    Final_Plateau = np.asarray(List_Plateau)
    Num_Discharges = np.linspace(0,len(Final_Plateau), len(Final_Plateau))    
   
    return Num_Discharges , Final_Plateau
def plot_data(Num_Discharges, List_Plateau, thresh):
    plt.figure(1)
    plt.plot(Num_Discharges, np.log(List_Plateau),'ko', markersize = 2)
    plt.ylabel('Plateau duration (s)')
    plt.xlabel('Discharge ID')
    plt.title('Plateau length with a threshold of {}.'.format(thresh))

    #plt.savefig('FIGURES/plateau_size_discharge_id_scatter_plot_t={}_log.pdf'.format(thresh))
    #plt.savefig('FIGURES/plateau_size_discharge_id_scatter_plot_t={}_log.png'.format(thresh))


thresh = [100]
for t in thresh: 
    Num_Discharges, List_Plateau = load_data(t)
    ## PLOTS ##

    plot_data(Num_Discharges, List_Plateau, t)


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
