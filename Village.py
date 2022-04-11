"""Village Information"""
import numpy as np
from colorama import Fore, Back, Style

class Village:

    VillageColor = Back.LIGHTBLACK_EX + Fore.RED + Style.NORMAL
    Space = VillageColor + " " + Style.RESET_ALL

    def __init__(self,Name,Canvas,StartingIndexOnCanvas=None,Row=None,Column=None,SpawningPoints=None):
        # StartintindexOnCanvas is w.r.t to canvas
        # SpawningPoint is w.r.t to Village
        self.VillageName = Name 
        self.AssociatedCanvas = Canvas
        self.StartingIndexOnCanvas = StartingIndexOnCanvas or [0,0]
        self.VillageRows = Row or Canvas.CanvasRow-1 # 1 for kings health bar on Canvas, otherwise fully overlap
        self.VillageColumns = Column or Canvas.CanvasColumn
        self.space = Village.VillageColor + " " + Style.RESET_ALL
        self.VillageLayout2DArray = np.full((self.VillageRows,self.VillageColumns), self.space)
        self.SpawningPoints = SpawningPoints or np.array([[self.VillageRows-1,0],[self.VillageRows-1,self.VillageColumns-1],[0,self.VillageColumns-1]]) 

        # These attribute would help making code robust, 
        # however for time being they haven't been taken use of
        # Because all function would need to be written in this convention to take use of it
        # But newer function can use it
        # Additional function within village like appending to list can be made that would also check
        # Currently it is just used for Levels and CPU API
        self.TownHall_list = []
        self.Cannon_list = []
        self.WizardTower_list = []
        self.Walls_list = []
        self.Huts_list = []
        self.Hero_list = []
        self.Barbarian_list = []
        self.Archer_list = []
        self.Balloon_list = []

    def AddBuildingOrWeaponToVillage(self, Building):
        # Every Building should have Starting index, 2D array of colors.
        if(self.checkBuilding(Building)):
            self.VillageLayout2DArray[Building.StartingIndexOnVillage[0]:Building.StartingIndexOnVillage[0]+Building.SizeOfInfrastructure[0],Building.StartingIndexOnVillage[1]:Building.StartingIndexOnVillage[1]+Building.SizeOfInfrastructure[1]] = Building.Array2D
        else:
            print("Boundary error")
    
    def checkBuilding(self, Building):
        return True

    def AddTroop(self, Troop):
        if(self.checkTroop(Troop)):
            filler = np.full((Troop.SizeOfInfrastructure[0],Troop.SizeOfInfrastructure[1]), self.space)
            self.VillageLayout2DArray[Troop.PreviousPosition[0]:Troop.PreviousPosition[0]+Troop.SizeOfInfrastructure[0],Troop.PreviousPosition[1]:Troop.PreviousPosition[1]+Troop.SizeOfInfrastructure[1]] = filler
            self.VillageLayout2DArray[Troop.Position[0]:Troop.Position[0]+Troop.SizeOfInfrastructure[0],Troop.Position[1]:Troop.Position[1]+Troop.SizeOfInfrastructure[1]] = Troop.Array2D
            return True
        else:
            return False
    
    def checkTroop(self,Troop):
        return True

    def Update(self):
        pass

    def UpdateCanvas(self):
        return self.AssociatedCanvas.UpdateCanvas(self.VillageLayout2DArray,self.StartingIndexOnCanvas)
        