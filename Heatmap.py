#### REMEMBER TO INDENT COMMANDS TO RUN ON IDE AND UNINDENT COMMANDS TO RUN ON SERVER BEFORE PUSHING CODE ####

import numpy as np

### This bloc of command is for running the code on the server (1/3) ###
import matplotlib
matplotlib.use('Agg')
import argparse

import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os

### This parser is to run the code on server. (2/3) ###
### PARSER ###
parser = argparse.ArgumentParser()
parser.add_argument('-f', dest = 'INFILE', help = 'Results file from Plateau.py')
args = parser.parse_args()
Results = pd.read_csv(args.INFILE)
outfile = args.INFILE.split('/')[-1].replace('.csv','.pdf')

# ### This command is for running the code outside of the server (1/2) ###
# Results = pd.read_csv("OUT_PLATEAUS_5kv_500ns_picpic.csv")

#Matrix to hold values
dv = np.unique(Results.voltage_delta)
dt = np.unique(Results.time_delta)

#Creating empty matrix(2) to store mean plateau length values and mean success rates
matrix_plateau, matrix_success = np.zeros((len(dv),len(dt))), np.zeros((len(dv), len(dt)))

#for loops(2) going through the initial data matrix to store plateau lengths and success rates
for t_index,t_val in enumerate(dt) :
    for v_index,v_val in enumerate(dv) :
        plateau_mean=Results[Results.voltage_delta == v_val][Results.time_delta == t_val].plateau_length.mean()
        success_rate=Results[Results.voltage_delta == v_val][Results.time_delta == t_val].success.mean()
    
        #Appending values to matrix(2) full of zeros
        matrix_plateau[v_index,t_index] += plateau_mean
        matrix_success[v_index,t_index] += success_rate
        print(v_index,t_index,plateau_mean, success_rate)

###PLOTS###

fig = plt.figure(figsize=(10,3))

ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

###The extent must be adapted to de the dt an dv aranges from Plateau.py###
###The extent= function seems to only accept number that are then converted to strings on the plot###
###The extent= function doesn't accept float, ints or strings as arguments###
im1 = ax1.imshow(matrix_plateau,cmap='Blues', extent=[200,5100,1,30], aspect='auto')
im2 = ax2.imshow(matrix_success,cmap='Reds', extent=[200,5100,1,30], aspect='auto')

#Axis labels
ax1.set_xlabel("Voltage threshold")
ax1.set_ylabel("Time threshold")
ax2.set_xlabel("Voltage threshold")
ax2.set_ylabel("Time threshold")

#Colorbar parameters
divider1 = make_axes_locatable(ax1)
divider2 = make_axes_locatable(ax2)
cax1 = divider1.append_axes("right", size="20%", pad=0.05)
cax2 = divider2.append_axes("right", size="20%", pad=0.05)
cbar1 = plt.colorbar(im1, cax = cax1)
cbar2 = plt.colorbar(im2, cax = cax2)

plt.tight_layout(pad=0.5, w_pad = 1)

#Title and save parameters depending on location of runing code

### This bloc of command is for running the code on server. (3/3) ###
### Update de dv,dt values of the arange ###
plt.savefig(os.path.join('OUT',outfile,"_dv_200_5100_dt_1_30"))
ax1.set_title("Plateau length for {}".format(args.INFILE))
ax2.set_title("Plateau detection success {}".format(args.INFILE))

# ### This bloc of command is for running the code outside of server (2/2) ###
# ax1.set_title("Plateau length")
# ax2.set_title("Success Rate")
#plt.savefig("caca.pdf")