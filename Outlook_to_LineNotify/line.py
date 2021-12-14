# Line nofity

import requests

class LineMain:
    def lineNotifyMessage(self, token, msg):  
        headers = {
            "Authorization": "Bearer " + token, 
            "Content-Type" : "application/x-www-form-urlencoded"
        }

        payload = {'message': msg }
        r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
        return r.status_code

if __name__ == '__main__':
    # token = 'iput token'
    # message = '基本功能測試'
    line = LineMain()
    line.lineNotifyMessage(token, message)

    


    
    