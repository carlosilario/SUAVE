## @ingroup Methods-Missions-Segments-Climb
# Constant_Mach_Linear_Altitude.py 
# Created:  Jul 2014, SUAVE Team
# Modified: Jun 2017, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import SUAVE

# ----------------------------------------------------------------------
#  initialize conditions
# ----------------------------------------------------------------------

## @ingroup Methods-Missions-Segments-Climb
def initialize_conditions(segment,state):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    Constrant dynamic pressure and constant rate of climb

    Source:
    N/A

    Inputs:
    segment.mach                                [unitless]
    segment.dynamic_pressure                    [pascals]
    segment.altitude_start                      [meters]
    segment.altitude_end                        [meters]
    segment.distance                            [meters]

    Outputs:
    conditions.frames.inertial.velocity_vector  [meters/second]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]
    conditions.frames.inertial.time             [seconds]

    Properties Used:
    N/A
    """        
    
    # unpack
    alt0       = segment.altitude_start 
    altf       = segment.altitude_end
    xf         = segment.distance
    mach       = segment.mach
    conditions = state.conditions
    
    # Update freestream to get speed of sound
    SUAVE.Methods.Missions.Segments.Common.Aerodynamics.update_atmosphere(segment,state)
    a          = conditions.freestream.speed_of_sound
    
    # Update freestream to get speed of sound
    SUAVE.Methods.Missions.Segments.Common.Aerodynamics.update_atmosphere(segment,state)
    a          = conditions.freestream.speed_of_sound
    
    # check for initial altitude
    if alt0 is None:
        if not state.initials: raise AttributeError('altitude not set')
        alt0 = -1.0 * state.initials.conditions.frames.inertial.position_vector[-1,2]

    # compute speed, constant with constant altitude
    air_speed = mach * a
    
    # dimensionalize time
    t_initial = conditions.frames.inertial.time[0,0]
    t_final   = xf / air_speed + t_initial
    t_nondim  = state.numerics.dimensionless.control_points
    time      = t_nondim * (t_final-t_initial) + t_initial
    
    # discretize on altitude
    alt = t_nondim * (altf-alt0) + alt0    
    
    segment.altitude = 0.5*(alt0 + altf)
    
    # pack
    state.conditions.freestream.altitude[:,0]             = alt[:,0]
    state.conditions.frames.inertial.position_vector[:,2] = -alt[:,0] # z points down
    state.conditions.frames.inertial.velocity_vector[:,0] = air_speed[:,0]
    state.conditions.frames.inertial.time[:,0]            = time[:,0]