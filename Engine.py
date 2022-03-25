import os
from time import sleep
from tkinter import HORIZONTAL
import numpy as np
import warnings
from colorama import Cursor, Fore, Style, Back

class Canvas:

    def __init__(self, CanvasOrigin=None, CanvasColumn=None, CanvasRow=None, Canvas2DArray=None):
        # Origin = [row,column] of Starting Index
        self.size = os.get_terminal_size()
        self.TerminalColumn = self.size.columns
        self.TerminalRow = self.size.lines 
        self.DefaultCanvasColumn = (self.TerminalColumn - 2*int(self.TerminalColumn/5))
        self.DefaultCanvasRow = (self.TerminalRow - 2*int(self.TerminalRow/5))
        self.DefaultCanvasOrigin = [int(self.TerminalRow/5)-1,int(self.TerminalColumn/5)-1]

        self.CanvasColumn = CanvasColumn or self.DefaultCanvasColumn
        self.CanvasRow = CanvasRow or self.DefaultCanvasRow 
        self.CanvasOrigin = CanvasOrigin or self.DefaultCanvasOrigin

        plus = Back.WHITE + Fore.WHITE + Style.NORMAL + "+" + Style.RESET_ALL
        space = Back.WHITE + Fore.WHITE + Style.NORMAL + " " + Style.RESET_ALL
        HorizontalLine = Back.WHITE + Fore.WHITE + Style.NORMAL + "-" + Style.RESET_ALL
        VerticalLine = Back.WHITE + Fore.WHITE + Style.NORMAL + "|" + Style.RESET_ALL

        self.DefaultCanvas2DArray = np.full((self.CanvasRow,self.CanvasColumn), space)
        for i in range(0,self.CanvasRow):
            for j in range(0,self.CanvasColumn):
                if(i == 0 or i == self.CanvasRow-1):
                    if(j == 0 or j == self.CanvasColumn-1):
                        self.DefaultCanvas2DArray[i][j] = plus
                    elif(j == 1 or j == self.CanvasColumn-2):
                        self.DefaultCanvas2DArray[i][j] = space
                    else:
                        self.DefaultCanvas2DArray[i][j] = HorizontalLine
                else:
                    if(j == 0 or j == self.CanvasColumn-1):
                        self.DefaultCanvas2DArray[i][j] = VerticalLine

        self.Canvas2DArray = (Canvas2DArray or self.DefaultCanvas2DArray).copy()

        self.CheckCompatibility() 

    def CheckCompatibility(self):
        # If values are within range okay return true, if outside, change it to default/appropriate and return false
        flag = True
        if(self.CanvasOrigin[0]<0 or self.CanvasOrigin[0]>=self.TerminalRow): 
            flag = False
            self.CanvasOrigin[0] = self.DefaultCanvasOrigin[0]
        if(self.CanvasOrigin[1]<0 or self.CanvasOrigin[1]>=self.TerminalColumn):
            flag = False
            self.CanvasOrigin[0] = self.DefaultCanvasOrigin[1]
        if((self.CanvasOrigin[0]+self.CanvasRow)>self.TerminalRow):
            flag = False
            self.CanvasColumn = self.TerminalRow-self.CanvasOrigin[0]
        if((self.CanvasOrigin[1]+self.CanvasColumn)>self.TerminalColumn):
            flag = False
            self.CanvasRow = self.TerminalColumn-self.CanvasOrigin[1]
        # Any check on Symbol?
        if(self.Canvas2DArray.shape[0]>self.DefaultCanvas2DArray.shape[0] or self.Canvas2DArray.shape[1]>self.DefaultCanvas2DArray.shape[1]):
            flag = False
            self.Canvas2DArray = self.Canvas2DArray[:min(self.Canvas2DArray.shape[0],self.DefaultCanvas2DArray.shape[0]),:min(self.Canvas2DArray.shape[1],self.DefaultCanvas2DArray.shape[1])]
        
        # Rudementary Warning handling
        if(flag == False):
            warnings.warn("Your Data doesn't Fit well inside Canvas, Default Behaviour Used")
            sleep(2)

    def UpdateCanvas(self,Array2D, Location=None):
        # Location is a [row,column] of Starting Index
        # The 2D Array would have element with colorama information inside string, and don't use u10 by yourself
        # If there is some boundary erros it returns false and don't do anything
        Location = Location or [0,0]
        if(Location[0]>=0 and Location[0]+Array2D.shape[0]<=self.CanvasRow and Location[1]>=0 and Location[1]+Array2D.shape[1]<=self.CanvasColumn):
            self.Canvas2DArray[Location[0]:Location[0]+Array2D.shape[0],Location[1]:Location[1]+Array2D.shape[1]] = Array2D
            return True 
        else:
            return False 
        
    def RenderCanvas(self):
        self.DrawCanvas()

    def DrawCanvas(self):
        space = Back.BLACK + Fore.WHITE + Style.NORMAL + " " + Style.RESET_ALL
        Terminal1DString = np.full((self.TerminalRow-1,self.TerminalColumn), space)
        Terminal1DString[self.CanvasOrigin[0]:self.CanvasOrigin[0]+self.CanvasRow,self.CanvasOrigin[1]:self.CanvasOrigin[1]+self.CanvasColumn] = self.Canvas2DArray
        Terminal1DString = Terminal1DString.reshape(-1) 
        Terminal1DString = "".join([str(i) for i in Terminal1DString])
        print(Terminal1DString,end='')

    def BringCursortoEnd(self):
        print(Cursor.POS(1,self.TerminalRow))

    @staticmethod
    def clear():
        if os.name in ("nt","dos"):
            os.system("cls")
        else:
            os.system("clear") 
    
    @staticmethod
    def BringCursortoStart():
        print(Cursor.POS(1,1), end='')