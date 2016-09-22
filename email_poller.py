import imaplib
from email.parser import HeaderParser
import email
import email.utils
import time
import parse_config as parse
import re
# parse the configuration
debug = True

def pollEmail(configFile):
    cfgResult = parse.readConfig(configFile)
    if not cfgResult[0] == "SUCCESS":
        print(cfgResult[1])
        exit(1)

    emailPass = {}
    delEmail = False
    cfgDict = cfgResult[1]
    username = cfgDict['emailAddress']
    password = cfgDict['emailPassword']
    emailServer = cfgDict['emailServer']

#    print(cfgDict)

    mail = imaplib.IMAP4_SSL(emailServer,993)

    mail.login(username, password)
    mail.select()
    status, data = mail.search(None, 'ALL')
    emailCount = len(data[0].split())
    if emailCount == 0:
        print("No Mail Available")
        return emailPass
    else:
        if debug:
            print("I think there are: {} emails available".format(emailCount ))
        for num in data[0].split():
            status, data = mail.fetch(num, '(RFC822)')
            msgNumber = num.decode('utf-8')
            if debug:
                print("Message Number: {}, Status: {}".format(msgNumber, status))
            raw_data = mail.fetch(num, '(BODY[HEADER])')


            parser = HeaderParser()
            header_data = raw_data[1][0][1].decode('utf-8')
            msg = parser.parsestr(header_data)

            if debug:
                print("Message To: {}".format(msg["To"]))
#            print("Message From: {}".format(msg["From"]))
#            print("Message Date: {}".format(msg["Date"]))
            emailDate = msg["Date"]
            # convert emailDate to a unix time
            # Wed, 30 Mar 2016 12:23:13 +0000
            # determine our current GMT offset
            localHour = time.strftime('%H',time.localtime())
            gmtHour = time.strftime('%H', time.gmtime())
            hourOffset = int(gmtHour) - int(localHour)
            unixTime = int(time.mktime(email.utils.parsedate(emailDate)))
            rightNow = int(time.time());
            diffTime = unixTime - rightNow
            inMinutes = diffTime / 60
            diffMinutes = (60 * hourOffset) - inMinutes
            msgSubject = msg["Subject"]
            if msgSubject == "Traders Password":
                delEmail = True
            else:
                delEmail = False

            if debug:
                print("Message Subject: {}".format(msgSubject))
                print("Email Body:")

            resp, data = mail.fetch(num, "(RFC822)")
            raw_email = data[0][1].decode('utf-8')
            mail_body = email.message_from_string(raw_email)

            for part in mail_body.walk():
                contType = part.get_content_type()
                if debug:
                    print("content type: {}".format(contType))
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    plainTextBody = body.decode('utf-8')
                    print(plainTextBody)

            extractedPass = "ERROR"
            for line in plainTextBody.split("\n"):
                m = re.search("Your password is:\s+(\S+)", line)
                if m:
                    extractedPass = m.groups()[0]


            if debug:
                print("Body Ends")
                print("extracted password: {}".format(extractedPass))
            emailPass[msg["To"]] = extractedPass
            # delete this email?
            if delEmail:
                mail.store(num, '+FLAGS', '\\Deleted')


    mail.expunge()
    mail.close()
    mail.logout()
    return emailPass

if __name__ == '__main__':
    print("Loaded as a main script - running in test mode.")
    debug = True
    resultDict = pollEmail('blacknova.config')
    print("Result dict from polling email server")
    print(resultDict)