import os, random, time #imports 
path=os.getcwd() #gets the current working directory 


#Tile class with attributes: row, coloumn, tile value and tile status, corresponding image of the tile 
class Tile:
    def __init__(self,r,c):
        self.r=r
        self.c=c
        self.v='0'
        self.s=1 #1 hidden #2 shown   
        self.hiddentile=loadImage(path+"/images/tile.png") #loading the hidden tile (uncovered) 
        
    def display(self): #displaying the tile method 
        if self.s==1: #if the tile status is 1, then we load the hidden tile 
            image(self.hiddentile,self.c*52,self.r*52) #we multiply by 52 because the width and height of the image is 52  
        else:
            image(self.img,self.c*52,self.r*52) 
            
#minesweeper class: creates a board that is NxN and has M mines                  
class Minesweeper:
    def __init__(self,numRows,numCols,numMines): #attributes of the minesweeper class
        self.numRows=numRows
        self.numCols=numCols
        self.numMines=numMines
        self.tiles=[] #creating an empty tiles list 
        self.loose=False
        self.win=False
        self.left_tiles=self.numRows*self.numCols
        self.gameoverimg=loadImage(path+"/images/gameover.png") #loading the gameover image 
        
        
        #appending tiles into the empty list of tiles 
        for r in range(self.numRows):
            for c in range(self.numCols):
                self.tiles.append(Tile(r,c))
                
        #creating mines randomly 
        for i in range(self.numMines): 
            tile=random.choice(self.tiles) #randomly chooses a tile from the list of tilea 
            if tile.v=="mine": #if its already a mine
                tile=random.choice(self.tiles) #choose another tile 
            tile.v="mine" #change the tile value to mine
            tile.img=loadImage(path+"/images/mine.png") #then i load the image of the mine on the tile 
            
        
        #assign numbers to the tiles
        for tile in self.tiles: #looping through the tiles 
            if tile.v!="mine": #if its not a mine 
                for r in [tile.r-1,tile.r,tile.r+1]: #neighboring rows [0,-1] [0,1]
                    for c in [tile.c-1,tile.c,tile.c+1]: #neighboring coloumns [0,-1] [0,1]
                        neighboring_tile=self.get_Tile(r,c) #return the neighboring tile 
                        if neighboring_tile!=False and neighboring_tile.v=='mine': #if the neighboring tile is a mine and not empty
                            tile.v=str(int(tile.v)+1) #update the tile value based on the number of mines 
                    tile.img=loadImage(path+"/images/"+(tile.v)+".png") #load the tile value with the proper number of mine values 
                    
    
    def display(self): #display method 
        for tile in self.tiles:
            tile.display()
        if self.loose==True: #if loose display game over image 
            image(self.gameoverimg,30,30)
            
        #adding a rectangular outline to the user's selection 
        if not self.win and not self.loose:
            col=mouseX//52
            row=mouseY//52
            stroke(0,350,0)
            noFill()
            strokeWeight(4)
            rect(col*52,row*52,52,52) 
            
            
    def get_Tile(self,r,c): #gets the row tile and coloumn tiles and returns them
        for tile in self.tiles:
            if tile.r==r and tile.c==c:
                return tile 
        return False 
    
    def open_tile(self,tile): #this function is responsible for opening the tiles based on user's selection 

        if tile.v=='mine': #if the tile has a mine, loosing condition becomes true 
            self.loose=True 
            for tile in self.tiles:
                tile.s=2 #the tile status chnages to uncovered 
        
        
        elif tile.v!='0': #if the tile value is not 0 
            tile.s=2 #then the tile status changes as well to uncovered
            self.left_tiles-=1 #left tiles decreases 
            return 

        else:
            tile.s=2 #else if the tile is uncovered and has no neighbors, we use recursion to open the neighbpring tiles
            self.left_tiles-=1
            for r in [tile.r-1,tile.r,tile.r+1]: #looping through the row neighbors 
                for c in [tile.c-1,tile.c,tile.c+1]: #looping through the coloumn neighbors 
                    try:
                        if self.get_Tile(r,c).s ==1: 
                            self.open_tile(self.get_Tile(r,c))
                    except:
                        None 
                    
    
    def tile_pressed(self):
        if not self.win and not self.loose:
            c=mouseX//52 #mouse locations
            r=mouseY//52
            tile=self.get_Tile(r,c) #if we dont win and not loose then we keep getting the tiles and opening them
            self.open_tile(tile)
            self.game_win() #then we check for winning conditions  
        
    def game_win(self): #winning condition with the left tiles are equal to the number of mines and not loosing (not choosing a mine)
        if self.left_tiles==self.numMines and not self.loose:
            self.win==True 
            print("Congratulations! you won the game!")
            time.sleep(1)
            exit() 
        
m = Minesweeper(10,10,7) #creating a minesweeper object out of the minesweeper class 

def setup(): #in charge of the size of the game 
    size(m.numCols*52,m.numRows*52) 
    background(0)
    
def draw(): #calls the display method of minesweeper 
    background(0)
    m.display() 
    
def mouseClicked(): #in charge of mouse movements 
    m.tile_pressed() 
