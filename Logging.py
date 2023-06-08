import sys
import datetime
def logLoginAttempt(Username, passed, sussy, additionalInfo=""):
    with open('log.txt', 'a') as sys.stdout:
        print(f'{Username} logged in on {datetime.datetime.now()}, which was ' +( "Successful" if passed else "unsuccessful")+("| Warning! possible suspicious activity" if sussy else "")+". Additional info: " + (additionalInfo if additionalInfo != "" else "none"))
    sys.stdout= sys.__stdout__

def logGeneric(object):
    with open('log.txt', 'a') as sys.stdout:
        print("Statement here")


