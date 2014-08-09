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

## secrets.json

```json
{
  "tableID": "ga:----------",
  "fromemail": "-------@---.com",
  "toemails": "-------@----.com, -------@----.com",
  "fromemail_user": "-------",
  "fromemail_pass": "------"
}

```

## Notes

* All `print` statements must be commented out for the cron unless you encode everything to utf-8 that's going out. If anything is printed it will create a Terminal email. If running on a server that would add up and be no good.
  * See [this stackoverflow](http://stackoverflow.com/a/492711/3784241) for more info.
* The title change is a big problem for the API. For example, on a query of the storyid and unique pageviews of 8/5/14 the most read piece is 31970913. This story had 1,146 hits total over two titles. The second title had 261 hits and the first had 885. This break, however, pushes the story out of the top five because the number five story has 896.


## How to

Before we begin, you will need:

* The [Google Analytics Table ID](https://developers.google.com/analytics/devguides/reporting/core/v3/index#user_reports) for the table you want to query
* The dimensions and metrics you want to query
* The email user and pass that you want to send from
* The emails you want to send to

Basic instructions:

1. Access your [Google dev console](https://console.developers.google.com) and create a new project
1. Allow Analytics API, create a new Client ID for an installed app and download JSON
1. mkdir and mkvirtualenv on your local box
1. Put these files in your local box 
1. Create/download omitted files that you need. See [Google APIs Client Library quick start]() for more info.
1. Add in your client_secrets.json that you downloaded. You will have to change it's name.
1. Add in your secrets.json file or simply add in your info to the script. 
1. Run `python yourScript.py` and allow access to the account.
1. You should be running just fine now.

Also see:

* [registerguard/tracker#444](https://github.com/registerguard/tracker/issues/444) (Private repo)
* [Hello Analytics API tutorial](https://developers.google.com/analytics/solutions/articles/hello-analytics-api)
* [Google APIs Client Library for Python Installation guide](https://developers.google.com/api-client-library/python/start/installation)
* [Core Reporting API](https://developers.google.com/analytics/devguides/reporting/core/v3/coreDevguide)
* Python [email](https://docs.python.org/2/library/email-examples.html)
* Python email [tutorial](http://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email)
* [GA API and Django](http://blog.iambob.me/accessing-google-analytics-from-django/)
