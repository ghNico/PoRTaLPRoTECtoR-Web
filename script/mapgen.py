import numpy as np
import time

spielfeldx = 13
spielfeldy = 6
berechnetefelder = 0
nummer =0


def zeigeMap(map):
    print(map)


def startMap():
    return np.zeros((spielfeldy, spielfeldx), dtype='int8')


def moeglicheWege(map, mx, my, bed):
    wege = []
    if my > 0 and map[my - 1, mx] == bed:
        wege.append((my - 1, mx))
    if my < spielfeldy - 1 and map[my + 1, mx] == bed:
        wege.append((my + 1, mx))
    if mx > 0 and map[my, mx - 1] == bed:
        wege.append((my, mx - 1))
    if mx < spielfeldx - 1 and map[my, mx + 1] == bed:
        wege.append((my, mx + 1))
    return wege



def setzeFeld(map, posx, posy, value):
    map[posy, posx] = value
    return map



def verbotWege(map, mx, my, bed1, bed2):
    wege = []
    if my > 0 and map[my - 1, mx] == bed1 or my > 0 and map[my - 1, mx] == bed2:
        wege.append((my - 1, mx))
    if my < spielfeldy - 1 and map[my + 1, mx] == bed1 or my < spielfeldy - 1 and map[my + 1, mx] == bed2:
        wege.append((my + 1, mx))
    if mx > 0 and map[my, mx - 1] == bed1 or mx > 0 and map[my, mx - 1] == bed2:
        wege.append((my, mx - 1))
    if mx < spielfeldx - 1 and map[my, mx + 1] == bed1 or mx < spielfeldx - 1 and map[my, mx + 1] == bed2:
        wege.append((my, mx + 1))
    return wege



def findeWeg(map, mx, my):
    global aktuelleMap, nummer
    wege = moeglicheWege(map, mx, my, 0)
    siegwege = moeglicheWege(map, mx, my, 2)
    if len(siegwege) != 0:
        np.save(f'maps/map{nummer}.npy',map)
        nummer+=1
        return
    if len(wege) == 0:
        print("Pfad zuende")
        return
    k = map
    for e in wege:
        verbot = verbotWege(k, e[1], e[0], 8, 1)
        if len(verbot) < 2:
            s = setzeFeld(k, e[1], e[0], 8)
            findeWeg(s, e[1], e[0])
            setzeFeld(k, e[1], e[0], 0)
    return

merkerx = 0
merkery = 0
var = 0
for y in range(6):
    for x in range(13):
        s = startMap()

        s = setzeFeld(s, 0, y, 1)
        s = setzeFeld(s, spielfeldx - 1, x, 2)

        merkerx = 0
        merkery = y
        print((var/78)*100)
        findeWeg(s, merkerx, merkery)
        var+=1

