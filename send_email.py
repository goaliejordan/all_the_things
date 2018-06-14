from mailer import Mailer
from mailer import Message
from reference_email_body import body as body

sent_from = 'jordansmitty01@gmail.com'
to ='goaliejordan@gmail.com'
subject = 'OMG Super Important Message'
body = body.format("jordan", "shannon", "caleb", "jordan")

message = Message(From=sent_from,
                    To=to,
                    charset="utf-8")
message.Subject = subject
message.Html = """<PRE>{}</PRE>""".format(body)
#message.Body = body

sender = Mailer(host='smtp.gmail.com', 
                port=465,
                use_ssl=True,
                usr='jordansmitty01',
                pwd='5t0r@g3!')
sender.send(message)

