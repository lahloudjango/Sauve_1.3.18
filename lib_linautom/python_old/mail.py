# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Module d'enrobage d'envoie de mail
"""
import smtplib
import datetime
import types


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import charset

__author__ = "Charly GONTERO"
__date__ = "2016-02-08 19:48:13"
__version__ = 1.1
__credits__ = """
 *  mail.py
 *
 *  Copyright 2011 Charly GONTERO
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 *  MA 02110-1301, USA.
"""

VERSION = __version__
def version():
	return __version__

def whatisit(a):
	print type(a)
	print dir(a)
	print a

class Mail(object):

	def __init__(self, mail):

		charset.add_charset('utf-8', charset.SHORTEST, None, "utf-8")

		self.envelope = MIMEText(mail, "plain", "utf-8")

		self.envelope["Date"] = datetime.datetime.now().strftime("%a, %d %b %Y %X %Z") #Sat, 04 Oct 2014 11:03:31 +0200
		self.envelope["X-Mailer"] = "Python mailler"
#		self.envelope["User-Agent"] = "Python mailler"
		self.list_to = []
		self.list_cc = []
		self.list_bcc = []

#		self.envelope["Resent-Date"] = "Test mail python"
#		self.envelope["Resent-From"] = "Test mail python"
#		self.envelope["Resent-Sender"] = "Test mail python"

	def from_(self, a_mail):
		self.envelope["From"] = a_mail

	def sender(self, a_mail):
		self.envelope["Sender"] = a_mail

	def reply_to(self, a_mail):
		self.envelope["Reply-To"] = a_mail

	def to(self, list_mail):
		if type(list_mail) == types.TupleType or type(list_mail) == types.ListType:
			self.list_to = list_mail
			self.envelope["To"] = ",".join(list_mail)
		elif type(list_mail) == types.UnicodeType or type(list_mail) == types.StringTypes:
			self.list_to = list_mail.split(",")
			self.envelope["To"] = list_mail
		else:
			raise ValueError("le distinataire doit être une liste ou une chaine de caractère")

	def cc(self, list_mail):
		if type(list_mail) == types.TupleType or type(list_mail) == types.ListType:
			self.list_cc = list_mail
			self.envelope["Cc"] = ",".join(list_mail)
		elif type(list_mail) == types.UnicodeType or type(list_mail) == types.StringTypes:
			self.list_cc = list_mail.split(",")
			self.envelope["Cc"] = list_mail
		else:
			raise ValueError("le distinataire doit être une liste ou une chaine de caractère")

	def bcc(self, list_mail):
		if type(list_mail) == types.TupleType or type(list_mail) == types.ListType:
			self.list_bcc = list_mail
			self.envelope["bcc"] = ",".join(list_mail)
		elif type(list_mail) == types.UnicodeType or type(list_mail) == types.StringTypes:
			self.list_bcc = list_mail.split(",")
			self.envelope["bcc"] = list_mail
		else:
			raise ValueError("le distinataire doit être une liste ou une chaine de caractère")

	def in_reply_to(self, a_mail):
		self.envelope["In-Reply-To"] = a_mail

	def references(self, text):
		self.envelope["References"] = text

	def subject(self, text):
		self.envelope["Subject"] = text

	def comments(self, text):
		self.envelope["Comments"] = text

	def keywords(self, text):
		self.envelope["Keywords"] = text

	def send(self, smtp, expediteur=None, user=None, password=None, starttls=False):
		smtp_conn = smtplib.SMTP(smtp)
		if starttls == True:
			smtp_conn.starttls()
		if user != None:
			smtp_conn.login(user, password)
		if expediteur == None:
			if self.envelope["Sender"] == None or self.envelope["Sender"] == "":
				self.envelope["Sender"] = expediteur 
			else:
				expediteur = self.envelope["Sender"]
		if len(self.list_to) > 0:
			smtp_conn.sendmail(expediteur, self.list_to, self.envelope.as_string())
		if len(self.list_cc) > 0:
			smtp_conn.sendmail(expediteur, self.list_cc, self.envelope.as_string())
		if len(self.list_bcc) > 0:
			smtp_conn.sendmail(expediteur, self.list_bcc, self.envelope.as_string())
		smtp_conn.quit()

class MailAttach(Mail):

	def __init__(self, mail):

		charset.add_charset('utf-8', charset.SHORTEST, None, "utf-8")

		self.envelope = MIMEMultipart("plain", "utf-8")

		self.envelope["Date"] = datetime.datetime.now().strftime("%a, %d %b %Y %X %Z") #Sat, 04 Oct 2014 11:03:31 +0200
		self.envelope["X-Mailer"] = "Python mailler"
#		self.envelope["User-Agent"] = "Python mailler"
		self.list_to = []
		self.list_cc = []
		self.list_bcc = []

#		self.envelope["Resent-Date"] = "Test mail python"
#		self.envelope["Resent-From"] = "Test mail python"
#		self.envelope["Resent-Sender"] = "Test mail python"

		self.envelope.attach(MIMEText(mail, "plain", "utf-8"))


	def attach(self, fichier):
		import email
		import os

		part = MIMEBase("application", "octet-stream; name=\"%s\"" %(os.path.basename(fichier)))
		part.set_payload(open(fichier, "rb").read())
		email.encoders.encode_base64(part)
		part.add_header("Content-Disposition", "attachment; filename=\"%s\"" %(os.path.basename(fichier)))
		self.envelope.attach(part)


	def attach_pdf(self, fichier):
		import email
		import os

		part = MIMEBase("application", "pdf; name=\"%s\"" %(os.path.basename(fichier)))
		part.set_payload(open(fichier, "rb").read())
		email.encoders.encode_base64(part)
		part.add_header("Content-Disposition", "attachment; filename=\"%s\"" %(os.path.basename(fichier)))
		self.envelope.attach(part)


	def attach_text(self, fichier, image_type=None):
		import email
		import os

		if image_type == None:
			part = MIMEBase("text", "plain; name=\"%s\"" %(os.path.basename(fichier)))
		else:
			part = MIMEBase("text", "%s; name=\"%s\"" %(image_type, os.path.basename(fichier)))
		part.set_payload(open(fichier, "rb").read())
		email.encoders.encode_7or8bit(part)
		part.add_header("Content-Disposition", "attachment; filename=\"%s\"" %(os.path.basename(fichier)))
		self.envelope.attach(part)


	def attach_html(self, fichier):
		import email
		import os

		part = MIMEBase("text", "html; name=\"%s\"" %(os.path.basename(fichier)))
		part.set_payload(open(fichier, "rb").read())
		email.encoders.encode_quopri(part)
		part.add_header("Content-Disposition", "attachment; filename=\"%s\"" %(os.path.basename(fichier)))
		self.envelope.attach(part)

	def attach_image(self, fichier, image_type):
		import email
		import os

		part = MIMEBase("image", "%s; name=\"%s\"" %(image_type, os.path.basename(fichier)))
		part.set_payload(open(fichier, "rb").read())
		email.encoders.encode_base64(part)
		part.add_header("Content-Disposition", "attachment; filename=\"%s\"" %(os.path.basename(fichier)))
		self.envelope.attach(part)

if __name__ == '__main__':

#	piece_jointe_text = r"/tmp/test.py"
#	piece_jointe_png = r"/home/gontero/.cache/mozilla/firefox/dihu8i3s.default/thumbnails/d4fd8e9d0e022695dcc8ae87cfebf4af.png"

	m = MailAttach("Mail de test\nce message êst ën ünïcôde … … !!")
	m.from_("Application_stockparis@takasago.com")
	m.reply_to("charly.gontero@linautom.fr")
#	m.to(["yanick_soufflet@takasago.com",])
	m.to(["charly.gontero@linautom.fr",])
	m.subject("test mail python … ütf-8")

#	m.attach_image(piece_jointe_png, "png")
#	m.attach_text(piece_jointe_text, "py")

	whatisit(m.envelope)
	whatisit(m.envelope["Sender"])
#	m.send("smtp.laposte.net", "charly.gontero@laposte.net", "charly.gontero", "1Addyson", starttls=True)
#	m.send("smtp.laposte.net", "charly.gontero@laposte.net", starttls=True)
#	m.send("par-srv-cas01.eu.takasago.com", "Application_stockparis@takasago.com", "Alpar", "Takasago!2016", starttls=True)
#	m.send(smtp="smtp.laposte.net", expediteur="Application_stockparis@takasago.com", user="Alpar", password="Takasago!2016", starttls=True)
	m.send(smtp="par-srv-cas01.eu.takasago.com", expediteur="Application_stockparis@takasago.com", user=None , password=None, starttls=False)

