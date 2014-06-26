# RG5

RG5 is a python script that accesses Google Analytics API and emails the top five stories to whoever you want.

Omitted files (for simplicity and security's sake) include:
* analytics.dat
* client_secrets.json
* secrets.json
* apiclient module folder
* oauth2client module folder
* httplib2 module folder
* uritemplate module folder

Basic instructions:

1. Access your dev console and create a new project
1. Allow Analytics API, create a new Client ID for an installed app and download JSON
1. mkdir and mkvirtualenv on your local box
1. Put these files in your local box 
1. Create/download omitted files that you need. See Google APIs Client Library quick start for more info.
1. Add in your client_secrets.json that you downloaded. You will have to change it's name.
1. Add in your secrets.json file or simply add in your info to the script. 
1. Run `python yourScript.py` and allow access to the account.
1. You should be running just fine now.
