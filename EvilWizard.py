import random
import time
import sys
from colorama import Fore, Style

# Used to apply text animation "typewriting" effect
def typewrite(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# creating a health bar for the player and wizard
def display_health_bar(name, health, max_health, state):
    bar_length = 20
    filled_length = int(bar_length * health / max_health)
    bar = f"{Fore.GREEN}{'█' * filled_length}{Fore.RED}{'█' * (bar_length - filled_length)}{Style.RESET_ALL}"
    if health <= max_health * 0.2:
        print(f"\n{Fore.YELLOW}{name}:\n{bar} {health}/{max_health}{Style.RESET_ALL}")
    else:
        print(f"\n{name}:\n{bar} {health}/{max_health}")
    active_states = [state_name for state_name, (active, _) in state.items() if active]
    if active_states:
        print(f"{Fore.BLUE}Status: {', '.join(active_states)}{Style.RESET_ALL}\n")

# generating a random event that impacts the battle
def random_event(player, wizard):
    events = [
        "rain",         
        "quake",         
        "blessing",      
        "curse",        
        "mana surge",    
        "meteor shower", 
    ]
    weights = [2, 2, 1, 1, 1, 2] 

    event = random.choices(events, weights=weights, k=1)[0] 

    time.sleep(1)
    print("\n" + "=" * 40)
    typewrite(f"🌟 Something is happening: {event.upper()}! 🌟")
    print("=" * 40 + "\n")
    time.sleep(1)

    if event == "rain":
        player.attack_power = max(1, int(player.attack_power * 0.8))
        wizard.attack_power = max(1, int(wizard.attack_power * 0.8))
        print("🌧️  The rain dampens everyone's weapons, reducing attack power by 20%!")
    elif event == "quake":
        print(f"🌍  A quake shakes the battlefield!")
        damage = random.randint(10, 30)
        if player.state['immune'][0]:
            print(f"{player.name} is immune and receives no damage!")
        elif player.state['armored'][0]:
            player.health = max(1, player.health - int(damage * 0.5))
            print(f"{player.name} is armored and receives {int(damage * 0.5)} damage!")
        else:
            player.health = max(1, player.health - damage)
            print(f"{player.name} takes {damage} damage!")
            
        if wizard.state['immune'][0]:
            print(f"{wizard.name} is immune and receives no damage!")
        elif wizard.state['armored'][0]:
            wizard.health = max(1, wizard.health - int(damage * 0.5))
            print(f"{wizard.name} is armored and receives {int(damage * 0.5)} damage!")
        else:
            wizard.health = max(1, wizard.health - damage)
            print(f"{wizard.name} takes {damage} damage!")
        
    elif event == "blessing":
        heal = random.randint(20, 60)
        player.health = min(player.max_health, player.health + heal)
        print(f"✨  A divine blessing heals the player for {heal} health!")
    elif event == "curse":
        player.state["poisoned"] = [True, 2]
        print("💀  A dark curse poisons the player for 2 turns!")
    elif event == "mana surge":
        wizard.attack_power = int(wizard.attack_power * 1.5)
        print("🔮  The wizard absorbs a mana surge, boosting attack power by 50%!")
    elif event == "meteor shower":
        print(f"☄️  Meteors rain down!")
        time.sleep(0.5)
        player_damage = random.randint(10, 50)
        wizard_damage = random.randint(10, 50)
        
        if player.state['immune'][0]:
            print(f"{player.name} is immune and receives no damage!")
        elif player.state['armored'][0]:
            player.health = max(1, player.health - int(player_damage * 0.5))
            print(f"{player.name} is armored and receives {int(player_damage * 0.5)} damage!")
        else:
            player.health = max(1, player.health - player_damage)
            print(f"{player.name} takes {player_damage} damage!")
            
        if wizard.state['immune'][0]:
            print(f"{wizard.name} is immune and receives no damage!")
        elif wizard.state['armored'][0]:
            wizard.health = max(1, wizard.health - int(wizard_damage * 0.5))
            print(f"{wizard.name} is armored and receives {int(wizard_damage * 0.5)} damage!")
        else:
            wizard.health = max(1, wizard.health - wizard_damage)
            print(f"{wizard.name} takes {wizard_damage} damage!")

    time.sleep(1)

# Base Character class
class Character:
    def __init__(self, name, health, attack_power, state=None):
        if state is None:
            state = {
                "zealous": [False, 0],
                "armored": [False, 0],
                "immune": [False, 0],
                "petrified": [False, 0],
                "confused": [False, 0],
                "poisoned": [False, 0],
            }
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.state = state
        self.max_health = health

    def attack(self, opponent):
        if self.handle_petrify():
            return

        elif opponent.state["immune"][0]:
            time.sleep(0.5)
            print(
                f"{self.name} attacks but {opponent.name} is immune to physical attacks and received no damage!"
            )
        else:
            if self.state["zealous"][0]:
                boosted_attack = int(self.attack_power * 1.2)
                curr_power = random.randint(boosted_attack - 5, boosted_attack + 5)
            else:
                curr_power = random.randint(
                    self.attack_power - 5, self.attack_power + 5
                )

            if opponent.state["armored"][0]:
                curr_power = int(curr_power * 0.5)

            if self.state["confused"][0]:
                self.health -= curr_power
                print(
                    f"\n{self.name} is confused and attacks himself for {curr_power} damage!"
                )
            else:
                opponent.health -= curr_power
                print(f"\n{self.name} attacks {opponent.name} for {curr_power} damage!")

        self.handle_poison()

    def heal(self):
        if self.handle_petrify():
            return
        else:
            heal_amount = 20
            actual_healed = min(heal_amount, self.max_health - self.health)
            self.health += actual_healed
            time.sleep(0.5)
            print(
                f"{self.name} healed for {actual_healed} health! Current health: {self.health}/{self.max_health}"
            )

        self.handle_poison()

    def display_stats(self):
        typewrite(
            f"{self.name}'s Stats - Health: {self.health}/{self.max_health}, Attack Power: {self.attack_power}"
        )
        active_states = [f"{state} ({turns} turns left)" for state, (active, turns) in self.state.items() if active]
        if active_states:
            print(f"\n{Fore.BLUE}Active Status Effects: {', '.join(active_states)}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.BLUE}Active Status Effects: None{Style.RESET_ALL}")

        if hasattr(self, "special_cooldown_1"):
            print(f"\n{Fore.CYAN}Special Ability 1 Cooldown: {self.special_cooldown_1} turns{Style.RESET_ALL}")
        if hasattr(self, "special_cooldown_2"):
            print(f"{Fore.CYAN}Special Ability 2 Cooldown: {self.special_cooldown_2} turns{Style.RESET_ALL}")

        self.handle_poison()


    def decrement_state_counters(self):
        for state, (active, counter) in self.state.items():
            if active and counter > 0:
                self.state[state][1] -= 1
                if self.state[state][1] == 0:
                    self.state[state][0] = False
                    time.sleep(0.5)
                    print(f"{self.name} is no longer {state}!")
                    
    def handle_poison(self):
        if self.state["poisoned"][0]:
            self.health -= 10
            print(f"{self.name} loses 10 health from poison") 
            
    def handle_petrify(self):
        if self.state["petrified"][0]:
            time.sleep(0.5)
            print(f"\n{self.name} is petrified and cannot act!")
            return True
        return False                               


# Warrior class (inherits from Character)
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=25)
        self.special_cooldown_1 = 0
        self.special_cooldown_2 = 0
        self.ultimate_available = True

    def special(self, opponent):
        if self.handle_petrify():
            return
        print("\n" + "=" * 40)
        typewrite("✨ --- Special Abilities --- ✨")
        print("=" * 40 + "\n")
        time.sleep(0.5)
        print("1. Battle Cry (Boost attack and petrify opponent)")
        time.sleep(0.5)
        print("2. Shield Slam (Stun opponent and deal damage)")
        time.sleep(0.5)
        if self.health <= self.max_health * 0.2 and self.ultimate_available:
            print(f"{Fore.CYAN}3. ULTIMATE: Armageddon{Style.RESET_ALL}")
            time.sleep(0.5)
        else:
            print(f"{Style.DIM}3. ULTIMATE: Armageddon{Style.RESET_ALL}")
            time.sleep(0.5)   
        choice = input("\nChoose a special ability: ")

        if choice == "1":
            if self.special_cooldown_1 > 0:
                time.sleep(0.5)
                print(
                    f"Battle Cry is on cooldown for {self.special_cooldown_1} more {'turn' if self.special_cooldown_1 == 1 else 'turns'}!"
                )
                return
            self.state["zealous"] = [True, 3]
            if not opponent.state["petrified"][0]:
                opponent.state["petrified"] = [True, 3]
            self.special_cooldown_1 = 6
            time.sleep(0.5)
            print(
                f"""{self.name} used Battle Cry! 
                \nIncreased attack power by 20% for {self.state['zealous'][1]} turns! 
                \n{opponent.name} is petrified for {opponent.state['petrified'][1]} turns!
                \nBattle cry is on cooldown for {self.special_cooldown_1} turns"""
            )
        elif choice == "2":
            if self.special_cooldown_2 > 0:
                time.sleep(0.5)
                print(
                    f"Shield Slam is on cooldown for {self.special_cooldown_2} more {'turn' if self.special_cooldown_2 == 1 else 'turns'}!"
                )
                return
            if not opponent.state["petrified"][0]:
                opponent.state["petrified"] = [True, 2]
            damage = random.randint(1, 35)
            opponent.health -= damage
            self.special_cooldown_2 = 4
            time.sleep(0.5)
            print(
                f"{self.name} used Shield Slam! {opponent.name} is stunned for {opponent.state['petrified'][1]} turns and took {damage} damage!"
            )
        elif choice == "3":
            if self.health > self.max_health * 0.2 or not self.ultimate_available:
                time.sleep(1)
                print("\n...not available")
            elif self.health <= self.max_health * 0.2 and self.ultimate_available:
                time.sleep(1.5)
                print(f"{Fore.CYAN}\n{self.name} let's out a deafening roar...{Style.RESET_ALL}")
                time.sleep(1)
                print(
                    f"{Fore.CYAN}\n...\"IT'S TIME FOR ARMAGEDDON!!\"{Style.RESET_ALL}"
                )
                time.sleep(0.5)
                smash = int(opponent.health * random.randint(3, 9) * 0.1)
                opponent.health -= smash
                print(f"{Fore.CYAN}\n{self.name} launches {opponent.name} in the air, jumps and SMASHES him for {smash} damage...{Style.RESET_ALL}")
                time.sleep(1)
                crash = int(opponent.health * random.randint(4, 8) * 0.1)
                opponent.health -= crash
                print(f"{Fore.CYAN}\n{opponent.name} crashes into the ground for {crash} damage!!!{Style.RESET_ALL}")
                opponent.state['immune'] = [False, 0]
                opponent.state['armored'] = [False, 0]
                opponent.state['petrified'] = [True, 1]
                self.ultimate_available = False    
        else:
            print("Invalid choice. Turn skipped.")

        self.handle_poison()

    def decrement_state_counters(self):
        if self.special_cooldown_1 > 0:
            self.special_cooldown_1 -= 1
        if self.special_cooldown_2 > 0:
            self.special_cooldown_2 -= 1
        super().decrement_state_counters()


