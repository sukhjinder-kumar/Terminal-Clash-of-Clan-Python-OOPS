# Sukhjinder Kumar (2020101055)

## How to Play?

---

1. When inside game folder, run ``python Game.py`` to run game
2. To see replay of your game, do ``cd Replays``, followed by ``python Replay.py ./ReplayFiles/<your particular replay.txt>``

## Controls

---

- `w`, `a`, `s`, `d` keys for controling King/Queen movement
- `j`, `k`, `l` for spawning barbarians from bottom left, bottom right and upper right
- `u`, `i`, `o` for spawning archer from bottom left, bottom right and upper right
- `n`, `m`, `','` for spawning balloon from bottom left, bottom right and upper right
- `<space>` (space) for attacking with king/Queen
- `y` to use Axe attack feature of king
- `r`, `h` to use Rage and Healing spell respectively
- `x` to quit game halfway

## Game Mechanics

---

### Barbarians

1. They are automated troops, spawed from 3 location of village (one at a time, and unlimited in number).
2. They move toward nearest non-wall target and if encounter a wall, breaks them.
3. They can override each other, i.e at a place multiple barbarian  can stand at same time.

### Cannons

1. They attack a single target within its range
2. By design the one that is nearest to it.

## Documentation

---

### Canvas

1. **Canvas(CanvasOrigin=None, CanvasRow=None, CanvasColumn=None, Canvas2DArray=None)**

    - It initialise an instance of canvas. It is a rectangular box printed on terminal.

    - CanvasOrigin is [row, column] from starting index.

    - By default, origin is center of terminal, CanvasRow and CanvasColumn are taken to be off by 40% percent. And Canvas2DArray is assumed (of appropriate size) to be a +----+ kinds system.

    - In case defalut behaviour is not assumed, a check function is made (**Canvas.CheckCompatibility()**) so as to check if boundary is crossed. If boundary condition are violated, neccesary steps like cutting off at fault point are assumed, making rendering still possible, but warning sign is shown while rendering.

    - *Scope for Improvement*: CanvasRow and CanvasColumn are kinda unneccesary if we have Canvas2DArray.

2. **Canvas.update(Array2D, location=None)**

    - By default is location is assumed to be origin.

    - This updates Canvas array with Array2D element at location (w.r.t canvas and as [row, column])

    - Returns False if Array2D with that location is out of bound

3. **Canvas.Render()**

    - It prints Canvas on terminal.

    - CanvasArray is smaller one, with starting index specified. Rest of area is filled with black spaces.

    - **Canvas.DrawCanvas()** does that same thing. Render calls DrawCanvas, so that in future error handling if any can be included

4. **Helper Function**

    - **Canvas.BringCursonToEnd(), Canvas.BringCursonToStart(), Canvas.Clear()** are static function (except BringCursonToEnd), that does what they say.

### Village

Basic philosophy for having village and canvas different is, that village contain information for the village. Everything from troops, village, Id, etc. And it should not be messed with printing and stuff. Village is being printed. Village is not a array to be printed. It is information about the game. Canvas is something that translate that to terminal window. Tomorrow if we want to make displaying more prettier, we just need to fiddle with Canvas function and not the village.

1. **Village(Name,Canvas,StartingIndexOnCanvas=None,Row=None,Column=None,SpawningPoints=None)**

    - Does as it says create instance of Village

    - We need to provide it with Name, and associated Canvas. Though For more modularity Canvas could have been kept seprate, but that would have increased boilerplate, this is the tradeoff I used.

    - Parameter added as optional are fairly intuitive

2. **Village.AddBuildingOrWeaponToVillage(building)**

    - This function updates village with particular building.

    - The building should contain it's coordinates w.r.t to village initial condition.

    - If there is a error in boundary, updation is not done and a print statement is shown on terminal

    - Note - Print statement in form of error would distort the gameplay, though it was intendeted that such things should leave game unaltered. But use of Colorama library allows so much only.

    - Another thing to note is that **Village.CheckBuilding(Building)** is not made. So checking must be done before hand. Sometime in future it might be implemented.

