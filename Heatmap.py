import matplotlib.pyplot as plt
import numpy as np
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
pdb.set_trace()

##Matrix to hold values##
dv = np.unique(Results.voltage_delta)
dt = np.unique(Results.time_delta)

matrix_plateau,matrix_success = np.zeros((len(dv),len(dt)))


for t_index,t_val in enumerate(dt) :
    for v_index,v_val in enumerate(dv) :
        plateau_mean=Results[Results.voltage_delta == v_val][Results.time_delta == t_val].plateau_length.mean()
        success_rate=Results[Results.voltage_delta == v_val][Results.time_delta == t_val].plateau_length.mean()
        
        matrix_plateau[t_index,v_index] += plateau_mean
        matrix_success[t_index,v_index] += success_rate

###PLOTS###

fig,ax = plt.subplots(ncols=2)

ax[0].imshow(matrix_plateau, cmap = 'Blues')
ax[0].colorbar()
ax[0].xlabel('Voltage threshold')
ax[0].ylabel('Time threshold')
ax[0].title('Influence of voltage and time threshold on plateau length in seconds for {}'.format(args.INFILE))

ax[1].imshow(matrix_success, cmap = 'Blues')
ax[1].colorbar()
ax[1].xlabel('Voltage threshold')
ax[1].ylabel('Time threshold')
ax[1].title('Plateau detection success rate for varying voltage and time thresholds for {}'.format(args.INFILE))

plt.savefig(os.path.join('OUT',outfile))