# initial_cruise_lift.py
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

def initial_cruise_lift(vehicle,conditions):
    
    mtow = vehicle.mass_properties.max_takeoff
    
    cruise_mass = 0.97*mtow    
    L = cruise_mass*conditions.gravity
    
    
    rho = conditions.freestream.density
    U = conditions.freestream.velocity
    S = vehicle.reference_area
    
    CL = L / (0.5*rho*U**2*S)
    
    return CL