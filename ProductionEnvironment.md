This guide explains how to setup RFDoc for production on Linux using [Apache 2](http://httpd.apache.org/) as the web server and [mod\_wsgi](http://code.google.com/p/modwsgi/) for running the RFDoc Django application.

The guide is divided as following:



# Installing requirements #

Apache 2, mod\_wsgi and Python virtualenv are required. On Debian-based distributions (incl. Ubuntu) these are installed with:
```
sudo apt-get install apache2 libapache2-mod-wsgi python-virtualenv
```


# Create a new user and a group for RFDoc #

Create a new user 'rfdoc', belonging to the group of the same name:
```
sudo groupadd rfdoc
sudo useradd --system --shell /bin/bash --gid rfdoc --create-home --home-dir /home/rfdoc rfdoc
```

Switch to the user 'rfdoc':
```
sudo su - rfdoc
```


# Initialize a new virtualenv #

Create a new virtualenv (named 'venv') and take it into use:
```
virtualenv venv
source venv/bin/activate
```


# Install RFDoc and Django inside the virtualenv #

To install RFDoc, run:
```
pip install robotframework-rfdoc
```

If you have [setuptools](http://pythonhosted.org/setuptools/) (or its fork [distribute](http://pythonhosted.org/distribute/)) installed, Django should be installed automatically. If this is not the case, run:
```
pip install django==1.6.1
```


# Create the settings file #

This will create a new settings file `rfdoc_settings.py` into the user's home directory:
```
python -m rfdoc.rfdocsettings_defaults $HOME
```


# Configure the settings for production #

Open the just created `$HOME/rfdoc_settings.py` with your editor of choice.

There are a couple of settings you definitely want to change for production use:
  * Set `PRODUCTION` to `True`. This causes the static content (images, styles, etc.) to be not served by Django. We configure Apache to serve this content.
  * Set `DATABASE_NAME` to `/home/rfdoc/rfdoc.db`
  * Set `ALLOWED_HOSTS` according to the comments in the file. Leaving its value to `['*']` may compromise the security if RFDoc is available from the public Internet.


# Create the database for RFDoc #

To create a new database using the set `DATABASE_NAME`, run:
```
PYTHONPATH=$HOME:$PYTHONPATH python -m rfdoc.manage syncdb
```

You can answer 'no' when syncdb asks you to create a local superuser for the database.


# Generate Django admin site layout #

To get the Django admin site layout working, run:
```
PYTHONPATH=$HOME:$PYTHONPATH python -m rfdoc.manage collectstatic
```

Answer 'yes' to the confirmation.


# Configure Apache and mod\_wsgi #

Run the following command as user 'rfdoc':
```
python -c "import rfdoc; print rfdoc.__path__[0]"
```

Copy the path to the clipboard. Now you can log out user 'rfdoc'.

As root, create a new file `/etc/apache2/sites-available/rfdoc.conf` with the following content:
```
# Set this to the RFDoc installation path.
Define rfdoc_path /home/rfdoc/venv/local/lib/python2.7/site-packages/robotframework_rfdoc-0.4-py2.7.egg/rfdoc

# The path where your settings file is in.
Define rfdoc_settings_path /home/rfdoc

# URL path to the RFDoc (e.g. set to `/rfdoc` for http://localhost/rfdoc)
Define rfdoc_url /rfdoc

# No need to edit below unless you know what you are doing
WSGIDaemonProcess rfdoc python-path=${rfdoc_path}:${rfdoc_settings_path} user=rfdoc group=rfdoc
WSGIProcessGroup rfdoc
WSGIScriptAlias ${rfdoc_url} ${rfdoc_path}/rfdoc_wsgi.py
Alias /static/ ${rfdoc_path}/rfdocapp/static/
BrowserMatch "RFDoc uploader" downgrade-1.0
<Directory ${rfdoc_path}>                                   
    Require all granted
</Directory>
```

Set `rfdoc_path` to the path on your clipboard. If you have not used different paths and are using RFDoc 0.4, you likely don't need to change anything in this file.


# Apache: Enable the site and restart #

Enable the site:
```
  sudo a2ensite rfdoc
```

Then restart the Apache:
```
   sudo /etc/init.d/apache2 restart
```

RFDoc should be now accessible at the designated URL (http://localhost/rfdoc by default).
