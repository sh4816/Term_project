import random
import json
import os

from pico2d import *
import game_framework
import game_world
import ScrollManager as scrollMgr

from player import Player

import MapEditor
import Map_Background
import Map_Tile
import Map_Box
import Map_Brick
import Map_Pipe
import Item_Coin
import Item_TransForm


name = "Map1"

player = None
bg = None

def enter():
    # Player 객체를 생성
    global player
    player = Player()

    # 맵 배경
    global bg
    bg = Map_Background.BG()
    game_world.add_object(bg, 0)
    bg.value = "map1"

    # 맵 오브젝트 불러오기
    MapEditor.editMap("map1")

    for tile in Map_Tile.tiles:
        game_world.add_object(tile, 0)

    for box in Map_Box.boxes:
        game_world.add_object(box, 0)

    for brick in Map_Brick.bricks:
        game_world.add_object(brick, 0)

    for pipe in Map_Pipe.pipes:
        game_world.add_object(pipe, 0)


    game_world.add_object(player, 1)


def exit():
    game_world.clear()

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            player.handle_event(event)


def update():
    #=== Scroll Update
    player.scrollX = scrollMgr.getScrollX("Map1", player)

    bg.scrollX = scrollMgr.getScrollX("Map1", player)

    for tile in Map_Tile.tiles:
        tile.scrollX = scrollMgr.getScrollX("Map1", player)

    for box in Map_Box.boxes:
        box.scrollX = scrollMgr.getScrollX("Map1", player)

    for brick in Map_Brick.bricks:
        brick.scrollX = scrollMgr.getScrollX("Map1", player)

    for pipe in Map_Pipe.pipes:
        pipe.scrollX = scrollMgr.getScrollX("Map1", player)

    for coin in Item_Coin.coins:
        coin.scrollX = scrollMgr.getScrollX("Map1", player)

    for t_item in Item_TransForm.t_items:
        t_item.scrollX = scrollMgr.getScrollX("Map1", player)

    for game_object in game_world.all_objects():
        game_object.update()

    #=== delay
    delay(0.01)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()