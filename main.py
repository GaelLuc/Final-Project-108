from dataclasses import dataclass
from designer import *
from random import randint
INITIAL_SPEED = 0
HERO_SPEED = 5
LASER_SPEED = 5
ZOMBIE_SPEED = 5
@dataclass
class World:
    hero: DesignerObject
    hero_speed: int
    lasers: list[DesignerObject]
    zombies: list[DesignerObject]

def create_world() -> World:
    """ Create the world """
    return World(create_hero(), INITIAL_SPEED, [], [])
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

def create_laser() -> DesignerObject:
    """ Create a Laser"""
    return rectangle("red", 15, 5)

def shoot_laser(world: World, key: str):
    """ Create a laser when the space bar is pressed """
    if key == 'space':
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

def create_zomie() -> DesignerObject:
    """ Create a zombie randomly on the right-side of the screen """
    zombie = emoji("👻")
    zombie.scale_x = 1
    zombie.scale_y = 1
    zombie.anchor = 'midbottom'
    zombie.x = get_width()
    zombie.y = randint(0, get_height())
    return zombie

def make_zombies(world: World):
    """ Create a new zombie at random times, if there aren't enough zombies """
    random_chance = randint(1, 10) == 1
    if len(world.zombies) < 10 and random_chance:
        world.zombies.append(create_zomie())

def zombie_run(world: World):
    """ Move all the zombies to the left """
    for zombie in world.zombies:
        zombie.x -= ZOMBIE_SPEED

def speedup_zombies(world: World):
    """ Make each zombie get a little bit faster """
    for zombie in world.zombies:
        zombie.x -= .01
        #zombie.scale_y += .01

def zombies_cross_the_line(world: World) -> bool:
    """ Return True if there are any zombies that cross the line """
    for zombie in world.zombies:
        if zombie.x <= 100:
            return True
    return False



when('starting', create_world)
when("updating", move_hero)
when("updating", bounce_hero)
when("typing", control_hero)
when('typing', shoot_laser)
when("updating", make_laser_fly)
when("updating", destroy_lasers_offscreen)
when("updating", make_zombies)
when("updating", zombie_run)
#when("updating", speedup_zombies)
when(zombies_cross_the_line, pause)
start()