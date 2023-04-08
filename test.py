from mcpi.minecraftstuff import MinecraftTurtle
from mcpi.minecraft import mc
from mcpi.block import *
x,y,z=mc.getPlayerPosition("babyYao521")

width = 5
height = 3
depth = 6
   # Create a hollow shell made of bricks.
mc.setBlocks(x, y, z+3, x+width, y+height, z+3+depth, BRICK_BLOCK.id)
mc.setBlocks(x+1, y, z+4, x+width-1, y+height-1, z+2+depth, AIR.id)
   # Set the floor.
mc.setBlocks(x-1, y-1, z+2, x+1+width, y-1, z+4+depth, COBBLESTONE.id)
   # Add a Door.
mc.setBlock(x+1, y, z+3,DOOR_WOOD.id, 0)
mc.setBlock(x+1, y+1, z+3, DOOR_WOOD.id, 8)
   # Add Windows.
mc.setBlocks(x+3, y+1, z+3, x+4, y+2, z+3,GLASS.id)
mc.setBlocks(x+2, y+1, z+3+depth, x+3, y+2, z+3+depth, GLASS.id)
mc.setBlocks(x, y+1, z+5, x, y+2, z+7, GLASS.id)
mc.setBlocks(x+width, y+1, z+5, x+width, y+2, z+7, GLASS.id)
   # Add a Roof.
for i in range(int(width/2) + 1):
    mc.setBlocks(x+i, y+height+i, z+3, x+i, y+height+i, z+3+depth, STAIRS_WOOD.id, 0)
    mc.setBlocks(x+width-i, y+height+i, z+3, x+width-i, y+height+i, z+3+depth, STAIRS_WOOD.id, 1)
 # Gable ends.
if (int(width/2) - i > 0):
    mc.setBlocks(x+1+i, y+height+i, z+3, x+width-i-1, y+height+i, z+3, BRICK_BLOCK.id, 0)
    mc.setBlocks(x+1+i, y+height+i, z+3+depth, x+width-i-1, y+height+i, z+3+depth, BRICK_BLOCK.id, 1)