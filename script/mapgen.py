import numpy as np
"""
Recursion to generate all possible maps as numpy arrays for a given format in our case 6x13

Every Possible Map would be way to much. We only took the maps with start and end in the top position left and right

This Algorithm can solve any Map with any start and end. The Generation took about 13 Hours and another 24 
Hours to zip and sort according to the complexity. From over 16 Million Maps we took random 30.000 as game maps. 

Source: Our Brain
"""

width = 13
heigth = 6
SolutionSum = 0


def startMap():
    """

    Returns: empty map in heigth x width format

    """
    return np.zeros((heigth, width), dtype='int8')


def availableWays(map, mx, my, condition):  # Hier wird geprüft ob oben, unten, links, oder rechts die Bedingung gilt
    """

    Arguments: map, position, condition


    Returns: list of possible ways match the condition top down left right

    """
    ways = []
    if my > 0 and map[my - 1, mx] == condition:
        ways.append((my - 1, mx))
    if my < heigth - 1 and map[my + 1, mx] == condition:
        ways.append((my + 1, mx))
    if mx > 0 and map[my, mx - 1] == condition:
        ways.append((my, mx - 1))
    if mx < width - 1 and map[my, mx + 1] == condition:
        ways.append((my, mx + 1))
    return ways


def setField(map, posx, posy, value):
    """

    Arguments: map, position in map, value

    Returns: manipulated map with the value at position

    """
    map[posy, posx] = value
    return map


def availableWays2(map, mx, my, condition1, condition2):
    """

    Arguments: map, position, two conditions


    Returns: list of possible ways match the two conditions top down left right

    """

    ways = []
    if my > 0 and map[my - 1, mx] == condition1 or my > 0 and map[my - 1, mx] == condition2:
        ways.append((my - 1, mx))
    if my < heigth - 1 and map[my + 1, mx] == condition1 or my < heigth - 1 and map[my + 1, mx] == condition2:
        ways.append((my + 1, mx))
    if mx > 0 and map[my, mx - 1] == condition1 or mx > 0 and map[my, mx - 1] == condition2:
        ways.append((my, mx - 1))
    if mx < width - 1 and map[my, mx + 1] == condition1 or mx < width - 1 and map[my, mx + 1] == condition2:
        ways.append((my, mx + 1))
    return ways


def recursivePathTracking(map, mx, my):
    """
    Recursive function to go through the map in all possible ways

    Arguments: map, position

    Returns: nothing just to break out the recursion
            If a map could be generated it is saved in a directory as numpy array

    """
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


if __name__ == "__main__":
    for y in range(heigth):
        for x in range(heigth):
            # Für jede möglichen Anfangs/End Punkte auf der linken und rechten Seite
            s = startMap()  # Leere Karte
            s = setField(s, 0, y, 1)  # Setze Anfang
            s = setField(s, width - 1, x, 2)  # Setze Ende
            # Setze den Merker auf das AnfangsFeld
            pos_x = 0
            pos_y = y
            recursivePathTracking(s, pos_x, pos_y)  # Rekursiver Algorithmus mit Backtracking
