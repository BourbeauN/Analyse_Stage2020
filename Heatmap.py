import numpy as np
import argparse
import pandas as pd
import pdb

####PARSER####

parser = argparse.ArgumentParser()
parser.add_argument('-f', dest = 'INFILE', help = 'Results file from Plateau.py')
args = parser.parse_args()
#ID, fname, t_thresh, v_thresh, Plateau, Success = np.genfromtxt(args.INFILE, dtype = float, skip_header = 1, delimiter = ',', unpack = True)
Results = pd.read_csv(args.INFILE)
outfile = args.INFILE.split('/')[-1].replace('.csv','.pdf')
pdb.set_trace()



# ##Matrix to hold values##
# dv = np.unique(v_thresh)
# dt = np.unique(t_thresh)

# matrix = np.zeros((len(dv),len(dt)))

# for t in t_thresh :
#     for v in v_thresh :
#         matrix[v,t] += Success()

# for i in range(len(Success)):
    
#     if Success[i] == 1 :
#         a = (v_thresh[i])/5
#         b = np.int(a-1)
#         c = np.int(t_thresh[i]-1)
        
#         matrix[b,c] += 1

plt.figure(1)

plt.imshow(matrix, cmap = 'Blues', vmin = 500, vmax = 1000)
plt.colorbar()
plt.xlabel('Voltage threshold')
plt.ylabel('Time threshold')
plt.title('Influence of voltage and time threshold on \n plateau length determination')

plt.show()
