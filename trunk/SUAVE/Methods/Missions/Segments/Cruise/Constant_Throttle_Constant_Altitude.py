## @ingroup Methods-Missions-Segments-Cruise
# Constant_Throttle_Constant_Altitude.py
# 
# Created:  Jul 2014, SUAVE Team
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np
from SUAVE.Methods.Geometry.Three_Dimensional \
     import angles_to_dcms, orientation_product, orientation_transpose

# ----------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------

## @ingroup Methods-Missions-Segments-Cruise
def unpack_unknowns(segment,state):
    
    # unpack unknowns
    unknowns   = state.unknowns
    velocity_x = unknowns.velocity_x
    time       = unknowns.time
    theta      = unknowns.body_angle
    
    # unpack givens
    v0         = segment.air_speed_start  
    vf         = segment.air_speed_end  
    t_initial  = state.conditions.frames.inertial.time[0,0]
    t_nondim   = state.numerics.dimensionless.control_points
    
    # time
    t_final    = t_initial + time  
    time       = t_nondim * (t_final-t_initial) + t_initial     

    #apply unknowns
    conditions = state.conditions
    conditions.frames.inertial.velocity_vector[:,0] = velocity_x
    conditions.frames.inertial.velocity_vector[0,0] = v0
    conditions.frames.body.inertial_rotations[:,1]  = theta[:,0]  
    conditions.frames.inertial.time[:,0]            = time[:,0]
    
# ----------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------    

## @ingroup Methods-Missions-Segments-Cruise
def initialize_conditions(segment,state):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    Constant throttle and constant altitude, allows for acceleration

    Source:
    N/A

    Inputs:
    segment.altitude                             [meters]
    segment.air_speed_start                      [meters/second]
    segment.air_speed_end                        [meters/second]
    segment.throttle	                         [unitless]
    segment.state.numerics.number_control_points [int]

    Outputs:
    state.conditions.propulsion.throttle        [unitless]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]

    Properties Used:
    N/A
    """   

    conditions = state.conditions

    # unpack inputs
    alt      = segment.altitude
    v0       = segment.air_speed_start
    vf       = segment.air_speed_end
    throttle = segment.throttle	
    N        = segment.state.numerics.number_control_points   
    
    # check for initial altitude
    if alt is None:
        if not state.initials: raise AttributeError('altitude not set')
        alt = -1.0 * state.initials.conditions.frames.inertial.position_vector[-1,2]
        segment.altitude = alt    

    # avoid having zero velocity since aero and propulsion models need non-zero Reynolds number
    if v0 == 0.0: v0 = 0.01
    if vf == 0.0: vf = 0.01

    # repack
    segment.air_speed_start = v0
    segment.air_speed_end   = vf
    
    # Initialize the x velocity unknowns to speed convergence:
    state.unknowns.velocity_x = np.linspace(v0,vf,N)
    
    # pack conditions
    state.conditions.propulsion.throttle[:,0] = throttle  
    state.conditions.freestream.altitude[:,0] = alt
    state.conditions.frames.inertial.position_vector[:,2] = -alt # z points down    

# ----------------------------------------------------------------------
#  Solve Residuals
# ----------------------------------------------------------------------    

## @ingroup Methods-Missions-Segments-Cruise
def solve_residuals(segment,state):
    """ Calculates a residual based on forces
    
        Assumptions:
        The vehicle accelerates, residual on forces and to get it to the final speed
        
        Inputs:
        segment.air_speed_end                  [meters/second]
        state.conditions:
            frames.inertial.total_force_vector [Newtons]
            frames.inertial.velocity_vector    [meters/second]
            weights.total_mass                 [kg]
        state.numerics.time.differentiate
            
        Outputs:
        state.residuals:
            forces               [meters/second^2]
            final_velocity_error [meters/second]
        state.conditions:
            conditions.frames.inertial.acceleration_vector [meters/second^2]

        Properties Used:
        N/A
                                
    """    

    # unpack inputs
    conditions = state.conditions
    FT = conditions.frames.inertial.total_force_vector
    vf = segment.air_speed_end
    v  = conditions.frames.inertial.velocity_vector
    D  = state.numerics.time.differentiate
    m  = conditions.weights.total_mass

    # process and pack
    acceleration = np.dot(D , v)
    conditions.frames.inertial.acceleration_vector = acceleration
    
    a  = state.conditions.frames.inertial.acceleration_vector

    state.residuals.forces[:,0] = FT[:,0]/m[:,0] - a[:,0]
    state.residuals.forces[:,1] = FT[:,2]/m[:,0] #- a[:,2]   
    state.residuals.final_velocity_error = (v[-1,0] - vf)

    return