# Mage class (inherits from Character)
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=35)
        self.special_cooldown_1 = 0
        self.special_cooldown_2 = 0
        self.ultimate_available = True

    def special(self, opponent):
        if self.handle_petrify():
            return
        print("\n" + "=" * 40)
        typewrite("✨ --- Special Abilities --- ✨")
        print("=" * 40 + "\n")
        time.sleep(0.5)
        print("1. Fireball (Ignores defense and deals high damage)")
        time.sleep(0.5)
        print("2. Arcane Shield (Reduce damage taken)")
        time.sleep(0.5)
        if self.health <= self.max_health * 0.2 and self.ultimate_available:
            print(f"{Fore.CYAN}3. ULTIMATE: Apocalypse{Style.RESET_ALL}")
            time.sleep(0.5)
        else:
            print(f"{Style.DIM}3. ULTIMATE: Apocalypse{Style.RESET_ALL}")
            time.sleep(0.5)   
        choice = input("\nChoose a special ability: ")

        if choice == "1":
            if self.special_cooldown_1 > 0:
                time.sleep(0.5)
                print(
                    f"Fireball is on cooldown for {self.special_cooldown_1} more {'turn' if self.special_cooldown_1 == 1 else 'turns'}!"
                )
                return
            damage = 40
            opponent.health -= damage
            self.special_cooldown_1 = 3
            time.sleep(0.5)
            print(
                f"""{self.name} used Fireball! {opponent.name} took {damage} damage!
                  \nFireball is on cooldown for {self.special_cooldown_1} turns"""
            )
        elif choice == "2":
            if self.special_cooldown_2 > 0:
                time.sleep(0.5)
                print(
                    f"Arcane Shield is on cooldown for {self.special_cooldown_2} more {'turn' if self.special_cooldown_2 == 1 else 'turns'}!"
                )
                return
            self.state["armored"] = [True, 2]
            self.special_cooldown_2 = 4
            time.sleep(0.5)
            print(
                f"""{self.name} used Arcane Shield! 
                \nDamage taken is reduced by 50% for {self.state['armored'][1]} turns!
                \nArcane Shield is on cooldown for {self.special_cooldown_2} turns"""
            )
        elif choice == "3":
            if self.health > self.max_health * 0.2 or not self.ultimate_available:
                time.sleep(1)
                print("\n...not available")
            elif self.health <= self.max_health * 0.2 and self.ultimate_available:
                time.sleep(1.5)
                print(f"{Fore.CYAN}\nThe time has come...{Style.RESET_ALL}")
                time.sleep(1)
                print(
                    f"{Fore.CYAN}\nTo bring forth the Apocalypse... {Style.RESET_ALL}"
                )
                damage = int(opponent.health * random.randint(5, 10) * 0.1)
                opponent.health -= damage
                time.sleep(1)
                print(
                    f"{Fore.CYAN}\n{opponent.name} was dealt {damage} damage!!{Style.RESET_ALL}"
                )
                self.ultimate_available = False
        else:
            print("Invalid choice. Turn skipped.")
            
        self.handle_poison()    

    def decrement_state_counters(self):
        if self.special_cooldown_1 > 0:
            self.special_cooldown_1 -= 1
        if self.special_cooldown_2 > 0:
            self.special_cooldown_2 -= 1
        super().decrement_state_counters()


