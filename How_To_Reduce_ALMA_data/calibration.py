# This is the script for calibrating the raw data from the terminal using the pipeline provided within the CASA software.
# Please read carefully the comments in the script to understand what the commands do.

# For any problems, you can look at the User Reference & Cookbook 4.7.2 (https://casa.nrao.edu/docs/cookbook/index.html)
# or at the Task Reference Manual -Oct 2016- (https://casa.nrao.edu/docs/TaskRef/TaskRef.html)

# --------------------------------------------------------------------------
# HOW TO RUN THE PIPELINE
# --------------------------------------------------------------------------

# Open the terminal and go to the directory 'member.uid...' within the downloaded folder

cd script/

# Modify the file scriptForPI.py: savingslevel = 3

casav472 --pipeline
# use the same version of casa used to obtain the products, which is specified in the file README of the downloaded folder

spacesaving = 3
# to be extra safe

execfile('scriptForPI.py')
# this creates a folder in the folder 'calibrated' and generates the visibility files therein

# It is a wise idea to copy the newly created folder and rename it with a simple name,
# so that you can access to it you mess the original folder up, by typing the following:

cd calibration/
cp -r uid___A002_Xbdcd3c_X2e96.ms.split.cal calibrated.ms
