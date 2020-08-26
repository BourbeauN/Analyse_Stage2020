import torch 
import pdb
import os
import numpy as np
from utility import *
#import matplotlib.pyplot as plt


## New functions
def detect_plateau(discharge):
    end = None # TO BE DETERMINED
    start = None # TO BE DET
    time_delta = end - start
    return time_delta
##

########This is a debugger
def main():
        data = load_data() # from utility 
        pdb.set_trace()
        detect_plateau(data[0][0])
main()
