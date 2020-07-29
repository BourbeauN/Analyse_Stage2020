import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
import pandas as pd
import pdb
import os

####PARSER####

parser = argparse.ArgumentParser()
parser.add_argument('-f', dest = 'INFILE', help = 'Results file from Plateau.py')
args = parser.parse_args()
#ID, fname, t_thresh, v_thresh, Plateau, Success = np.genfromtxt(args.INFILE, dtype = float, skip_header = 1, delimiter = ',', unpack = True)
Results = pd.read_csv(args.INFILE)
outfile = args.INFILE.split('/')[-1].replace('.csv','.pdf')

##Matrix to hold values##
dv = np.unique(Results.voltage_delta)
dt = np.unique(Results.time_delta)

matrix_plateau, matrix_success = np.zeros((len(dv),len(dt))), np.zeros((len(dv), len(dt)))


for t_index,t_val in enumerate(dt) :
    for v_index,v_val in enumerate(dv) :
        plateau_mean=Results[Results.voltage_delta == v_val][Results.time_delta == t_val].plateau_length.mean()
        success_rate=Results[Results.voltage_delta == v_val][Results.time_delta == t_val].success.mean()
        
        matrix_plateau[v_index,t_index] += plateau_mean
        matrix_success[v_index,t_index] += success_rate
        print(v_index,t_index,plateau_mean, success_rate)


###PLOTS###

fig,ax = plt.subplots(ncols=2)

ax[0].imshow(matrix_plateau, cmap = 'Blues')
cbar0 = plt.colorbar(ax[0].imshow(matrix_plateau,cmap='Blues'))
ax[0].set_xlabel('Voltage threshold')
ax[0].set_xticks(dv)
ax[0].set_ylabel('Time threshold')
ax[0].set_yticks(dt)
ax[0].set_title('Influence of voltage and time\nthreshold on plateau length\nin seconds for\n{}'.format(args.INFILE))

ax[1].imshow(matrix_success, cmap = 'Blues')
cbar1 = plt.colorbar(ax[1].imshow(matrix_success,cmap='Blues'))
ax[1].set_xlabel('Voltage threshold')
ax[1].set_xticks(dv)
ax[1].set_ylabel('Time threshold')
ax[1].set_yticks(dt)
ax[1].set_title('Plateau detection success\nrate for varying voltage\n and time thresholds for\n{}'.format(args.INFILE))
#plt.tight_layout()
plt.savefig(os.path.join('OUT',outfile))
