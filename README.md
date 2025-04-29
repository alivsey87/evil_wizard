
# Defeat The Evil Wizard

---
---

### Welcome to my Defeat The Evil Wizard game!!

---
---

## TABLE OF CONTENTS

1. [UI](#1-ui)

2. [Character](#2-character)

3. [Warrior](#3-warrior)

4. [Mage](#4-mage)

5. [Archer](#5-archer)

---
---

## 1. UI

The UI consists of a main create character menu and options during battle.

### Character Creation

#### create_character()

This function defines the menu and functionality for selecting a character class and naming the character:

```py
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
```

I've included some validation to allow the user 3 chances to select a valid character class, otherwise defaulting to the Warrior class. I used the [time.sleep()] to make the process more immersive.

### Battle System

#### battle()

This is where the action happens!

```py
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
```

The player enters into the battle arena with the Evil Wizard. Here the options for battle are displayed along with the [health bar] for the player and the wizard. The turn-based system stays active as long as the health of the player and wizard are above 0. I've included [Random events] and a secret character [Gilagamesh] who appears randomly. The options available for the player during battle are [Attack](#attack), [Special Ability], [Heal] and [View Stats] which are defined in the [Character](#2-character) base class and the [Warrior], [Mage], [Archer] and [Paladin] classes.

---
---

## 2. Character

This is the base character class that includes the core functionality for all the characters in the game.

```py
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
```

The Character class has 5 properties: `name`, `health`, `attack_power` and `state`. `state` is a dictionary that manages the state of each character, keeping the state name as a key, and a list value containing a boolean and integer that indicates if the state is active and for how long.

### States

#### - Zealous

- character is given a boost of strength

#### - Armored

- character receives 50% less damage

#### - Immune

- character is immune to physical damage

#### - Petrified

- character is unable to perform any action other then [View stats]

#### - Confused

- character will inflict damage on themselves if using [Attack](#attack)

#### - Poisoned

- character receives 10 damage after every action

### attack()

This handles the Attack option for both the player and wizard:

```py
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
```

When called, first checks if character is [petrified](#--petrified) with [handle_petrify()](#handle_petrify). It then proceeds to see if the opponent is [immune](#--immune) to physical attacks. Next the damage for the attack is calculated based on the character's `attack_power` and whether they are [zealous](#--zealous) or not. The final output is a random number generated from the range of +-5 that damage. The method then checks if the opponent is [armored](#--armored) and if the the player is [confused](#--confused) before finally applying the final result of the attack.

### heal()

This method handles the healing option for the player:

```py
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
```

It checks if the player is [petrified](#--petrified) before applying a healing amount of 20 health (which is re-calculated if the health is within 20 of the max health)

### display_stats()

This handles the option to view status information of the player:

```py
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
```

This displays the player's current health, if they have any active states and the cool down left for their special abilities.

### decrement_state_counters()

Crucial for handling the state of the characters:

```py
def decrement_state_counters(self):
        for state, (active, counter) in self.state.items():
            if active and counter > 0:
                self.state[state][1] -= 1
                if self.state[state][1] == 0:
                    self.state[state][0] = False
                    time.sleep(0.5)
                    print(f"{self.name} is no longer {state}!")
```

Iterates through [state](#states) dictionary of each character and decrements the counter of any active state every turn until it reaches 0.

### handle_poison()

Checks if the character is [poisoned](#--poisoned):

```py
def handle_poison(self):
        if self.state["poisoned"][0]:
            self.health -= 10
            print(f"{self.name} loses 10 health from poison")
```

This is called after every action. If the character is indeed in a poisoned state, they will lose 10 health.

### handle_petrify()

Checks if a character is [petrified](#--petrified):

```py
def handle_petrify(self):
        if self.state["petrified"][0]:
            time.sleep(0.5)
            print(f"\n{self.name} is petrified and cannot act!")
            return True
        return False
```

Returns a boolean indicating a petrified state or not which effects certain actions.

---
---

## 3. Warrior

The Warrior character class:

```py
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
```

### Warrior special()

The warrior class has 3 special abilities, including an [ULTIMATE] ability:

#### - Battle Cry

- Warrior becomes [Zealous](#--zealous) for 3 turns
- Opponent becomes [Petrified](#--petrified) for 3 turns
- 6 turn cool down

#### - Shield Slam

- Warrior deals 1 - 35 damage to opponent
- Opponent is [Petrified](#--petrified) for 2 turns
- 4 turn cool down

#### - ULTIMATE: Armageddon

- Warrior launches opponent in the air and causes damage equal to 30% - 90% of opponent's health
- Opponent crashes into the ground, receiving damage equal to 40% - 80% of remaining health
- Opponent loses any [Immune](#--immune) and [Armored](#--armored) state and also becomes [Petrified](#--petrified) for one turn

---
---

## 4. Mage

The Mage class:

```py
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
```

### Mage special()

The mage class has 3 special abilities, including an [ULTIMATE] ability:

#### - Fireball

- Mage deals 40 damage to opponent
- 3 turn cool down

#### - Arcane Shield

- Mage is [Armored](#--armored) for 2 turns
- 4 turn cool down

#### - ULTIMATE: Apocalypse

- Mage inflicts damage equal to 50% - 100% of opponent's remaining health

## 5. Archer

The Archer class:

```py
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
```

### Archer special()

The archer class has 3 special abilities, including an [ULTIMATE] ability:

#### - Piercing Arrow

- Archer deals 40 damage to opponent
- 4 turn cool down

#### - Volley

- Archer shoots 3 arrows at opponent, each dealing between 0 - 30 damage
- 5 turn cool down

#### - ULTIMATE: Asteroids

- 3 - 10 asteroids come crashing on opponent, dealing 10 - 60 damage each

## 6. Paladin

The Paladin class:

```py
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
```

### Paladin special()

The archer class has 3 special abilities, including an [ULTIMATE] ability:

#### - Holy Strike

- Paladin deals 10 - 50 damage to opponent
- Opponent is [Petrified](#--petrified) for 1 turn
- 4 turn cool down

#### - Divine Shield

- Paladin is [Immune](#--immune) for 2 turns
- 4 turn cool down

#### - ULTIMATE: Archangel

- Archangel is summoned and deals damage equal to 80% of opponent's health
- Opponent is no longer [Immune](#--immune) or [Armored](#--armored)


[back to top](#e-commerce-product-listing-app)