# Archer class (inherits from Character)
class Archer(Character):
    def __init__(self, name):
        super().__init__(name, health=120, attack_power=30)
        self.special_cooldown_1 = 0
        self.special_cooldown_2 = 0
        self.ultimate_available = True

    def special(self, opponent):
        if self.handle_petrify():
            return
        print("\n" + "=" * 40)
        typewrite("✨ --- Special Abilities --- ✨")
        print("=" * 40 + "\n")
        time.sleep(0.5)
        print("1. Piercing Arrow (Ignores defense and deals high damage)")
        time.sleep(0.5)
        print("2. Volley (Hits multiple times)")
        time.sleep(0.5)
        if self.health <= self.max_health * 0.2 and self.ultimate_available:
            print(f"{Fore.CYAN}3. ULTIMATE: Asteroids{Style.RESET_ALL}")
            time.sleep(0.5)
        else:
            print(f"{Style.DIM}3. ULTIMATE: Asteroids{Style.RESET_ALL}")
            time.sleep(0.5)    
        choice = input("\nChoose a special ability: ")

        if choice == "1":
            if self.special_cooldown_1 > 0:
                time.sleep(0.5)
                print(
                    f"Piercing Arrow is on cooldown for {self.special_cooldown_1} more {'turn' if self.special_cooldown_1 == 1 else 'turns'}!"
                )
                return
            damage = 40
            opponent.health -= damage
            self.special_cooldown_1 = 4
            time.sleep(0.5)
            print(
                f"""{self.name} used Piercing Arrow!
                \n{opponent.name} took {damage} damage!
                \nPiercing Arrow on cooldown for {self.special_cooldown_1} turns"""
            )

        elif choice == "2":
            if self.special_cooldown_2 > 0:
                time.sleep(0.5)
                print(
                    f"Volley is on cooldown for {self.special_cooldown_2} more {'turn' if self.special_cooldown_2 == 1 else 'turns'}!"
                )
                return
            time.sleep(0.5)
            self.special_cooldown_2 = 5
            print(f"{self.name} used Volley!\n")
            time.sleep(1)

            damage1 = random.randint(0, 30)
            opponent.health -= damage1
            print(f"{opponent.name} took {damage1} damage!")
            time.sleep(0.5)
            damage2 = random.randint(0, 30)
            opponent.health -= damage2
            print(f"{opponent.name} took {damage2} damage!")
            time.sleep(0.5)
            damage3 = random.randint(0, 30)
            opponent.health -= damage3
            print(f"{opponent.name} took {damage3} damage!")
            time.sleep(0.5)
            print(f"Volley is on cooldown for {self.special_cooldown_2} turns")

        elif choice == "3":
            if self.health > self.max_health * 0.2 or not self.ultimate_available:
                time.sleep(1)
                print("\n...not available")
            elif self.health <= self.max_health * 0.2 and self.ultimate_available:
                time.sleep(1.5)
                print(f"{Fore.CYAN}\nThe sky suddenly darkens...{Style.RESET_ALL}")
                time.sleep(1)
                print(f"{Fore.CYAN}\nAsteroids start raining down... {Style.RESET_ALL}")
                trigger = random.randint(3, 10)
                for i in range(trigger):
                    damage = random.randint(10, 60)
                    opponent.health -= damage
                    print(
                        f"{Fore.CYAN}\n{opponent.name} hit for {damage} damage!!{Style.RESET_ALL}"
                    )
                    time.sleep(0.5)
                self.ultimate_available = False

        else:
            print("Invalid choice. Turn skipped.")
            
        self.handle_poison()    

    def decrement_state_counters(self):
        if self.special_cooldown_1 > 0:
            self.special_cooldown_1 -= 1
        if self.special_cooldown_2 > 0:
            self.special_cooldown_2 -= 1
        super().decrement_state_counters()


