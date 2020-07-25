<<<<<<< HEAD
import smtplib, ssl

def mail (name, netID, user=False):

    sent_email = "el25" + "@princeton.edu"

    tiger_gainz_pass = "WorkoutTinder123"
    tiger_gainz_email = "no.reply.tigergainz@gmail.com"

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()

    s.login(tiger_gainz_email, tiger_gainz_pass)

    if user==False:
        message = f'''\
        Subject: Your New Workout Buddy


        Hi!

        We are so excited to present you with your new workout partner, {name}! You can contact them via email: {sent_email}


        Happy exercising,

        TigerGainz'''


    else:
        message = f'''\
        Subject: Your New Workout Buddy


        Hi!

        We are sending a confirmation email regarding your new workout partner, {name}! You can contact them via email: {sent_email}


        Happy exercising,

        TigerGainz'''


    s.sendmail(tiger_gainz_email, sent_email, message)
    s.quit()

#import data

    #import names of both people that got matched
=======
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def mail(name, netID, user=False):

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your New Workout Buddy"

    sent_email = netID + "@princeton.edu"
    tiger_gainz_pass = "WorkoutTinder123"
    tiger_gainz_email = "no.reply.tigergainz@gmail.com"

    if user == False:

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
>>>>>>> 9130ac83786c827af0a8cb38babd4ed333f70b85