3. **Village.AddTroop(Troop)**

    - It is different from above function as troops move, and while updating there new position of village array, there previous information must be removed.

    - Before going to junk of function, **Village.CheckTroop(Troop)** is not yet build. So checking must be done before hand, otherwise error would come.

    - *Filling Mechanism*: We create a filler array of size of troop, with color that of village skin. In Troop we must have a PreviousPosition attribute by same name. Also a very rudamentary filling takes place. Previous location is filled with filler and new position is filled with troopArray. This might cause glicth if -

        a. Current Position of Troop overlaps some other object, then that object information be replaced by our troop

        b. Previous Position of Troop should not overlap with other object. If checking function is implemented (either at Village level or for time being at Troop level), no error should occur.

4. **Village.UpdateCanvas()**

    - Canvas is updated of the changes. I.e village array is updated on Canvas.

    - Basically it takes use of Canvas.Update() function.

    - Earlier **Village.Update()** was to be made, however that leads to added complexity. The idea was that it would act of common API for all building and troops alike, and from here different update would be made based on class. Nothing to with UpdateCanvas(), it is quite different.

### CentralProcessingUnit

---

1. **CentralProcessingUnit.UpdatingVillage(ch,Village Information)**

    - Village Information: Village,TownHall,Huts_list,Walls_list,Cannon_list,King,Barbarian_list

    - It takes input `ch` and Village information as input

    - This function handles all the mechanics of the game and hides it from `Game.py`. I.e based on input (whether it is Null or not), decides and updates the village. Including automatic task like cannon, etc

    - It output [IsEnd, Win] list. IsEnd is used in while loop to check if game is ended and Win is to know the outcome of the game.

    - It called **CPU.InputToOutput(ch)** for input based updates and **CPU.Background()** for background processes.

2. **CentralProcesssingUnit.InputToOutput(ch, Village information)**

    - Based on ch output is decided.

    - Return IsEnd, though True only when user presses `x`. Main checking of ending and winning is done is background

    - After all corresponding function are called, in which village is updated, Village.UpdateOnCanvas() is run. So outside class it appears as super function (CPU.UpdatingVillage()) says.

3. **CentralProcessingUnit.Background(Village Information)**

    - Here background processes like barbarian movement, attack, cannon attack, etc are implemented

    - Algorithm like in which direction to move, which troop to attack are made.

    - After direction or troop is decided, related function are called which update on village according to our convention and after calling these function we Village.UpdateOnCanvas

    - Also we check if game has ended by looking at health of townhall, cannon left, hut left. Also for lost case king health, barbarian health.

        - Win is decided if all building are destroryed. Lost is decided if all troops are dead.

        - Note: It might happen that number of troops that can be spawned be infinite, however when what we mean is living troops at a moment. If at instant cumulative health of troops account to zero, gain is declared lost.

### Scope for Improvement

---

1. Highlighting structure of classes. At many places common structure of troops and building are assumed. And this is a problem. Any new troop must be either derived from the super class or should have essential attributes.  

2. Known mess, sometimes same function is made in many different ways to avoid complexity. Like updating on village. We have 2 function in Village itself that take troop and building class. But in respective troop and building classes, we have there on own UpdateOnVillage function. That made easy printing as corner cases can be checked. However it is clearly not optimal and it is a design problem, needs to be addresed.

3. Troop List, there is no complete list of troop every troop needs to be send indiviually. This needs to be corrected.

4. Information is stored very ineffeciently in village. Basically indiviual component information is stored independent instances, that in thoery can have nothing to do with village. What I mean is there is no single container in which information regarding village is stored. It is scattered and to gain information iteration through all objects is needed.

5. Object recognition is done very poorely. What I mean by this is, when we want to identify which object is lying at certain coordinate only way to know is by looking up character and color characterstic. It is not the optimal way to identify object. In some sense I feel like once problem 4. is solved, fifth would follow pursuit

6. Organization in terms of where Village is being updated. E.g when king moves, king.Move() within itself update it on village, although this philosophy is followed throughout this doesn't sound quite optimal in terms of longevity of code

7. Data needs to be drilled, Something like a Redux store needs to be made for easy to flow of information
