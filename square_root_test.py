import numpy as np 
import math

x = np.arange(0,1000,1)

def f1(data):
    return np.sqrt(data)

# def f2(data):
#     return math.sqrt(data)

y_nump = f1(x)
#y_mat = f2(x)

print(y_nump)