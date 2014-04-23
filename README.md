cercisanat.com
==============

This repository contains the codebase used in http://cercisanat.com. Cerci Sanat is a non-profit, collective, online arts magazine published by volunteers. 

The site is running on a (mostly) conventional Django installation. If you want to try cercisanat.com on your local machine, please follow the steps specified below.

1. Install [http://www.virtualenv.org/en/latest/](virtualenv) and preferably [https://bitbucket.org/dhellmann/virtualenvwrapper](virtualenvwrapper)

2. run the following commands:

```
cd into directory where you want to install cerci sanat

# clone the repository
cd cercisanat.com

# edit cerci/settings_local.py and update database information
# create the database specified in settings_local.py

# create an virtualenv
mkvirtualenv cerci

# install the dependencies
pip install -r requirements.txt

# run the installation command:
make install
```

if everything is fine Cerci Sanat website should be available on http://localhost:8000


