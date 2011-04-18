import smtplib
import traceback
from email.mime.text import MIMEText

""" Send email using Gmail. This is used to notify operations of events. """

class Gmailer:
	user = None
	password = None

	def __init__(self, user, password):
		self.user = user
		self.password = password

	def send_gmail(self, recipients, subject, message):
		''' Send email using Gmail. Prints out on error, but doesn't fail otherwise. '''

		try:
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.ehlo()
			server.starttls()
			server.login(self.user, self.password)

			msg = MIMEText(message)
			msg['Subject'] =  subject
			msg['From'] = self.user 
			msg['To'] = ','.join(recipients)

			server.sendmail(self.user, recipients, msg.as_string())
			server.quit()
		except:
			trace = traceback.format_exc()
			print trace
