This guide explains how to get RFDoc running on Linux, OS X or Windows.

The guide is divided as following:


# Requirements #

RFDoc requires Django 1.5 and additionally Django requires Python 2.6.5 or later.

If you have [setuptools](http://pythonhosted.org/setuptools/) (or its fork [distribute](http://pythonhosted.org/distribute/)) installed, Django should be installed automatically by both of the installation approaches.

If not, you can first install Django by following the instructions for your operating system available at [Django's official installation instructions](https://docs.djangoproject.com/en/dev/topics/install/#install-the-django-code).

# Installation #

## Using pip ##

If you have [pip package manager](http://www.pip-installer.org) available, the easiest way to install RFDoc is to run:
```
pip install robotframework-rfdoc
```

## Using source distribution ##

If you do not want to install `pip`, you can install RFDoc from source as following:
  1. Download the source tar.gz at https://pypi.python.org/pypi/robotframework-rfdoc.
  1. Extract the package to a temporary location.
  1. Open a terminal / command prompt.
  1. `cd` to the extracted directory.
  1. Run `python setup.py install`


# Configure RFDoc #

You can start up RFDoc without any configuration, but you likely want to configure at least the database location.

Run the following command to create a new configuration file to an **existing** directory:
```
python -m rfdoc.rfdocsettings_defaults /an/existing/directory/
```

The created `rfdocsettings.py` is created in the given directory. Make sure to append the directory to your PYTHONPATH before proceeding.

Now open up `rfdocsettings.py` for documentation on settings and do your changes.


# Set up the database #

RFDoc uses [SQlite3](http://www.sqlite.org/) database by default, and the earlier mentioned `rfdocsettings.py` specifies where the database file is or will be located.

**Note**: `rfdocsettings.py` must be found in your PYTHONPATH when running the following commands.

Create/update the database schema:
```
python -m rfdoc.manage syncdb
```

You can answer 'no' when `syncdb` asks you to create a local superuser for the database.

In those rare cases when RFDoc's database model is changed, this command needs to be executed again.


# Django admin site #

To get the Django admin site (http://localhost:8000/admin) layout working, run:
```
python -m rfdoc.manage collectstatic
```

Answer 'yes' to the confirmation.


# Start up RFDoc locally #

```
python -m rfdoc.manage runserver
```

Now navigate to http://localhost:8000/ and you should see the RFDoc front page.


# Emptying the database #

```
python -m rfdoc.manage flush
```