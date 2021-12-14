# mail receive

import win32com.client
from datetime import date, datetime, timedelta
from line import LineMain
import os

mail_file = 'mail_list.txt'

class ReadOutlookMail:
    def __init__(self):
        self.outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        self.accounts = win32com.client.Dispatch("Outlook.Application").Session.Accounts
    
    def check_mail(self):
        
        # check file is exit
        if os.path.exists("%s" %(mail_file)):
            os.remove("%s" %(mail_file))
        else:
            print("The file does not exist")

        print ('<<< Scanning Unread Mail >>>')
        result = []    
        inbox = self.outlook.GetDefaultFolder(6)
        
        try:
            for message in inbox.Items:
                if message.UnRead == True:
                    result.append('<<< subject: >>>' + message.Subject + message.body)
        except:
            print ('<<< Not found New Mail >>>')

        if result != []:
            for result1 in result:
                with open("%s" %(mail_file),"a+", encoding = 'utf-8') as f:
                    result1 = result1.replace('\r\n','') 
                    f.write("%s\n" %(result1))
                    a = '-'*30
                    f.write('%s\n' %(a))
            return 1
        else:
            return 0

    def send_notify(self):
        
        with open("%s" %(mail_file),"r", encoding='UTF-8') as f:
            reading_file = f.read()
        return reading_file

if __name__ == '__main__':
    get_date = datetime.now().strftime('%m/%d/%Y')
    print ('Scan mail date = {}'.format(get_date))
    mail = ReadOutlookMail()
    get_mail_list = mail.check_mail()
    if get_mail_list == 1:
        message = mail.send_notify()
        # --- line ---
        token = 'line token'
        line = LineMain()
        line.lineNotifyMessage(token=token, msg=message)
    else:
        print ('No mail to send to Line')

    
    

    


    
    