from colorama import init
import sys

"""Custom Modules"""
import input
import Engine 
from CentralProcessingUnit import CentralProcessingUnit 
from StartingEnding import StartingEnding
from Village import Village
import Infrastructure
import Army
from datetime import datetime
import sys
from time import sleep


# -----------------------------Starting--------------------------------------------------
init()
if(len(sys.argv) != 2):
    exit("Please give in file to read")

path = sys.argv[1]
InputOutputer = open(path,'r')
StartingEnding.Start()


# -----------------------------Variable Initialization----------------------------------
Window = Engine.Canvas()
Village = Village("Sukhu",Window) 

TownHall = Infrastructure.TownHall([9,40])
TownHall.UpdateOnVillage(Village)

Huts_list = []
Huts_list.append(Infrastructure.Huts([7,37]))
Huts_list.append(Infrastructure.Huts([7,48]))
Huts_list.append(Infrastructure.Huts([12,37]))
Huts_list.append(Infrastructure.Huts([12,48]))
Huts_list.append(Infrastructure.Huts([5,5]))
for hut in Huts_list:
    hut.UpdateOnVillage(Village)

Walls_list = []
for row in range(5,16):
    for column in range(33,55):
        if(row == 5 or row == 15 or column == 33 or column == 54):
            Walls_list.append(Infrastructure.Walls([row,column]))
for wall in Walls_list:
    wall.UpdateOnVillage(Village)

Cannon_list = []
Cannon_list.append(Infrastructure.Cannon([9,37]))
Cannon_list.append(Infrastructure.Cannon([9,48]))
for cannon in Cannon_list:
    cannon.UpdateOnVillage(Village)

King = Army.King()
King.UpdateOnVillage(Village)
Window.UpdateCanvas(King.KingHealthBar(Village),[Village.StartingIndexOnCanvas[0]+Village.VillageRows,Village.StartingIndexOnCanvas[1]])

Barbarian_list = []

if(not Village.UpdateCanvas()):
    sys.exit("Boundary Condition exceeded")
IsEnd = False
Win = False

print(Village.VillageName) # Just for that cursor glitch
Window.RenderCanvas()


# ----------------------------------------GamePlay------------------------------------
while(not IsEnd):
    Engine.Canvas.BringCursortoStart()
    ch = InputOutputer.read(1)
    [IsEnd,Win] = CentralProcessingUnit.UpdatingVillage(ch,Village,TownHall,Huts_list,Walls_list,Cannon_list,King,Barbarian_list)
    Window.UpdateCanvas(King.KingHealthBar(Village),[Village.StartingIndexOnCanvas[0]+Village.VillageRows,Village.StartingIndexOnCanvas[1]])
    Window.RenderCanvas()
    sleep(0.2)


# ----------------------------------------Ending--------------------------------------- 
Window.BringCursortoEnd()
StartingEnding.Ending(Win)
