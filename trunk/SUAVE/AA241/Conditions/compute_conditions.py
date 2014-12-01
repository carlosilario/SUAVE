# compute_conditions.py
#
# Created:  Tim MacDonald, Sep 2014
# Modified: Tim Macdonald, Oct 2014

import SUAVE

from SUAVE.Attributes.Results import Result

# python imports
import os, sys, shutil
from copy import deepcopy
from warnings import warn

# package imports
import numpy as np
import scipy as sp

from SUAVE.Structure import (
Data, Container, Data_Exception, Data_Warning,
)

def compute_conditions(altitude,mach):
    
    # ----- Standard Atmosphere Model --------------############
    
    if altitude < 11000:
        T = 15.04-0.00649*altitude
    else:
        T = -56.46
    
    if altitude < 11000:
        p = 101.29*((T+273.15)/288.08)**5.256
    else:
        p = 22.65*np.exp(1.73-0.000157*altitude)
    
    mew = (1.458*10**-6*np.sqrt(T+273.15)) / (1+110.4/(T+273.15))
    
    rho = p/(.287*(T+273.15))
    
    c = np.sqrt(287*1.4*(T+273.15))
    
    velocity = mach*c
    
    # ----------------------------------------------############
    
    conditions = Data()
    conditions.freestream = Data()
    conditions.freestream.temperature         = T
    conditions.freestream.pressure            = p
    conditions.freestream.viscosity           = mew # kinematic viscosity
    conditions.freestream.velocity            = velocity
    conditions.freestream.mach_number         = mach
    conditions.freestream.density             = rho
    conditions.freestream.altitude            = altitude
    conditions.freestream.speed_of_sound      = c
    conditions.gravity                        = 9.81 # m/s^2
    
    return conditions