from read_pnml_file import *
from mapping_in_minecraft import *
from mcpi.minecraft import mc
#read alphaminer.pnml
place_info,transition_info,arc_info,place_name,transition_name,transition_name_info=read_pnml_file("inductivePN.pnml")
print(place_info)
print(transition_info)
print(arc_info)
print(place_name)
print(transition_name)

scale=0.5
x, y, z = mc.getPlayerPosition("babyYao521")
#move person
move_persion((float(place_info[0][1])-1)*scale,0,(float(place_info[0][2])-1)*scale)
#draw path
duration_info=0
for i in range(0,len(arc_info)):
    if arc_info[i][1] in place_name:
        for j in range(0,len(place_info)):
            if place_info[j][0]==arc_info[i][1]:
                a_x=place_info[j][1]
                a_y=place_info[j][2]
    elif arc_info[i][1] in transition_name:
        for j in range(0,len(transition_info)):
            if transition_info[j][0]==arc_info[i][1]:
                a_x=transition_info[j][1]
                a_y=transition_info[j][2]
    if arc_info[i][2] in place_name:
        for j in range(0,len(place_info)):
            if place_info[j][0]==arc_info[i][2]:
                b_x=place_info[j][1]
                b_y=place_info[j][2]
    elif arc_info[i][2] in transition_name:
        for j in range(0,len(transition_info)):
            if transition_info[j][0]==arc_info[i][2]:
                b_x=transition_info[j][1]
                b_y=transition_info[j][2]

    mapping_path(float(a_x)*scale,float(a_y)*scale,float(b_x)*scale,float(b_y)*scale,duration_info)

#draw place
for i in range(0,len(place_info)):
    mapping_place(float(place_info[i][1])*scale,float(place_info[i][2])*scale)
#draw transition
count=10
for i in range(0,len(transition_info)):
    mapping_transition(float(transition_info[i][1])*scale,float(transition_info[i][2])*scale,0,transition_name_info[i],count)
