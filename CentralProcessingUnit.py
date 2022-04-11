"""Map Input to Function"""
"""Main returns a bool indicating IsEnd, and IsChanged"""
from matplotlib.cbook import is_writable_file_like
import numpy as np
import math
from time import sleep
from Army import Rage,Healing,Army,BarBarian,Archer,Balloon
from Infrastructure import Cannon, WizardTower

class CentralProcessingUnit:

    @classmethod
    def UpdatingVillage(cls,ch,Village,TownHall,Huts_list,Walls_list,Cannon_list,WizardTower_list,Hero,Barbarian_list,Archer_list,Balloon_list,IsKing):
        IsEnd1 = cls.InputToOutput(ch,Village,TownHall,Huts_list,Walls_list,Cannon_list,WizardTower_list,Hero,Barbarian_list,Archer_list,Balloon_list,IsKing)
        [IsEnd2,Win] = cls.BackGround(Village,TownHall,Huts_list,Walls_list,Cannon_list,WizardTower_list,Hero,Barbarian_list,Archer_list,Balloon_list,IsKing)
        IsEnd = IsEnd1 or IsEnd2
        return [IsEnd,Win]

    @staticmethod
    def InputToOutput(ch,Village,TownHall,Huts_list,Walls_list,Cannon_list,WizardTower_list,Hero,Barbarian_list,Archer_list,Balloon_list,IsKing):        
        IsEnd = False

        # Exit the game
        if(ch == "x"):
            IsEnd = True # only place where IsEnd is changed

        # Moving the Hero
        if(ch in ["w","s","a","d"]):
            Hero.Move(ch,Village)
            Hero.UpdateOnVillage(Village)

        # Attacking Hero 
        if(ch == " "):
            Hero.Attack(Village,TownHall,Huts_list,Walls_list,Cannon_list,WizardTower_list)
        if(IsKing and ch == "y"):
            Hero.Axe(Village,TownHall,Huts_list,Walls_list,Cannon_list,WizardTower_list)
        
        # Barbarian Spawning
        if(ch in ["j","k","l"] and BarBarian.TotalBarBarian<Army.Number_Barbarian):
            if(ch == "j"):
                SpawningPos = Village.SpawningPoints[0]
            elif(ch == "k"):
                SpawningPos = Village.SpawningPoints[1]
            else:
                SpawningPos = Village.SpawningPoints[2]

            Barbarian_list.append(BarBarian([SpawningPos[0],SpawningPos[1]]))
            Barbarian_list[-1].UpdateOnVillage(Village)

        # Archer Spawning
        if(ch in ["u","i","o"] and Archer.TotalArcher<Army.Number_Archer):
            if(ch == "u"):
                SpawningPos = Village.SpawningPoints[0]
            elif(ch == "i"):
                SpawningPos = Village.SpawningPoints[1]
            else:
                SpawningPos = Village.SpawningPoints[2]

            Archer_list.append(Archer([SpawningPos[0],SpawningPos[1]]))
            Archer_list[-1].UpdateOnVillage(Village)

        # Balloon Spawning
        if(ch in ["n","m",","] and Balloon.TotalBalloon<Army.Number_Balloon):
            if(ch == "n"):
                SpawningPos = Village.SpawningPoints[0]
            elif(ch == "m"):
                SpawningPos = Village.SpawningPoints[1]
            else:
                SpawningPos = Village.SpawningPoints[2]

            Balloon_list.append(Balloon([SpawningPos[0],SpawningPos[1]]))
            Balloon_list[-1].UpdateOnVillage(Village)

        # Spells
        if(ch in ["r","h"]):
            if(ch == "r"):
                Rage.Action(Hero,Barbarian_list,Archer_list,Balloon_list,IsKing)
            else:
                Healing.Action(Hero,Barbarian_list,Archer_list,Balloon_list)

        Village.UpdateCanvas()    
        return IsEnd

    @staticmethod
    def Distancebw2points(pos1,pos2):
        return math.sqrt( (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 )

    @staticmethod
    def BackGround(Village,TownHall,Huts_list,Walls_list,Cannon_list,WizardTower_list,Hero,Barbarian_list,Archer_list,Balloon_list,IsKing):

        # Barbarian Movement and Attack
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
            for wizardtower in WizardTower_list:
                dis = CentralProcessingUnit.Distancebw2points(barbarian.Position,wizardtower.Center)
                if(dis <= ShortestDistance):
                    [ShortestDistance, Building] = [dis, wizardtower] 
            
            # Still defauly behaviour at end of the game, barbarian move towards townhall as there is nothing else to initialise.
            barbarian.Attack(Village,TownHall,Huts_list,Walls_list,Cannon_list,WizardTower_list)
            barbarian.Move(Building,Village,Walls_list,TownHall,Cannon_list,WizardTower_list,Huts_list)

        # Archer Movement and Attack
        for archer in Archer_list:
            [ShortestDistance, Building] = [CentralProcessingUnit.Distancebw2points(archer.Position,TownHall.Center), TownHall]
            if(TownHall.HealthLeft == 0):
                ShortestDistance = 100000
            for hut in Huts_list:
                dis = CentralProcessingUnit.Distancebw2points(archer.Position,hut.Center)
                if(dis < ShortestDistance):
                    [ShortestDistance, Building] = [dis, hut] 
            for cannon in Cannon_list:
                dis = CentralProcessingUnit.Distancebw2points(archer.Position,cannon.Center)
                if(dis <= ShortestDistance):
                    [ShortestDistance, Building] = [dis, cannon] 
            for wizardtower in WizardTower_list:
                dis = CentralProcessingUnit.Distancebw2points(archer.Position,wizardtower.Center)
                if(dis <= ShortestDistance):
                    [ShortestDistance, Building] = [dis, wizardtower] 
            if(ShortestDistance>archer.Range):
                for wall in Walls_list:
                    dis = CentralProcessingUnit.Distancebw2points(archer.Position,wall.Center)
                    if(dis < ShortestDistance):
                        [ShortestDistance, Building] = [dis, wall]

            archer.Attack(Village,Building,TownHall,Huts_list,Walls_list,Cannon_list,WizardTower_list)
            archer.Move(Building,Village,Walls_list,TownHall,Cannon_list,WizardTower_list,Huts_list)

        # Balloon Movement and Attack
        for balloon in Balloon_list:
            ShortestDistance = 100000
            for cannon in Cannon_list:
                dis = CentralProcessingUnit.Distancebw2points(balloon.Position,cannon.Center)
                if(dis <= ShortestDistance):
                    [ShortestDistance, Building] = [dis, cannon] 
            for wizardtower in WizardTower_list:
                dis = CentralProcessingUnit.Distancebw2points(balloon.Position,wizardtower.Center)
                if(dis <= ShortestDistance):
                    [ShortestDistance, Building] = [dis, wizardtower] 
            if(not (Cannon_list or WizardTower_list)):
                [ShortestDistance, Building] = [CentralProcessingUnit.Distancebw2points(balloon.Position,TownHall.Center), TownHall]
                if(TownHall.HealthLeft == 0):
                    ShortestDistance = 100000
                for hut in Huts_list:
                    dis = CentralProcessingUnit.Distancebw2points(balloon.Position,hut.Center)
                    if(dis < ShortestDistance):
                        [ShortestDistance, Building] = [dis, hut] 
            balloon.Move(Building,Village,Walls_list,TownHall,Cannon_list,WizardTower_list,Huts_list)
            if(ShortestDistance==0):
                balloon.Attack(Village,TownHall,Huts_list,Walls_list,Cannon_list,WizardTower_list)

        # Cannon Attack
        for cannon in Cannon_list:
            IsHero = True 
            IsBarbarian = False
            IsArcher = False
            [ShortestDistance,Troop] = [CentralProcessingUnit.Distancebw2points(cannon.Center,Hero.Position), Hero]

            for barbarian in Barbarian_list:
                dis = CentralProcessingUnit.Distancebw2points(cannon.Center,barbarian.Position)
                if(dis < ShortestDistance):
                    IsHero = False 
                    IsBarbarian = True
                    IsArcher = False
                    [ShortestDistance, Troop] = [dis, barbarian]

            for archer in Archer_list:
                dis = CentralProcessingUnit.Distancebw2points(cannon.Center,archer.Position)
                if(dis < ShortestDistance):
                    IsHero = False 
                    IsArcher = True
                    IsBarbarian = False
                    [ShortestDistance, Troop] = [dis, archer]

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
                if(IsArcher):
                    Archer_list.remove(Troop)

            if(not IsHero):
                Troop.SetColorBasedOnHealthLeft()
            
        # Wizard Tower          
        for wizardtower in WizardTower_list:
            IsHero = True 
            IsBarbarian = False
            IsArcher = False
            IsBalloon = False
            [ShortestDistance,Troop] = [CentralProcessingUnit.Distancebw2points(wizardtower.Center,Hero.Position), Hero]

            for barbarian in Barbarian_list:
                dis = CentralProcessingUnit.Distancebw2points(wizardtower.Center,barbarian.Position)
                if(dis < ShortestDistance):
                    IsHero = False 
                    IsBarbarian = True
                    IsArcher = False
                    IsBalloon = False
                    [ShortestDistance, Troop] = [dis, barbarian]

            for archer in Archer_list:
                dis = CentralProcessingUnit.Distancebw2points(wizardtower.Center,archer.Position)
                if(dis < ShortestDistance):
                    IsHero = False 
                    IsArcher = True
                    IsBarbarian = False
                    IsBalloon = False
                    [ShortestDistance, Troop] = [dis, archer]

            for balloon in Balloon_list:
                dis = CentralProcessingUnit.Distancebw2points(wizardtower.Center,balloon.Position)
                if(dis < ShortestDistance):
                    IsHero = False 
                    IsBalloon = True
                    IsBarbarian = False
                    IsArcher = False
                    [ShortestDistance, Troop] = [dis, balloon]

            if(ShortestDistance < wizardtower.Range):        
                
                # Check AOERange for all troops                 
                IsHero = True 
                IsBarbarian = False
                IsArcher = False
                IsBalloon = False
                
                # King First
                [Distance,Troop_] = [CentralProcessingUnit.Distancebw2points(Troop.Position,Hero.Position), Hero]
                if(Distance<=wizardtower.AOERange):
                    Troop_.HealthLeft -= wizardtower.Damage 
                    wizardtower.SetColorBasedOnHealthLeft(Village,True)
                    
                    if(Troop_.HealthLeft < 0):
                        Troop_.HealthLeft = 0
                        filler = np.full((Troop_.SizeOfInfrastructure[0],Troop_.SizeOfInfrastructure[1]), Village.space)
                        Village.VillageLayout2DArray[Troop_.Position[0]:Troop_.Position[0]+Troop_.SizeOfInfrastructure[0],Troop_.Position[1]:Troop_.Position[1]+Troop_.SizeOfInfrastructure[1]] = filler
                        if(IsBarbarian):
                            Barbarian_list.remove(Troop_)
                        if(IsArcher):
                            Archer_list.remove(Troop_)

                # barbarian 
                for barbarian in Barbarian_list:
                    dis = CentralProcessingUnit.Distancebw2points(Troop.Position,barbarian.Position)
                    if(dis <= wizardtower.AOERange):
                        IsHero = False 
                        IsArcher = False
                        IsBarbarian = True
                        IsBalloon = False
                        [Distance, Troop_] = [dis, barbarian]
                         
                        Troop_.HealthLeft -= wizardtower.Damage 
                        wizardtower.SetColorBasedOnHealthLeft(Village,True)
                         
                        if(not IsHero):
                            Troop_.SetColorBasedOnHealthLeft()
                        
                        if(Troop_.HealthLeft < 0):
                            Troop_.HealthLeft = 0
                            filler = np.full((Troop_.SizeOfInfrastructure[0],Troop_.SizeOfInfrastructure[1]), Village.space)
                            Village.VillageLayout2DArray[Troop_.Position[0]:Troop_.Position[0]+Troop_.SizeOfInfrastructure[0],Troop_.Position[1]:Troop_.Position[1]+Troop_.SizeOfInfrastructure[1]] = filler
                            if(IsBarbarian):
                                Barbarian_list.remove(Troop_)
                            if(IsArcher):
                                Archer_list.remove(Troop_)
                
                # archer
                for archer in Archer_list:
                    dis = CentralProcessingUnit.Distancebw2points(Troop.Position,archer.Position)
                    if(dis <= wizardtower.AOERange):
                        IsHero = False 
                        IsBarbarian = False
                        IsArcher = True
                        IsBalloon = False
                        [Distance, Troop_] = [dis, archer]

                        Troop_.HealthLeft -= wizardtower.Damage 
                        wizardtower.SetColorBasedOnHealthLeft(Village,True)
                        if(not IsHero):
                            Troop_.SetColorBasedOnHealthLeft()
                        
                        if(Troop_.HealthLeft < 0):
                            Troop_.HealthLeft = 0
                            filler = np.full((Troop_.SizeOfInfrastructure[0],Troop_.SizeOfInfrastructure[1]), Village.space)
                            Village.VillageLayout2DArray[Troop_.Position[0]:Troop_.Position[0]+Troop_.SizeOfInfrastructure[0],Troop_.Position[1]:Troop_.Position[1]+Troop_.SizeOfInfrastructure[1]] = filler
                            if(IsBarbarian):
                                Barbarian_list.remove(Troop_)
                            if(IsArcher):
                                Archer_list.remove(Troop_)

                # balloon
                for balloon in Balloon_list:
                    dis = CentralProcessingUnit.Distancebw2points(Troop.Position,balloon.Position)
                    if(dis <= wizardtower.AOERange):
                        IsHero = False 
                        IsBalloon = True
                        IsBarbarian = False
                        IsArcher = False
                        [Distance, Troop_] = [dis, balloon]
                         
                        Troop_.HealthLeft -= wizardtower.Damage 
                        wizardtower.SetColorBasedOnHealthLeft(Village,True)
                         
                        if(not IsHero):
                            Troop_.SetColorBasedOnHealthLeft()
                        
                        if(Troop_.HealthLeft < 0):
                            Troop_.HealthLeft = 0
                            filler = np.full((Troop_.SizeOfInfrastructure[0],Troop_.SizeOfInfrastructure[1]), Troop_.OnTopSymbol)
                            Village.VillageLayout2DArray[Troop_.Position[0]:Troop_.Position[0]+Troop_.SizeOfInfrastructure[0],Troop_.Position[1]:Troop_.Position[1]+Troop_.SizeOfInfrastructure[1]] = filler
                            if(IsBarbarian):
                                Barbarian_list.remove(Troop_)
                            if(IsArcher):
                                Archer_list.remove(Troop_)
                            if(IsBalloon):
                                Balloon_list.remove(Troop_)
                
            else:
                wizardtower.SetColorBasedOnHealthLeft(Village,False)


        Village.UpdateCanvas()

        
        if( not(TownHall.HealthLeft>0 or Huts_list or Cannon_list or WizardTower_list) ):
            IsEnd = True
            Win = True
        elif( not(Hero.HealthLeft > 0 or Barbarian_list or Archer_list or Balloon_list) ):
            IsEnd = True
            Win = False
        else:
            IsEnd = False
            Win = False # no one cares whats here lets keep for continuity in return

        return [IsEnd,Win]
