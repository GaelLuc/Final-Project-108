from dataclasses import dataclass
from designer import *
from random import randint
INITIAL_SPEED = 0
HERO_SPEED = 5
LASER_SPEED = 5
ZOMBIE_SPEED = 3
FAST_ZOMBIE_SPEED = 5
@dataclass
class World:
    hero: DesignerObject
    hero_speed: int
    lasers: list[DesignerObject]
    zombies: list[DesignerObject]
    speed_zombies: list[DesignerObject]
    stars: list[DesignerObject]
    special_lasers: list[DesignerObject]
    is_special: bool
    score: int
    counter: DesignerObject

def create_world() -> World:
    """ Create the world """
    return World(create_hero(), INITIAL_SPEED, [], [], [], [], [], False, 0,
                 text("black", "Score: ", 35, int(get_width() * (1/2)), int(get_height() * (1 / 8))))
def create_hero() -> DesignerObject:
    """ Create the hero """
    hero = emoji("🤺")
    grow(hero, 2)
    hero.y = get_height() * (1/2)
    hero.x = get_width() * (1/8)
    hero.flip_x = True
    print(hero.x)
    return hero

def move_hero(world: World):
    """ Move the hero vertically """
    world.hero.y += world.hero_speed

def bounce_hero(world: World):
    """ Handle the hero bouncing off a wall """
    if world.hero.y > get_height() -20:
        world.hero_speed = -HERO_SPEED
    elif world.hero.y < 20:
        world.hero_speed = HERO_SPEED

def control_hero(world: World, key: str):
    """ Change the direction that the hero is moving """
    if key == "up":
        world.hero_speed = -HERO_SPEED
    elif key == "down":
        world.hero_speed = HERO_SPEED

def create_house() -> DesignerObject:
    """ Create a zombie randomly on the right-side of the screen """
    house = emoji("🏠")
    house.scale_x = 3
    house.scale_y = 3
    house.anchor = 'midbottom'
    house.x = 30
    house.y = get_height()/2
    return house

def create_laser() -> DesignerObject:
    """ Create a Laser"""
    return rectangle("red", 15, 5)

def shoot_laser(world: World, key: str):
    """ Create a laser when the space bar is pressed """
    if key == 'space' and not world.is_special:
        new_laser = create_laser()
        laser_position(new_laser, world.hero)
        world.lasers.append(new_laser)

def laser_position(left: DesignerObject, center: DesignerObject):
    """ Move the left object to be infront the center object """
    left.y = center.y - center.height/4
    left.x = center.x + center.width/2

def make_laser_fly(world: World):
    """ Move all the lasers to the left """
    for laser in world.lasers:
        laser.x += LASER_SPEED

def destroy_lasers_offscreen(world: World):
    """ Destroy any lasers that are offscreen """
    kept = []
    for laser in world.lasers:
        if laser.x < get_width():
            kept.append(laser)
        else:
            destroy(laser)
    world.lasers = kept

def create_bullet_laser() -> DesignerObject:
    """ Create a bullet Laser"""
    return rectangle("gold", 15, 5)

def create_wave_laser() -> DesignerObject:
    """ Create a wave Laser"""
    return rectangle('gold', 5, 30)

def shoot_special_laser(world: World, key: str):
    """ Create a One Special laser when world.is_special is true and the space bar is pressed """
    if world.is_special and key == 'space':
        random_chance = randint(1, 2)
        if random_chance == 1:
            new_bullet_laser = create_bullet_laser()
            laser_position(new_bullet_laser, world.hero)
            world.special_lasers.append(new_bullet_laser)
        elif random_chance == 2:
            new_wave_laser = create_wave_laser()
            laser_position(new_wave_laser, world.hero)
            world.special_lasers.append(new_wave_laser)
        world.is_special = False

def move_special_laser(world: World):
    for special_laser in world.special_lasers:
        special_laser.x += LASER_SPEED

def destroy_special_lasers_offscreen(world: World):
    """ Destroy any lasers that are offscreen """
    kept = []
    for special_laser in world.special_lasers:
        if special_laser.x < get_width():
            kept.append(special_laser)
        else:
            destroy(special_laser)
    world.special_lasers = kept

def create_star() -> DesignerObject:
    """ Create a star randomly on the left-side of the screen, when conditions are met"""
    star = emoji("🌟")
    star.scale_x = 0.6
    star.scale_y = 0.6
    star.anchor = 'midbottom'
    star.x = get_width() * (1/8)
    star.y = randint(50, get_height() - 50)
    return star

def make_stars_randomly(world: World):
    """ Create a new star at random times, only when there is no stars """
    star_chance_50 = randint(1, 50) == 1
    star_chance_40 = randint(1, 60) == 1
    star_chance_30 = randint(1, 70) == 1
    star_chance_20 = randint(1, 80) == 1
    star_chance_10 = randint(1, 90) == 1
    # Creating the scale feature for the Stars
    if world.score >= 50 and len(world.stars) < 2 and star_chance_50:
        world.stars.append(create_star())
    elif world.score >= 40 and len(world.stars) < 2 and star_chance_40:
        world.stars.append(create_star())
    elif world.score >= 30 and len(world.stars) < 2 and star_chance_30:
        world.stars.append(create_star())
    elif world.score >= 20 and len(world.stars) < 1 and star_chance_20:
        world.stars.append(create_star())
    elif world.score >= 8 and len(world.stars) < 1 and star_chance_10:
        world.stars.append(create_star())

