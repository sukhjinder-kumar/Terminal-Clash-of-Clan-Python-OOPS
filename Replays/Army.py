from ctypes import sizeof
from re import T
from symtable import Symbol
from termios import PARODD
import warnings
from colorama import Back,Fore,Style
import numpy as np
import math

class Army:

    def __init__(self,SizeOfInfrastructure,Color):
        self.SizeOfInfrastructure = SizeOfInfrastructure
        self.Color = Color

class Troops(Army):

    def __init__(self,Position,PreviousPosition,Array2D,HitPoint,Damage,MovementSpeed,SizeOfInfrastructure,Color):
        super().__init__(SizeOfInfrastructure,Color)
        self.HitPoint = HitPoint 
        self.HealthLeft = self.HitPoint
        self.Damage = Damage 
        self.MovementSpeed = MovementSpeed 
        self.Position = Position
        self.PreviousPosition = PreviousPosition
        self.Array2D = Array2D

    def UpdateOnVillage(self,Village):
        Village.AddTroop(self)

class King(Troops):

    HitPoint = 500
    Damage = 40
    MovementSpeed = 3
    Size = [3,3]
    Color = Back.YELLOW + Fore.RED + Style.NORMAL

    def __init__(self,Position=None,HitPoint=None,Damage=None,MovementSpeed=None,SizeOfInfrastructure=None,Color=None):
        HitPoint_ = HitPoint or King.HitPoint
        Damage_ = Damage or King.Damage
        MovementSpeed_ = MovementSpeed or King.MovementSpeed
        Size_ = SizeOfInfrastructure or King.Size 
        Color_ = Color or King.Color
        Position_ = Position or [0,0]
        PreviousPosition_ = Position_

        self.Symbol = Color_ + "K" + Style.RESET_ALL
        King2DArray = np.full((Size_[0],Size_[1]), self.Symbol)
        self.AxeDamage = 40
        self.AxeRange = 5

        super().__init__(Position_,PreviousPosition_,King2DArray,HitPoint_,Damage_,MovementSpeed_,Size_,Color_)

    def KingHealthBar(self,Village):
        Symbol = Back.YELLOW + Fore.RED + Style.BRIGHT + " " + Style.RESET_ALL
        SymbolCanvas = Back.WHITE + Fore.WHITE + Style.NORMAL + " " + Style.RESET_ALL
        return np.hstack( (np.full((1,int(Village.VillageColumns/self.HitPoint*self.HealthLeft)), Symbol),np.full( (1,Village.VillageColumns-int(Village.VillageColumns/self.HitPoint*self.HealthLeft)), SymbolCanvas)) )

    def Move(self,key,Village):
        self.PreviousPosition = self.Position

        # up
        if(key == "w"):
            for i in range(0,self.MovementSpeed): 
                if(self.Position[0]-1 >= 0):
                    UpperSpaceArray = np.full((1,self.SizeOfInfrastructure[1]), Village.space)
                    if( (Village.VillageLayout2DArray[self.Position[0]-1:self.Position[0],self.Position[1]:self.Position[1]+self.SizeOfInfrastructure[1]] == UpperSpaceArray).all() ):
                        self.Position = [self.Position[0]-1,self.Position[1]]

        # down
        if(key == "s"):
            for i in range(0,self.MovementSpeed):
                if(self.Position[0]+self.SizeOfInfrastructure[0]-1+1 <= Village.VillageRows-1):
                    LowerSpaceArray = np.full((1,self.SizeOfInfrastructure[1]), Village.space)
                    if( (Village.VillageLayout2DArray[self.Position[0]+self.SizeOfInfrastructure[0]:self.Position[0]+self.SizeOfInfrastructure[0]+1,self.Position[1]:self.Position[1]+self.SizeOfInfrastructure[1]] == LowerSpaceArray).all() ):
                        self.Position = [self.Position[0]+1,self.Position[1]]

        # right
        if(key == "d"):
            for i in range(0,self.MovementSpeed):
                if(self.Position[1]+self.SizeOfInfrastructure[1]-1+1 <= Village.VillageColumns-1):
                    RightSpaceArray = np.full((self.SizeOfInfrastructure[0],1), Village.space)
                    if( (Village.VillageLayout2DArray[self.Position[0]:self.Position[0]+self.SizeOfInfrastructure[0],self.Position[1]+self.SizeOfInfrastructure[1]:self.Position[1]+self.SizeOfInfrastructure[1]+1] == RightSpaceArray).all() ):
                        self.Position = [self.Position[0],self.Position[1]+1]

        # left
        if(key == "a"):  
            for i in range(0,self.MovementSpeed):
                if(self.Position[1]-1 >= 0):
                    LeftSpaceArray = np.full((self.SizeOfInfrastructure[0],1), Village.space)
                    if( (Village.VillageLayout2DArray[self.Position[0]:self.Position[0]+self.SizeOfInfrastructure[0],self.Position[1]-1:self.Position[1]] == LeftSpaceArray).all() ):
                        self.Position = [self.Position[0],self.Position[1]-1] 

    def FindBuilding(self,InfrastructureType,Coordinates,TownHall,Huts_list,Walls_list,Cannon_list):
        if(InfrastructureType in [TownHall.ColorForCriticalStage1 + "T" + Style.RESET_ALL,TownHall.ColorForCriticalStage2 + "T" + Style.RESET_ALL,TownHall.ColorForCriticalStage3 + "T" + Style.RESET_ALL]):
            if(self.IsThisTheBuilding(TownHall,Coordinates)):
                return TownHall
        elif(Huts_list and InfrastructureType in [Huts_list[0].ColorForCriticalStage1 + "H" + Style.RESET_ALL,Huts_list[0].ColorForCriticalStage2 + "H" + Style.RESET_ALL,Huts_list[0].ColorForCriticalStage3 + "H" + Style.RESET_ALL]):
            for hut in Huts_list:
                if(self.IsThisTheBuilding(hut,Coordinates)):
                    return hut
        elif(Walls_list and InfrastructureType in [Walls_list[0].ColorForCriticalStage1 + "W" + Style.RESET_ALL,Walls_list[0].ColorForCriticalStage2 + "W" + Style.RESET_ALL,Walls_list[0].ColorForCriticalStage3 + "W" + Style.RESET_ALL]):
            for wall in Walls_list:
                if(self.IsThisTheBuilding(wall,Coordinates)):
                    return wall
        elif(Cannon_list and InfrastructureType in [Cannon_list[0].ColorForCriticalStage1 + "C" + Style.RESET_ALL,Cannon_list[0].ColorForCriticalStage2 + "C" + Style.RESET_ALL,Cannon_list[0].ColorForCriticalStage3 + "C" + Style.RESET_ALL,Back.CYAN + Fore.WHITE + Style.NORMAL + "C" + Style.RESET_ALL]):
            for cannon in Cannon_list:
                if(self.IsThisTheBuilding(cannon,Coordinates)):
                    return cannon
        else:
            pass

    def FindBuildingType(self,InfrastructureType,Coordinates,TownHall,Huts_list,Walls_list,Cannon_list):
        if(InfrastructureType in [TownHall.ColorForCriticalStage1 + "T" + Style.RESET_ALL,TownHall.ColorForCriticalStage2 + "T" + Style.RESET_ALL,TownHall.ColorForCriticalStage3 + "T" + Style.RESET_ALL]):
            if(self.IsThisTheBuilding(TownHall,Coordinates)):
                return "T"
        elif(Huts_list and InfrastructureType in [Huts_list[0].ColorForCriticalStage1 + "H" + Style.RESET_ALL,Huts_list[0].ColorForCriticalStage2 + "H" + Style.RESET_ALL,Huts_list[0].ColorForCriticalStage3 + "H" + Style.RESET_ALL]):
            for hut in Huts_list:
                if(self.IsThisTheBuilding(hut,Coordinates)):
                    return "H"
        elif(Walls_list and InfrastructureType in [Walls_list[0].ColorForCriticalStage1 + "W" + Style.RESET_ALL,Walls_list[0].ColorForCriticalStage2 + "W" + Style.RESET_ALL,Walls_list[0].ColorForCriticalStage3 + "W" + Style.RESET_ALL]):
            for wall in Walls_list:
                if(self.IsThisTheBuilding(wall,Coordinates)):
                    return "W"
        elif(Cannon_list and InfrastructureType in [Cannon_list[0].ColorForCriticalStage1 + "C" + Style.RESET_ALL,Cannon_list[0].ColorForCriticalStage2 + "C" + Style.RESET_ALL,Cannon_list[0].ColorForCriticalStage3 + "C" + Style.RESET_ALL, Back.CYAN + Fore.WHITE + Style.NORMAL + "C" + Style.RESET_ALL]):
            for cannon in Cannon_list:
                if(self.IsThisTheBuilding(cannon,Coordinates)):
                    return "C"
        else:
            pass
   
    def IsThisTheBuilding(self,Building,Coordinates):
        return (Coordinates[0]>=Building.StartingIndexOnVillage[0] and Coordinates[0]<=Building.StartingIndexOnVillage[0]+Building.SizeOfInfrastructure[0]-1 and Coordinates[1]>=Building.StartingIndexOnVillage[1] and Coordinates[1]<=Building.StartingIndexOnVillage[1]+Building.SizeOfInfrastructure[1]-1)

    def MakeChangesInBuilding(self,Building,BuildingType,Village,Huts_list,Walls_list,Cannon_list):
        if(not (Building is None)):
            Building.HealthLeft -= self.Damage
            if(Building.HealthLeft < 0):
                Building.HealthLeft = 0
        if(not (Building is None) and Building.HealthLeft > 0):
            Building.ColorBasedOnHitPoint = Building.DecideColorBasedOnHealthLeft()
            Building.Symbol = Building.ColorBasedOnHitPoint + BuildingType + Style.RESET_ALL
            Building.Array2D = np.full((Building.SizeOfInfrastructure[0],Building.SizeOfInfrastructure[1]), Building.Symbol)
            Building.UpdateOnVillage(Village)
        elif(not (Building is None)):
            filler = np.full((Building.SizeOfInfrastructure[0],Building.SizeOfInfrastructure[1]), Village.space)
            Village.VillageLayout2DArray[Building.StartingIndexOnVillage[0]:Building.StartingIndexOnVillage[0]+Building.SizeOfInfrastructure[0],Building.StartingIndexOnVillage[1]:Building.StartingIndexOnVillage[1]+Building.SizeOfInfrastructure[1]] = filler
            if(BuildingType == "H"):
                Huts_list.remove(Building)
            if(BuildingType == "W"):
                Walls_list.remove(Building)
            if(BuildingType == "C"):
                Cannon_list.remove(Building)
        else:
            pass
        
    def Attack(self,Village,TownHall,Huts_list,Walls_list,Cannon_list):

        # Upper Check First, followed by Right, bottom and then left
        
        if(self.Position[0] == 0 or self.Position[1] == 0 or self.Position[1]+self.SizeOfInfrastructure[1]-1 == Village.VillageColumns-1):
            if(self.Position[0] == 0):
                dummy1 = np.full((1,self.SizeOfInfrastructure[1]+2), Village.space).reshape(-1)
            elif(self.Position[1] == 0):
                temp = np.full((1,1), Village.space).reshape(-1)
                dummy1 = np.hstack( (temp,(Village.VillageLayout2DArray[self.Position[0]-1:self.Position[0],self.Position[1]:self.Position[1]+self.SizeOfInfrastructure[1]+1]).copy().reshape(-1)) )
            else:
                temp = np.full((1,1), Village.space).reshape(-1)
                dummy1 = np.hstack( ((Village.VillageLayout2DArray[self.Position[0]-1:self.Position[0],self.Position[1]-1:self.Position[1]+self.SizeOfInfrastructure[1]]).copy().reshape(-1),temp) )
        else:
            dummy1 = (Village.VillageLayout2DArray[self.Position[0]-1:self.Position[0],self.Position[1]-1:self.Position[1]+self.SizeOfInfrastructure[1]+1]).copy().reshape(-1)


        if(self.Position[1]+self.SizeOfInfrastructure[1]-1 == Village.VillageColumns-1):
            dummy2 = np.full((1,self.SizeOfInfrastructure[0]), Village.space).reshape(-1)
        else:
            dummy2 = (Village.VillageLayout2DArray[self.Position[0]:self.Position[0]+self.SizeOfInfrastructure[0],self.Position[1]+self.SizeOfInfrastructure[1]:self.Position[1]+self.SizeOfInfrastructure[1]+1]).copy().reshape(-1)


        if(self.Position[0]+self.SizeOfInfrastructure[0]-1 == Village.VillageRows-1 or self.Position[1] == 0 or self.Position[1]+self.SizeOfInfrastructure[1]-1 == Village.VillageColumns-1):
            if(self.Position[0]+self.SizeOfInfrastructure[0]-1 == Village.VillageRows-1):
                dummy3 = np.full((1,self.SizeOfInfrastructure[1]+2), Village.space).reshape(-1)
            elif(self.Position[1] == 0):
                temp = np.full((1,1), Village.space).reshape(-1)
                dummy3 = np.hstack( (temp,(Village.VillageLayout2DArray[self.Position[0]+self.SizeOfInfrastructure[0]:self.Position[0]+self.SizeOfInfrastructure[0]+1,self.Position[1]:self.Position[1]+self.SizeOfInfrastructure[1]+1]).copy().reshape(-1)) )
            else:
                temp = np.full((1,1), Village.space).reshape(-1)
                dummy3 = np.hstack( ((Village.VillageLayout2DArray[self.Position[0]+self.SizeOfInfrastructure[0]:self.Position[0]+self.SizeOfInfrastructure[0]+1,self.Position[1]-1:self.Position[1]+self.SizeOfInfrastructure[1]]).copy().reshape(-1),temp) )
        else:
            dummy3 = (Village.VillageLayout2DArray[self.Position[0]+self.SizeOfInfrastructure[0]:self.Position[0]+self.SizeOfInfrastructure[0]+1,self.Position[1]-1:self.Position[1]+self.SizeOfInfrastructure[1]+1]).copy().reshape(-1)
        
        if(self.Position[1] == 0):
            dummy4 = np.full((1,self.SizeOfInfrastructure[0]), Village.space).reshape(-1)
        else:
            dummy4 = (Village.VillageLayout2DArray[self.Position[0]:self.Position[0]+self.SizeOfInfrastructure[0],self.Position[1]-1:self.Position[1]]).copy().reshape(-1)

        dummy = np.hstack((dummy1,dummy2,dummy3,dummy4))
            
        InfrastructureType = Village.space
        countupper = 0
        countright = 0
        countlower = 0
        countleft = 0

        for i in range(0,2*self.SizeOfInfrastructure[1]+4+2*self.SizeOfInfrastructure[0]):
            ch = dummy[i]

            # upper
            if(i <= self.SizeOfInfrastructure[1]+1):
                if(ch != Village.space):
                    InfrastructureType = ch 
                    if(not(self.FindBuilding(InfrastructureType,[self.Position[0]-1,self.Position[1]-1+countupper],TownHall,Huts_list,Walls_list,Cannon_list) is None)):
                        Building = self.FindBuilding(InfrastructureType,[self.Position[0]-1,self.Position[1]-1+countupper],TownHall,Huts_list,Walls_list,Cannon_list)
                        BuildingType = self.FindBuildingType(InfrastructureType,[self.Position[0]-1,self.Position[1]-1+countupper],TownHall,Huts_list,Walls_list,Cannon_list)
                        self.MakeChangesInBuilding(Building,BuildingType,Village,Huts_list,Walls_list,Cannon_list)
                        break
                countupper += 1 
            
            # right
            elif(i > self.SizeOfInfrastructure[1]+1 and i <= self.SizeOfInfrastructure[1]+1+self.SizeOfInfrastructure[0]):
                if(ch != Village.space):
                    InfrastructureType = ch 
                    if(not(self.FindBuilding(InfrastructureType,[self.Position[0]+countright,self.Position[1]+self.SizeOfInfrastructure[0]],TownHall,Huts_list,Walls_list,Cannon_list) is None)):
                        Building = self.FindBuilding(InfrastructureType,[self.Position[0]+countright,self.Position[1]+self.SizeOfInfrastructure[0]],TownHall,Huts_list,Walls_list,Cannon_list)
                        BuildingType = self.FindBuildingType(InfrastructureType,[self.Position[0]+countright,self.Position[1]+self.SizeOfInfrastructure[0]],TownHall,Huts_list,Walls_list,Cannon_list)
                        self.MakeChangesInBuilding(Building,BuildingType,Village,Huts_list,Walls_list,Cannon_list)
                        break
                countright += 1 

            # lower
            elif(i > self.SizeOfInfrastructure[1]+1+self.SizeOfInfrastructure[0] and i <= 2*self.SizeOfInfrastructure[1]+1+self.SizeOfInfrastructure[0]+2):
                if(ch != Village.space):
                    InfrastructureType = ch 
                    if(not(self.FindBuilding(InfrastructureType,[self.Position[0]+self.SizeOfInfrastructure[0],self.Position[1]-1+countlower],TownHall,Huts_list,Walls_list,Cannon_list) is None)):
                        Building = self.FindBuilding(InfrastructureType,[self.Position[0]+self.SizeOfInfrastructure[0],self.Position[1]-1+countlower],TownHall,Huts_list,Walls_list,Cannon_list)
                        BuildingType = self.FindBuildingType(InfrastructureType,[self.Position[0]+self.SizeOfInfrastructure[0],self.Position[1]-1+countlower],TownHall,Huts_list,Walls_list,Cannon_list)
                        self.MakeChangesInBuilding(Building,BuildingType,Village,Huts_list,Walls_list,Cannon_list)
                        break
                countlower += 1 

            # left
            else:
                if(ch != Village.space):
                    InfrastructureType = ch 
                    if(not(self.FindBuilding(InfrastructureType,[self.Position[0]+countleft,self.Position[1]-1],TownHall,Huts_list,Walls_list,Cannon_list) is None)):
                        Building = self.FindBuilding(InfrastructureType,[self.Position[0]+countleft,self.Position[1]-1],TownHall,Huts_list,Walls_list,Cannon_list)
                        BuildingType = self.FindBuildingType(InfrastructureType,[self.Position[0]+countleft,self.Position[1]-1],TownHall,Huts_list,Walls_list,Cannon_list)
                        self.MakeChangesInBuilding(Building,BuildingType,Village,Huts_list,Walls_list,Cannon_list)
                        break
                countleft += 1 
        
    @staticmethod
    def Distancebw2points(pos1,pos2):
        return math.sqrt( (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 )

    def MakeChangesInBuildingOnAxeAttack(self,Village,Building,BuildingType,Huts_list,Cannon_list,Walls_list):
        Building.HealthLeft -= self.AxeDamage
        if(Building.HealthLeft < 0):
            Building.HealthLeft = 0
        if(Building.HealthLeft == 0):
            filler = np.full((Building.SizeOfInfrastructure[0],Building.SizeOfInfrastructure[1]), Village.space)
            Village.VillageLayout2DArray[Building.StartingIndexOnVillage[0]:Building.StartingIndexOnVillage[0]+Building.SizeOfInfrastructure[0],Building.StartingIndexOnVillage[1]:Building.StartingIndexOnVillage[1]+Building.SizeOfInfrastructure[1]] = filler
            if(BuildingType == "H"):
                Huts_list.remove(Building)
            if(BuildingType == "W"):
                Walls_list.remove(Building)
            if(BuildingType == "C"):
                Cannon_list.remove(Building)
        if(Building.HealthLeft > 0):
            Building.ColorBasedOnHitPoint = Building.DecideColorBasedOnHealthLeft()
            Building.Symbol = Building.ColorBasedOnHitPoint + BuildingType + Style.RESET_ALL
            Building.Array2D = np.full((Building.SizeOfInfrastructure[0],Building.SizeOfInfrastructure[1]), Building.Symbol)
            Building.UpdateOnVillage(Village)

    def Axe(self,Village,TownHall,Huts_list,Walls_list,Cannon_list):

        if(King.Distancebw2points(self.Position,TownHall.Center) <= self.AxeRange):
            self.MakeChangesInBuildingOnAxeAttack(Village,TownHall,"T",Huts_list,Cannon_list,Walls_list)

        for hut in Huts_list:
            if(King.Distancebw2points(self.Position,hut.Center) <= self.AxeRange):
                self.MakeChangesInBuildingOnAxeAttack(Village,hut,"H",Huts_list,Cannon_list,Walls_list)
        
        for wall in Walls_list:
            if(King.Distancebw2points(self.Position,wall.Center) <= self.AxeRange):
                self.MakeChangesInBuildingOnAxeAttack(Village,wall,"W",Huts_list,Cannon_list,Walls_list)
        
        for cannon in Cannon_list:
            if(King.Distancebw2points(self.Position,cannon.Center) <= self.AxeRange):
                self.MakeChangesInBuildingOnAxeAttack(Village,cannon,"C",Huts_list,Cannon_list,Walls_list)
        

    
class BarBarian(Troops):

    HitPoint = 100
    Damage = 10
    MovementSpeed = 3
    Size = [1,1]
    ColorForCriticalStage1 = Back.WHITE + Fore.WHITE + Style.DIM
    ColorForCriticalStage2 = Back.WHITE + Fore.WHITE + Style.NORMAL
    ColorForCriticalStage3 = Back.WHITE + Fore.WHITE + Style.BRIGHT

    def __init__(self,Position,HitPoint=None,Damage=None,MovementSpeed=None,SizeOfInfrastructure=None,Color=None):
        HitPoint_ = HitPoint or BarBarian.HitPoint
        Damage_ = Damage or BarBarian.Damage
        MovementSpeed_ = MovementSpeed or BarBarian.MovementSpeed
        Size_ = SizeOfInfrastructure or BarBarian.Size 
        Color_ = Color or BarBarian.ColorForCriticalStage1
        Position_ = Position
        PreviousPosition_ = Position_

        self.Symbol = Color_ + "B" + Style.RESET_ALL
        Barbarian2DArray = np.full((Size_[0],Size_[1]), self.Symbol)

        super().__init__(Position_,PreviousPosition_,Barbarian2DArray,HitPoint_,Damage_,MovementSpeed_,Size_,Color_)

    def SetColorBasedOnHealthLeft(self):
        if(self.HealthLeft<=self.HitPoint and self.HealthLeft>=int(self.HitPoint/2)):
            self.Symbol = self.ColorForCriticalStage1 + "B" + Style.RESET_ALL
            self.Array2D = np.full((self.SizeOfInfrastructure[0],self.SizeOfInfrastructure[1]), self.Symbol)
        if(self.HealthLeft<=int(self.HitPoint/2) and self.HealthLeft>=int(self.HitPoint/5)):
            self.Symbol = self.ColorForCriticalStage2 + "B" + Style.RESET_ALL
            self.Array2D = np.full((self.SizeOfInfrastructure[0],self.SizeOfInfrastructure[1]), self.Symbol)
        if(self.HealthLeft<=int(self.HitPoint/5) and self.HealthLeft>=0):
            self.Symbol = self.ColorForCriticalStage3 + "B" + Style.RESET_ALL
            self.Array2D = np.full((self.SizeOfInfrastructure[0],self.SizeOfInfrastructure[1]), self.Symbol)
    
    def IsBuilding(self,InfrastructureType,Walls_list,TownHall,Cannon_list,Huts_list):
        return ( (Walls_list and InfrastructureType in [Walls_list[0].ColorForCriticalStage1 + "W" + Style.RESET_ALL,Walls_list[0].ColorForCriticalStage2 + "W" + Style.RESET_ALL,Walls_list[0].ColorForCriticalStage3 + "W" + Style.RESET_ALL]) or (InfrastructureType in [TownHall.ColorForCriticalStage1 + "T" + Style.RESET_ALL,TownHall.ColorForCriticalStage2 + "T" + Style.RESET_ALL,TownHall.ColorForCriticalStage3 + "T" + Style.RESET_ALL]) or (Huts_list and InfrastructureType in [Huts_list[0].ColorForCriticalStage1 + "H" + Style.RESET_ALL,Huts_list[0].ColorForCriticalStage2 + "H" + Style.RESET_ALL,Huts_list[0].ColorForCriticalStage3 + "H" + Style.RESET_ALL]) or (Cannon_list and InfrastructureType in [Cannon_list[0].ColorForCriticalStage1 + "C" + Style.RESET_ALL,Cannon_list[0].ColorForCriticalStage2 + "C" + Style.RESET_ALL,Cannon_list[0].ColorForCriticalStage3 + "C" + Style.RESET_ALL, Back.CYAN + Fore.WHITE + Style.NORMAL + "C" + Style.RESET_ALL]) or (InfrastructureType == (Back.YELLOW + Fore.RED + Style.NORMAL + "K" + Style.RESET_ALL) ) )

    def Move(self, Building, Village, Walls_list, TownHall, Cannon_list, Huts_list):

        self.PreviousPosition = self.Position

        for i in range(0,self.MovementSpeed):
            
            # up
            if(self.Position[0] > Building.Center[0]+1 and self.Position[1] == Building.Center[1]):
                # No boundary check as can't cross village, building can't come in bw, and can overlap barbarian and don't do anything if just standing in front, wait for it to be killed
                if(not self.IsBuilding(Village.VillageLayout2DArray[self.Position[0]-1][self.Position[1]],Walls_list,TownHall,Cannon_list,Huts_list)):
                    self.Position = [self.Position[0]-1,self.Position[1]]

            # up right
            if(self.Position[0] > Building.Center[0] and self.Position[1] < Building.Center[1]):
                if(not(self.Position[0]-1 == Building.Center[0] and self.Position[1]+1 == Building.Center[1])):
                    if(not self.IsBuilding(Village.VillageLayout2DArray[self.Position[0]-1][self.Position[1]+1],Walls_list,TownHall,Cannon_list,Huts_list)):
                        self.Position = [self.Position[0]-1,self.Position[1]+1]

            # right 
            if(self.Position[0] == Building.Center[0] and self.Position[1] < Building.Center[1]-1):
                if(not self.IsBuilding(Village.VillageLayout2DArray[self.Position[0]][self.Position[1]+1],Walls_list,TownHall,Cannon_list,Huts_list)):
                    self.Position = [self.Position[0],self.Position[1]+1]

            # down right
            if(self.Position[0] < Building.Center[0] and self.Position[1] < Building.Center[1]):
                if(not(self.Position[0]+1 == Building.Center[0] and self.Position[1]+1 == Building.Center[1])):
                    if(not self.IsBuilding(Village.VillageLayout2DArray[self.Position[0]+1][self.Position[1]+1],Walls_list,TownHall,Cannon_list,Huts_list)):
                        self.Position = [self.Position[0]+1,self.Position[1]+1]

            # down
            if(self.Position[0] < Building.Center[0]-1 and self.Position[1] == Building.Center[1]):
                if(not self.IsBuilding(Village.VillageLayout2DArray[self.Position[0]+1][self.Position[1]],Walls_list,TownHall,Cannon_list,Huts_list)):
                    self.Position = [self.Position[0]+1,self.Position[1]]

            # down left
            if(self.Position[0] < Building.Center[0] and self.Position[1] > Building.Center[1]):
                if(not(self.Position[0]+1 == Building.Center[0] and self.Position[1]-1 == Building.Center[1])):
                    if(not self.IsBuilding(Village.VillageLayout2DArray[self.Position[0]+1][self.Position[1]-1],Walls_list,TownHall,Cannon_list,Huts_list)):
                        self.Position = [self.Position[0]+1,self.Position[1]-1]

            # left
            if(self.Position[0] == Building.Center[0] and self.Position[1] > Building.Center[1]+1):
                if(not self.IsBuilding(Village.VillageLayout2DArray[self.Position[0]][self.Position[1]-1],Walls_list,TownHall,Cannon_list,Huts_list)):
                    self.Position = [self.Position[0],self.Position[1]-1]

            # up left
            if(self.Position[0] > Building.Center[0] and self.Position[1] > Building.Center[1]):
                if(not(self.Position[0]-1 == Building.Center[0] and self.Position[1]-1 == Building.Center[1])):
                    if(not self.IsBuilding(Village.VillageLayout2DArray[self.Position[0]-1][self.Position[1]-1],Walls_list,TownHall,Cannon_list,Huts_list)):
                        self.Position = [self.Position[0]-1,self.Position[1]-1]

        self.UpdateOnVillage(Village) 

    def FindBuilding(self,InfrastructureType,Coordinates,TownHall,Huts_list,Walls_list,Cannon_list):
        if(InfrastructureType in [TownHall.ColorForCriticalStage1 + "T" + Style.RESET_ALL,TownHall.ColorForCriticalStage2 + "T" + Style.RESET_ALL,TownHall.ColorForCriticalStage3 + "T" + Style.RESET_ALL]):
            if(self.IsThisTheBuilding(TownHall,Coordinates)):
                return TownHall
        elif(Huts_list and InfrastructureType in [Huts_list[0].ColorForCriticalStage1 + "H" + Style.RESET_ALL,Huts_list[0].ColorForCriticalStage2 + "H" + Style.RESET_ALL,Huts_list[0].ColorForCriticalStage3 + "H" + Style.RESET_ALL]):
            for hut in Huts_list:
                if(self.IsThisTheBuilding(hut,Coordinates)):
                    return hut
        elif(Walls_list and InfrastructureType in [Walls_list[0].ColorForCriticalStage1 + "W" + Style.RESET_ALL,Walls_list[0].ColorForCriticalStage2 + "W" + Style.RESET_ALL,Walls_list[0].ColorForCriticalStage3 + "W" + Style.RESET_ALL]):
            for wall in Walls_list:
                if(self.IsThisTheBuilding(wall,Coordinates)):
                    return wall
        elif(Cannon_list and InfrastructureType in [Cannon_list[0].ColorForCriticalStage1 + "C" + Style.RESET_ALL,Cannon_list[0].ColorForCriticalStage2 + "C" + Style.RESET_ALL,Cannon_list[0].ColorForCriticalStage3 + "C" + Style.RESET_ALL, Back.CYAN + Fore.WHITE + Style.NORMAL + "C" + Style.RESET_ALL]):
            for cannon in Cannon_list:
                if(self.IsThisTheBuilding(cannon,Coordinates)):
                    return cannon
        else:
            pass

    def FindBuildingType(self,InfrastructureType,Coordinates,TownHall,Huts_list,Walls_list,Cannon_list):
        if(InfrastructureType in [TownHall.ColorForCriticalStage1 + "T" + Style.RESET_ALL,TownHall.ColorForCriticalStage2 + "T" + Style.RESET_ALL,TownHall.ColorForCriticalStage3 + "T" + Style.RESET_ALL]):
            if(self.IsThisTheBuilding(TownHall,Coordinates)):
                return "T"
        elif(Huts_list and InfrastructureType in [Huts_list[0].ColorForCriticalStage1 + "H" + Style.RESET_ALL,Huts_list[0].ColorForCriticalStage2 + "H" + Style.RESET_ALL,Huts_list[0].ColorForCriticalStage3 + "H" + Style.RESET_ALL]):
            for hut in Huts_list:
                if(self.IsThisTheBuilding(hut,Coordinates)):
                    return "H"
        elif(Walls_list and InfrastructureType in [Walls_list[0].ColorForCriticalStage1 + "W" + Style.RESET_ALL,Walls_list[0].ColorForCriticalStage2 + "W" + Style.RESET_ALL,Walls_list[0].ColorForCriticalStage3 + "W" + Style.RESET_ALL]):
            for wall in Walls_list:
                if(self.IsThisTheBuilding(wall,Coordinates)):
                    return "W"
        elif(Cannon_list and InfrastructureType in [Cannon_list[0].ColorForCriticalStage1 + "C" + Style.RESET_ALL,Cannon_list[0].ColorForCriticalStage2 + "C" + Style.RESET_ALL,Cannon_list[0].ColorForCriticalStage3 + "C" + Style.RESET_ALL, Back.CYAN + Fore.WHITE + Style.NORMAL + "C" + Style.RESET_ALL]):
            for cannon in Cannon_list:
                if(self.IsThisTheBuilding(cannon,Coordinates)):
                    return "C"
        else:
            pass
   
    def IsThisTheBuilding(self,Building,Coordinates):
        return (Coordinates[0]>=Building.StartingIndexOnVillage[0] and Coordinates[0]<=Building.StartingIndexOnVillage[0]+Building.SizeOfInfrastructure[0]-1 and Coordinates[1]>=Building.StartingIndexOnVillage[1] and Coordinates[1]<=Building.StartingIndexOnVillage[1]+Building.SizeOfInfrastructure[1]-1)

    def MakeChangesInBuilding(self,Building,BuildingType,Village,Huts_list,Walls_list,Cannon_list):
        if(not (Building is None)):
            Building.HealthLeft -= self.Damage
        if(not (Building is None) and Building.HealthLeft > 0):
            Building.ColorBasedOnHitPoint = Building.DecideColorBasedOnHealthLeft()
            Building.Symbol = Building.ColorBasedOnHitPoint + BuildingType + Style.RESET_ALL
            Building.Array2D = np.full((Building.SizeOfInfrastructure[0],Building.SizeOfInfrastructure[1]), Building.Symbol)
            Building.UpdateOnVillage(Village)
        elif(not (Building is None)):
            filler = np.full((Building.SizeOfInfrastructure[0],Building.SizeOfInfrastructure[1]), Village.space)
            Village.VillageLayout2DArray[Building.StartingIndexOnVillage[0]:Building.StartingIndexOnVillage[0]+Building.SizeOfInfrastructure[0],Building.StartingIndexOnVillage[1]:Building.StartingIndexOnVillage[1]+Building.SizeOfInfrastructure[1]] = filler
            if(BuildingType == "H"):
                Huts_list.remove(Building)
            if(BuildingType == "W"):
                Walls_list.remove(Building)
            if(BuildingType == "C"):
                Cannon_list.remove(Building)
        else:
            pass
        
    def Attack(self,Village,TownHall,Huts_list,Walls_list,Cannon_list):

        # Upper Check First, followed by Right, bottom and then left
        
        if(self.Position[0] == 0 or self.Position[1] == 0 or self.Position[1]+self.SizeOfInfrastructure[1]-1 == Village.VillageColumns-1):
            if(self.Position[0] == 0):
                dummy1 = np.full((1,self.SizeOfInfrastructure[1]+2), Village.space).reshape(-1)
            elif(self.Position[1] == 0):
                temp = np.full((1,1), Village.space).reshape(-1)
                dummy1 = np.hstack( (temp,(Village.VillageLayout2DArray[self.Position[0]-1:self.Position[0],self.Position[1]:self.Position[1]+self.SizeOfInfrastructure[1]+1]).copy().reshape(-1)) )
            else:
                temp = np.full((1,1), Village.space).reshape(-1)
                dummy1 = np.hstack( ((Village.VillageLayout2DArray[self.Position[0]-1:self.Position[0],self.Position[1]-1:self.Position[1]+self.SizeOfInfrastructure[1]]).copy().reshape(-1),temp) )
        else:
            dummy1 = (Village.VillageLayout2DArray[self.Position[0]-1:self.Position[0],self.Position[1]-1:self.Position[1]+self.SizeOfInfrastructure[1]+1]).copy().reshape(-1)


        if(self.Position[1]+self.SizeOfInfrastructure[1]-1 == Village.VillageColumns-1):
            dummy2 = np.full((1,self.SizeOfInfrastructure[0]), Village.space).reshape(-1)
        else:
            dummy2 = (Village.VillageLayout2DArray[self.Position[0]:self.Position[0]+self.SizeOfInfrastructure[0],self.Position[1]+self.SizeOfInfrastructure[1]:self.Position[1]+self.SizeOfInfrastructure[1]+1]).copy().reshape(-1)


        if(self.Position[0]+self.SizeOfInfrastructure[0]-1 == Village.VillageRows-1 or self.Position[1] == 0 or self.Position[1]+self.SizeOfInfrastructure[1]-1 == Village.VillageColumns-1):
            if(self.Position[0]+self.SizeOfInfrastructure[0]-1 == Village.VillageRows-1):
                dummy3 = np.full((1,self.SizeOfInfrastructure[1]+2), Village.space).reshape(-1)
            elif(self.Position[1] == 0):
                temp = np.full((1,1), Village.space).reshape(-1)
                dummy3 = np.hstack( (temp,(Village.VillageLayout2DArray[self.Position[0]+self.SizeOfInfrastructure[0]:self.Position[0]+self.SizeOfInfrastructure[0]+1,self.Position[1]:self.Position[1]+self.SizeOfInfrastructure[1]+1]).copy().reshape(-1)) )
            else:
                temp = np.full((1,1), Village.space).reshape(-1)
                dummy3 = np.hstack( ((Village.VillageLayout2DArray[self.Position[0]+self.SizeOfInfrastructure[0]:self.Position[0]+self.SizeOfInfrastructure[0]+1,self.Position[1]-1:self.Position[1]+self.SizeOfInfrastructure[1]]).copy().reshape(-1),temp) )
        else:
            dummy3 = (Village.VillageLayout2DArray[self.Position[0]+self.SizeOfInfrastructure[0]:self.Position[0]+self.SizeOfInfrastructure[0]+1,self.Position[1]-1:self.Position[1]+self.SizeOfInfrastructure[1]+1]).copy().reshape(-1)
        
        if(self.Position[1] == 0):
            dummy4 = np.full((1,self.SizeOfInfrastructure[0]), Village.space).reshape(-1)
        else:
            dummy4 = (Village.VillageLayout2DArray[self.Position[0]:self.Position[0]+self.SizeOfInfrastructure[0],self.Position[1]-1:self.Position[1]]).copy().reshape(-1)

        dummy = np.hstack((dummy1,dummy2,dummy3,dummy4))
            
        InfrastructureType = Village.space
        countupper = 0
        countright = 0
        countlower = 0
        countleft = 0

        for i in range(0,2*self.SizeOfInfrastructure[1]+4+2*self.SizeOfInfrastructure[0]):
            ch = dummy[i]

            # upper
            if(i <= self.SizeOfInfrastructure[1]+1):
                if(ch != Village.space):
                    InfrastructureType = ch 
                    if(not(self.FindBuilding(InfrastructureType,[self.Position[0]-1,self.Position[1]-1+countupper],TownHall,Huts_list,Walls_list,Cannon_list) is None)):
                        Building = self.FindBuilding(InfrastructureType,[self.Position[0]-1,self.Position[1]-1+countupper],TownHall,Huts_list,Walls_list,Cannon_list)
                        BuildingType = self.FindBuildingType(InfrastructureType,[self.Position[0]-1,self.Position[1]-1+countupper],TownHall,Huts_list,Walls_list,Cannon_list)
                        self.MakeChangesInBuilding(Building,BuildingType,Village,Huts_list,Walls_list,Cannon_list)
                        break
                countupper += 1 
            
            # right
            elif(i > self.SizeOfInfrastructure[1]+1 and i <= self.SizeOfInfrastructure[1]+1+self.SizeOfInfrastructure[0]):
                if(ch != Village.space):
                    InfrastructureType = ch 
                    if(not(self.FindBuilding(InfrastructureType,[self.Position[0]+countright,self.Position[1]+self.SizeOfInfrastructure[0]],TownHall,Huts_list,Walls_list,Cannon_list) is None)):
                        Building = self.FindBuilding(InfrastructureType,[self.Position[0]+countright,self.Position[1]+self.SizeOfInfrastructure[0]],TownHall,Huts_list,Walls_list,Cannon_list)
                        BuildingType = self.FindBuildingType(InfrastructureType,[self.Position[0]+countright,self.Position[1]+self.SizeOfInfrastructure[0]],TownHall,Huts_list,Walls_list,Cannon_list)
                        self.MakeChangesInBuilding(Building,BuildingType,Village,Huts_list,Walls_list,Cannon_list)
                        break
                countright += 1 

            # lower
            elif(i > self.SizeOfInfrastructure[1]+1+self.SizeOfInfrastructure[0] and i <= 2*self.SizeOfInfrastructure[1]+1+self.SizeOfInfrastructure[0]+2):
                if(ch != Village.space):
                    InfrastructureType = ch 
                    if(not(self.FindBuilding(InfrastructureType,[self.Position[0]+self.SizeOfInfrastructure[0],self.Position[1]-1+countlower],TownHall,Huts_list,Walls_list,Cannon_list) is None)):
                        Building = self.FindBuilding(InfrastructureType,[self.Position[0]+self.SizeOfInfrastructure[0],self.Position[1]-1+countlower],TownHall,Huts_list,Walls_list,Cannon_list)
                        BuildingType = self.FindBuildingType(InfrastructureType,[self.Position[0]+self.SizeOfInfrastructure[0],self.Position[1]-1+countlower],TownHall,Huts_list,Walls_list,Cannon_list)
                        self.MakeChangesInBuilding(Building,BuildingType,Village,Huts_list,Walls_list,Cannon_list)
                        break
                countlower += 1 

            # left
            else:
                if(ch != Village.space):
                    InfrastructureType = ch 
                    if(not(self.FindBuilding(InfrastructureType,[self.Position[0]+countleft,self.Position[1]-1],TownHall,Huts_list,Walls_list,Cannon_list) is None)):
                        Building = self.FindBuilding(InfrastructureType,[self.Position[0]+countleft,self.Position[1]-1],TownHall,Huts_list,Walls_list,Cannon_list)
                        BuildingType = self.FindBuildingType(InfrastructureType,[self.Position[0]+countleft,self.Position[1]-1],TownHall,Huts_list,Walls_list,Cannon_list)
                        self.MakeChangesInBuilding(Building,BuildingType,Village,Huts_list,Walls_list,Cannon_list)
                        break
                countleft += 1 
      
class Spell():
    def __init__(self,name):
        self.name = name 
    
    def Action(self,King,Barbarian_list):
        print("Nothing assigned yet")

class Rage(Spell):

    def __init__(self):
        super().__init__("Rage")

    @classmethod
    def Action(cls,King,Barbarian_list):
        King.Damage *= 2
        King.AxeDamage *= 2
        King.MovementSpeed *= 2

        for barbarian in Barbarian_list:
            barbarian.Damage *= 2  
            barbarian.MovementSpeed *= 2

class Healing(Spell):
    def __init__(self):
        super().__init__("Healing")

    @classmethod
    def Action(cls,King,Barbarian_list):
        King.HealthLeft = min(int(1.5*King.HealthLeft),King.HitPoint)
        for barbarian in Barbarian_list:
            barbarian.HealthLeft = min(int(1.5*barbarian.HealthLeft),barbarian.HitPoint)