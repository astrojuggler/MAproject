# This is the script for generating Channel Maps, Moment Maps and Position-Velocity (P-V) Diagrams out of an ALMA datacube, using the CASA software.
# Please read carefully the comments in the script to understand what the commands do.

# For any problems, you can look at the User Reference & Cookbook 4.7.2 (https://casa.nrao.edu/docs/cookbook/index.html)
# or at the Task Reference Manual -Oct 2016- (https://casa.nrao.edu/docs/TaskRef/TaskRef.html)

# --------------------------------------------------------------------------
# HOW TO CREATE MARVELLOUS MAPS
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

# 1. CHANNEL MAPS

# Channel Maps are basically datacubes with fewer images, few enough that can be displayed all together on a single screen.
# Each image is obtained integrating the images of an equal number of native channels.
# Beofre creating the Channel Maps, you need to decide the frequency range and how many maps you want in there.
# Once you've made your mind on the Channel Maps design, you have to split the continuum-subtracted visibilities accordingly, using the following task:

inputvis = 'calibrated.ms.contsub'
outfile = 'co10_50kms.ms'
mstransform(vis=inputvis,
            outputvis=outfile,
	        field = '4',
            spw = '2',
            datacolumn = 'data',
            regridms = True,
            mode = 'velocity',
            start = '-200km/s',		# the beginning of the frequency (velocity) range
            width = '50km/s',	# the spectral size of each map
	        nchan = 10,		# number of maps
            restfreq = '111.67526GHz',  # sky (obs) freq of CO(1-0) at z = 0.0322
            outframe = 'BARY')

# Don't be afraid of experimenting a different 'mode' (channel or frequency for instance)

# You can view the Channel Maps with the Viewer, adjusting the Number of Panels in the Panel Display Option

# 2. MOMENT MAPS

# Moment Maps are single images obtained integrating the intensity of each pixel over the spectral axis, weighted with some power of the spectral coordinate:
# Integral[I(v) v^m dv] where m=0,1,2,3,4,5... is called the moment order

# Alternatively the Moment Maps can be seen as the integrals of the spectral coordinate (elevated to some power), weighted with the intensity.
# This justifies the following nomenclature:

# m=0 integrated spectrum -> Intensity Map
# m=1 intensity weighted coordinate -> Velocity Map
# m=2 intensity weighted dispersion of coordinate -> Dispersion Velocity Map


inputcube = 'co10_cube_contsub.image.pbcor'
outfile = 'co10_moments'
immoments(axis = 'spectral',
          imagename = inputcube,
          moments = [0,1,2],	# orders of the Moment Maps you want to create
          includepix = [0.003,1.0],  # range of intensities in Jy, pixels out of this range will be discarded
          region = 'box[[342.41214120deg, -19.28082935deg], [342.39743688deg, -19.26694048deg]]',	# square, specified with sky coordinates, to crop the cube (*)
          chans = '420~516', # frequency range over which you want to integrate
          outfile = outfile)

# (*) You can select such a region with the Viewer, when studying the datacube, drawing a rectangle and saving it as a CASA Region File.
#     When you open that file, you can just copy the sky coordinates written in there.

# You can view the Moment Maps with the Viewer, altogethere or one at a time.

# 3. P-V Diagrams

# The physical meaning of P-V Diagrams can be somewhat more tricky to understand. However, if you know how to create one, their definition should become clear.
# First thing you need for creating a P-V diagram is a slit, for which you decide the length, orientation and width on the sky.
# The 'Position', the x-axis of the Diagram, is the offset from the centre of the slit.
# The 'Velocity', the y-axis of the Diagram, indicates for each value of P what is the velocity (frequency) of the emission most dected in that point of the sky.

# You can create a P-V Diagram using the following task:

impv(imagename = 'co10_cube.contsub.sym.cut.automask.pbcor.subimage',
     outfile = 'co10_automask.PV.PA180.image',
     mode = 'length',
     center = [75,73],		# check on the Viewer the pixel coordinates for the centre of the slit you want
     pa = '180deg',		# pa is the position angle (PA), namely the inclination of the slit
     length = '28arcsec', 	# length of the slit
     width = 1)		# size of the slit in units of pixels

# You can view the P-V Diagram with the Viewer
