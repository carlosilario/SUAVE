# fuselage_parasite_drag.py
#
# Created:  Tim MacDonald, Sep 2014
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

def fuselage_parasite_drag(vehicle,conditions):
    
    # ----- Values are unpacked as needed for calculations
    
    l = vehicle.fuselages.Fuselage.lengths.total
    U = conditions.freestream.velocity
    mew = conditions.freestream.viscosity
    rho = conditions.freestream.density
    
    Re = l*rho*U/mew
    
    T  = conditions.freestream.temperature
    Ma = conditions.freestream.mach_number
    reference_area = vehicle.reference_area
    
    # Determine skin friction coefficient
    # Note that this formula does not include roughness - it is assumed to be accounted for in misc drag
    cd_skin_friction = skin_friction_drag_cofficient(Re,Ma,T,vehicle)
    
    # Determine the drag coefficient due to upsweep
    cd_upsweep = upsweep_drag_coefficient(vehicle)
    
    # Add values to determine total drag coefficient for the fuselage
    total_cd = cd_skin_friction + cd_upsweep
    
    return total_cd
    
def skin_friction_drag_cofficient(Re,Ma,T,vehicle):
    
    # Calculate Reynolds number correction for cf
    
    Tinf = T
    cf_inc = skin_friction_cofficient(Re) # get baseline cf
    TwTinf = 1 + 0.178*Ma**2
    TpTinf = 1 + 0.035*Ma**2 + 0.45*(TwTinf-1)
    Tp = Tinf*TpTinf
    mewpmewinf = (TpTinf)**1.5 * (T+216)/(T+216)
    RpRinf = (1/mewpmewinf) * (1/TpTinf)
    cf = cf_inc*(1/TpTinf)*(1/RpRinf)**0.2
    
    # Calculate form factor k
    C = 2.3 # standard value
    H = vehicle.fuselages.Fuselage.heights.maximum
    W = vehicle.fuselages.Fuselage.width
    L = vehicle.fuselages.Fuselage.lengths.cabin
    R = (H-W)/(H+W)
    Deff = (W/2+H/2)*(64-3*R**4)/(64-16*R**2)
    d = Deff/L
    D = np.sqrt((1-(1-Ma**2)*d**2))
    a = 2*(1-Ma**2)*d**2/(D**3)*(np.arctanh(D)-D)
    dumaxu0 = a/((2-a)*np.sqrt(1-Ma**2))
    kf = (1 + C*dumaxu0)**2
    
    cab_l = vehicle.fuselages.Fuselage.lengths.cabin
    nose_l = vehicle.fuselages.Fuselage.lengths.nose
    tail_l = vehicle.fuselages.Fuselage.lengths.tail
    Swet = Deff*cab_l*np.pi + 0.75*np.pi*Deff*nose_l + 0.72*np.pi*Deff*tail_l
    Sref = vehicle.reference_area
    
    # Roughness Calculation
    cf = cf * 1.08
    
    cd_skin_friction = kf*cf*Swet/Sref
    
    return cd_skin_friction
    
def skin_friction_cofficient(Re):
    
    # For a fully turbulent flat plate
    cf = 0.455 / (np.log10(Re)**2.58)
    
    return cf

def upsweep_drag_coefficient(vehicle):
    
    # Take a standard value
    cd_base = 0.006
    fuse_ref = vehicle.fuselages.Fuselage.areas.front_projected
    sref = vehicle.reference_area
    
    # Correct for vehicle reference area
    cd_upsweep = cd_base*fuse_ref/sref
    
    return cd_upsweep