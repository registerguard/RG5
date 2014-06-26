#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

# import the Auth Helper class
import analytics_auth
from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError

# to get "yesterday" we import these
from datetime import date, timedelta

# email
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import json

with open("secrets.json") as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """Get the secret variable or return explicit exception."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

### ********************* ###
### ******* MAIN ******** ###
### ********************* ###

def main(argv):
  # Initialize the Analytics Service Object
  service = analytics_auth.initialize_service()

  try:
    results = get_results(service)
    print_data_table(results)
    #print_results(results)

  except TypeError, error:
    # Handle errors in constructing a query.
    print ('There was an error in constructing your query : %s' % error)

  except HttpError, error:
    # Handle API errors.
    print ('Arg, there was an API error : %s : %s' %
           (error.resp.status, error._get_reason()))

  except AccessTokenRefreshError:
    # Handle Auth errors.
    print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize')

### *********************** ###
### ****** YESTERDAY ****** ###
### *********************** ###

yes = date.today() - timedelta(1)
yesStr = yes.isoformat()

### ********************* ###
### ******* QUERY ******* ###
### ********************* ###

def get_results(service):
  # Use the Analytics Service Object to query the Core Reporting API
  return service.data().ga().get(
      ids=get_secret("tableID"),
      start_date=yesStr,
      end_date=yesStr,
      #metrics='ga:sessions' ).execute()
      metrics='ga:pageviews',
      dimensions='ga:pagePath,ga:pageTitle',
      sort='-ga:pageviews',
      max_results='5' ).execute()

### *********************** ###
### ******* RESULTS ******* ###
### *********************** ###

def print_data_table(results):
  # Print headers.
  output = []
  for header in results.get('columnHeaders'):
    output.append('%s' % header.get('name'))
  output.append(';') # add semicolon to end of first line in list

  # Print rows.
  if results.get('rows', []):
    for row in results.get('rows'):
      #output = [] #this resets the list each row
      for cell in row:
        output.append('%s' % cell)
        #print output #prints for each cell
      output.append(';') # add semicolon to end of each row
      outputStr = ', '.join(output) # converts list to string
      #print output #prints for each row
    #print output #prints at end
  else:
    print 'No Results Found'

  # Format string to get rid of Title stuff, semicolon stuff and make links absolute
  # Has new line on semicolon
  #outputStr = outputStr.replace(" | The Register-Guard | Eugene, Oregon","").replace(";","\n").replace(", /rg/","http://registerguard.com/rg/")
  # Does not have new line on semicolon
  outputStr = outputStr.replace(" | The Register-Guard | Eugene, Oregon","").replace(";","").replace(", /rg/","http://registerguard.com/rg/")

  # Split the string back into a list to call in email
  outputList = outputStr.split(',')

  # Create email text
  emailHead = "<!DOCTYPE html><head><style>body{font-family:'Arial', sans-serif}</style></head><body><h1>Top stories</h1><ol><!-- #1 -->"
  # Each story must call API data in the list
  email1 = "<li><b><a href='%(LINK1)s'>%(TITLE1)s</a></b> <br>- Clicks:     %(VIEWS1)s</li>" % {'LINK1': outputList[3], 'TITLE1': outputList[4], 'VIEWS1': outputList[5]}
  email2 = "<li><b><a href='%(LINK2)s'>%(TITLE2)s</a></b> <br>- Clicks:     %(VIEWS2)s</li>" % {'LINK2': outputList[6], 'TITLE2': outputList[7], 'VIEWS2': outputList[8]}
  email3 = "<li><b><a href='%(LINK3)s'>%(TITLE3)s</a></b> <br>- Clicks:     %(VIEWS3)s</li>" % {'LINK3': outputList[9], 'TITLE3': outputList[10], 'VIEWS3': outputList[11]}
  email4 = "<li><b><a href='%(LINK4)s'>%(TITLE4)s</a></b> <br>- Clicks:     %(VIEWS4)s</li>" % {'LINK4': outputList[12], 'TITLE4': outputList[13], 'VIEWS4': outputList[14]}
  email5 = "<li><b><a href='%(LINK5)s'>%(TITLE5)s</a></b> <br>- Clicks:     %(VIEWS5)s</li>" % {'LINK5': outputList[15], 'TITLE5': outputList[16], 'VIEWS5': outputList[17]}
  emailFoot = "</ol><p><small>If this does not display correctly, contact <a href='mailto:rob.denton@registerguard.com'>Rob Denton</a></small></p></body>"
  # Concatenate
  email = emailHead + email1 + email2 + email3 + email4 + email5 + emailFoot
  # encode so that it doesn't throw an error in the email
  email = email.encode('utf-8')
  
### ********************* ###
### ******* EMAIL ******* ###
### ********************* ###

  # From:
  fromaddr = get_secret("email")
  # To: 
  toaddr = [get_secret("rob"),get_secret("rob2"),get_secret("rob3")]
  msg = MIMEMultipart('alternative')
  msg['From'] = fromaddr
  #Subject
  msg['Subject'] = "Yesterday's top stories"

  body = email
  msg.attach(MIMEText(body, 'html'))

  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.ehlo()
  # From email user and pass
  server.login(get_secret("email_user"), get_secret("email_pass"))
  server.sendmail(fromaddr, toaddr, msg.as_string())

  print "sent!" # Hooray!

### ******************** ###
### ******* CALL ******* ###
### ******************** ###

if __name__ == '__main__':
  main(sys.argv)

print "done" # YUS
