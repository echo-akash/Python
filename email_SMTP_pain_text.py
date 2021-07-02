# import necessary packages
 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib,ssl
 
# create message object instance
msg = MIMEMultipart()
 
 
message = "Hello World Message"

 
# setup the parameters of the message
password = "***********"
msg['From'] = "email@email.com"
msg['To'] = "email@email.com"
msg['Subject'] = "SMTP Email Check"
 
# add in the message body
msg.attach(MIMEText(message, 'plain'))
 
#create server
server = smtplib.SMTP_SSL('smtp.hostinger.com', 465)

 
# Login Credentials for sending the mail
server.login(msg['From'], password)
 
 
# send the message via the server.
server.sendmail(msg['From'], msg['To'], msg.as_string())
 
server.quit()
 
print ("successfully sent email")
