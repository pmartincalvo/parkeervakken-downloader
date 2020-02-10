# Parkeervakken downloader

## Intro

This repo contains the scripts necessary to download a daily copy of the city parking map from Amsterdam.nl API. 

See https://api.data.amsterdam.nl/parkeervakken/parkeervakken/ for more datils.

## How to run

1. Set up a .env file that provides the variables specified at .env-example.
2. Install the requirements in requirements.txt. Using a virtualenv is recommended.
3. Run the run.py python file.

*NOTE*: this repo doesn't contain any scheduling features. You can either run it manually, or use tools like cron to schedule the execution of the script.
## Requirements

*  Python 3.6+ and dependent packages.

## Possible issues

The user running run.py must have the required privileges to create the folders specified in the .env file.

For everything else, check the log file located at the base path.