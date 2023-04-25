#If all else fails, download the helper library from https://www.twilio.com/docs/python/install
import os
import sys
from twilio.rest import Client
#5/1/2022

with open('SID_AUTH_FILE.txt', 'r') as filep:
	TWILIO_ACCOUNT_SID = filep.readline()
	TWILIO_AUTH_TOKEN = filep.readline()
	TWILIO_VIRT_NUM = filep.readline()

numArgs = len(sys.argv)
#Needs 2 senttonum, 3 app name var, 4 act spec var
#will have a case to run with just 0, 1, 2 and 0, 1, 2, 3
if (numArgs < 2):
    print("use virtual number, recipient number. optionally, application and action specifier")
    quit()


#TWILIO_VIRT_NUM = sys.argv[1]
SENT_TO_NUM = '+1' + sys.argv[1]
if (numArgs < 3):
    APPLICATION_NAME_VAR = "[DEFAULT, SPECIFY APPLICATION IF PERMISSIBLE]"
    ACTION_SPECIFIER_VAR = "[DEFAULT ACTION]"

elif(numArgs < 4):
    APPLICATION_NAME_VAR = sys.argv[2]
    ACTION_SPECIFIER_VAR = "[DEFAULT ACTION]"
else:
    APPLICATION_NAME_VAR = sys.argv[2]
    ACTION_SPECIFIER_VAR = sys.argv[3]
    
#TODO populate or change
initialMessage = "Alert: " + APPLICATION_NAME_VAR + " has " + ACTION_SPECIFIER_VAR + " Pending"
followupMessage = " \r\nReply stop to stop"
#Do not serve unless client requests
stopMessage = "stop"
cycSendVar = ""


 


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN

#create client instance with SID and Token
client = Client(account_sid, auth_token)
#set client instance message to JSON-like inc MESSAGE,FROM,TO
message = client.messages \
                .create(
                     body=initialMessage,
                     from_=TWILIO_VIRT_NUM,
                     to= SENT_TO_NUM
                    #debug
                     
                     #to = TWILIO_RECIP_NUM
                 )

#print(message.sid)
