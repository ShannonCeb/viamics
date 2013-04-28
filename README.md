_Viamics is no longer being developed. Thanks for your interest._

 Viamics
===============================================================================

  "Visual and statistical analysis framework for microbial communities, and more".

 Framework
===============================================================================

 This codebase contains the pre-alpha version of a statistical analysis and
visualization framework that has been developed mainly for microbial community
and microbial ecology studies.

 Publication of this study, titled "A framework for analysis of metagenomic
sequencing data", is here:

    http://www.ncbi.nlm.nih.gov/pubmed/21121041

 Also a static snapshot of the framework, along with some basic information
about it's purpose, could be found here:

    http://meren.org/framework/



 Licence
===============================================================================

 This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

 This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


 Installation
===============================================================================

 Although it is quite straightforward, installation might be tricky for novice users.

 Following information is mostly to give an idea to programmers and command line enthusiasts who like to get
the framework running.


     # APT INSTALLATION SCRIPT FOR UBUNTU/DEBIAN:
     #     This python script: https://raw.github.com/meren/viamics/install/install.py will 
     #     download all dependencies and install Viamics using the apt package manager and
     #     other sources (cran for R packages, pip for certain python modules).
     #
     #     After running the install script:
     cd viamics/framework;python server.py # start the viamics server
     cd viamics/framework/clients/ferrisweb;python manage.py runserver # start the django web interface
     
     # go to http://localhost:8000 in your browser to try it out
     
     --------------------------------------------------------------------------------
     
     # The framework was developed and tested on Pardus Corporate (64 bit) version.
     # It should work on any Linux distribution and even Mac, but most of the
     # commands in the following section will work only on Pardus Corporate. You
     # may evaluate the commands and use appropriate packages for your distro,
     # but if you would like to go with Pardus Corporate, you can download it
     # here:
     #
     #   ftp://ftp.pardus.org.tr/pub/ISO/Kurulan/Corporate2/Alpha/x86_64/
     #
     cat /etc/pardus-release
     Pardus Corporate 2 Alpha
     
     # at this point I assume you have the codebase and you are in the root
     # directory of the Framework
     sudo pisi it matplotlib
     sudo pisi it numeric
     sudo pisi it scipy
     sudo pisi it kernel-headers
     sudo pisi it xorg-proto
     sudo pisi it xorg-font-extra xorg-font urw-fonts
     sudo pisi it make
     
     #R
     wget http://cran.opensourceresources.org/src/base/R-2/R-2.11.1.tar.gz
     ./configure --enable-R-shlib && make && make install
     ldconfig
     # run R:
     sudo R
     # in the R command line:
         install.packages('gtools')
         install.packages('gdata')
         install.packages('caTools')
         install.packages('bitops')
         install.packages('gplots')
     # quit R.
     
     
     #RPy2
     wget http://downloads.sourceforge.net/project/rpy/rpy2/2.1.x/rpy2-2.1.8.tar.gz
     echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib64/R/bin:/usr/local/lib64/R/lib' >> ~/.bashrc
     su
     export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib64/R/bin:/usr/local/lib64/R/lib
     export PATH=$PATH:/usr/local/bin/
     python setup.py install
     
     # download RDP and put it somewhere on the disk, then edit your config file.
     wget http://downloads.sourceforge.net/project/rdp-classifier/rdp-classifier/rdp_classifier_2.2.zip
     
     # PyCogent
     wget http://downloads.sourceforge.net/project/pycogent/PyCogent/1.4.1/PyCogent-1.4.1.tgz?use_mirror=cdnetworks-us-1
     
     #server stuff
     sudo pisi it Django
     sudo pisi it apache
     sudo pisi it mod_python
     sudo service apache on
     sudo service apache start
     
     # configure server
     # set AllowOverride All in /etc/apache2/vhosts.d/00_default_vhost.conf
     # .htaccess content:
     
     ---8<---8<---8<---8<---8<---8<---8<---8<---8<-----
     AddHandler mod_python .py
     SetHandler python-program
     
     Header set Pragma "no-cache"
     Header set Cache-Control "no-cache"
     Header set Expires "-1"
     
     PythonPath "['/PATH/TO/FRAMEWORK/../'] + sys.path"
     
     PythonHandler django.core.handlers.modpython
     SetEnv DJANGO_SETTINGS_MODULE ferrisweb.settings
     PythonDebug On
     ---8<---8<---8<---8<---8<---8<---8<---8<---8<-----


 Running
===============================================================================

 1. Running the server: run "python server.py" command in "framework"
 directory.

 2. Running web client: run "python manage.py runserver" command in
 "framework/clients/ferrisweb/" directory, it will run a lightweighted web
 server you can use to connect to the framework. You will see the address in
 the output (or instead you can setup your Apache installation and use .htaccess
 file to relay web requests to the framework codebase).
