import zulip
import time

'''
This script is a half baked test deploying two zulip bots but requires a human
player as well
'''


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


"""
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
"""

