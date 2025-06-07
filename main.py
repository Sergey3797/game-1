from map import Map
from helicopter import Helicopter as Helico
from clouds import Clouds
import time
import os
from pynput import keyboard
import json

TICK_SLEEP = 0.05
TREE_UPDATE = 50
CLOUDS_UPDATE = 100
FIRE_UPDATE = 75
MAP_W, MAP_H = 20, 10

newMap = Map(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)
helic = Helico(MAP_W, MAP_H)
tick = 1

MOVES = {'w': (-1, 0), 'd': (0, 1), 's': (1, 0), 'a': (0, -1)}

def process_key(key):
    global helic, tick, clouds, newMap
    pressed_key = key.char.lower()
    if pressed_key in MOVES.keys():
        dx, dy = MOVES[pressed_key][0], MOVES[pressed_key][1]
        helic.move(dx, dy)
    if (pressed_key == 'f'):
        data = {"helicopter": helic.export_data(), 
                "clouds": clouds.export_data(), 
                "map": newMap.export_data(),
                "tick": tick}
        with open("level.json", "w") as lvl:
            json.dump(data, lvl)
    elif (pressed_key == 'g'):
        with open("level.json", "r") as lvl:
            data = json.load(lvl)
            tick = data["tick"] or 1
            helic.import_data(data["helicopter"])
            newMap.import_data(data["map"])
            clouds.import_data(data["clouds"]), 


listener = keyboard.Listener(
    on_press=None,
    on_release=process_key)
listener.start()
 

while True:
    os.system("cls")
    newMap.process_helicopter(helic, clouds)
    helic.print_stats()
    newMap.print_map(helic, clouds)
    print("TICK", tick)
    tick +=1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDATE == 0):
        newMap.generate_tree()
    if (tick % FIRE_UPDATE == 0):
        newMap.update_fires()
    if (tick % CLOUDS_UPDATE == 0):
        clouds.update_clouds()