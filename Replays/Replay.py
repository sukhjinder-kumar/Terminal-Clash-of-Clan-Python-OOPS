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
from Level import LevelLayout
from datetime import datetime
from time import sleep


# -----------------------------Starting--------------------------------------------------
init()
if(len(sys.argv) != 2):
    exit("Please give in file to read")

path = sys.argv[1]
InputOutputer = open(path,'r')
IsKing = int(InputOutputer.read(1))
Level = int(InputOutputer.read(1))


# -----------------------------Variable Initialization----------------------------------
Window = Engine.Canvas()

# VillageName random selected
Village = Village("Random",Window) 
LevelLayout(Village,Level,IsKing)

IsEnd = False
Win = False

print(Village.VillageName) # Just for that cursor glitch
Window.RenderCanvas()


# ----------------------------------------GamePlay------------------------------------
while(not IsEnd):
    Engine.Canvas.BringCursortoStart()
    ch = InputOutputer.read(1)
    [IsEnd,Win] = CentralProcessingUnit.UpdatingVillage(ch,Village,Village.TownHall_list[0],Village.Huts_list,Village.Walls_list,Village.Cannon_list,Village.WizardTower_list,Village.Hero_list[0],Village.Barbarian_list,Village.Archer_list,Village.Balloon_list,IsKing)
    Window.UpdateCanvas(Village.Hero_list[0].HealthBar(Village),[Village.StartingIndexOnCanvas[0]+Village.VillageRows,Village.StartingIndexOnCanvas[1]])
    Window.RenderCanvas()
    sleep(0.1)

# ----------------------------------------Ending--------------------------------------- 
Window.BringCursortoEnd()
StartingEnding.Ending(Win)