# Paladin class (inherits from Character)
class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=160, attack_power=20)
        self.special_cooldown_1 = 0
        self.special_cooldown_2 = 0
        self.ultimate_available = True

    def special(self, opponent):
        if self.handle_petrify():
            return
        print("\n" + "=" * 40)
        typewrite("✨ --- Special Abilities --- ✨")
        print("=" * 40 + "\n")
        time.sleep(0.5)
        print("1. Holy Strike (Deals damage and stuns)")
        time.sleep(0.5)
        print("2. Divine Shield (Blocks all damage for a turn)")
        time.sleep(0.5)
        if self.health <= self.max_health * 0.2 and self.ultimate_available:
            print(f"{Fore.CYAN}3. ULTIMATE: Archangel{Style.RESET_ALL}")
            time.sleep(0.5)
        else:
            print(f"{Style.DIM}3. ULTIMATE: Archangel{Style.RESET_ALL}")
            time.sleep(0.5)   
        choice = input("\nChoose a special ability: ")

        if choice == "1":
            if self.special_cooldown_1 > 0:
                time.sleep(0.5)
                print(
                    f"Holy Strike is on cooldown for {self.special_cooldown_1} more {'turn' if self.special_cooldown_1 == 1 else 'turns'}!"
                )
                return
            damage = random.randint(10, 50)
            opponent.health -= damage
            opponent.state["petrified"] = [True, 1]
            self.special_cooldown_1 = 4
            time.sleep(0.5)
            print(
                f"{self.name} used Holy Strike! {opponent.name} took {damage} damage and is stunned!"
            )
        elif choice == "2":
            if self.special_cooldown_2 > 0:
                time.sleep(0.5)
                print(
                    f"Divine Shield is on cooldown for {self.special_cooldown_2} more {'turn' if self.special_cooldown_2 == 1 else 'turns'}!"
                )
                return
            self.state["immune"] = [True, 2]
            self.special_cooldown_2 = 4
            time.sleep(0.5)
            print(
                f"""{self.name} used Divine Shield! 
                \n{self.name} is immune to physical damage for {self.state['immune'][1]} turn!"""
            )
        elif choice == "3":
            if self.health > self.max_health * 0.2 or not self.ultimate_available:
                time.sleep(1)
                print("\n...not available")
            elif self.health <= self.max_health * 0.2 and self.ultimate_available:
                time.sleep(1.5)
                print(f"{Fore.CYAN}\nYou have awoken the Archangel...{Style.RESET_ALL}")
                time.sleep(1)
                print(
                    f"{Fore.CYAN}\nHe charges forth with his Great Sword... {Style.RESET_ALL}"
                )
                damage = int(opponent.health * 0.8)
                opponent.health -= damage
                opponent.state["immune"] = [False, 0]
                opponent.state["armored"] = [False, 0]
                time.sleep(1)
                print(
                    f"{Fore.CYAN}\n...and deals {damage} damage to {opponent.name}!!{Style.RESET_ALL}"
                )
                self.ultimate_available = False

        else:
            print("Invalid choice. Turn skipped.")
            
        self.handle_poison()    

    def decrement_state_counters(self):
        if self.special_cooldown_1 > 0:
            self.special_cooldown_1 -= 1
        if self.special_cooldown_2 > 0:
            self.special_cooldown_2 -= 1
        super().decrement_state_counters()


