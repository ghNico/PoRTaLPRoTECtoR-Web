import numpy as np

spielfeldx = 13
spielfeldy = 6
nummer = 0


def startMap():
    return np.zeros((spielfeldy, spielfeldx), dtype='int8')


def moeglicheWege(map, mx, my, bed):  # Hier wird geprüft ob oben, unten, links, oder rechts die Bedingung gilt
    wege = []
    if my > 0 and map[my - 1, mx] == bed:  # oben
        wege.append((my - 1, mx))
    if my < spielfeldy - 1 and map[my + 1, mx] == bed:  # unten
        wege.append((my + 1, mx))
    if mx > 0 and map[my, mx - 1] == bed:  # links
        wege.append((my, mx - 1))
    if mx < spielfeldx - 1 and map[my, mx + 1] == bed:  # rechts
        wege.append((my, mx + 1))
    return wege


def setzeFeld(map, posx, posy, value):  # An der Stelle in der Map den Wert einfügen
    map[posy, posx] = value
    return map


def verbotWege(map, mx, my, bed1, bed2):  # gleich wie moeglicheWege() aber hier werden zwei Bedingungen geprüft
    wege = []
    if my > 0 and map[my - 1, mx] == bed1 or my > 0 and map[my - 1, mx] == bed2:  # oben
        wege.append((my - 1, mx))
    if my < spielfeldy - 1 and map[my + 1, mx] == bed1 or my < spielfeldy - 1 and map[my + 1, mx] == bed2:  # unten
        wege.append((my + 1, mx))
    if mx > 0 and map[my, mx - 1] == bed1 or mx > 0 and map[my, mx - 1] == bed2:  # linka
        wege.append((my, mx - 1))
    if mx < spielfeldx - 1 and map[my, mx + 1] == bed1 or mx < spielfeldx - 1 and map[my, mx + 1] == bed2:  # rechts
        wege.append((my, mx + 1))
    return wege


def findeWeg(map, mx, my):
    global nummer  # Lösungsnummer
    wege = moeglicheWege(map, mx, my, 0)  # Alle Wege, die von der Startposition möglich sind
    siegwege = moeglicheWege(map, mx, my, 2)  # Alle Wege, in welchen man in einem Schritt das Ziel erreicht
    if len(siegwege) != 0:  # Wenn es die Möglichkeit gibt in einem Schritt zum Ende zu kommen
        np.save(f'maps/map{nummer}.npy', map)  # Speichern der Map als Numpy Array
        nummer += 1  # Lösungsanzahl wird inkrementiert
        return  # Ausbruch aus der Rekursion
    if len(wege) == 0:  # Wenn es keine Möglichkeit gibt einen Schritt in eine Richtung zu machen
        return  # Ausbruch aus der Rekursion
    k = map  # Speichern der Karte als lokale Kopie innerhalb der Rekursion
    for e in wege:  # Für alle möglichen Wege
        verbot = verbotWege(k, e[1], e[0], 8, 1)  # Überprüfen, ob es innerhalb der Wege legale Wege gibt.
        if len(verbot) < 2:  # Wenn die Wege nicht nebeneinander sind
            s = setzeFeld(k, e[1], e[0], 8)  # Man geht den ersten Weg
            findeWeg(s, e[1], e[0])  # und sucht den weiteren Weg ab der Position
            setzeFeld(k, e[1], e[0], 0)  # Egal ob Erfolg oder Fehler, man entfernt den Weg den man gegangen ist
    return  # und schaut ob es noch andere Abzweigungen gab ansonsten Ausbruch aus Rekursion


merkerx = 0
merkery = 0
for y in range(spielfeldy):
    for x in range(spielfeldy):
        # Für jede möglichen Anfangs/End Punkte
        s = startMap()  # Leere Karte
        s = setzeFeld(s, 0, y, 1)  # Setze Anfang
        s = setzeFeld(s, spielfeldx - 1, x, 2)  # Setze Ende
        # Setze den Merker auf das AnfangsFeld
        merkerx = 0
        merkery = y
        findeWeg(s, merkerx, merkery)  # Rekursiver Algorithmus mit Backtracking
