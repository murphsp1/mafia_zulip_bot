import sys
import zulip
import mafia


# Keyword arguments 'email' and 'api_key' are not required if you are using ~/.zuliprc
client = zulip.Client(email="Mafia-bot@students.hackerschool.com",
                      api_key="ynj6gS3cxyMyGX25lYkLopBUqhOILjEK")


if __name__ == '__main__':
    #Create new Mafia game
    game = mafia.Mafia(client)
    client.call_on_each_message(lambda msg: game.operator(msg) )