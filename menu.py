from player import player, inv
from locations import crashsite

# from combat import combat ???
class Menu:
    def __init__(self):
        self._MAIN = '''What would you like to do?:
    1. Talk
    2. Attack
    3. Open inventory
    4. Board fighter
    9. Save and exit
'''
        self._inMain = True
        self._inInv = False
        self._inFighter = False
        self._dialogue_outcome = None
        self._location = ""
        self._location_desc = ""

        self._NO_TALK = "There's nobody here to talk to."


    def location_stage_handling(self, location):
        if location == 1:
            self._location = crashsite.get_name()
            self._location_desc = crashsite.get_desc()
        else:
            print("Error - Invalid location data")

    def dialogue(self, location, stage):
        if location == 1 and not crashsite.get_canTalk(): # crash site
            print(self._NO_TALK)
            self._dialogue_outcome = "goodbye"
        elif location == 1 and crashsite.get_canTalk():
            self._dialogue_outcome = crashsite.initiate_dialogue(stage)
    
    def check_dialogue_outcome(self):
        if self._dialogue_outcome == "goodbye":
            pass
        elif self._dialogue_outcome == "resolved":
            self._dialogue_outcome = "advance"
        elif self._dialogue_outcome == "placeholder":
            print("Still under construction. Whoops!")
        else:
            # print("Summin ain't right.")
            pass
        self._inMain = False
    
    def inventory(self):
        self._inInv = True
        while self._inInv:
            print(f'''\n{player.get_wpn()} - {player.get_wpnDesc()} It deals {player.get_atk()} damage and holds {player.get_clipSize()} bullets.
{player.get_amr()} - {player.get_amrDesc()} It provides {player.get_dfe()} points of protection.
{inv.get_SLOT1()} - {inv.get_DESC1()} You have {inv.get_count1()}.
{inv.get_SLOT2()} - {inv.get_DESC2()} You have {inv.get_count2()}.
{inv.get_SLOT3()} - {inv.get_DESC3()} You have {inv.get_count3()}.

1. Use healthshot
9. Exit inventory menu''')
            self._choice = int(input())
            if self._choice == 1 and inv.get_count1() > 0:
                if player.get_damage() == player.get_hp():
                    print("You are already at max HP!")
                else: 
                    print(f"You restore 10 hitpoints. You currently have {player.get_damage()} hitpoints.")
                    player.deal_damage(-10)
                    inv.add_SLOT1(-1)
            elif self._choice == 1 and inv.get_count1() <= 0:
                print("You have no healthshots.")
            elif self._choice == 9:
                self._inInv = False
    
    def fighter(self, stage):
        self._inFighter = True
        while self._inFighter:
            print(f"You are at: {self._location}")
            print(self._location_desc)
            print("Current objective:")
            if stage == 0:
                print('''Find out the fate of the Intragalactic Peacekeeping Navy Ship Whistler.

Using what little info the IPF provided me, I have to figure out what the hell is going on here. Bizzarly, there are prospectors already on-site.
Salvation isn't a rich colony by any means. But they're sure as shit not this poor to loot of the corpses of those who are protecting them.''')
            
            elif stage == 1 and crashsite.get_prospector_surived():
                print('''Head to the nearby town of New Hope for more information.
                      
The prospectors have (reluctantly) left in peace, but I have no info on what to do next. Perhaps the denizens of New Hope will have more information for me.
If there's a bar, that'll be as good a place as any. I could certainly use the drink after this.''')
            elif stage == 1 and not crashsite.get_prospector_surived():
                print('''Head to the nearby town of New Hope for more information.
                      
I've killed the prospectors, but I have no info on what to do next. Perhaps the denizens of New Hope will have more information for me.
If there's a bar, that'll be as good a place as any. I could certainly use the drink after this.''')

            elif stage == 1:
                print('''Head to the nearby town of New Hope for more information.
                      
I've dealt with the prospectors, but have no info on what to do next. Perhaps the denizens of New Hope will have more information for me.
If there's a bar, that'll be as good a place as any. I could certainly use the drink after this.''')
            
            else:
                print(" << Nothing. Await further assignment >>")

            self._inFighter = False

    def main_menu_runtime(self, location, stage):
        self._inMain = True
        self._choice = 0

        self.location_stage_handling(location)
        
        while self._inMain:
            if player.get_damage() <= 0 or self._dialogue_outcome == "player_died": # Checks for death 
                self._inMain = False
                return "player_died"
            if self._dialogue_outcome == "advance":
                self._dialogue_outcome = None
                self._inMan = False
                return "advance"
            print(self._MAIN)
            self._choice = int(input())
            if self._choice == 1:
                self.dialogue(location, stage)
                self.check_dialogue_outcome()
            elif self._choice == 2:
                print(f"You point your {player.get_wpn()} at your targets, but shake as you forget your training. You get gunned to death instead.")
                player.deal_damage(player.get_damage())
            elif self._choice == 3:
                self.inventory()
            elif self._choice == 4:
                self.fighter(stage)
            elif self._choice == 9:
                self._inMain = False
                return "exit"
            

main_menu = Menu()