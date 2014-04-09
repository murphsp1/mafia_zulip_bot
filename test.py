# ON HEROKU:

# request.values is:  CombinedMultiDict([ImmutableMultiDict([]), ImmutableMultiDict([('MessageSid', u'SM614f1398d69aa2fedc01e66b84fc6534'), ('ToCountry', u'US'), ('ApiVersion', u'2010-04-01'), ('ToState', u'CA'), ('ToCity', u'LOS ANGELES'), ('FromZip', u'91042'), ('NumMedia', u'0'), ('To', u'+17472335925'), ('ToZip', u''), ('SmsSid', u'SM614f1398d69aa2fedc01e66b84fc6534'), ('Body', u'Hi'), ('SmsStatus', u'received'), ('SmsMessageSid', u'SM614f1398d69aa2fedc01e66b84fc6534'), ('FromState', u'CA'), ('FromCity', u'LOS ANGELES'), ('FromCountry', u'US'), ('AccountSid', u'AC8713d29f391c6ccdc9b9942d98a407df'), ('From', u'+18185218419')])])


# ON LOCAL HOST:

#   request.values is:  CombinedMultiDict([ImmutableMultiDict([('Body', u'Heyyy there!'), ('MessageSid', u'01234567890123456789012345678901234'), ('From', u'+18185218419'), ('To', u'+17472335925'), ('NumMedia', u'0'), ('AccountSid', u'ACec58767d0255847dccc2c2834851802a'), ('SmsSid', u'01234567890123456789012345678901234')]), ImmutableMultiDict([])])
#   request.values.keys() ['Body', 'MessageSid', 'From', 'To', 'NumMedia', 'AccountSid', 'SmsSid']

import zulip
import time

to = "Mafia-bot@students.hackerschool.com"


client_1 = zulip.Client(email="John_Smith_Test-bot@students.hackerschool.com",
                      api_key="Sds3pNLrZYhQelVNh7jrjvzUxWN1SbAG")

client_2 = zulip.Client(email="Sandy_Smith_Test-bot@students.hackerschool.com",
                        api_key = "qqVIDH6gILCujojOv6UyeThLAEDKt2ei")


def send_message(client, content):
            m = {'type':'private', 'to':to, 'content':content}
            client.send_message(m)
            time.sleep(2)


send_message(client_1, 'hi')
send_message(client_2, 'hello!')


send_message(client_1, 'John')
send_message(client_2, 'Sandy')



#game begins

#mafia deliberates
"""send_message(player1[0], "let's shoot ruby")
send_message(player2[0], "yeah, let's shoot ruby")
send_message(player1[0], "we should murder ruby")
send_message(player1[0], "i agree")

"""
# mafia votes
send_message(client_1, 'kill sean')


send_message(player1[0], 'kill jill')
send_message(player2[0], 'I thought we were going after ruby??')
send_message(player1[0], 'kill ruby')
send_message(player2[0], 'kill ruby')
time.sleep(1)
send_message(player1[0], 'kill jane')
send_message(player2[0], 'kill jane')
send_message(player3[0], 'kill jane')
send_message(player4[0], 'kill jane')
send_message(player5[0], 'kill jane')
send_message(player6[0], 'kill jane')
time.sleep(1)

send_message(player1[0], 'kill jill')

send_message(player1[0], "kill Cynthia")
send_message(player5[0], 'kill Leah')
send_message(player3[0], "i am dead but speaking!")
send_message(player6[0], 'kill Leah')

thirtyfour = '01234567890123456789012345678901234'
payload = {'MessageSid': thirtyfour, 'SmsSid': thirtyfour, 'AccountSid': 'ACec58767d0255847dccc2c2834851802a',
               'From': '+18185218419', 'To': '+17472335925', 'Body': '', 'NumMedia': '0'}
r = requests.get("http://127.0.0.1:5000/restart", params=payload)

#send_message(player1[0], 'kill jane')

# time.sleep(2)
#send_message(player2[0], 'kill jane')

# time.sleep(2)
# send_message(player2[0], 'kill jane')
