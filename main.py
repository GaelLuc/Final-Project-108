from dataclasses import dataclass
from designer import *
INITIAL_SPEED = 0
HERO_SPEED = 5
@dataclass
class World:
    hero: DesignerObject
    hero_speed: int

def create_world() -> World:
    """ Create the world """
    return World(create_hero(), INITIAL_SPEED)
def create_hero() -> DesignerObject:
    """ Create the copter """
    hero = emoji("🤺")
    grow(hero, 2)
    hero.y = get_height() * (1/2)
    hero.x = get_width() * (1/8)
    hero.flip_x = True
    return hero

def move_hero(world: World):
    """ Move the copter horizontally"""
    world.hero.y += world.hero_speed

def bounce_hero(world: World):
    """ Handle the copter bouncing off a wall """
    if world.hero.y > get_height() -20:
        world.hero_speed = -HERO_SPEED
    elif world.hero.y < 20:
        world.hero_speed = HERO_SPEED

def control_hero(world: World, key: str):
    """ Change the direction that the copter is moving """
    if key == "up":
        world.hero_speed = -HERO_SPEED
    elif key == "down":
        world.hero_speed = HERO_SPEED


when('starting', create_world)
when("updating", move_hero)
when("updating", bounce_hero)
when("typing", control_hero)
start()