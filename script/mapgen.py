import numpy as np

width = 13
heigth = 6
SolutionSum = 0


def startMap():
    return np.zeros((heigth, width), dtype='int8')


def availableWays(map, mx, my, condition):  # Hier wird geprüft ob oben, unten, links, oder rechts die Bedingung gilt
    ways = []
    if my > 0 and map[my - 1, mx] == condition:  # oben
        ways.append((my - 1, mx))
    if my < heigth - 1 and map[my + 1, mx] == condition:  # unten
        ways.append((my + 1, mx))
    if mx > 0 and map[my, mx - 1] == condition:  # links
        ways.append((my, mx - 1))
    if mx < width - 1 and map[my, mx + 1] == condition:  # rechts
        ways.append((my, mx + 1))
    return ways


def setField(map, posx, posy, value):  # An der Stelle in der Map den Wert einfügen
    map[posy, posx] = value
    return map


def availableWays2(map, mx, my, condition1, condition2):  # gleich wie moeglicheWege() aber hier werden zwei Bedingungen geprüft
    wege = []
    if my > 0 and map[my - 1, mx] == condition1 or my > 0 and map[my - 1, mx] == condition2:  # oben
        wege.append((my - 1, mx))
    if my < heigth - 1 and map[my + 1, mx] == condition1 or my < heigth - 1 and map[my + 1, mx] == condition2:  # unten
        wege.append((my + 1, mx))
    if mx > 0 and map[my, mx - 1] == condition1 or mx > 0 and map[my, mx - 1] == condition2:  # linka
        wege.append((my, mx - 1))
    if mx < width - 1 and map[my, mx + 1] == condition1 or mx < width - 1 and map[my, mx + 1] == condition2:  # rechts
        wege.append((my, mx + 1))
    return wege


def recursivePathTracking(map, mx, my):
    global SolutionSum  # Lösungsnummer
    ways = availableWays(map, mx, my, 0)  # Alle Wege, die von der Startposition möglich sind
    waystoend = availableWays(map, mx, my, 2)  # Alle Wege, in welchen man in einem Schritt das Ziel erreicht
    if len(waystoend) != 0:  # Wenn es die Möglichkeit gibt in einem Schritt zum Ende zu kommen
        np.save(f'maps/map{SolutionSum}.npy', map)  # Speichern der Map als Numpy Array
        SolutionSum += 1  # Lösungsanzahl wird inkrementiert
        return  # Ausbruch aus der Rekursion
    if len(ways) == 0:  # Wenn es keine Möglichkeit gibt einen Schritt in eine Richtung zu machen
        return  # Ausbruch aus der Rekursion
    localmap = map  # Speichern der Karte als lokale Kopie innerhalb der Rekursion
    for oneway in ways:  # Für alle möglichen Wege
        legalways = availableWays2(localmap, oneway[1], oneway[0], 8, 1)  # Überprüfen, ob es innerhalb der Wege legale Wege gibt.
        if len(legalways) < 2:  # Wenn die Wege nicht nebeneinander sind
            newway = setField(localmap, oneway[1], oneway[0], 8)  # Man geht den ersten Weg
            recursivePathTracking(newway, oneway[1], oneway[0])  # und sucht den weiteren Weg ab der Position
            setField(localmap, oneway[1], oneway[0], 0)  # Egal ob Erfolg oder Fehler, man entfernt den Weg den man gegangen ist
    return  # und schaut ob es noch andere Abzweigungen gab ansonsten Ausbruch aus Rekursion



for y in range(heigth):
    for x in range(heigth):
        # Für jede möglichen Anfangs/End Punkte
        s = startMap()  # Leere Karte
        s = setField(s, 0, y, 1)  # Setze Anfang
        s = setField(s, width - 1, x, 2)  # Setze Ende
        # Setze den Merker auf das AnfangsFeld
        pos_x = 0
        pos_y = y
        recursivePathTracking(s, pos_x, pos_y)  # Rekursiver Algorithmus mit Backtracking
