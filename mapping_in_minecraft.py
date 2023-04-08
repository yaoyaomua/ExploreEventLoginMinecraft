from mcpi.minecraft import mc
from mcpi.minecraft import mcDrawing
from mcpi.block import *
import math

from mcpi.minecraftstuff import MinecraftTurtle, Vec3


def move_persion(position_x,y,postion_y):
    mc.setPlayerPosition("babyYao521",position_x,y,postion_y)

def mapping_place(position_x,position_y):
    mc.setBlocks(int(position_x), 0, int(position_y),int(position_x), 0, int(position_y), "lime_wool")
    # red, orange,yellow,green,blue,indigo,violet
    rainbow = ["red", "orange", "yellow", "green", "cyan", "purple"]
    radius = 8
    for angle in range(360):
        for i in range(0, 6):
            x = int(position_y) + (radius - i) * math.cos(angle * math.pi / 180)
            y = 0 + (radius - i) * math.sin(angle * math.pi / 180)
            mc.setBlock(int(position_x), y + 2, x, rainbow[i] + "_wool")
def mapping_transition(position_x,position_y,frequency,transition_name_info,count):
    if count>=2:
        if transition_name_info!='tau from tree':
            x = int(position_x)
            y = 1
            z = int(position_y)
            width = 5
            height = 3+(frequency/10)
            depth = 6

            # Create a hollow shell made of bricks.
            mc.setBlocks(x, y, z + 3, x + width, y + height, z + 3 + depth, "bricks")
            mc.setBlocks(x + 1, y, z + 4, x + width - 1, y + height - 1, z + 2 + depth, "air")
            # Set the floor.
            mc.setBlocks(x - 1, y - 1, z + 2, x + 1 + width, y - 1, z + 4 + depth, "cobblestone")
            # Add a Door.
            mc.setBlock(x + 1, y, z + 3, "dark_oak_wood", 0)
            mc.setBlock(x + 1, y + 1, z + 3, "dark_oak_wood", 8)
            # Add Windows.
            mc.setBlocks(x + 3, y + 1, z + 3, x + 4, y + 2, z + 3, "light_gray_stained_glass")
            mc.setBlocks(x + 2, y + 1, z + 3 + depth, x + 3, y + 2, z + 3 + depth, "light_gray_stained_glass")
            mc.setBlocks(x, y + 1, z + 5, x, y + 2, z + 7, "light_gray_stained_glass")
            mc.setBlocks(x + width, y + 1, z + 5, x + width, y + 2, z + 7, "light_gray_stained_glass")
            # Add a Roof.
            for i in range(int(width / 2) + 1):
                mc.setBlocks(x + i, y + height + i, z + 3, x + i, y + height + i, z + 3 + depth, "oak_stairs",
                             0)
            mc.setBlocks(x + width - i, y + height + i, z + 3, x + width - i, y + height + i, z + 3 + depth,
                         "oak_stairs", 1)
            # Gable ends.
            if (int(width / 2) - i > 0):
                mc.setBlocks(x + 1 + i, y + height + i, z + 3, x + width - i - 1, y + height + i, z + 3,
                             "bricks", 0)
            mc.setBlocks(x + 1 + i, y + height + i, z + 3 + depth, x + width - i - 1, y + height + i, z + 3 + depth,
                         "bricks", 1)
        else:
            mc.setBlocks(position_x,0,position_y,position_x+6,6,position_y+6,"black_wool",1)

    elif count==0:
        pos = Vec3(position_x, 0, position_y)
        # create minecraft turtle
        new_turtle = MinecraftTurtle(mc, pos)
        new_turtle.setverticalheading(90)

        # set speed
        new_turtle.speed(0)
        new_turtle.setposition(int(position_x), 0, int(position_y))
        # call the tree fractal
        tree(6, new_turtle)
    else:
        mc.setBlocks(position_x,0,position_y,position_x,10,position_y ,"pink_wool",1)
    mc.setSign(int(position_x) + 8, 0, int(position_y) + 4, 68, 1, transition_name_info.split())


def mapping_path(a_x,a_y,b_x,b_y,duration_info):
    scale=1000000
    print(int(duration_info)/scale)
    if int(duration_info)/scale < 1000:
        mcDrawing.drawLine(int(a_x), 0, int(a_y), int(a_x), 0, int(b_y), "quartz_slab")
        mcDrawing.drawLine(int(a_x), 0, int(b_y), int(b_x), 0, int(b_y), "quartz_slab")
    elif int(duration_info)/scale >= 1000 and int(duration_info)/scale < 4000:
        mcDrawing.drawLine(int(a_x), 0, int(a_y), int(a_x), 0, int(b_y), "purpur_slab")
        mcDrawing.drawLine(int(a_x), 0, int(b_y), int(b_x), 0, int(b_y), "purpur_slab")
    elif int(duration_info) / scale >= 4000 and int(duration_info )/ scale < 7000:
        mcDrawing.drawLine(int(a_x), 0, int(a_y), int(a_x), 0, int(b_y), "crimson_slab")
        mcDrawing.drawLine(int(a_x), 0, int(b_y), int(b_x), 0, int(b_y), "crimson_slab")
    else:
        mcDrawing.drawLine(int(a_x), 0, int(a_y), int(a_x), 0, int(b_y), "nether_brick_slab")
        mcDrawing.drawLine(int(a_x), 0, int(b_y), int(b_x), 0, int(b_y), "nether_brick_slab")


def tree(branchLen, t):
    if branchLen > 1:

        if branchLen > 1:
            t.changeblock("pink_wool")
        if branchLen > 3:
            t.changeblock("lime_wool")
        if branchLen > 5:
            t.changeblock("black_wool")
        # for performance
        x, y, z = t.position.x, t.position.y, t.position.z
        # draw branch
        t.forward(branchLen)

        t.up(20)
        tree(branchLen - 1, t)

        t.right(90)
        tree(branchLen - 1, t)

        t.left(180)
        tree(branchLen - 1, t)

        t.down(40)
        t.right(90)
        tree(branchLen - 1, t)
        t.up(20)
        # go back
        # t.backward(branchLen)
        # for performance - rather than going back over every line
        t.setposition(x, y, z)






