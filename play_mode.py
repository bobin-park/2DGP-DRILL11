import random
from pico2d import *

import game_framework
import game_world

from boy import Boy
from grass import Grass
from ball import Ball
from zombie import Zombie

boy = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)

def init():
    global boy
    global balls
    balls = [Ball(random.randint(100, 1600 - 100), 60, 0) for _ in range(30)]
    game_world.add_objects(balls, 1)

    #소년과 공 사이의 충돌 검사가 필요하다는 내용 추가
    game_world.add_collision_pair('boy:ball', boy, None)
    for ball in balls:
        game_world.add_collision_pair('boy:ball', None, ball)

    grass = Grass()
    game_world.add_object(grass, 0)
    game_world.add_collision_pair('grass:ball', grass, None)

    boy = Boy()
    game_world.add_object(boy, 1)


def update():
    game_world.update()
    game_world.handle_collisions()

    for ball in balls:
        if game_world.collide(boy, ball):
            print('COLLISION boy : ball')
            boy.ball_count += 1
            game_world.remove_object(ball)
            balls.remove(ball)



def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass
def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

