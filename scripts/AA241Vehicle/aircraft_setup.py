# aircraft_setup.py
# 
# Created:  SUave Team    , Aug 2014
# Modified: Tim MacDonald , Oct 2014

""" setup file for a mission with an aircraft of your choice
"""


# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import SUAVE
from SUAVE.Attributes import Units

import numpy as np
import pylab as plt

import copy, time
from SUAVE.AA241.Conditions.compute_conditions import compute_conditions
from SUAVE.AA241.Drag.fuselage_parasite_drag   import fuselage_parasite_drag

from SUAVE.Structure import (
Data, Container, Data_Exception, Data_Warning,
)

def full_setup():

    vehicle = vehicle_setup()
    
    # ------- Set sizing case here ------------------------############
    
    altitude = 35000 * Units.ft      # default is meters
    mach = 0.8    
    
    # -----------------------------------------------------############
    
    conditions = compute_conditions(altitude,mach)   
    
    cd_fuselage = fuselage_parasite_drag(vehicle,conditions)
    
    print cd_fuselage
    
    # ------- Calculate flat plate area -------------------############
    
    flat_plate_area = 0

    # -----------------------------------------------------############
    
    print flat_plate_area
    
    return vehicle

def vehicle_setup():
    
    # ------------------------------------------------------------------
    #   Initialize the Vehicle
    # ------------------------------------------------------------------    
    
    vehicle = SUAVE.Vehicle()
    vehicle.tag = 'AA241 Vehicle'    
    
    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------    

    # mass properties
    vehicle.mass_properties.max_takeoff               = 0.   # kg
    vehicle.mass_properties.operating_empty           = 0.   # kg
    vehicle.mass_properties.takeoff                   = 0.   # kg
    vehicle.mass_properties.max_zero_fuel             = 0.   # kg
    vehicle.mass_properties.cargo                     = 0.   # kg
    
    vehicle.mass_properties.center_of_gravity         = [0 , 0, 0]  # default is meters
    vehicle.mass_properties.moments_of_inertia.tensor = [[0, 0, 0],[0, 0, 0,],[0,0, 0]] # default in SI
    
    # envelope properties
    vehicle.envelope.ultimate_load = 0.
    vehicle.envelope.limit_load    = 0.

    # basic parameters
    vehicle.reference_area        = 0.   # m^2    
    vehicle.passengers            = 0
    vehicle.systems.control       = "fully powered" # Choose type of control surface here
    vehicle.systems.accessories   = "medium range" # Choose type of mission here 
    
    # ------------------------------------------------------------------        
    #   Main Wing
    # ------------------------------------------------------------------        
    
    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'Main Wing'
    
    wing.areas.reference = 0.         # m^2
    wing.aspect_ratio    = 0.         # 
    wing.spans.projected = 0.         # m
    wing.sweep           = 0. * Units.deg
    wing.symmetric       = True
    wing.thickness_to_chord = 0.
    wing.taper           = 0.
    wing.chords.root     = 0.
    wing.chords.tip      = 0.
    wing.areas.wetted    = 0.
    
    wing.chords.mean_aerodynamic = 0.
    wing.areas.exposed           = 0.
    wing.areas.affected          = 0.
    wing.span_efficiency         = 0.
    wing.twists.root             = 0.
    wing.twists.tip              = 0.
    wing.origin                  = [0,0,0]
    wing.aerodynamic_center      = [0,0,0] 
    wing.vertical                = False
    wing.eta                     = 0.
    
    # add to vehicle
    vehicle.append_component(wing)

    # ------------------------------------------------------------------        
    #  Horizontal Stabilizer
    # ------------------------------------------------------------------        
    
    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'Horizontal Stabilizer'
    
    wing.areas.reference = 0.         # m^2
    wing.aspect_ratio    = 0.         # 
    wing.spans.projected = 0.         # m
    wing.sweep           = 0. * Units.deg
    wing.symmetric       = True
    wing.thickness_to_chord = 0.
    wing.taper           = 0.
    wing.chords.root     = 0.
    wing.chords.tip      = 0.
    wing.areas.wetted    = 0.
    
    wing.chords.mean_aerodynamic = 0.
    wing.areas.exposed           = 0.
    wing.areas.affected          = 0.
    wing.span_efficiency         = 0.
    wing.twists.root             = 0.
    wing.twists.tip              = 0.
    wing.origin                  = [0,0,0]
    wing.aerodynamic_center      = [0,0,0] 
    wing.vertical                = False
    wing.eta                     = 0.
    
    # add to vehicle
    vehicle.append_component(wing)
    
    # ------------------------------------------------------------------
    #   Vertical Stabilizer
    # ------------------------------------------------------------------
    
    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'Vertical Stabilizer'    
    
    wing.areas.reference = 0.         # m^2
    wing.aspect_ratio    = 0.         # 
    wing.spans.projected = 0.         # m
    wing.sweep           = 0. * Units.deg
    wing.symmetric       = True
    wing.thickness_to_chord = 0.
    wing.taper           = 0.
    wing.chords.root     = 0.
    wing.chords.tip      = 0.
    wing.areas.wetted    = 0.
    
    wing.chords.mean_aerodynamic = 0.
    wing.areas.exposed           = 0.
    wing.areas.affected          = 0.
    wing.span_efficiency         = 0.
    wing.twists.root             = 0.
    wing.twists.tip              = 0.
    wing.origin                  = [0,0,0]
    wing.aerodynamic_center      = [0,0,0] 
    wing.vertical                = False
    wing.eta                     = 0.
    wing.t_tail                  = False
        
    # add to vehicle
    vehicle.append_component(wing)

    # ------------------------------------------------------------------
    #  Fuselage
    # ------------------------------------------------------------------
    
    fuselage = SUAVE.Components.Fuselages.Fuselage()
    fuselage.tag = 'Fuselage'
    
    fuselage.number_coach_seats = 0
    fuselage.seats_abreast      = 0.
    fuselage.seat_pitch         = 0. 
    fuselage.fineness.nose      = 0.
    fuselage.fineness.tail      = 0.
    fuselage.lengths.fore_space = 0.
    fuselage.lengths.aft_space  = 0.
    fuselage.width                              = 0.
    fuselage.heights.maximum                    = 0. 
    fuselage.areas.side_projected               = 0. 
    fuselage.heights.at_quarter_length          = 0.
    fuselage.heights.at_three_quarters_length   = 0.
    fuselage.heights.at_wing_root_quarter_chord = 0.
    fuselage.differential_pressure              = 0. # Maximum differential pressure
    
    fuselage.lengths.nose  = 0.
    fuselage.lengths.tail  = 0.
    fuselage.lengths.cabin = 0.
    fuselage.lengths.total = 0.
    fuselage.areas.wetted  = 0.
    fuselage.effective_diameter        = 0.
    fuselage.areas.front_projected     = 0.
    
    # add to vehicle
    vehicle.append_component(fuselage)
    
    # ------------------------------------------------------------------
    #  Turbofan
    # ------------------------------------------------------------------    
    
    turbofan = SUAVE.Components.Propulsors.TurboFanPASS()
    turbofan.tag = 'Turbo Fan'
    
    turbofan.propellant = SUAVE.Attributes.Propellants.Jet_A()
    
    turbofan.diffuser_pressure_ratio       = 0.
    turbofan.fan_pressure_ratio            = 0. 
    turbofan.fan_nozzle_pressure_ratio     = 0. 
    turbofan.lpc_pressure_ratio            = 0. 
    turbofan.hpc_pressure_ratio            = 0. 
    turbofan.burner_pressure_ratio         = 0. 
    turbofan.turbine_nozzle_pressure_ratio = 0. 
    turbofan.Tt4                           = 0. 
    turbofan.bypass_ratio                  = 0. 
    turbofan.thrust.design                 = 0. 
    turbofan.number_of_engines             = 0. 
    
    turbofan.lengths = Data()
    turbofan.lengths.engine                = 0.
    
    # size the turbofan
    turbofan.A2          = 0.
    turbofan.df          = 0.
    turbofan.nacelle_dia = 0.
    turbofan.A2_5        = 0.
    turbofan.dhc         = 0.
    turbofan.A7          = 0.
    turbofan.A5          = 0.
    turbofan.Ao          = 0.
    turbofan.mdt         = 0.
    turbofan.mlt         = 0.
    turbofan.mdf         = 0.
    turbofan.mdlc        = 0.
    turbofan.D           = 0.
    turbofan.mdhc        = 0.
    
    # add to vehicle
    vehicle.append_component(turbofan)    

    # ------------------------------------------------------------------
    #   Define Configurations
    # ------------------------------------------------------------------

    # --- Takeoff Configuration ---
    config = vehicle.new_configuration("takeoff")
    # this configuration is derived from the baseline vehicle

    # --- Cruise Configuration ---
    config = vehicle.new_configuration("cruise")
    # this configuration is derived from vehicle.configs.takeoff

    # --- Takeoff Configuration ---
    takeoff_config = vehicle.configs.takeoff
    takeoff_config.wings['Main Wing'].flaps_angle  = 0. * Units.deg
    takeoff_config.wings['Main Wing'].slats_angle  = 0. * Units.deg
    takeoff_config.V2_VS_ratio                     = 0.
    takeoff_config.maximum_lift_coefficient        = 0.

    # --- Landing Configuration ---
    landing_config = vehicle.new_configuration("landing")
    landing_config.wings['Main Wing'].flaps_angle = 0. * Units.deg
    landing_config.wings['Main Wing'].slats_angle = 0. * Units.deg
    landing_config.Vref_VS_ratio                  = 0.
    landing_config.maximum_lift_coefficient       = 0.
    landing_config.mass_properties.landing        = 0.
    

    # ------------------------------------------------------------------
    #   Vehicle Definition Complete
    # ------------------------------------------------------------------
    
    return vehicle    

if __name__ == '__main__':
    full_setup()