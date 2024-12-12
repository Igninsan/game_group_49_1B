from random import randint, choice


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.__health} damage: {self.__damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None
        self.stun = 0

    @property
    def defence(self):
        return self.__defence

    def choose_defence(self, heroes):
        hero = choice(heroes)
        self.__defence = hero.ability

    def attack(self, heroes):
        if self.stun > 0:
            print('Boss is stunned')
            self.stun -= 1
        else:
            for hero in heroes:
                if hero.health > 0:
                    if type(hero) == Berserk and self.defence != hero.ability:
                        block = choice([5, 10])  # 5 or 10
                        hero.blocked_damage = block
                        hero.health -= (self.damage - block)
                    else:
                        hero.health -= self.damage

    def __str__(self):
        return f'BOSS ' + super().__str__() + f' defence: {self.__defence}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss):
        boss.health -= self.damage

    def apply_super_power(self, boss, heroes):
        pass


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'CRIT')

    def apply_super_power(self, boss, heroes):
        coef = randint(2, 5)
        boss.health -= self.damage * coef
        print(f'Warrior {self.name} hit critically {self.damage * coef}')


class Magic(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BOOST')

    def apply_super_power(self, boss, heroes):
        if round_number == 1:
            for hero in heroes:
                hero.damage += 4
        if round_number == 4:
            for hero in heroes:
                hero.damage -= 4


class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, 'HEAL')
        self.__heal_points = heal_points

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health > 0 and self != hero:
                hero.health += self.__heal_points


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BLOCK_REVERT')
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss, heroes):
        boss.health -= self.blocked_damage
        print(f'Berserk {self.name} reverted {self.__blocked_damage} damage to boss')


class Witcher(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'REVIVE')

    def attack(self, boss):
        pass

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health == 0:
                hero.health, self.health = self.health, 0
                print(f'Witcher {self.name} revived {hero.name}')
                break


class Hacker(Hero):
    def __init__(self, name, health, damage, hack_value):
        super().__init__(name, health, damage,'HACK')
        self.__hack_value = hack_value

    @property
    def hack_value(self):
        return self.__hack_value

    def apply_super_power(self, boss, heroes):
        if round_number % 2 == 0:
            boss.health -= self.__hack_value
            hero = choice(heroes)
            if hero.health != 0:
                hero.health += self.__hack_value
                print(f'Hacker {self.name} stole health from {boss.name} and healed {hero.name}')
            else:
                self.health += 0
                print(f'Hacker {self.name} stole health from {boss.name} and healed {self.name}')


class Thor(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'STUN')

    def apply_super_power(self, boss, heroes):
        if randint(1, 10) == 10:
            boss.stun += 1
            print(f'Thor {self.name} stunned boss {boss.name}')


class Samurai(Hero):
    def __init__(self, name, health, damage, shuriken_power):
        super().__init__(name, health, damage, 'SHURIKEN_THROW')
        self.__shuriken_power = shuriken_power

    @property
    def shuriken_power(self):
        return self.__shuriken_power

    def apply_super_power(self, boss, heroes):
        if randint(1, 2) == 1:
            boss.health -= self.__shuriken_power
            print(f'Samurai {self.name} threw Virus and dealt {self.__shuriken_power} damage to boss {boss.name}')
        else:
            boss.health += self.__shuriken_power
            print(f'Samurai {self.name} threw Vaccine and healed {self.__shuriken_power} health to boss {boss.name}')

round_number = 0


def is_game_over(boss, heroes):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
        return True
    return False


def play_round(boss, heroes):
    global round_number
    round_number += 1
    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if hero.health > 0 and boss.health > 0 and hero.ability != boss.defence:
            hero.attack(boss)
            hero.apply_super_power(boss, heroes)
    show_statistics(boss, heroes)


def show_statistics(boss, heroes):
    print(f'ROUND {round_number} -------------')
    print(boss)
    for hero in heroes:
        print(hero)


def start_game():
    boss = Boss('Lord', 1200, 50)
    warrior_1 = Warrior('Brane', 280, 15)
    warrior_2 = Warrior('Alucard', 270, 20)
    magic = Magic('Subaru', 290, 10)
    doc = Medic('Merlin', 250, 5, 15)
    assistant = Medic('Florin', 300, 5, 5)
    berserk = Berserk('Guts', 260, 10)
    witcher = Witcher('Gerald', 280, 0)
    hacker = Hacker('Jeff', 250, 5, 15)
    thor = Thor('Chris', 270, 10)
    samurai = Samurai('Genji', 250, 5, 10)

    heroes_list = [warrior_1, warrior_2, magic, doc, assistant, berserk, witcher, hacker, thor, samurai]

    show_statistics(boss, heroes_list)
    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


start_game()
