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
        sleep(1) # to add delay to verify 
        Engine.Canvas.clear()

    @staticmethod
    def Ending(Win):
        Engine.Canvas.clear()
        if(Win):
            print("You have what it takes to be Clash of Clan master. VICTORY!")
        else:
            print("You need to train harder. LOST!")
        print("Thankyou for Playing")