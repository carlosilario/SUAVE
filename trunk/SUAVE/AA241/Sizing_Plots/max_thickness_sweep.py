# max_thickness_sweep.py
#
# Created:  Tim MacDonald, Nov 2014
# Modified: Tim MacDonald, Nov 2014

import SUAVE

# suave imports

# python imports
import os, sys, shutil
from copy import deepcopy
from warnings import warn

# package imports
import numpy as np
import scipy as sp
import pylab as plt

def max_thickness_sweep(vehicle,conditions):
    
    sweep = np.linspace(0,35,30)*np.pi/180.
    cl_norm = conditions.cl_initial / np.cos(sweep)**2
    
    MDiv = conditions.freestream.mach_number
    
    Mcc_peaky  = MDiv/(1.02+0.08*(1-np.cos(sweep))) - 0.04
    
    Minf_perp = Mcc_peaky*np.cos(sweep)
    
    a = (2.969-2.738*cl_norm+1.469*cl_norm**2)
    b = -(1.963-1.078*cl_norm+0.350*cl_norm**2)
    c = 0.954-.235*cl_norm+0.0259*cl_norm**2 - Minf_perp
    
    tc_perp = np.zeros(np.size(sweep))
    tc      = np.zeros(np.size(sweep))
    for ii in range(len(a)):
        pol = np.poly1d([a[ii], b[ii], c[ii]])
        tc_perp[ii] = pol.r[1]
        tc[ii] = tc_perp[ii]*np.cos(sweep[ii]) 
        
    fig = plt.figure('Maximum t/c by Sweep')
    axes = plt.gca()
    axes.plot(sweep*180./np.pi,tc)  
    axes.grid(True)
    axes.set_xlabel('Sweep (Degrees)')
    axes.set_ylabel('t/c')
    axes.set_title('Maximum t/c by Sweep')
    plt.show()
    
    
    return