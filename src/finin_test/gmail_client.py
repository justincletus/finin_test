import email
from django.conf import settings
import imaplib
import json

class EmailFn:

    def __init__(self):
        super().__init__()

    def send_email_test(self):

        email_account = settings.EMAIL_DETAILS

        con = imaplib.IMAP4_SSL(str(email_account['IMAP_URL']))
        
        try:
            con.login(str(email_account['USERNAME']), str(email_account['PASSWORD']))
            con.select('Inbox')
            list_element = ['invoice', 'subscription', 'bill']
            response = []

            for x in list_element:
                context = {}
                messages = self.get_emails(self.search('Subject', str(x), con), con)
                context[x] = messages
                response.append(context)
            
            return response

        except Exception as e:
            print(e)

    def search(self, key, value, con):
        result, data = con.search(None, key, '"{}"'.format(value))
        return data

    def get_emails(self, results, con):
        msgs = []
        for num in results[0].split():
            typ, data = con.fetch(num, '(RFC822)')
            msgs.append(data)

        message_list = []
        # context = {}

        for msg in msgs[::-1]:
            for send in msg:
                context = {}
                if type(send) is tuple:
                    content = str(send[1], 'utf-8')
                    data = str(content)

                    try:
                        indexStart = data.find("ltr")
                        data2 = data[indexStart + 5: len(data)]
                        
                        indexEnd = data2.find("<div dir=3D")
                        message_body = data2[0: indexEnd]
                        
                        context['body'] = message_body
                        # message_list.append(context)

                    except UnicodeEncodeError as eu:
                        pass

                    try:             

                        attached = data.find("Content-Type: application/pdf;")
                        data3  = data[attached : len(data)]
                        indexEnd2 = data3.find(".pdf")
                        attached_file = data3[0: indexEnd2 + 5]

                        context['attachment'] = attached_file

                        message_list.append(context)



                    except UnicodeEncodeError as eu:
                        pass
                    
                    # print(str(context))

                    # message_list.append(context)
        #print(message_list)
        return message_list
        # print(message_list)

                    # print(data)

    def get_body(self, msg):
        if msg.is_multipart():
            return get_body(msg.get_payload(0))

        else:
            return msg.get_payload(None, True)
