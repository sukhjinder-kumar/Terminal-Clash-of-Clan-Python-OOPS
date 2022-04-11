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


# -----------------------------Starting--------------------------------------------------
init()
[VillageName,IsKing, Level] = StartingEnding.Start()
today = datetime.today()
name = f"{VillageName}: {today.year}-{today.month}-{today.day}-{today.hour}-{today.minute}-{today.second}"
path = f"./Replays/ReplayFiles/{name}"
InputStorage = open(path,'wt')
InputStorage.write(str(IsKing))
InputStorage.write(str(Level))


# -----------------------------Variable Initialization----------------------------------
Window = Engine.Canvas()
Village = Village(VillageName,Window) 
LevelLayout(Village,Level,IsKing)

IsEnd = False
Win = False

print(Village.VillageName) # Just for that cursor glitch
Window.RenderCanvas()


# ----------------------------------------GamePlay------------------------------------
while(not IsEnd):
    Engine.Canvas.BringCursortoStart()
    ch = input.input_to(input.Get())
    if(not(ch is None)):
        InputStorage.write(ch)
    if(ch is None):
        InputStorage.write("Q")
    [IsEnd,Win] = CentralProcessingUnit.UpdatingVillage(ch,Village,Village.TownHall_list[0],Village.Huts_list,Village.Walls_list,Village.Cannon_list,Village.WizardTower_list,Village.Hero_list[0],Village.Barbarian_list,Village.Archer_list,Village.Balloon_list,IsKing)
    Window.UpdateCanvas(Village.Hero_list[0].HealthBar(Village),[Village.StartingIndexOnCanvas[0]+Village.VillageRows,Village.StartingIndexOnCanvas[1]])
    Window.RenderCanvas()


# ----------------------------------------Ending--------------------------------------- 
Window.BringCursortoEnd()
StartingEnding.Ending(Win)
