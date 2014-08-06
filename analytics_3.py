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

import pprint

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

# MAKE THIS SEVEN DAYS

yes = date.today() - timedelta(1) # Get yesterday
yesStr = yes.isoformat() # Get year-month-day date for Analytics API
yesH1 = yes.strftime("%m/%d/%Y") # Get full month/day/year date
yesDay = yes.strftime("%A") # Get full weekday name

### ********************* ###
### ******* QUERY ******* ###
### ********************* ###

def get_results(service):
  # Use the Analytics Service Object to query the Core Reporting API
  return service.data().ga().get(
      ids=get_secret("tableID"),
      start_date=yesStr,
      end_date=yesStr,
      dimensions='ga:dimension1, ga:dimension2, ga:dimension3, ga:dimension4, ga:dimension5',
      metrics='ga:uniquePageviews',
      sort='-ga:uniquePageviews',
      max_results='10' ).execute()

### *********************** ###
### ******* RESULTS ******* ###
### *********************** ###

def print_data_table(results):
  # Print headers.
  output = []
  for result in results:
    print "   type:", type(result)
    print "   dir:", dir(result)
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
    #pprint.pprint(output) # output #prints at end
  else:
    print 'No Results Found'

  # Format string to get rid of Title stuff, semicolon stuff and make links absolute
  # Has new line on semicolon
  #outputStr = outputStr.replace(" | The Register-Guard | Eugene, Oregon","").replace(";","\n").replace(", /rg/","http://registerguard.com/rg/")
  # Does not have new line on semicolon
  #outputStr = outputStr.replace(" | The Register-Guard | Eugene, Oregon","").replace(", /rg/","http://registerguard.com/rg/")

  # Split the string back into a list to call in email
  outputList = outputStr.split(',')
  print outputList

  # Create email text
  emailHead = "<!DOCTYPE html><head><style>body{font-family:'Arial', sans-serif}</style></head><body><h1>Top stories from %(WKDY)s, %(DAY)s</h1><ol><!-- #1 -->" % {'WKDY': yesDay, 'DAY': yesH1}
  # Each story must call API data in the list
  email1 = "<li><b><a href='%(LINK1)s'>%(TITLE1)s</a></b> - %(AUTHOR1)s <br>- Clicks:     %(VIEWS1)s</li>" % {'LINK1': outputList[11], 'TITLE1': outputList[12], 'AUTHOR1': outputList[7], 'VIEWS1': outputList[13]}
  email2 = "<li><b><a href='%(LINK2)s'>%(TITLE2)s</a></b> - %(AUTHOR2)s <br>- Clicks:     %(VIEWS2)s</li>" % {'LINK2': outputList[19], 'TITLE2': outputList[20], 'AUTHOR2': outputList[15], 'VIEWS2': outputList[21]}
  email3 = "<li><b><a href='%(LINK3)s'>%(TITLE3)s</a></b> - %(AUTHOR3)s <br>- Clicks:     %(VIEWS3)s</li>" % {'LINK3': outputList[27], 'TITLE3': outputList[28], 'AUTHOR3': outputList[23], 'VIEWS3': outputList[29]}
  email4 = "<li><b><a href='%(LINK4)s'>%(TITLE4)s</a></b> - %(AUTHOR4)s <br>- Clicks:     %(VIEWS4)s</li>" % {'LINK4': outputList[35], 'TITLE4': outputList[36], 'AUTHOR4': outputList[31], 'VIEWS4': outputList[37]}
  email5 = "<li><b><a href='%(LINK5)s'>%(TITLE5)s</a></b> - %(AUTHOR5)s <br>- Clicks:     %(VIEWS5)s</li>" % {'LINK5': outputList[43], 'TITLE5': outputList[44], 'AUTHOR5': outputList[39], 'VIEWS5': outputList[45]}
  emailFoot = "</ol><p><small>If this does not display correctly, please contact the web team at <a href='mailto:webeditors@registerguard.com'>webeditors@registerguard.com</a></small></p></body>"
  # Concatenate
  email = emailHead + email1 + email2 + email3 + email4 + email5 + emailFoot
  print email
  # encode so that it doesn't throw an error in the email
  email = email.encode('utf-8')
  
### ********************* ###
### ******* EMAIL ******* ###
### ********************* ###

  # From:
  fromaddr = get_secret("fromemail")
  # To: 
  toaddr = [get_secret("toemail")]
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
  server.login(get_secret("fromemail_user"), get_secret("fromemail_pass"))
  
  # *** UNCOMMENT THIS TO SEND EMAIL ***
  server.sendmail(fromaddr, toaddr, msg.as_string())
  print "sent!" # Hooray!

### ******************** ###
### ******* CALL ******* ###
### ******************** ###

if __name__ == '__main__':
  main(sys.argv)

print "done" # YUS
