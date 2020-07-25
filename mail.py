import smtplib, ssl
from email.mime.text import MIMEText

def mail (name, netID, user=False):


    sent_email = netID + "@princeton.edu"

    tiger_gainz_pass = "WorkoutTinder123"
    tiger_gainz_email = "no.reply.tigergainz@gmail.com"

 
    if user==False:

        text = f'''\
        Hi!

        We are so excited to present you with your new workout partner, {name}! You can contact them via email: {sent_email}


        Happy exercising,

        TigerGainz'''
        
        
     else:
        
        text = f'''\
        Hi!

        We are sending a confirmation email regarding your new workout partner, {name}! You can contact them via email: {sent_email}


        Happy exercising,

        TigerGainz'''
        
        
    message.attach(MIMEText(text, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(tiger_gainz_email, tiger_gainz_pass)
        s.sendmail(tiger_gainz_email, sent_email, message.as_string())
        s.quit()

#import data

    #import names of both people that got matched
    

