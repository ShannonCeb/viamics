#!/usr/bin/python

# TODO: 
#   - This is a very crude start to a script to install viamics.
#   - Right now it only supports Debian-Based Linux Distrobutrions that use apt-get to install software packages. We should add support for other OSes (Not you, Windows!)
#   - This needs commenting and organization...BAD >_<
#   - rdp_classifier should download if it is already there...likewise it shouldn't unzip if already unzipped.
#   - FINAL STAGE - copy config.py and update with PATH to rdp_classifier and framework

import os
import sys
import urllib
import zipfile

#
# Only works on linux :)
#

if sys.platform != "linux2":
    print "Sorry, but right this script only works in Debian-Based Linux Distros using apt-get!\nShutting down...Goodbye!\n"
    sys.exit(0)

#
# install the entire repository that apt-get has...everything!
#    
    
try:
    os.system("sudo apt-get install git unzip python-matplotlib python-scipy python-numeric r-base r-recommended python-rpy2 python-setuptools python-dev python-django apache2 libapache2-mod-python")
except:
    print "apt-get was unable to run install.\n"
    sys.exit(0)
    
#
# Porbably unecessary, but double check that rpy2 is properly installed before we go diving in with rpy2 calls.
#

try:
    import rpy2.robjects as R
except:
    print "Python Module - 'rpy2' - was not properly installed.\nRe-Attempting apt-get install..."
    os.system("sudo apt-get install python-rpy2")
    try:
        import rpy2.robjects as R
    except:
        print " FAILED!\nPython Module - 'rpy2' was unable to be installed. Please install this module manually.\n"
        sys.exit(0)
        
#
# Install R packages
#
        
print 'Installing R packages...'
f = open("rpackages.script", "w")

# Set the CRAN to default repository (this may need to be changed to ensure that if this repo goes down, we have another option)
# And second command in script updates all current packages in R...as of 2/28/11 a fresh install of R does in fact have packages requiring updates.

script_commands = ["options(repos=c(CRAN=\"http://streaming.stat.iastate.edu/CRAN/\"))\n","update.packages(ask=FALSE)\n"]
from rpy2.robjects.packages import importr

# Check for each required R package. If they are not found, add them to a temporary R script file to be installed later.
try: 
    importr('gtools')
except:
    script_commands.append("install.packages('gtools')\n")
try:
    importr('gdata')
except:
    script_commands.append("install.packages('gdata')\n")
try:
    importr('caTools')
except:
    script_commands.append("install.packages('caTools')\n")
try:
    importr('bitops')
except:
    script_commands.append("install.packages('bitops')\n")
try:
    importr('gplots')
except:
    script_commands.append("install.packages('gplots')\n")
    
script_commands.append("quit()\n")
f.writelines(script_commands)
f.close()

# Execute R script file
try:
    os.system("sudo R -f %s" % f.name)
except:
    print "Can't find %s!" % f.name
    sys.exit(0)
    print "FAILED!\nThere was an error installing the packages required for R!\n"

# Remove Temp R Script file
os.remove(f.name)

# Ensure that R libraries can be found

try:
    importr('gtools')
    importr('gdata')
    importr('caTools')
    importr('bitops')
    importr('gplots')
except:
    print "FAILED!\n Please try to manual install the following R packages:\n\n\tgtools\n\tgdata\n\tcaTools\n\tbitops\n\tgplots\n\nGoodbye...\n"

#
# Download and unzip rdp_classifier
#
# Note: Uses system call to unzip to unzip. I was unable to get zipfile library to work without OSError. This may be a bug in library.

rdp_name = "rdp_classifier_2.2"
rdp_zip_name = rdp_name + ".zip"

# SHOULDN'T DOWNLOAD IF ALREADY THERE!
def reporthook(blocks_read, block_size, total_size): 
    print "% 3.1f%% of %d bytes\r" % (min(100, float(blocks_read * block_size) / total_size * 100), total_size),
    sys.stdout.flush()

try:
    urllib.urlretrieve("http://downloads.sourceforge.net/project/rdp-classifier/rdp-classifier/rdp_classifier_2.2.zip", rdp_zip_name, reporthook)
except:
    if not rdp_zip_name in os.listdir("."):
        print "Unable to find %s from sourceforge.net. Our link may be out-of-date, please manually download this file to this directory and execute this script again!\nGoodbye...\n" % rdp_zip_name
        sys.exit(0)
if zipfile.is_zipfile(rdp_zip_name):
    # Possibly check if the folder is already there?
    try:
        os.system("unzip %s" % rdp_zip_name)
    except:
        print "There was an error unzipping %s\n" % rdp_zip_name

#
# Install pip for installation of cogent
#    

try:
    os.system("sudo easy_install -U pip")
except:
    print "Unable to install pip. Please do so manually\n"

#
# Install cogent
#

cogent_file = open("cogent-requirements.txt", "w")
cogent_file.writelines(["cogent\nnumpy>=1.3.0"])
cogent_file.close()

os.system("DONT_USE_PYREX=1")
try:
    os.system("sudo pip install -r %s" % cogent_file.name)
except:
    print "Unable to install cogent!\n"
try:
    os.rm(cogent_file.name)
except:
    pass

#
# Change apache config file so that all instances of 'AllowOverride None' -> 'AllowOverride All'
#

original_text = "AllowOverride None"
new_text = "AllowOverride All"

apache_file_path = "/etc/apache2/sites-enabled/000-default"
apache_file = open(apache_file_path, "r")
text = apache_file.read()
apache_file.close()
apache_file = open(apache_file_path, "w")
apache_file.write(text.replace(original_text, new_text))
apache_file.close()

#
# Clone Viamics
#
os.system("git clone git://github.com/meren/viamics.git")

print "SUCCESS!\n"
    

