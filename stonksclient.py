import smtplib, ssl
from email.message import EmailMessage

att = {
    "sms" : "{}@txt.att.net",
    "mms" : "{}@mms.att.net"
}
tmobile = {
    "sms" : "{}@tmomail.net",
    "mms" : "{}@tmomail.net"
}
verizon = {
    "sms" : "{}@vtext.com",
    "mms" : "{}@vzwpix.com"
}
sprint = {
    "sms" : "{}@messaging.sprintpcs.com",
    "mms" : "{}@pm.sprint.com"
}

def send_email(stock):
    timestamp, symbol, price, threshold = stock
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "@gmail.com"  #WARNING: Turn Allow less secure apps to ON. Be aware that this makes it easier for others to gain access to your account.
    phone_number = ""
    receiver_email = att["sms"].format(phone_number)  # Enter receiver address
    password = ""
    message = format_message(timestamp, symbol, price, threshold)

    email = EmailMessage()
    # email.set_content(message + "\n\nPlease do not reply to this email. Messages sent to this email address are not monitored.")
    email['Subject'] = "{}: {}".format(symbol, price)
    email['From'] = sender_email
    email['To'] = receiver_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(email)


def format_message(timestamp, symbol, price, threshold):
    p = "{:.2f}".format(price)
    t = "{:.2f}".format(threshold)
    action = "dropped below" if price < threshold else "risen above"
    return "\n{timestamp} {symbol}: ${p}\n{symbol} has {action} ${t}.".format(timestamp, symbol, action, p, t)