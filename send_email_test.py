import smtplib
import argparse

gmail_user = 'jordansmitty01@gmail.com'
gmail_password = '5t0r@g3!'

parser = argparse.ArgumentParser(description='Send email for background check references.')
parser.add_argument("-a", "-applicant", type=str,
                    help='name of applicant to be checked')
parser.add_argument("-ref", "-reference_name", type=str, nargs='+',
                    help='name of reference(s) to send email')
parser.add_argument("-refemail", "-reference_email", type=str, nargs='+',
                    help='email address of reference(s)')

args = parser.parse_args()
sent_from = 'jordansmitty01@gmail.com'
to_email = args.reference_email
applicant_name = args.applicant
reference = args.reference_name
subject = 'OMG Super Important Message'
body = """
        REFERENCE INTERVIEW FORM
        Grace Covenant Church 1255 N Greenfield Rd. Gilbert, AZ 85234 480.813.3637
        Dear: 
        Applicant: %s
        Name of Reference: %s
        Reference Phone: 
        Reference Address: 
        Reference E-mail Address: %s
        """ % (applicant_name, reference, to_email)
email_text = 'Subject: {}\n\n{}'.format(subject, body)


try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to_email, email_text)

    print 'email sent!'
except:
    print 'Something went wrong...'


print args
