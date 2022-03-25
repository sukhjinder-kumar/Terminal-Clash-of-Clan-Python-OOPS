import warnings
from colorama import Back, Fore, Style
import numpy as np

class Infrastructure:

    def __init__(self,HitPoint,SizeOfInfrastructure=None,ColorForCriticalStage1=None,ColorForCriticalStage2=None,ColorForCriticalStage3=None):
        self.MaxHitPoint = HitPoint or 100
        self.HealthLeft = self.MaxHitPoint
        self.ColorForCriticalStage1 = ColorForCriticalStage1 or Back.GREEN + Fore.RED + Style.DIM
        self.ColorForCriticalStage2 = ColorForCriticalStage2 or Back.RED + Fore.RED + Style.NORMAL
        self.ColorForCriticalStage3 = ColorForCriticalStage3 or Back.YELLOW + Fore.RED + Style.BRIGHT
        self.ColorBasedOnHitPoint = self.ColorForCriticalStage1 
        self.SizeOfInfrastructure = SizeOfInfrastructure or [1,1]

    def DecideColorBasedOnHealthLeft(self):
        if(self.HealthLeft<=self.MaxHitPoint and self.HealthLeft>=int(self.MaxHitPoint/2)):
            return self.ColorForCriticalStage1
        if(self.HealthLeft<=int(self.MaxHitPoint/2) and self.HealthLeft>=int(self.MaxHitPoint/5)):
            return self.ColorForCriticalStage2
        if(self.HealthLeft<=int(self.MaxHitPoint/5) and self.HealthLeft>=0):
            return self.ColorForCriticalStage3 


# I made it seprate say, like king as a defender can move so Starting index is mobile.
class Building(Infrastructure):

    def __init__(self,HitPoint,StartingIndexOnVillage,Array2D,SizeOfInfrastructure=None,ColorForCriticalStage1=None,ColorForCriticalStage2=None,ColorForCriticalStage3=None):
        super().__init__(HitPoint,SizeOfInfrastructure,ColorForCriticalStage1,ColorForCriticalStage2,ColorForCriticalStage3)
        self.StartingIndexOnVillage = StartingIndexOnVillage 
        self.Center = [self.StartingIndexOnVillage[0]+int(self.SizeOfInfrastructure[0]/2),self.StartingIndexOnVillage[1]+int(self.SizeOfInfrastructure[1]/2)]
        self.Array2D = Array2D

    def UpdateOnVillage(self, Village):
        Village.AddBuildingOrWeaponToVillage(self)


class TownHall(Building):

    NumberOfTownHall = 0
    ColorForCriticalStage1 = Back.GREEN + Fore.RED + Style.DIM
    ColorForCriticalStage2 = Back.GREEN + Fore.RED + Style.NORMAL
    ColorForCriticalStage3 = Back.GREEN + Fore.RED + Style.BRIGHT
    HitPoint = 1000
    Size = [3,8]

    def __init__(self,StartingIndexOnVillage,HitPoint=None,SizeOfInfrastructure=None,ColorForCriticalStage1=None,ColorForCriticalStage2=None,ColorForCriticalStage3=None):
        Color_For_Critical_Stage1 = ColorForCriticalStage1 or TownHall.ColorForCriticalStage1
        Color_For_Critical_Stage2 = ColorForCriticalStage2 or TownHall.ColorForCriticalStage2
        Color_For_Critical_Stage3 = ColorForCriticalStage3 or TownHall.ColorForCriticalStage3
        Hit_Point = HitPoint or TownHall.HitPoint 
        Size_ = SizeOfInfrastructure or TownHall.Size 
        
        self.Symbol = Color_For_Critical_Stage1 + "T" + Style.RESET_ALL
        self.TownHall2DArray = np.full((Size_[0],Size_[1]), self.Symbol)

        super().__init__(Hit_Point,StartingIndexOnVillage,self.TownHall2DArray,Size_,Color_For_Critical_Stage1,Color_For_Critical_Stage2,Color_For_Critical_Stage3)

        TownHall.AddOneTownHall()
        if(TownHall.NumberOfTownHall > 1):
            warnings.warn("You have more than 1 Town Hall")

    @classmethod
    def AddOneTownHall(cls):
        TownHall.NumberOfTownHall += 1      


