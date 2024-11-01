from json import load
from random import randint

from combat import combat
from player import player
from npc import *


class Location:
    def __init__(self, ID, name, desc, canTalk, available):
        self._ID = ID 
        self._name = name
        self._desc = desc
        self._canTalk = canTalk
        self._available = available

        self._contents = None

    def get_ID(self):
        return self._ID
    
    def set_name(self, name):
        self._name = name
    def get_name(self):
        return self._name
    
    def set_desc(self, desc):
        self._desc = desc
    def get_desc(self):
        return self._desc
    
    def set_canTalk(self, canTalk):
        self._canTalk = canTalk
    def get_canTalk(self):
        return self._canTalk
    
    def set_available(self, available):
        self._available = available
    def get_available(self):
        return self._available
    
class Crash_Site(Location):
    def __init__(self, ID, name, desc, canTalk, available):
        super().__init__(ID, name, desc, canTalk, available)
        self._prospector_survived = None

    def set_prospector_survived(self, prospector_survived):
        self._prospector_survived = prospector_survived
    def get_prospector_surived(self):
        return self._prospector_survived
    
    def enter(self, stage):
        print(f"You arrive at: {self.get_name()}. {self.get_desc()}")
        if stage == 0:
            self._canTalk = True
            print("Some prospectors, showing no respect for this tragedy, are already at the crash site. They've spotted you.\n")
        elif stage >= 1 and self._prospector_survived:
            self._canTalk = False
            print("The site is a lot calmer now that the prospectors have moved on.\n")
        elif stage >= 1 and not self._prospector_survived:
            self._canTalk = False
            print("The corpses of the prospectors lay still.\n")
        else:
            self._canTalk = False
            print("")

    def initiate_dialogue(self, stage): # when the code is spaghetti
        if stage >= 1:
            self._canTalk = False
            self._status = None
        else:

            with open(r"JSON\dialogue.json") as speech:
                self._contents = load(speech)
            self._status = "talk"
            self._running = True
            print(self._contents["prospectors"]["greeting"])
            while self._running:
                self._choice = int(input('''
        1. What are you doing here?
        2. You aren't supposed to be here. Leave before someone gets shot.
        3. [ROLL] You're out here, disrespecting the dead by looting off of them. I think you should leave.
'''))
                if self._choice == 1:
                    print(self._contents["prospectors"]["angry"])
                elif self._choice == 2:
                    print(self._contents["prospectors"]["threatened"])
                    self._status = combat([player, p_bob, p_lisa, p_sbot])
                    if self._status == "player_died":
                        self._running = False
                    elif self._status == "victory":
                        self._prospector_survived = False
                        self._status = "resolved"
                        self._running = False
                
                elif self._choice == 3: # Roll not yet programmed.
                    self._roll = randint(1, 10)
                    if self._roll >= 5:
                        print(self._contents["prospectors"]["roll_pass"]) 

                        self._prospector_survived = True
                        self._status = "resolved"
                        self._running = False
                    else:
                        print(self._contents["prospectors"]["roll_fail"])
                        self._status = combat([player, p_bob, p_lisa, p_sbot])
                        if self._status == "player_died":
                            self._running = False
                        elif self._status == "victory":
                            self._prospector_survived = False
                            self._status = "resolved"
                            self._running = False
                if self._status == "talk":
                    print(self._contents["prospectors"]["generic"])
                else:
                    pass
        return self._status

class New_Hope(Location):
    def __init__(self, ID, name, desc, canTalk, available):
        super().__init__(ID, name, desc, canTalk, available)

    def enter(self, stage):
        print(f"You arrive at: {self.get_name()}. {self.get_desc()}")
        if stage == 1:
            self._canTalk = True
            print("You decide to enter The New Hope Central. It's a rather quiet bar, with a band playing smooth jazz and the general atmosphere being calm.")
            print("Though in town such as this, that shouldn't be of any surprise. The bartender's grin is welcoming, albeit creepy.")
        
    
crashsite = Crash_Site(1, "Crash site",
                    "Crash site of the IPNS Whistler, an ageing Sol-class observation ship. Fires can be seen all around the crash site. There were definitely no survivors here.",
                    False, True)

new_hope = New_Hope(2, "New Hope",
                    r"A small town with all amenities necessary for its survival, including a bar, named 'The New Hope Central'. ",
                    False, False)