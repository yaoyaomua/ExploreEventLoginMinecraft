import xml.dom.minidom as xmldom
from xml.etree import ElementTree
import os
def read_pnml_file(filename):
    xmlfilepath = os.path.abspath(filename)
    domobj = xmldom.parse(xmlfilepath)
    # 得到元素对象
    elementobj = domobj.documentElement
    # 获得子标签
    subElementObj_place = elementobj.getElementsByTagName("place")
    subElementObj_position = elementobj.getElementsByTagName("position")
    subElementObj_transition = elementobj.getElementsByTagName("transition")
    subElementObj_arc = elementobj.getElementsByTagName("arc")
    subElementObj_transition_name = elementobj.getElementsByTagName("text")
    num_place = len(subElementObj_place)
    #num_position include the position of place and transition
    num_position = len(subElementObj_position)
    num_transition = len(subElementObj_transition)
    num_arc=len(subElementObj_arc)
    num_text=len(subElementObj_transition_name)
    # 获得标签属性值
    #place_info :place_id,x_position,y_position
    w, h = 3, num_place
    place_info = [[0 for x in range(w)] for y in range(h)]
    w, h = 1, num_place
    place_name = [[0 for x in range(w)] for y in range(h)]
    for i in range(0, num_place):
        place_info[i][0] = subElementObj_place[i].getAttribute("id")
        place_info[i][1] = subElementObj_position[i].getAttribute("x")
        place_info[i][2] = subElementObj_position[i].getAttribute("y")
        place_name[i] = subElementObj_place[i].getAttribute("id")

    #transition_info :transition_id,x_postion,y_position
    w, h = 3, num_transition
    transition_info = [[0 for x in range(w)] for y in range(h)]
    w, h = 1, num_transition
    transition_name = [[0 for x in range(w)] for y in range(h)]
    for i in range(0, num_transition):
        transition_info[i][0] = subElementObj_transition[i].getAttribute("id")
        transition_info[i][1] = subElementObj_position[i+num_place].getAttribute("x")
        transition_info[i][2] = subElementObj_position[i+num_place].getAttribute("y")
        transition_name[i] = subElementObj_transition[i].getAttribute("id")

    #arc_info:arc_id,source,target
    w, h = 3, num_arc
    arc_info = [[0 for x in range(w)] for y in range(h)]
    for i in range(0, num_arc):
        arc_info[i][0] = subElementObj_arc[i].getAttribute("id")
        arc_info[i][1] = subElementObj_arc[i].getAttribute("source")
        arc_info[i][2] = subElementObj_arc[i].getAttribute("target")

    #transition_name
    w, h = 1, num_transition
    transition_name_info = [[0 for x in range(w)] for y in range(h)]
    print(num_place)
    for i in range(0, num_transition):
        transition_name_info[i]=subElementObj_transition_name[num_place+3+i].firstChild.data
    print("transition_name_info")
    print(transition_name_info)

    return place_info, transition_info, arc_info,place_name,transition_name,transition_name_info
