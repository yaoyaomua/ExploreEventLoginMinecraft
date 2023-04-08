from read_xml_file import *
from mapping_in_minecraft import *
from mcpi.minecraft import mc
#read extension-log.xml
transition_info,transition_name,arc_info,duration_info=read_xml_file("discoFuzzyMinerwithDay.xml")
print(transition_info)
print(transition_name)
print(arc_info)

scale=100
x, y, z = mc.getPlayerPosition("babyYao521")
#move person
move_persion(float(transition_info[0][1])*scale-1,y,float(transition_info[0][2])*scale-1)
#draw path
for i in range(0,len(arc_info)):
    for j in range(0,len(transition_info)):
            if transition_info[j][0]==arc_info[i][0]:
                a_x=transition_info[j][1]
                a_y=transition_info[j][2]
            if transition_info[j][0]==arc_info[i][1]:
                b_x = transition_info[j][1]
                b_y = transition_info[j][2]
    mapping_path(float(a_x)*scale,float(a_y)*scale,float(b_x)*scale,float(b_y)*scale,duration_info[i])

#draw transition
count=0
for i in range(0,len(transition_info)):
    mapping_transition(float(transition_info[i][1])*scale,float(transition_info[i][2])*scale,float(transition_info[i][3])/700,
                       transition_name[i],count)
    count+=1
