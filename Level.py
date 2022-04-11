import sys
import Engine 
from Village import Village
import Infrastructure
import Army

def LevelLayout(Village,Level,IsKing):

    if(Level == 1):
        Army.Number_Barbarian = 3
        Army.Number_Archer = 3
        Army.Number_Balloon = 3

        TownHall = Infrastructure.TownHall([9,40])
        Village.TownHall_list.append(TownHall)
        TownHall.UpdateOnVillage(Village)

        Village.Huts_list.append(Infrastructure.Huts([7,37]))
        Village.Huts_list.append(Infrastructure.Huts([7,48]))
        Village.Huts_list.append(Infrastructure.Huts([12,37]))
        Village.Huts_list.append(Infrastructure.Huts([12,48]))
        Village.Huts_list.append(Infrastructure.Huts([5,5]))
        for hut in Village.Huts_list:
            hut.UpdateOnVillage(Village)

        for row in range(5,16):
            for column in range(33,55):
                if(row == 5 or row == 15 or column == 33 or column == 54):
                    Village.Walls_list.append(Infrastructure.Walls([row,column]))
        for wall in Village.Walls_list:
            wall.UpdateOnVillage(Village)

        Village.Cannon_list.append(Infrastructure.Cannon([9,37]))
        Village.Cannon_list.append(Infrastructure.Cannon([9,48]))
        for cannon in Village.Cannon_list:
            cannon.UpdateOnVillage(Village)

        Village.WizardTower_list.append(Infrastructure.WizardTower([10,10]))
        Village.WizardTower_list.append(Infrastructure.WizardTower([10,15]))
        for wizardtower in Village.WizardTower_list:
            wizardtower.UpdateOnVillage(Village)

        if(IsKing):
            Village.Hero_list.append(Army.King())  
        else:
            Village.Hero_list.append(Army.ArcherQueen())  
        for hero in Village.Hero_list:
            hero.UpdateOnVillage(Village)

        Village.AssociatedCanvas.UpdateCanvas(Village.Hero_list[0].HealthBar(Village),[Village.StartingIndexOnCanvas[0]+Village.VillageRows,Village.StartingIndexOnCanvas[1]])
        if(not Village.UpdateCanvas()):
            sys.exit("Boundary Condition exceeded")
    
    if(Level == 2):
        Army.Number_Barbarian = 6
        Army.Number_Archer = 6
        Army.Number_Balloon = 3
    
        TownHall = Infrastructure.TownHall([9,37])
        Village.TownHall_list.append(TownHall)
        TownHall.UpdateOnVillage(Village)

        Village.Cannon_list.append(Infrastructure.Cannon([9,34]))
        Village.Cannon_list.append(Infrastructure.Cannon([9,45]))
        Village.Cannon_list.append(Infrastructure.Cannon([6,42]))
        for cannon in Village.Cannon_list:
            cannon.UpdateOnVillage(Village)

        Village.WizardTower_list.append(Infrastructure.WizardTower([12,37]))
        Village.WizardTower_list.append(Infrastructure.WizardTower([12,42]))
        Village.WizardTower_list.append(Infrastructure.WizardTower([6,37]))
        for wizardtower in Village.WizardTower_list:
            wizardtower.UpdateOnVillage(Village)

        Village.Huts_list.append(Infrastructure.Huts([7,34]))
        Village.Huts_list.append(Infrastructure.Huts([7,45]))
        Village.Huts_list.append(Infrastructure.Huts([12,34]))
        Village.Huts_list.append(Infrastructure.Huts([12,45]))
        Village.Huts_list.append(Infrastructure.Huts([12,40],Infrastructure.Huts.HitPoint,[3,2]))
        Village.Huts_list.append(Infrastructure.Huts([6,40],Infrastructure.Huts.HitPoint,[3,2]))
        for hut in Village.Huts_list:
            hut.UpdateOnVillage(Village)

        for row in range(5,16):
            for column in range(33,49):
                if(row == 5 or row == 15 or column == 33 or column == 48):
                    Village.Walls_list.append(Infrastructure.Walls([row,column]))
        for wall in Village.Walls_list:
            wall.UpdateOnVillage(Village)

        if(IsKing):
            Village.Hero_list.append(Army.King())  
        else:
            Village.Hero_list.append(Army.ArcherQueen())  
        for hero in Village.Hero_list:
            hero.UpdateOnVillage(Village)

        Village.AssociatedCanvas.UpdateCanvas(Village.Hero_list[0].HealthBar(Village),[Village.StartingIndexOnCanvas[0]+Village.VillageRows,Village.StartingIndexOnCanvas[1]])
        if(not Village.UpdateCanvas()):
            sys.exit("Boundary Condition exceeded")

    if(Level == 3):
        Army.Number_Barbarian = 9
        Army.Number_Archer = 9
        Army.Number_Balloon = 6

        TownHall = Infrastructure.TownHall([9,37])
        Village.TownHall_list.append(TownHall)
        TownHall.UpdateOnVillage(Village)

        for row in range(6,15):
            for column in range(34,48):
                if(row == 6 or row == 14 or column == 34 or column == 47):
                    Village.Walls_list.append(Infrastructure.Walls([row,column]))
        for wall in Village.Walls_list:
            wall.UpdateOnVillage(Village)

        Village.Cannon_list.append(Infrastructure.Cannon([9,30]))
        Village.Cannon_list.append(Infrastructure.Cannon([6,49]))
        Village.Cannon_list.append(Infrastructure.Cannon([12,49]))
        Village.Cannon_list.append(Infrastructure.Cannon([3,39]))
        for cannon in Village.Cannon_list:
            cannon.UpdateOnVillage(Village)

        Village.WizardTower_list.append(Infrastructure.WizardTower([6,30]))
        Village.WizardTower_list.append(Infrastructure.WizardTower([12,30]))
        Village.WizardTower_list.append(Infrastructure.WizardTower([9,49]))
        Village.WizardTower_list.append(Infrastructure.WizardTower([15,39]))
        for wizardtower in Village.WizardTower_list:
            wizardtower.UpdateOnVillage(Village)

        Village.Huts_list.append(Infrastructure.Huts([4,30]))
        Village.Huts_list.append(Infrastructure.Huts([4,33]))
        Village.Huts_list.append(Infrastructure.Huts([4,36]))
        Village.Huts_list.append(Infrastructure.Huts([15,30]))
        Village.Huts_list.append(Infrastructure.Huts([15,33]))
        Village.Huts_list.append(Infrastructure.Huts([15,36]))
        Village.Huts_list.append(Infrastructure.Huts([4,43]))
        Village.Huts_list.append(Infrastructure.Huts([4,46]))
        Village.Huts_list.append(Infrastructure.Huts([4,49]))
        Village.Huts_list.append(Infrastructure.Huts([15,43]))
        Village.Huts_list.append(Infrastructure.Huts([15,46]))
        Village.Huts_list.append(Infrastructure.Huts([15,49]))
        for hut in Village.Huts_list:
            hut.UpdateOnVillage(Village)

        for row in range(2,19):
            for column in range(29,53):
                if(row == 2 or row == 18 or column == 29 or column == 52):
                    Village.Walls_list.append(Infrastructure.Walls([row,column]))
        for wall in Village.Walls_list:
            wall.UpdateOnVillage(Village)

        if(IsKing):
            Village.Hero_list.append(Army.King())  
        else:
            Village.Hero_list.append(Army.ArcherQueen())  
        for hero in Village.Hero_list:
            hero.UpdateOnVillage(Village)

        Village.AssociatedCanvas.UpdateCanvas(Village.Hero_list[0].HealthBar(Village),[Village.StartingIndexOnCanvas[0]+Village.VillageRows,Village.StartingIndexOnCanvas[1]])
        if(not Village.UpdateCanvas()):
            sys.exit("Boundary Condition exceeded")
