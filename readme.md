# Sukhjinder Kumar (2020101055) 

## How to Play?

1. When inside game folder, run ``python Game.py`` to run game
2. To see replay of your game, do ``cd Replays``, followed by ``python Replay.py ./ReplayFiles/<your particular replay.txt>``

## Controls

- "w", "a", "s", "d" keys for controling King movement
- "j", "k", "l" for spawing barbarians from bottom left, bottom right, upper right
- " " (space) for attacking with king
- "y" to use Axe attack feature of king
- "r", "h" to use Rage and Healing spell respectively 
- "x" to quit game halfway 

## Game Mechanics 
### Barbarians
1. They are automated troops, spawed from 3 location of village (one at a time, and unlimited in number). 
2. They move toward nearest non-wall target and if encounter a wall, breaks them. 
3. They can override each other, i.e at a place multiple barbarian  can stand at same time.

### Cannons
1. They attack a single target within its range
2. By design the one that is nearest to it.