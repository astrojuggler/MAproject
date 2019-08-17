# This is the script for for adjusting the ALMA datacube and for making it ready to use as input when running 3D-Barolo.
# All the changes of the datacube are made using the CASA software.
# Please read carefully the comments in the script to understand what the commands do.

# For any problems, you can look at the User Reference & Cookbook 4.7.2 (https://casa.nrao.edu/docs/cookbook/index.html)
# or at the Task Reference Manual -Oct 2016- (https://casa.nrao.edu/docs/TaskRef/TaskRef.html)

# --------------------------------------------------------------------------
# HOW TO PREPARE THE INPUT ALMA DATACUBE
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

# All we have to do consists in three steps:

# 1. crop the datacube with a squared region of the sky slightly larger than the galaxy disk
# 2. cut the datacube selecting only the spectral range of interest in the rotation pattern
# 3. convert the CASA-datacube in the format .fits

# The first two steps can be accomplished with the following task:

inputfile = 'co10_cube_zcorr.image.pbcor'
outputfile = 'co10_cube_zcorr.image.pbcor.box35.+-250kms'
imsubimage(imagename = inputfile,
	   outfile = outputfile,
       chans = '141~240',   # selected spectral range
	   region = 'box [[342.40996795deg, -19.27880609deg], [342.39966815deg, -19.26908388deg]]',    #selected cropped region of the sky (*)
	   overwrite = True)

# (*) Read on how to specify a region in the file maps.py (in the comment of the task 'immoments')

# You can view the new datacube with the Viewer

# The third step is:

exportfits(imagename = 'co10_cube_zcorr.image.pbcor.box35.+-250kms',
	   fitsimage = 'co10_cube_zcorr.image.pbcor.box35.+-250kms.fits',
	   velocity = True,    # IMPORTANT: velocity units for the spectral axis
	   optical = True,
	   overwrite = True)

# WARNING Spectral axis is non-linear in the requested output quantity,
#        but CASA can presently only write linear axes to FITS.
#        In this image, the maximum deviation from linearity is 5204.02 m/s
# Not a big deal: it's one native channel

# The file you have just generated is the input file of Barolo

# One last thing to do is to get some info about the datacube parameters (especially the beam size):

imhead(imagename = 'co10_cube_zcorr.image.pbcor.box35.+-250kms',
       mode = 'list')
