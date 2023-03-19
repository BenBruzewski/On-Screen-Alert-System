
#Final Project, On-Screen Alert System
#validation file for Account SID

#check hex
def isThisHex(stringIn):
        for charIn in stringIn:
                if ((charIn < '0' or charIn > '9' ) and
                    (charIn < 'a' or charIn > 'f') and
                    (charIn != '\n')):
                        return False
        if len(stringIn) == 33:
                return True
        else:
                return False

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


with open('SID_AUTH_FILE.txt', 'r') as filep:
	account_sid = filep.readline()
	auth_token = filep.readline()
try:
	client = Client(account_sid, auth_token)
	verification_check = client.verify \
                .v2 \
                
except TwilioRestException as err:
	
	print(err)
#print(client) #potentially unecessary
#print(auth_token)
print(isThisHex(auth_token))

#Problems: literal random string text does not throw a failure all the time,
#might need to make sure that it does or check output with validator class

