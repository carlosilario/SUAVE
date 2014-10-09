# fuselage_parasite_drag.py
#
# Created:  Tim MacDonald, Sep 2014
# Modified: 

import SUAVE

# suave imports

# python imports
import os, sys, shutil
from copy import deepcopy
from warnings import warn

# package imports
import numpy as np
import scipy as sp

def fuselage_parasite_drag(vehicle,conditions):
    
    # ----- Add equation here ----------------------############

    # You will need a unpack values for this calculation,
    # use the syntax shown below
    
    Re = 0.
    
    # ----------------------------------------------############
    
    # Unpack values needed for computations
    T  = conditions.freestream.temperature
    Ma = conditions.freestream.mach_number
    reference_area = vehicle.reference_area
    
    cd_skin_friction = skin_friction_drag_cofficient(Re,Ma,T,vehicle)
    
    cd_upsweep = upsweep_drag_coefficient(vehicle)
    
    cd_misc = miscellaneous_drag(cd_skin_friction+cd_upsweep)
    
    # ----- Add equations here ---------------------############
    # determine total cd and flat plate area
    total_cd = 0.
    
    return total_cd
    
def skin_friction_drag_cofficient(Re,Ma,T,vehicle):
    
    # ----- Add equations here ---------------------############
    
    cd_skin_friction = 0.
    
    return cd_skin_friction
    
def skin_friction_cofficient(Re):
    
    # ----- Add equations here ---------------------############
    cf = 0.
    
    return cf

def upsweep_drag_coefficient(vehicle):
    
    # ----- Add equations here ---------------------############
    
    cd_upsweep = 0.
    
    return cd_upsweep

def miscellaneous_drag(cd):
    
    # ----- Add equations here ---------------------############
    cd_misc = 0.
    
    return cd_misc