import pdb
import numpy as np
import matplotlib.pyplot as plt
import os

def find_plateau(voltage, time , volt_threshold, time_threshold):
        ## Beginning of plateau phase ##
        
        begin = np.where(voltage == np.ndarray.max(voltage))[0][0] ### to be validated ( tested on 10 )
        ## End of plateau phase ##
        for i in range(begin, len(voltage)):
            if np.abs(voltage[i] - voltage[i-time_threshold]) > volt_threshold:
                if (i + begin )  < len(voltage):
                    return time[begin], time[i + begin]
        return float("nan"), float("nan") 

def load_data(filename):    
    
    time, voltage, current = np.array(np.loadtxt(filename, dtype = float, delimiter = ',', skiprows = 12, unpack = True))

    return time, voltage, current 

def compute_plateaus_on_data(path):
    """
    FUN: takes in a path and returns a PLATEAU 
    ARGS: list of cool args and don't mess them up 
    !!!!!!!!!!!!!!!!!
    """
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    # list of voltage deltas  
    dv = np.arange(5, 150, 5)
    
    # time deltas  
    dt = np.arange(30) + 1 

    # RESULTS
    RESULTS_TABLE = []
    # cycle through all files 
    for i, f in enumerate(files) :
        time, voltage, current = load_data(os.path.join(path,f))
        # compute all results from all parameters
        for v_thresh in dv :
            for t_thresh in dt :
                start , end = find_plateau (voltage, time , v_thresh, t_thresh)
                if start==start and end==end : 
                    plateau = end - start
                    success = 1
                    # do smthing
                else : 
                    plateau = float("nan")
                    success = 0
                    #do nothing
                
                # store results
                print([i, f, t_thresh, v_thresh, plateau, success])
                RESULTS_TABLE.append([f, t_thresh, v_thresh, plateau, success])
    # return results
    return np.asarray(RESULTS_TABLE)

def main():
    

    thresh = np.concatenate((np.arange(5, 100, 5), [100,200,300])) 
    # thresh = np.asarray([1,5,10,20,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,200,300,400,500,600,700,800,900,1000])
    success_rate_list = []
    
    nao_path = "/Users/Naomi/Documents/GitHub/Analyse_Stage2020/Git_5kv_100nspicpic"
    leo_path = "5kv_100nspicpic" 
    RESULTS_TABLE = compute_plateaus_on_data(leo_path)
    pd.DataFrame(RESULTS_TABLE, columns = ["fname", "time_delta", "voltage_delta", "plateau_length", "success"]).to_csv("out_test_1.csv") 

main()

""" 
    plt.plot(thresh, succes_rate_list)
    plt.title ("Influence of threshold value on the efficiency of the plateau finding algorithm")
    plt.xlabel("Thresh value")
    plt.ylabel("Unsuccessful runs")
    plt.savefig("FIGURES/success_vs_t.pdf")
"""

"""
def load_data(thresh):
    leo_path = '5kv_100nspicpic'
    #
    path = leo_path
    #pdb.set_trace()
    List_Plateau = []
    # Succ, Failed = 0,0 
    success = 0
    # files = sorted(os.listdir(path))
    for j in files:
        time, voltage, current = np.array(np.loadtxt(os.path.join(path, j), dtype = float, delimiter = ',', skiprows = 12, unpack = True))
        
        #print(j) 
        try :  
            begin, end = find_plateau(voltage, time, thresh) 
            success += 1
            
        except TypeError: 
            # print ('unable to find plateau')
            # No_Plateau += 1
            begin, end  = float('nan'), float('nan')
    
        plateau = end - begin
        
        List_Plateau.append(plateau)
 
    Final_Plateau = np.asarray(List_Plateau)
    Num_Discharges = np.linspace(0,len(Final_Plateau), len(Final_Plateau))    
    success_rate = float(success) / len(files)
    return Num_Discharges , Final_Plateau, success_rate 
"""
def plot_data(Num_Discharges, List_Plateau, thresh):
    plt.figure(1)
    plt.plot(Num_Discharges, np.log(List_Plateau),'ko', markersize = 2)
    plt.ylabel('Plateau duration (s)')
    plt.xlabel('Discharge ID')
    plt.title('Plateau length with a threshold of {}.'.format(thresh))

    #plt.savefig('FIGURES/plateau_size_discharge_id_scatter_plot_t={}_log.pdf'.format(thresh))
    #plt.savefig('FIGURES/plateau_size_discharge_id_scatter_plot_t={}_log.png'.format(thresh))

##### DEBUG TO FIND THE RATIO OF EFFICIENCY OF THE ALGORITHM TO FIND THE PLATEAU LENGTH ######

for t in thresh : 
    #total,Success = 0,0
    
    Num_Discharges, List_Plateau, success_rate = load_data(t)
    
    success_rate_list.append(success_rate)
    
    print(t, success_rate)

    # Plateau determination success rate
    # Success = np.float(Succ_data)
    # Success_Rate[t] += Success
    
    # Plateau determination failure rate
    # Failure = np.float(Failed_data)
    # Failure_Rate[t] += Failure
    
    
    #print(thresh[t],Success_Rate[t],Failure_Rate[t])

## PLOTS ##
    #plot_data(Num_Discharges, List_Plateau, t)


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
