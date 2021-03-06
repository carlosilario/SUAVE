## @ingroup Input_Output-SU2
# call_SU2_CFD.py
# 
# Created:  Oct 2016, T. MacDonald
# Modified: Jan 2017, T. MacDonald

import subprocess
from SUAVE.Core import Data
import sys, os

## @ingroup Input_Output-SU2
def call_SU2_CFD(tag,parallel=False,processors=1):
    """This calls SU2 to perform an analysis according to the related .cfg file.

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    tag                          <string>  This determines what .cfg is used and what the output file is called.
    parallel   (optional)        <boolean> This determines if SU2 will be run in parallel. This setting requires that SU2 has been built to allow this.
    processors (optional)        [-]       The number of processors used for a parallel computation.

    Outputs:
    <tag>._forces_breakdown.dat  This file has standard SU2 run information.
    CL                           [-]
    CD                           [-]

    Properties Used:
    N/A
    """       
    
    if parallel==True:
        sys.path.append(os.environ['SU2_HOME'])
        from parallel_computation import parallel_computation
        parallel_computation( tag+'.cfg', processors )
        pass
    else:
        subprocess.call(['SU2_CFD',tag+'.cfg'])
        
    f = open(tag + '_forces_breakdown.dat')
        
    SU2_results = Data()    
    
    # only the total forces have the ":"
    for line in f:
        if line.startswith('Total CL:'):
            print 'CL:',line.split()[2]
            SU2_results.coefficient_of_lift = float(line.split()[2])
        elif line.startswith('Total CD:'):
            print 'CD:',line.split()[2]
            SU2_results.coefficient_of_drag = float(line.split()[2])
        elif line.startswith('Total CMx:'):
            print 'CMx:',line.split()[2]
            SU2_results.moment_coefficient_x = float(line.split()[2])
        elif line.startswith('Total CMy:'):
            print 'CMy:',line.split()[2]
            SU2_results.moment_coefficient_y = float(line.split()[2])
        elif line.startswith('Total CMz:'):
            print 'CMz:',line.split()[2]
            SU2_results.moment_coefficient_z = float(line.split()[2])
           
    CL = SU2_results.coefficient_of_lift
    CD = SU2_results.coefficient_of_drag
            
    return CL,CD

if __name__ == '__main__':
    call_SU2_CFD('cruise',parallel=True)