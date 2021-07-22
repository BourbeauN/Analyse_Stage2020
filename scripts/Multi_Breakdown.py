import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal
from scipy.signal import find_peaks
import pdb

Data = pd.read_csv("30/ (2).csv",skiprows=11,dtype=float)

time_t = Data['TIME'].ravel()
current_t = Data["CH1"].ravel()
voltage_t = Data["CH2"].ravel()

time = time_t[(np.abs(time_t)<1e-5)&(np.abs(voltage_t)<1e5)&(np.abs(current_t)<1e4)]
voltage = voltage_t[(np.abs(time_t)<1e-5)&(np.abs(voltage_t)<1e5)&(np.abs(current_t)<1e4)]*1000
current = current_t[(np.abs(time_t)<1e-5)&(np.abs(voltage_t)<1e5)&(np.abs(current_t)<1e4)]

peaks1, _ = find_peaks(voltage, distance=300,height=10000,prominence=1000)
peaks2, _ = find_peaks(voltage, distance=300,height=10000,prominence=3000)

plt.figure(1)
plt.plot(time,voltage,linewidth=0,marker='.',markersize=5,color='gray')
#plt.plot(time[peaks1],voltage[peaks1],linewidth=0,marker='x',markersize=10,color='red')
plt.plot(time[peaks2],voltage[peaks2],linewidth=0,marker='*',markersize=15,color='crimson')
#plt.figure(2)
#plt.plot(time,current,linewidth=0,marker='.',markersize=2)

plt.show()