# EvilWizard class (inherits from Character)
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=20)
        self.ultimate_available = True

    def regenerate(self):
        self.health += 5
        time.sleep(0.5)
        print(f"{self.name} regenerates 5 health! Current health: {self.health}")

    def barrier(self):
        if self.health <= self.max_health * 0.8:
            trigger = random.randint(1, 4)
            if trigger == 3 and not self.state["petrified"][0]:
                self.state["armored"] = [True, 3]
                self.state["immune"] = [True, 2]
                self.health += 40
                time.sleep(1)
                print(
                    f"""{Fore.LIGHTMAGENTA_EX}\n\n{self.name} activated Barrier!
                    \n{self.name} has 50% increase in defense for {self.state['armored'][1]} turns!
                    \n{self.name} is immune to physical damage for {self.state['immune'][1] - 1} turn!
                    \n{self.name} received 40 health! Current health: {self.health}{Style.RESET_ALL}"""
                )
                return True
            else:
                return False

    def curse(self, opponent):
        trigger = random.randint(1, 5)
        if trigger == 3 and not self.state["petrified"][0]:
            opponent.state["confused"] = [True, 2]
            opponent.state["poisoned"] = [True, 2]
            time.sleep(1)
            print(
                f"""{Fore.RED}\n\n{self.name} has cursed {opponent.name}!
                \n{opponent.name} is now confused and poisoned for {opponent.state['confused'][1]} turns!{Style.RESET_ALL}"""
            )
            return True
        else:
            return False
        
    def antimatter(self, opponent):
        if self.health <= self.max_health * 0.2 and self.ultimate_available:
           trigger = random.randint(1, 2)
           if trigger == 2:
               time.sleep(1.5)
               typewrite(f"{Fore.MAGENTA}\n...so...you think you're winning?...{Style.RESET_ALL}")
               time.sleep(1)
               typewrite(f"{Fore.MAGENTA}\n...I call upon...ANTIMATTER!\n{Style.RESET_ALL}")
               time.sleep(0.5)
               opponent.state['poisoned'] = [True, 3]
               opponent.state['confused'] = [True, 3]
               opponent.state['petrified'] = [True, 2]
               opponent.health = max(1, int(opponent.health * 0.5))
               print(f"{Fore.MAGENTA}\n{self.name} slashed {opponent.name}'s health in half!!{Style.RESET_ALL}")
               self.ultimate_available = False
        

