# This is the script for subtracting the continuum emission from the target line emission, using the CASA software.
# Please read carefully the comments in the script to understand what the commands do.

# For any problems, you can look at the User Reference & Cookbook 4.7.2 (https://casa.nrao.edu/docs/cookbook/index.html)
# or at the Task Reference Manual -Oct 2016- (https://casa.nrao.edu/docs/TaskRef/TaskRef.html)

# --------------------------------------------------------------------------
# HOW TO SUBTRACT THE CONTINUUM FROM THE LINE EMISSION
# --------------------------------------------------------------------------

# Open the terminal and launch casa just by typing 'casa':

casa
# casa offers an interactive Python-based interface
# the functions of casa are called 'tasks' and can be executed in the terminal specifying properly the parameters
# a log-messages window will appear, don't close it as it'll be useful later on

# First go to the directory that contains the visibility files:

cd ../calibrated/

# Import the following libraries:

import re
import os

# In order to measure the continuum emission in the spectral window of the target line,
# you need to create a collapsed map selecting only the channels that are not contaminated by the line emission

# Use the Spectral Profile Tool of the Viewer to extract a spectrum from the datacube, using a circular aperture centred at the target source.
# Usually the spectra are plotted using 'Optical velocity (km/s)' for the spectral axis, and 'Flux density (Jy)' for the vertical axis, but you can change that as you like.

# Use the tclean task with the 'mfs' mode specifying the proper channels in the 'spw' parameter (see 'CLEANING OF COLLAPSED MAPS' in imaging.py)

# Different notations are available for specifying the frequency range you want to image,
# Find out more at https://casaguides.nrao.edu/index.php/Selecting_Spectral_Windows_and_Channels

# Open the collapsed map with the Viewer and measure the significance of the continuum emission, following the instructions below:

# 1. Draw an ellipse of the same size of the beam and place it on the maximum of the continuum emission
# 2. In the Regions panel go to Fit, click on 'gaussfit' and write down the Integrflux value in Jy
# 3. Now move the ellipse in a region not contaminated by the continuum emission, where you expect noise only
# 4. In the Regions panel go to Statistics and write down the Rms value
# 5. Repeat steps 3. and 4. for different positions of the ellipse at least 5-6 times and compute the average Rms
# 6. The signal-to-noise ratio of the continuum emission is S/N = IntegrFlux / AverageRms

# The S/N is often expressed in units of sigma, where sigma is indeed the Rms

# It is time to go ahead with the continuum subtraction, which starts from the original visibilities:

visfile='calibrated.ms'

# The following task subtracts the continuum in the visibility plane and create the continuum-subtracted visibility file, named: visfile + '.contsub'

uvcontsub(vis = visfile,
	  field = '4',
	  spw = '2',
	  fitspw = '2:4~7;50~59', # frequency range you want to fit the continuum over
	  solint='int',        # leave it at the default
	  fitorder=0)          # mean only

# Now you just have to repeat the cleaning of the datacube (tclean task) using, as input, the continuum-subtracted visibilites
