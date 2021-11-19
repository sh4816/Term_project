import random
import json
import os

from pico2d import *
import game_framework
import game_world
import ScrollManager as scrollMgr

from player import Player, reset_variable
import game_data
import MapEditor
import Map_Background
import Map_Tile
import Map_Box
import Map_Brick
import Map_Pipe
import Map_Castle
import Map_Flag
import Item_Coin
import Item_TransForm
import ball
import mob_goomba


name = "Map1"

player = None
bg = None

def enter():
    # Player 객체를 생성
    global player
    player = Player()

    #=== 맵 배경
    global bg
    bg = Map_Background.BG()
    game_world.add_object(bg, 0)
    bg.value = "map1"

    #=== 맵 오브젝트 불러오기
    MapEditor.editMap("map1")

    # 뒤
    game_world.add_objects(Map_Tile.tiles, 0)
    game_world.add_objects(Map_Castle.castles, 0)

    # 앞
    game_world.add_objects(Map_Box.boxes, 1)
    game_world.add_objects(Map_Brick.bricks, 1)
    game_world.add_objects(Map_Pipe.pipes, 1)
    game_world.add_objects(Map_Castle.doors, 1)
    game_world.add_objects(Map_Flag.flags, 1)
    game_world.add_objects(Item_Coin.coins, 1)
    game_world.add_objects(Item_TransForm.transItems, 1)
    game_world.add_objects(mob_goomba.goombas, 1)

    game_world.add_object(player, 1)


def exit():
    Map_Tile.removeAll()
    Map_Tile.removeAll()
    Map_Box.removeAll()
    Map_Brick.removeAll()
    Map_Pipe.removeAll()
    Map_Castle.removeAll()
    Map_Flag.removeAll()
    Item_Coin.removeAll()
    Item_TransForm.removeAll()
    ball.removeAll()
    mob_goomba.removeAll()
    for game_object in game_world.all_objects():
        game_world.remove_object(game_object)
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
    #=== player State Update
    if not player.transform == game_data.gameData.transform:
        player.transform = game_data.gameData.transform

    #=== Scroll Update
    player.scrollX = scrollMgr.getScrollX("Map1", player)

    bg.scrollX = scrollMgr.getScrollX("Map1", player)

    for tile in Map_Tile.tiles:
        tile.scrollX = scrollMgr.getScrollX("Map1", player)

    for box in Map_Box.boxes:
        box.scrollX = scrollMgr.getScrollX("Map1", player)

    for brick in Map_Brick.bricks:
        brick.scrollX = scrollMgr.getScrollX("Map1", player)

    for castle in Map_Castle.castles:
        castle.scrollX = scrollMgr.getScrollX("Map1", player)

    for door in Map_Castle.doors:
        door.scrollX = scrollMgr.getScrollX("Map1", player)

    for flag in Map_Flag.flags:
        flag.scrollX = scrollMgr.getScrollX("Map1", player)

    for pipe in Map_Pipe.pipes:
        pipe.scrollX = scrollMgr.getScrollX("Map1", player)

    for coin in Item_Coin.coins:
        coin.scrollX = scrollMgr.getScrollX("Map1", player)

    for t_item in Item_TransForm.transItems:
        t_item.scrollX = scrollMgr.getScrollX("Map1", player)

    for fireball in ball.fireballs:
        fireball.scrollX = scrollMgr.getScrollX("Map1", player)

    for goomba in mob_goomba.goombas:
        goomba.scrollX = scrollMgr.getScrollX("Map1", player)

    for game_object in game_world.all_objects():
        game_object.update()



def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