# Secret random character Gilgamesh who has a chance to appear in battle to help player
class Gilgamesh(Character):
    def __init__(self, name):
        super().__init__(name, health=9999, attack_power=9999)

    @staticmethod
    def swords(opponent, player):
        if opponent.health > 0 and player.health <= player.max_health * 0.6:
            trigger = random.randint(1, 15)
            if trigger == 7:
                sword = random.randint(1, 3)
                print("\n" + "=" * 40)
                time.sleep(1)
                typewrite(f"{Fore.GREEN}\n\n*** I AM GILGAMESH ***{Style.RESET_ALL}")
                time.sleep(1)
                print("\n" + "=" * 40)
                time.sleep(0.5)
                typewrite(f"{Fore.GREEN}\n I will attack with...{Style.RESET_ALL}")
                time.sleep(1.5)
                if sword == 1:
                    typewrite(f"{Fore.GREEN}\n...the first one!{Style.RESET_ALL}")
                    time.sleep(1)
                    damage = random.randint(50, 201)
                    opponent.health -= damage
                    print(f"\nGilgamesh dealt {damage} damage to {opponent.name}!\n")
                elif sword == 2:
                    typewrite(f"{Fore.GREEN}\n...the second one!{Style.RESET_ALL}")
                    time.sleep(1)
                    damage = random.randint(5, 40)
                    opponent.health -= damage
                    print(f"\nGilgamesh dealt {damage} damage to {opponent.name}!\n")
                elif sword == 3:
                    typewrite(f"{Fore.GREEN}\n...the third one!{Style.RESET_ALL}")
                    time.sleep(1)
                    opponent.health -= 1
                    print(f"\nGilgamesh dealt 1 damage to {opponent.name}!\n")

