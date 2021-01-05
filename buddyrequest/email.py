import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def mail(name_partner, netID_user,netID_partner, user=False):

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your New Workout Buddy"

    # sent_email = netID_user + "@princeton.edu"
    # contact = netID_partner + "@princeton.edu"
    sent_email = 'vkonuru' + "@princeton.edu"
    contact = 'vkonuru' + "@princeton.edu"

    tiger_gainz_pass = os.environ.get("EMAIL_PASSWORD")
    tiger_gainz_email = "no.reply.tigergainz@gmail.com"

    if user == True:

        text = f'''\
        Hi!

        We are so excited to present you with your new workout partner, {name_partner}! You can contact them via email: {contact}

        Happy exercising,
        TigerGainz'''


    else:

        text = f'''\
        Hi!

        We are sending a confirmation email regarding your new workout partner, {name_partner}! You can contact them via email: {contact}

        Happy exercising,
        TigerGainz'''

    message.attach(MIMEText(text, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(tiger_gainz_email, tiger_gainz_pass)
        s.sendmail(tiger_gainz_email, sent_email, message.as_string())
        s.quit()