class Huts(Building):

    NumberOfHuts = 0
    ColorForCriticalStage1 = Back.CYAN + Fore.MAGENTA + Style.DIM
    ColorForCriticalStage2 = Back.CYAN + Fore.MAGENTA + Style.NORMAL
    ColorForCriticalStage3 = Back.CYAN + Fore.MAGENTA + Style.BRIGHT
    HitPoint = 100
    Size = [2,3]

    def __init__(self,StartingIndexOnVillage,HitPoint=None,SizeOfInfrastructure=None,ColorForCriticalStage1=None,ColorForCriticalStage2=None,ColorForCriticalStage3=None):
        Color_For_Critical_Stage1 = ColorForCriticalStage1 or Huts.ColorForCriticalStage1
        Color_For_Critical_Stage2 = ColorForCriticalStage2 or Huts.ColorForCriticalStage2
        Color_For_Critical_Stage3 = ColorForCriticalStage3 or Huts.ColorForCriticalStage3
        Hit_Point = HitPoint or Huts.HitPoint 
        Size_ = SizeOfInfrastructure or Huts.Size 
        
        self.Symbol = Color_For_Critical_Stage1 + "H" + Style.RESET_ALL
        self.Huts2DArray = np.full((Size_[0],Size_[1]), self.Symbol)

        super().__init__(Hit_Point,StartingIndexOnVillage,self.Huts2DArray,Size_,Color_For_Critical_Stage1,Color_For_Critical_Stage2,Color_For_Critical_Stage3)

        Huts.AddOneHut()


    @classmethod
    def AddOneHut(cls):
        Huts.NumberOfHuts += 1  


class Walls(Building):

    NumberOfWalls = 0
    ColorForCriticalStage1 = Back.RED + Fore.YELLOW + Style.DIM
    ColorForCriticalStage2 = Back.RED + Fore.YELLOW + Style.NORMAL
    ColorForCriticalStage3 = Back.RED + Fore.YELLOW + Style.BRIGHT
    HitPoint = 50
    Size = [1,1]

    def __init__(self,StartingIndexOnVillage,HitPoint=None,SizeOfInfrastructure=None,ColorForCriticalStage1=None,ColorForCriticalStage2=None,ColorForCriticalStage3=None):
        Color_For_Critical_Stage1 = ColorForCriticalStage1 or Walls.ColorForCriticalStage1
        Color_For_Critical_Stage2 = ColorForCriticalStage2 or Walls.ColorForCriticalStage2
        Color_For_Critical_Stage3 = ColorForCriticalStage3 or Walls.ColorForCriticalStage3
        Hit_Point = HitPoint or Walls.HitPoint 
        Size_ = SizeOfInfrastructure or Walls.Size 
        
        self.Symbol = Color_For_Critical_Stage1 + "W" + Style.RESET_ALL
        self.Walls2DArray = np.full((Size_[0],Size_[1]), self.Symbol)

        super().__init__(Hit_Point,StartingIndexOnVillage,self.Walls2DArray,Size_,Color_For_Critical_Stage1,Color_For_Critical_Stage2,Color_For_Critical_Stage3)

        Walls.AddOneWall()


    @classmethod
    def AddOneWall(cls):
        Walls.NumberOfWalls += 1  


class Weapons(Infrastructure):
    def __init__(self,HitPoint,Damage,Range,Center,StartingIndexOnVillage,Array2D,SizeOfInfrastructure=None,ColorForCriticalStage1=None,ColorForCriticalStage2=None,ColorForCriticalStage3=None):
        super().__init__(HitPoint,SizeOfInfrastructure,ColorForCriticalStage1,ColorForCriticalStage2,ColorForCriticalStage3)
        self.StartingIndexOnVillage = StartingIndexOnVillage 
        self.Array2D = Array2D
        self.Damage = Damage
        self.Center = Center 
        self.Range = Range # Int, distance measured from center of weapon, make center too

    def UpdateOnVillage(self, Village):
        Village.AddBuildingOrWeaponToVillage(self) 


