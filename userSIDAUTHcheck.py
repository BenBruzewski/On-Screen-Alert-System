
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

#import CLient and Exceptions
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

print("SID: 34 characters beginning with AC then 32 chars 0x0-0xf")
print("AUTH: 32 characters 0x0-0xf")
print("from number: purchased from TWILIO or your number, '+1' + '----------' 10 digit phone number (US Only) ")
with open('SID_AUTH_FILE.txt', 'r') as filep:
	account_sid = filep.readline()
	auth_token = filep.readline()
	from_number = filep.readline()
try:
	client = Client(account_sid, auth_token)
	phone_number = client.lookups.v2.phone_numbers(from_number).fetch()
	test_number = client.pricing.v2.voice.numbers(from_number).fetch()
	print("SID/AUTH and phone check:",phone_number.valid)        
except TwilioRestException as err:
	print(err)
	print("False")
#print(client) #debug start
#print(auth_token)
#print("auth check:", isThisHex(auth_token)) #debug end
print("input Enter to dismiss")
dismiss = input()
#Problems: literal random string text does not throw a failure all the time, but if the user goes to the trouble to do that we cannot help them


