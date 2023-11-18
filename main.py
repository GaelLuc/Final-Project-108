from dataclasses import dataclass
from designer import *
INITIAL_SPEED = 0
HERO_SPEED = 5
LASER_SPEED = 5
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
    """ Destroy any lasers that have landed on the ground """
    kept = []
    for laser in world.lasers:
        if laser.x < get_width():
            kept.append(laser)
        else:
            destroy(laser)
    world.lasers = kept


when('starting', create_world)
when("updating", move_hero)
when("updating", bounce_hero)
when("typing", control_hero)
when('typing', shoot_laser)
when("updating", make_laser_fly)
when("updating", destroy_lasers_offscreen)
start()