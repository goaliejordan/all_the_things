import smtplib
import argparse

gmail_user = 'jordansmitty01@gmail.com'
gmail_password = '5t0r@g3!'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send email for background check references.')
    parser.add_argument('--applicant-name', '-n', type=str, dest='applicant_fn',
                        help='name of applicant to be checked')
    parser.add_argument('--reference-name', '-r', type=str, nargs='+', dest='reference_fn',
                        help='name of reference(s) to send email')
    parser.add_argument('--reference-email', '-e', type=str, nargs='+', dest='reference_email',
                        help='email address of reference(s)')

    args = parser.parse_args()
    sent_from = gmail_user
    applicant_name = args.applicant_fn
    reference_name = args.reference_fn
    reference_email = args.reference_email

    if len(reference_name) != len(reference_email):
        print '''
                **** If two references are provided, there must also be two emails provided ****
                     Please re-enter the command with the correct names and emails.
              '''
    else:
        for reference, email in zip(reference_name, reference_email):
            to_email = email
            reference_name = reference
            subject = 'Character reference for %s' % applicant_name
            body = """
            REFERENCE INTERVIEW FORM

            Grace Covenant Church 1255 N Greenfield Rd. Gilbert, AZ 85234 480.813.3637

 
            Dear: %s

            Applicant: %s 

            Reference E-mail Address: %s


            %s has volunteered to serve in a ministry at Grace Covenant Church that provides care for minors.  
            As such, they have agreed to allow us to do a background check; part of that process involves allowing us to contact the character references they have provided to us. 
            They have given us a signed authorization so that we can gather this information.


            We would be very grateful if you could reply to this e-mail and provide your responses within the e-mail questionnaire. 
            If you have any questions or concerns, please feel free to contact me.

            Sincerely,

            Jordan Smith

            Safety Committee

            Grace Covenant Church, Gilbert, Arizona

            480-494-7668

            ----------------------------------------


            How long have you known the applicant? 

 

            In what capacity do you know this person?   

 

            On a scale of 1 to 10, with 10 being very strong and 1 being not at all, how would you rate the applicant in the following areas:  (If needed, please write additional comments below)

            1.       Relates well to children/youth:   ___

            2.       Demonstrates wisdom in matters of safety: ___

            3.       Demonstrates responsibility:  ___

            4.       Prepares with diligence for assigned tasks: ___

            5.       Demonstrates personal integrity:  ___ 

            6.       Works well with others: ___

            7.       Responds well to authority:   ___

            8.       Interacts well with parents of children: ___

            To the best of your knowledge, has the applicant ever... (Please answer Y/N)    

            1.       Been convicted or pleaded guilty to any crime (other than minor traffic offenses)?  ____      

            2.       Had criminal charges and/or a civil lawsuit against him for reasons related to child abuse, negligence, or sexual misconduct?   ____   

            3.       Resigned or been dismissed from a volunteer or compensated position for child abuse, negligence, or sexual misconduct ?  ____ 

 
            Is there anything else you feel we should know about the applicant that would help us to determine his suitability as a volunteer serving children and youth?

 

            Please type in your name to serve as an electronic signature:    _________________ 

            Date:  ___________

            _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


            For Grace Covenant Church Use Only

            Grace Covenant Church Screener name: ____________________________________________

            Signature of Screener: _________________________________    Date: __________________

            Sincerely,

                Jordan Smith

            Safety Committee

            Grace Covenant Church, Gilbert, Arizona

            480-494-7668
            """ % (reference, applicant_name, email, applicant_name)
            email_text = 'Subject: {}\n\n{}'.format(subject, body)

            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(gmail_user, gmail_password)
                server.sendmail(sent_from, email, email_text)

                print 'email sent!'
            except:
                print 'Something went wrong...'

            print args
