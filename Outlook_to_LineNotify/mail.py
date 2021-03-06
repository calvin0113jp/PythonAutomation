# mail receive

import win32com.client
from datetime import date, datetime, timedelta
from line import LineMain
import os
from shutil import copyfile

mail_file = 'mail_list.txt'
mail_file_old = 'mail_listOld.txt'

class ReadOutlookMail:
    def __init__(self):
        self.outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        self.accounts = win32com.client.Dispatch("Outlook.Application").Session.Accounts
    
    def compare_file(self):
        import filecmp
        result = filecmp.cmp(mail_file_old, mail_file)
        return result
    
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
        diff_file = mail.compare_file()
        if diff_file == False:
            message = mail.send_notify()
            # --- line ---
            token = 'token'
            line = LineMain()
            line.lineNotifyMessage(token=token, msg=message)
            copyfile(src=mail_file, dst=mail_file_old)
        else:
            print ('Comapre the same mail , no send out')
    else:
        print ('No mail to send to Line')

    
    

    


    
    
