# import necessary packages
 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib,ssl
 
# create message object instance
msg = MIMEMultipart()
 
 
message = "Hello World"

# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nmyclassroom.online"
html = """\

<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
<style>
body {
  background-color: black;
  text-align: center;
  color: white;
  font-family: Arial, Helvetica, sans-serif;
}
</style>
</head>
<body>

<h1>This is a Heading</h1>
<p>This is a paragraph.</p>
<p>Edit the code in the window to the left, and click "Run" to view the result.</p>
<img src="avatar.png" alt="Avatar" style="width:200px">

</body>
</html>


"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

 
# setup the parameters of the message
password = "**********"
msg['From'] = "email@address.com"
msg['To'] = "email@address.com"
msg['Subject'] = "SMTP Email Check"
 
 
#create server
server = smtplib.SMTP_SSL('smtp.hostinger.com', 465)

 
# Login Credentials for sending the mail
server.login(msg['From'], password)
 
 
# send the message via the server.
server.sendmail(msg['From'], msg['To'], msg.as_string())
 
server.quit()
 
print ("successfully sent email")
