import random
import math
import zulip

class Mafia:
    class Player:
        def __init__(self, number):
            self.mafia = False
            self.alive = True
            self.number = number
            self.name = ''
            self.ballot = ''

        def add_name(self, name):
            self.name = name

        def __str__(self):
            return self.name


    def __init__(self, client):
        self.debug = True
        self.client = client
        self.start_game()


    def start_game(self):
        #self.game_id = game_id
        self.player_count = 0
        self.to_kill = ''
        self.state = 'join'
        self.player_list = []
        self.min_players = 2



    def send_text(self, number, text_string):
        '''
        This function is meant for messaging directly to one player
        '''
        print "***MSG: ", text_string, "TO: ", number

        self.client.send_message({'type':'private',
                                'to':number,
                                'content':text_string})


    def send_group(self, group_str, announcement):
        '''
        This function fires off private messages to everyone in the specified group
        Not a fan of the implementation because it depends on the communications
        layer.
        '''
        if group_str == 'mafia':
            group = [player for player in self.player_list if player.mafia]
        elif group_str == 'innocents':
            group = [player for player in self.player_list if not player.mafia]
        else:
            group = self.player_list

        print "**TO GRP: ", group_str, " MSG: ", announcement

        for person in group:
            m = {'type':'private', 'to':person.number, 'content':announcement}
            self.client.send_message(m)


    def get_number_alive(self):
        alive = [p for p in self.player_list if p.alive]
        return len(alive)


    def get_mafia_names(self):
        mafia_names = [player.name for player in self.player_list if player.mafia]
        return mafia_names


    def get_player(self, number):
        p = [player for player in self.player_list if player.number == number]
        if p is not None:
            p = p[0]
        return p


    def tally_votes(self, group_str):
        if group_str == 'mafia':
            mafia_list = [player for player in self.player_list if (player.mafia and player.alive)]
            votes = set()
            for mafioso in mafia_list:
                if mafioso.ballot == '':
                    return False
                else:
                    votes.add(mafioso.ballot)
            if len(votes) != 1:
                self.send_group('mafia', "You must reach consensus before someone is killed.")
                return False
            else:
                self.to_kill = votes.pop()
                return True
        elif group_str == 'all':
            votes = []
            alive_people = [player for player in self.player_list if player.alive]
            for player in alive_people:
                if player.ballot == '':
                    return False
                else:
                    votes.append(player.ballot)
            minimum_votes = math.ceil(self.get_number_alive() / 2.0)
            for accused in votes:
                if votes.count(accused) >= minimum_votes:
                    self.to_kill = accused

                    return True
                    # TODO: send something to tell them to keep voting
            self.send_group('all',
                            'No one has a majority of votes to be executed. You can change your vote. Keep voting.')
            return False


    def check_end_condition(self):
        mafiosos = [player for player in self.player_list if (player.mafia and player.alive)]
        num_mafiosos = len(mafiosos)
        innocents = [player for player in self.player_list if (not player.mafia and player.alive)]
        num_innocents = len(innocents)
        if num_innocents > 0 and num_mafiosos > 0:
            return False
        elif num_innocents == 0 and num_mafiosos > 0:
            self.mafia_wins()
            return True
        elif num_mafiosos == 0 and num_innocents > 0:
            self.innocents_win()
            return True
        else:
            return False


    def mafia_wins(self):
        self.send_group('all', 'Mafia wins.')
        mafia_string = " ".join([x.capitalize() for x in self.get_mafia_names()])
        self.send_group('all', "Here's who was in the mafia: " + mafia_string)
        self.state = 'end'


    def innocents_win(self):
        self.send_group('all', 'The mafia was defeated!')
        self.state = 'end'


    def kill_player(self):
        if self.to_kill != '':
            player = [player for player in self.player_list if player.name == self.to_kill][0]
            player.alive = False


    def setup_game(self):
        #send instructions (help)
        self.prune()
        self.help_message('all')
        self.assign_groups()
        self.begin_night()
        self.state = 'night'


    def join(self, word_list, number):
        text_string = ''
        if self.player_count >= self.min_players and 'begin' in word_list:
            self.setup_game()
        else:
            if 'begin' in word_list:
                text_string = 'Not enough players yet'
            else:
                if not number in [player.number for player in self.player_list]:
                    text_string = "Welcome, what's your name?"
                    self.player_list.append(self.Player(number))
                else:
                    name = word_list[0]
                    if not name in [player.name for player in self.player_list]:
                        this_player = [player for player in self.player_list if player.number == number]
                        this_player[0].add_name(name)
                        self.player_count += 1
                        text_string = "Welcome to the game, " + name.capitalize() + "."
                        if self.player_count >= self.min_players:
                            self.send_group('all',
                                            "Sufficient players have joined the game, text 'begin' if everyone's here.")
                    else:
                        text_string = "We already have someone named that, pick a different name."
                self.send_text(number, text_string)


    def begin_night(self):
        self.kill_player()
        if self.to_kill != '':
            self.send_group('all', "The group has executed: " + self.to_kill)
        self.to_kill = ""
        if self.check_end_condition():
            return
        self.clear_ballots()
        self.send_group('all', "the night has begun.")
        self.send_group('mafia', "During the night, you can converse in secret.")
        self.send_group('mafia', "Text 'kill' and a valid name to cast your vote.")
        to_kill = [player for player in self.player_list if player.mafia == False and player.alive == True]
        kill_string = ''
        for potential_victim in to_kill:
            kill_string += potential_victim.name.capitalize() + "\n"
        self.send_group('mafia', "Here is who you may kill: " + kill_string)
        #self.state = 'night'
        #print "in begin night"


    def night(self, text_list, number):
        player = [player for player in self.player_list if player.number == number]
        if player[0].mafia and player[0].alive:
            self.mafia_night(text_list, player[0])
            pass
        else:
            self.send_text(number, "it's night time... go back to sleep...")


    def mafia_night(self, text_list, mafioso):
        self.send_group('mafia', mafioso.name.capitalize() + " says: " + " ".join(text_list))
        if 'kill' in text_list:
            to_kill = text_list[1]
            if to_kill.lower() in [player.name for player in self.player_list if not player.mafia and player.alive]:
                if mafioso.ballot != '':
                    self.send_text(mafioso.number,
                                   "You have changed your voted from: " + mafioso.ballot + " to: " + to_kill)
                mafioso.ballot = to_kill
            else:
                self.send_text(mafioso.number, "Not a valid name of someone to kill: " + to_kill)
            if self.tally_votes('mafia'):
                self.begin_day()


    def begin_day(self):
        self.kill_player()
        self.send_group('all', self.to_kill.capitalize() + " was killed last night.")
        self.to_kill = ""
        if self.check_end_condition():
            return
        self.clear_ballots()
        self.send_group('all', "While everyone was sleeping, someone else died. Time to accuse the possible mafiosos.")
        self.state = "day"


    def day(self, text_list, number):
        this_player = self.get_player(number)
        if this_player.alive:
            self.send_group('all', this_player.name.capitalize() + " says: " + " ".join(text_list))
            if 'kill' in text_list:
                to_kill = text_list[1]
                if to_kill.lower() in [player.name for player in self.player_list if player.alive]:
                    if this_player.ballot != '':
                        self.send_text(this_player.number,
                                       "You have changed your vote from" + this_player.ballot.capitalize() + " to " + to_kill.capitalize())
                    this_player.ballot = to_kill
                else:
                    self.send_text(this_player.number,
                                   "Not a valid name of someone in to kill: " + to_kill.capitalize())
                if self.tally_votes('all'):
                    self.begin_night()
                    self.state = 'night'


    def operator(self, msg):
        number = msg['sender_email']
        print number
        if msg['sender_email'] != 'Mafia-bot@students.hackerschool.com':
            text_list = msg['content']
            text_list = text_list.lower().split(' ')
            if self.state == 'join':
                self.join(text_list, number)
            elif self.state == 'night':
                self.night(text_list, number)
            elif self.state == 'day':
                self.day(text_list, number)
            elif self.state == 'end':
                self.restart_game()
            else:
                print "error"


    def assign_groups(self):
        if not self.debug:
            random.shuffle(self.player_list)
        total_players = self.player_count
        number_mafia = self.player_count / 3
        if number_mafia == 0:
            number_mafia = 1
        for i, player in enumerate(self.player_list):
            if i < number_mafia:
                player.mafia = True
                print player.name, " is in the mafia."
        self.send_group('mafia', "looks like you're in the mafia!")
        self.send_group('innocents', "what mafia????")


    def help_message(self, who_to_send):
        help_string = "Here's a bunch of introductory instructions."
        if who_to_send == 'all':
            self.send_group('all', help_string)
        else:
            self.send_text(who_to_send.number, help_string)


    def prune(self):
        self.player_list = [player for player in self.player_list if player.name != '']


    def clear_ballots(self):
        print "in clear ballots **"
        for player in self.player_list:
            player.ballot = ''



