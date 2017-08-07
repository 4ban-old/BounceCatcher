#! /usr/bin/python
# -*- coding: UTF-8 -*-
# Have to install gmail from sourcecode

from gmail import Gmail
import re

# Settings
login = 'your email' # Login for gmail account
password = 'password' # Password for gmail account
template = ['Rejected','Undeliverable','Failure', 'Delay'] # Stop words to search bounces
safeemail = [login,'mailer-daemon@googlemail.com'] # email that shouldn't be in the final list
# The big number of message in inbox can stuck your OS. Python eat a lot of RAM.
rd = True # Param to get unread only messages. If you want to get all mesagges put it False
st = False # Star message. If you want to star message put it True
dl = False # Delete message. If you want to delete message put it True

g = Gmail()
g.login(login, password)
# there are a lot of parameters for filtering here https://github.com/charlierguo/gmail
mails = g.inbox().mail(unread=rd) # Get emails

with open('bounced.txt', 'a') as result:
	for mail in mails:
		res = ''
		mail.fetch()
		if any(tmp in mail.subject for tmp in template):
			try:
				res = mail.headers['X-Failed-Recipients']
				print 'EMAIL:', res, '\033[32m', mail.fr, '\033[0m'
				result.write(res+'\n')
				if st:
					mail.star()
				if dl:
					mail.delete()
				continue
			except KeyError:
				res = re.findall(r'\b[\w.-]+?@\w+?\.\w+?\b', mail.body)
				if res:
					for x in safeemail:
						while x in res:
							res.remove(x)
					res = list(set(res))
					print 'EMAIL:', res, '\033[34m', mail.fr, '\033[0m'
					for x in res:
						result.write(x+'\n')
					if st:
						mail.star()
					if dl:
						mail.delete()
					continue
				print 'EMAIL: no \033[31m',mail.fr,'\033[0m'
g.logout()