class Cannon(Weapons):

    NumberOfCannon = 0
    ColorForCriticalStage1 = Back.BLUE + Fore.YELLOW + Style.DIM
    ColorForCriticalStage2 = Back.BLUE + Fore.YELLOW + Style.NORMAL
    ColorForCriticalStage3 = Back.BLUE + Fore.YELLOW + Style.BRIGHT
    ColorWhileAttacking = Back.CYAN + Fore.WHITE + Style.NORMAL
    HitPoint = 200
    Size = [3,3]
    Damage = 10
    Range = 6

    def __init__(self,StartingIndexOnVillage,Damage=None,Range=None,HitPoint=None,SizeOfInfrastructure=None,ColorForCriticalStage1=None,ColorForCriticalStage2=None,ColorForCriticalStage3=None):
        Color_For_Critical_Stage1 = ColorForCriticalStage1 or Cannon.ColorForCriticalStage1
        Color_For_Critical_Stage2 = ColorForCriticalStage2 or Cannon.ColorForCriticalStage2
        Color_For_Critical_Stage3 = ColorForCriticalStage3 or Cannon.ColorForCriticalStage3
        self.ColorWhileAttacking = Cannon.ColorWhileAttacking
        Hit_Point = HitPoint or Cannon.HitPoint 
        Size_ = SizeOfInfrastructure or Cannon.Size 
        Damage_ = Damage or Cannon.Damage
        Range_ = Range or Cannon.Range
        Center = [StartingIndexOnVillage[0]+int(Size_[0]/2),StartingIndexOnVillage[1]+int(Size_[1]/2)]
        
        self.Symbol = Color_For_Critical_Stage1 + "C" + Style.RESET_ALL
        Cannon2DArray_ = np.full((Size_[0],Size_[1]), self.Symbol)

        super().__init__(Hit_Point,Damage_,Range_,Center,StartingIndexOnVillage,Cannon2DArray_,Size_,Color_For_Critical_Stage1,Color_For_Critical_Stage2,Color_For_Critical_Stage3)

        Cannon.AddOneCannon()

    def SetColorBasedOnHealthLeft(self,Village,IsAttacking):
        if(IsAttacking):
            self.Symbol = self.ColorWhileAttacking + "C" + Style.RESET_ALL
            self.Array2D = np.full((self.SizeOfInfrastructure[0],self.SizeOfInfrastructure[1]), self.Symbol)
        else:
            if(self.HealthLeft<=self.HitPoint and self.HealthLeft>=int(self.HitPoint/2)):
                self.Symbol = self.ColorForCriticalStage1 + "C" + Style.RESET_ALL
                self.Array2D = np.full((self.SizeOfInfrastructure[0],self.SizeOfInfrastructure[1]), self.Symbol)
            if(self.HealthLeft<=int(self.HitPoint/2) and self.HealthLeft>=int(self.HitPoint/5)):
                self.Symbol = self.ColorForCriticalStage2 + "C" + Style.RESET_ALL
                self.Array2D = np.full((self.SizeOfInfrastructure[0],self.SizeOfInfrastructure[1]), self.Symbol)
            if(self.HealthLeft<=int(self.HitPoint/5) and self.HealthLeft>=0):
                self.Symbol = self.ColorForCriticalStage3 + "C" + Style.RESET_ALL
                self.Array2D = np.full((self.SizeOfInfrastructure[0],self.SizeOfInfrastructure[1]), self.Symbol)
        self.UpdateOnVillage(Village)

    @classmethod
    def AddOneCannon(cls):
        Cannon.NumberOfCannon += 1    