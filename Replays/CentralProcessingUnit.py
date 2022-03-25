"""Map Input to Function"""
"""Main returns a bool indicating IsEnd, and IsChanged"""
import numpy as np
from Army import BarBarian
import math
from time import sleep
from Army import Rage,Healing
from Infrastructure import Cannon

class CentralProcessingUnit:

    @classmethod
    def UpdatingVillage(cls,ch,Village,TownHall,Huts_list,Walls_list,Cannon_list,King,Barbarian_list):
        IsEnd1 = cls.InputToOutput(ch,Village,TownHall,Huts_list,Walls_list,Cannon_list,King,Barbarian_list)
        [IsEnd2,Win] = cls.BackGround(Village,TownHall,Huts_list,Walls_list,Cannon_list,King,Barbarian_list)
        IsEnd = IsEnd1 or IsEnd2
        return [IsEnd,Win]

    @staticmethod
    def InputToOutput(ch,Village,TownHall,Huts_list,Walls_list,Cannon_list,King,Barbarian_list):        
        IsEnd = False

        if(ch == "x"):
            IsEnd = True # only place where IsEnd is changed

        if(ch in ["w","s","a","d"]):
            King.Move(ch,Village)
            King.UpdateOnVillage(Village)

        if(ch == " "):
            King.Attack(Village,TownHall,Huts_list,Walls_list,Cannon_list)
        if(ch == "y"):
            King.Axe(Village,TownHall,Huts_list,Walls_list,Cannon_list)
        
        if(ch in ["j","k","l"]):
            if(ch == "j"):
                SpawningPos = Village.SpawningPoints[0]
            elif(ch == "k"):
                SpawningPos = Village.SpawningPoints[1]
            else:
                SpawningPos = Village.SpawningPoints[2]

            Barbarian_list.append(BarBarian([SpawningPos[0],SpawningPos[1]]))
            Barbarian_list[-1].UpdateOnVillage(Village)

        if(ch in ["r","h"]):
            if(ch == "r"):
                Rage.Action(King,Barbarian_list)
            else:
                Healing.Action(King,Barbarian_list)

        Village.UpdateCanvas()    
        return IsEnd

    @staticmethod
    def Distancebw2points(pos1,pos2):
        return math.sqrt( (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 )

    @staticmethod
    def BackGround(Village,TownHall,Huts_list,Walls_list,Cannon_list,King,Barbarian_list):

        # barbarian Movement and attack
        for barbarian in Barbarian_list:
            [ShortestDistance, Building] = [CentralProcessingUnit.Distancebw2points(barbarian.Position,TownHall.Center), TownHall]
            if(TownHall.HealthLeft == 0):
                ShortestDistance = 100000
            # for wall in Walls_list:
            #     dis = CentralProcessingUnit.Distancebw2points(barbarian.Position,wall.Center)
            #     if(dis < ShortestDistance):
            #         [ShortestDistance, Building] = [dis, wall]
            for hut in Huts_list:
                dis = CentralProcessingUnit.Distancebw2points(barbarian.Position,hut.Center)
                if(dis < ShortestDistance):
                    [ShortestDistance, Building] = [dis, hut] 
            for cannon in Cannon_list:
                dis = CentralProcessingUnit.Distancebw2points(barbarian.Position,cannon.Center)
                if(dis <= ShortestDistance):
                    [ShortestDistance, Building] = [dis, cannon] 
            
            # Still defauly behaviour at end of the game, barbarian move towards townhall as there is nothing else to initialise.
            barbarian.Attack(Village,TownHall,Huts_list,Walls_list,Cannon_list)
            barbarian.Move(Building,Village,Walls_list,TownHall,Cannon_list,Huts_list)

        # Cannon Attack
        for cannon in Cannon_list:
            IsBarbarian = False
            [ShortestDistance,Troop] = [CentralProcessingUnit.Distancebw2points(cannon.Center,King.Position), King]
            for barbarian in Barbarian_list:
                dis = CentralProcessingUnit.Distancebw2points(cannon.Center,barbarian.Position)
                if(dis < ShortestDistance):
                    IsBarbarian = True
                    [ShortestDistance, Troop] = [dis, barbarian]

            if(ShortestDistance < cannon.Range):        
                Troop.HealthLeft -= cannon.Damage 
                cannon.SetColorBasedOnHealthLeft(Village,True)
            else:
                cannon.SetColorBasedOnHealthLeft(Village,False)

            if(Troop.HealthLeft < 0):
                Troop.HealthLeft = 0
                filler = np.full((Troop.SizeOfInfrastructure[0],Troop.SizeOfInfrastructure[1]), Village.space)
                Village.VillageLayout2DArray[Troop.Position[0]:Troop.Position[0]+Troop.SizeOfInfrastructure[0],Troop.Position[1]:Troop.Position[1]+Troop.SizeOfInfrastructure[1]] = filler
                if(IsBarbarian):
                    Barbarian_list.remove(Troop)

            if(IsBarbarian == True):
                Troop.SetColorBasedOnHealthLeft()
            
        Village.UpdateCanvas()

        
        if( not(TownHall.HealthLeft>0 or Huts_list or Cannon_list) ):
            IsEnd = True
            Win = True
        elif( not(King.HealthLeft > 0 or Barbarian_list) ):
            IsEnd = True
            Win = False
        else:
            IsEnd = False
            Win = False # no one cares whats here lets keep for continuity in return

        return [IsEnd,Win]