# Menu to create character
def create_character():
    time.sleep(0.5)
    print("\n" + "=" * 40)
    typewrite("🌟 Welcome to the Character Creation Menu 🌟")
    print("=" * 40)
    typewrite("Choose your character class:\n")
    time.sleep(1)
    print("1. 🛡️   Warrior")
    print("2. 🔥  Mage")
    print("3. 🏹  Archer")
    print("4. ✨  Paladin")
    print("\n" + "=" * 40)

    while True:
        attempts = 0  
        while attempts < 3:  
            class_choice = input("Enter the number of your class choice: ")
            if class_choice in ["1", "2", "3", "4"]:
                time.sleep(0.5)
                print("\nGreat choice!\n")
                time.sleep(0.5)
                break
            else:
                attempts += 1
                time.sleep(0.5)
                print(
                    f"\n❌ Invalid choice. You have {3 - attempts} attempts remaining.\n"
                )
        else:
            time.sleep(1)
            print("\n...Defaulting to Warrior.\n")
            class_choice = "1"
        break

    name = input("Enter your character's name: ")

    if class_choice == "1":
        time.sleep(0.5)
        print(f"\nGet ready, {name}!")
        time.sleep(1)
        return Warrior(name)
    elif class_choice == "2":
        time.sleep(0.5)
        print(f"\nGet ready, {name}!")
        time.sleep(1)
        return Mage(name)
    elif class_choice == "3":
        time.sleep(0.5)
        print(f"\nGet ready, {name}!")
        time.sleep(1)
        return Archer(name)
    elif class_choice == "4":
        time.sleep(0.5)
        print(f"\nGet ready, {name}!")
        time.sleep(1)
        return Paladin(name)

# Turn-based battle system
def battle(player, wizard):
    while wizard.health > 0 and player.health > 0:
        
        if random.randint(1, 5) == 1:
            random_event(player, wizard)

        print("\n" + "=" * 40)
        display_health_bar(player.name, player.health, player.max_health, player.state)
        display_health_bar(wizard.name, wizard.health, wizard.max_health, wizard.state)
        print("=" * 40 + "\n")

        print("\n" + "=" * 40)
        print("⚔️  --- Your Turn --- ⚔️")
        print("=" * 40 + "\n")
        time.sleep(0.5)
        print("1. 🗡️   Attack")
        print("2. ✨  Use Special Ability")
        print("3. ❤️   Heal")
        print("4. 📊  View Stats")
        print("=" * 40 + "\n")

        choice = input("Choose an action: ")

        if choice == "1":
            player.attack(wizard)
        elif choice == "2":
            player.special(wizard)
        elif choice == "3":
            player.heal()
        elif choice == "4":
            player.display_stats()
        else:
            print("\n❌ Invalid choice. Lost turn.\n")

        player.decrement_state_counters()
        Gilgamesh.swords(wizard, player)

        if wizard.health > 0:
            wizard.antimatter(player)
            time.sleep(0.5)
            print("\n" + "=" * 40)
            print("🧙‍♂️ --- Wizard's Turn --- 🧙‍♂️")
            print("=" * 40 + "\n")
            if not wizard.barrier():
                wizard.regenerate()
            if not wizard.curse(player):
                wizard.attack(player)
            wizard.decrement_state_counters()

        if player.health <= 0:
            time.sleep(1)
            typewrite("\n...")
            time.sleep(1)
            print(f"\n💀 {player.name} has been defeated!")
            break

    if wizard.health <= 0:
        time.sleep(1.5)
        print(f"\n🎉 {player.name} has defeated the Dark Wizard!")

# main function that calls the core game functions
def main():
    player = create_character()
    wizard = EvilWizard("The Dark Wizard")
    battle(player, wizard)


if __name__ == "__main__":
    main()
