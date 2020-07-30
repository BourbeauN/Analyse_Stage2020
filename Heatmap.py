import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable

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

fig = plt.figure()

ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

im1 = ax1.imshow(matrix_plateau,cmap='Blues',extent=[np.float(dv[0]),np.float(dv[-1]),np.float(dt[0]),np.float(dt[-1])])
im2 = ax2.imshow(matrix_success,cmap='Reds',extent=[np.float(dv[0]),np.float(dv[-1]),np.float(dt[0]),np.float(dt[-1])])

ax1.set_title("Influence of voltage and time\nthreshold on plateau length\nin seconds for\n{}".format(args.INFILE))
ax2.set_title("Plateau detection success\nrate for varying voltage\n and time thresholds for\n{}".format(args.INFILE))

ax1.invert_yaxis()
ax2.invert_yaxis()

divider1 = make_axes_locatable(ax1)
divider2 = make_axes_locatable(ax2)

cax1 = divider1.append_axes("right", size="20%", pad=0.05)
cax2 = divider2.append_axes("right", size="20%", pad=0.05)

cbar1 = plt.colorbar(im1, cax = cax1)
cbar2 = plt.colorbar(im2, cax = cax2)

plt.tight_layout()
plt.savefig(os.path.join('OUT',outfile))