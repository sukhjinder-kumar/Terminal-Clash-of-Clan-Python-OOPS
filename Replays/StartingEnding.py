"""Decides what goes before and after Game"""
from time import sleep
import Engine

class StartingEnding:

    @staticmethod
    def PrintClashOfClans():
        print("clash of clans")

    @staticmethod
    def Start():
        StartingEnding.PrintClashOfClans() # We can use this preSleep period for things like loading screen etc, also this coc title can go inside game window

        # Ask Village_name, whether king or Queen, Level
        VillageName = input("Enter Village Name: ")
        IsKing = int(input("King(1) or Queen(0): "))
        while(not IsKing in [0,1]):
            print("Enter 0 | 1 only!")
            IsKing = int(input("King(1) or Queen(0): "))
        Level = int(input("Enter Level 1 | 2 | 3 : "))
        while(not Level in [1,2,3]):
            print("Enter Level amongst 1, 2, 3!")
            Level = int(input("Enter Level 1 | 2 | 3 : "))

        sleep(1) # to add delay to verify 
        Engine.Canvas.clear()
        return [VillageName,IsKing,Level]

    @staticmethod
    def Ending(Win):
        Engine.Canvas.clear()
        if(Win):
            print("You have what it takes to be Clash of Clan master. VICTORY!")
        else:
            print("You need to train harder. LOST!")
        print("Thankyou for Playing")