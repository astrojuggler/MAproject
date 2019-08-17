# This is the script for imaging the interferometric data using the so-called cleaning algorithm of the CASA software.
# Please read carefully the comments in the script to understand what the commands do.

# For any problems, you can look at the User Reference & Cookbook 4.7.2 (https://casa.nrao.edu/docs/cookbook/index.html)
# or at the Task Reference Manual -Oct 2016- (https://casa.nrao.edu/docs/TaskRef/TaskRef.html) 

# --------------------------------------------------------------------------
# HOW TO TURN VISIBILITIES INTO IMAGES
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

# Before calling the cleaning task, it is always recommended to check the content of the visibily files, by typing:

visfile = 'calibrated.ms.contsub_CO'
# assign to a variable the string of the name of the folder containing the visibility files you want to work on

listobs(vis=visfile)
# this will display on the log window lots of information about the visiblity files and the observations carried on for obtaining them

#2019-03-18 08:32:40 INFO listobs	Computing scan and subscan properties...
#2019-03-18 08:32:40 INFO listobs	Data records: 55965       Total elapsed time = 394.656 seconds
#2019-03-18 08:32:40 INFO listobs	   Observed from   11-Mar-2017/16:31:29.4   to   11-Mar-2017/16:38:04.0 (UTC)
#2019-03-18 08:32:40 INFO listobs
#2019-03-18 08:32:40 INFO listobs	   ObservationID = 0         ArrayID = 0
#2019-03-18 08:32:40 INFO listobs	  Date        Timerange (UTC)          Scan  FldId FieldName             nRows     SpwIds   Average Interval(s)    ScanIntent
#2019-03-18 08:32:40 INFO listobs	  11-Mar-2017/16:31:29.4 - 16:38:04.0    11      0 MCG-03-58-007            55965  [0]  [6.05] [OBSERVE_TARGET#ON_SOURCE]
#2019-03-18 08:32:40 INFO listobs	           (nRows = Total number of rows per scan)
#2019-03-18 08:32:40 INFO listobs	Fields: 1
#2019-03-18 08:32:40 INFO listobs	  ID   Code Name                RA               Decl           Epoch   SrcId      nRows
#2019-03-18 08:32:40 INFO listobs	  0    none MCG-03-58-007       22:49:37.100000 -19.16.26.00000 ICRS    0          55965
#2019-03-18 08:32:40 INFO listobs	Spectral Windows:  (1 unique spectral windows and 1 unique polarization setups)
#2019-03-18 08:32:40 INFO listobs	  SpwID  Name                                      #Chans   Frame   Ch0(MHz)  ChanWid(kHz)  TotBW(kHz) CtrFreq(MHz) BBC Num  Corrs
#2019-03-18 08:32:40 INFO listobs	  0      X911794111#ALMA_RB_03#BB_1#SW-01#FULL_RES    960   TOPO  110745.373      1953.125   1875000.0 111681.8968        1  XX  YY
#2019-03-18 08:32:40 INFO listobs	Sources: 1
#2019-03-18 08:32:40 INFO listobs	  ID   Name                SpwId RestFreq(MHz)  SysVel(km/s)
#2019-03-18 08:32:40 INFO listobs	  0    MCG-03-58-007       0     115271.202     9653.3171476
#2019-03-18 08:32:40 INFO listobs	Antennas: 41:

# Your visibility files might include observations of more than one source* (Field) and for each source more than one frequency range (Spectral Window)
# It is important to read in the Log the FiledID and SpwID you are interested in
# You can also read the observed time and date, the properties of the spectral windows such as the frequency range and the frequency bins (called channels), the number of antennas...

# *i.e sources used for the calibration

# You can read about the purpose of a task and its with the command:
inp(listobs)

# The task that performs the cleaning is 'tclean'
# There are two main options for the imaging, which are specified with the 'specmode' parameter:
# 'cube' keeps the spectral information and its outcome is a datacube, namely a sequence of images of the source, one for each frequency bin of the spectral windows
# 'mfs' integrates the spectral information and its outcome is a single collapsed image of the sources

# 1. CLEANING OF DATACUBES

outfile = 'co10_cube_zcorr'
# assign a name to the outcome file of the tclean tasks

# I encourage you to read about the parameters of the
#optical velocity conversion f = f0 / (1-v/c)

tclean(vis = visfile,   #input visibilities
      imagename = outfile,
      field = '0',  # FieldID of your target source
      spw = '0',    # SpwID of your target spectral window
      specmode = 'cube',    # the outcome will be a datacube
      width = 1,    # width is the size of the frequency channels of the output datacube, given in units of native frequency channels
      restfreq = '111.65795GHz',    # observed frequency of the line you are imaging: you can compute it in the website https://www.cv.nrao.edu/php/splat/ (you need to know the redshift z)
      outframe = 'BARY',    # Barycentric is a commonly used frame that has virtually replaced the older Heliocentric standard (*)
      interpolation = 'linear',
      gridder = 'standard',
      niter = 10000,
      threshold = '2.5mJy',     # the thumbrule is to choose 2-3 times the sigma_rms (sensitivity of the data), which you can read in the README
      imsize = [512, 512],
      cell = '0.2arcsec',   # at least 1/5-1/6 of synthesised beam or smaller (related to the Sampling Theorem), read the beam size in the README
      weighting = 'briggs',
      robust = 0.0,
      phasecenter = 4,      # same as FieldID
      pbcor = True,     # an extra file will be created: the image corrected for the primary beam effect, which is the one you are supposed to use for your analysis
      interactive = False,    # regarding the mask, which assists the algorithm to find the sources in the sky
      usemask='auto-multithresh',   # automask is the best option, especially when emission location is a function of the frequency
      sidelobethreshold=2.0,
      noisethreshold=4.25,
      lownoisethreshold=1.5,
      minbeamfrac=0.3,
      growiterations=75,
      negativethreshold=15.0,
      verbose=True)

# (*) Given the small difference between the Barycentric and Heliocentric frames, they are frequently used interchangeably.

# The cleaning task launched with the 'cube' mode will take up to a few hours.
# You can follow the process in the Log window but after a couple of minutes you will be bored, so... yes you can go and grab a coffe!

# When the task is completed, it is time to view the cube! To do that, type:

viewer
# the Data Manager window of the viewer will open, select the image file, named outfile+'image.pbcor' and click 'raster image'

# Now you can just play around with the cube within the Viewer interface: use the slide, play movies, draw selections, zoom in, extract spectra and lots more...

# 2. CLEANING OF COLLAPSED MAPS

visfile = 'calibrated.ms.contsub_CO'
outfile = 'collapsedMap'
tclean(vis = visfile,
      imagename = outfile,
      field = '0',
      spw = '0',
      specmode = 'mfs',     # the outcome will be a collapes map
      restfreq = '0:4~7;50~59', # 0 is the SpwID, only channels from 4 to 7 and from 50 to 59 will be imaged
      outframe = 'BARY',
      interpolation = 'linear',
      gridder = 'standard',
      niter = 10000,
      threshold = '2.5mJy',
      imsize = [512, 512],
      cell = '0.2arcsec',
      weighting = 'briggs',
      robust = 0.0,
      phasecenter = 4,
      pbcor = True,
      interactive = False,
      usemask='auto-multithresh',
      sidelobethreshold=2.0,
      noisethreshold=3.0,
      lownoisethreshold=1.5,
      minbeamfrac=0.3,
      growiterations=75,
      negativethreshold=15.0,
      verbose=True)

# This time the cleaning task should take only a few minutes.

# You can see the collapsed map using the Viewer, as explained above
