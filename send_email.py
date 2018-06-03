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
message.Subject = "An HTML Email"
message.Html = """This email uses <strong>HTML</strong>!"""
message.Body = body

sender = Mailer('smtp.gmail.com')
sender.send(message)