def create_zomie() -> DesignerObject:
    """ Create a zombie randomly on the right-side of the screen """
    zombie = emoji("zombie")
    zombie.scale_x = 1
    zombie.scale_y = 1
    zombie.anchor = 'midbottom'
    zombie.x = get_width()
    zombie.y = randint(50, get_height()-50)
    return zombie

def create_speed_zomie() -> DesignerObject:
    """ Create a zombie randomly on the right-side of the screen """
    zombie = emoji("zombie")
    zombie.scale_x = 1
    zombie.scale_y = 1
    zombie.anchor = 'midbottom'
    zombie.x = get_width()
    zombie.y = randint(100, get_height()-100)
    return zombie
def make_zombies(world: World):
    """ Create a new zombie at random times, if there aren't enough zombies """
    random_chance = randint(1, 20) == 1
    special_chance = randint(1, 40) == 1
    if len(world.zombies) < 10 and random_chance:
        world.zombies.append(create_zomie())
    if world.score >= 20 and len(world.zombies) < 10 and special_chance:
        world.speed_zombies.append(create_speed_zomie())

def zombie_run(world: World):
    """ Move all the zombies to the left """
    for zombie in world.zombies:
        zombie.x -= ZOMBIE_SPEED
    for zombie in world.speed_zombies:
        zombie.x -= FAST_ZOMBIE_SPEED

def zombies_cross_the_line(world: World) -> bool:
    """ Return True if there are any zombies that cross the line """
    for zombie in world.zombies:
        if zombie.x <= 100 or colliding(world.hero, zombie):
            return True
    for speed_zombie in world.speed_zombies:
        if speed_zombie.x <= 100 or colliding(world.hero, speed_zombie):
            return True
    return False

def collide_laser_zombie(world: World):
    destroyed_lists = deleting_both_colliding_objects(world, world.lasers, world.zombies)
    world.lasers = filter_from(world.lasers, destroyed_lists[0])
    world.zombies = filter_from(world.zombies, destroyed_lists[1])

def deleting_both_colliding_objects(world: World, laser_list: list[DesignerObject], character_list: list[DesignerObject]):
    final_list = []
    destroyed_laser_list = []
    destroyed_character_list = []
    for laser in laser_list:
        for character in character_list:
            if colliding(laser, character):
                destroyed_laser_list.append(laser)
                destroyed_character_list.append(character)
                world.score += 1
    final_list.append(destroyed_laser_list)
    final_list.append(destroyed_character_list)
    return final_list


def collide_laser_speed_zombie(world: World):
    destroyed_lists = deleting_both_colliding_objects(world, world.lasers, world.speed_zombies)
    world.lasers = filter_from(world.lasers, destroyed_lists[0])
    world.speed_zombies = filter_from(world.speed_zombies, destroyed_lists[1])


def collide_star_hero(world: World):
    destroyed_stars = []
    for star in world.stars:
        if colliding(star, world.hero):
            destroyed_stars.append(star)
            world.is_special = True
    world.stars = filter_from(world.stars, destroyed_stars)

def collide_special_laser_zombie(world: World):
    destroyed_zombies = deleting_one_colliding_objects(world, world.special_lasers, world.zombies)
    world.zombies = filter_from(world.zombies, destroyed_zombies)

def collide_special_laser_speed_zombie(world: World):
    destroyed_speed_zombies = deleting_one_colliding_objects(world, world.special_lasers, world.speed_zombies)
    world.speed_zombies = filter_from(world.speed_zombies, destroyed_speed_zombies)

def deleting_one_colliding_objects(world: World, laser_list: list[DesignerObject], character_list: list[DesignerObject]):
    """Helper function that cuts down repetitive code"""
    destroyed_character_list = []
    for laser in laser_list:
        for character in character_list:
            if colliding(laser, character):
                destroyed_character_list.append(character)
                world.score += 1
    return destroyed_character_list

def filter_from(old_list: list[DesignerObject], elements_to_not_keep: list[DesignerObject]) -> list[DesignerObject]:
    new_values = []
    for item in old_list:
        if item in elements_to_not_keep:
            destroy(item)
        else:
            new_values.append(item)
    return new_values

def update_score(world):
    """ Update the score """
    world.counter.text = "Score: " + str(world.score)

def flash_game_over(world):
    """ Show the game over message """
    world.counter.text = "GAME OVER! Your score was " + str(world.score)



when('starting', create_world)
when("updating", create_house)
when("updating", move_hero)
when("updating", bounce_hero)
when("typing", control_hero)
when('typing', shoot_laser)
when("updating", make_laser_fly)
when("updating", destroy_lasers_offscreen)
when("updating", make_stars_randomly)
when("updating", make_zombies)
when("updating", zombie_run)
when('updating', collide_laser_zombie)
when("updating", collide_laser_speed_zombie)
when("updating", collide_star_hero)
when("typing", shoot_special_laser)
when("updating", move_special_laser)
when("updating", destroy_special_lasers_offscreen)
when("updating", collide_special_laser_zombie)
when("updating", collide_special_laser_speed_zombie)
when("updating", update_score)
when(zombies_cross_the_line, flash_game_over, pause)
start()