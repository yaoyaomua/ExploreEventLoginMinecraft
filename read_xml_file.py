import xml.dom.minidom as xmldom
import os
def read_xml_file(filename):
    xmlfilepath = os.path.abspath(filename)
    domobj = xmldom.parse(xmlfilepath)
    # 得到元素对象
    elementobj = domobj.documentElement
    # 获得子标签
    subElementObj_node = elementobj.getElementsByTagName("Node")
    subElementObj_startnode = elementobj.getElementsByTagName("StartNode")
    subElementObj_endnode = elementobj.getElementsByTagName("EndNode")
    subElementObj_edge = elementobj.getElementsByTagName("Edge")
    subElementObj_layout = elementobj.getElementsByTagName("Layout")
    subElementObj_frequency = elementobj.getElementsByTagName("Frequency")
    subElementObj_duration= elementobj.getElementsByTagName("Duration")

    num_transition = len(subElementObj_node)
    num_arc=len(subElementObj_edge)
    # 获得标签属性值
    #transition_info :transition_id,x_position,y_position,frequency
    w, h = 4, num_transition+2
    transition_info = [[0 for x in range(w)] for y in range(h)]
    w, h = 1, num_transition+2
    transition_name = [[0 for x in range(w)] for y in range(h)]
    # startnode
    transition_info[0][0] = subElementObj_startnode[0].getAttribute("index")
    transition_info[0][1] = subElementObj_layout[num_transition + 1].getAttribute("x")
    transition_info[0][2] = subElementObj_layout[num_transition + 1].getAttribute("y")
    #transition_name[0] = subElementObj_startnode[0].getAttribute("activity")
    transition_name[0] = "start"
    # endnode
    transition_info[1][0] = subElementObj_endnode[0].getAttribute("index")
    transition_info[1][1] = subElementObj_layout[num_transition + 2].getAttribute("x")
    transition_info[1][2] = subElementObj_layout[num_transition + 2].getAttribute("y")
    #transition_name[1] = subElementObj_endnode[0].getAttribute("activity")
    transition_name[1] = "end"
    for i in range(2, num_transition+2):
        transition_info[i][0] = subElementObj_node[i-2].getAttribute("index")
        transition_info[i][1] = subElementObj_layout[i-1].getAttribute("x")
        transition_info[i][2] = subElementObj_layout[i-1].getAttribute("y")
        transition_info[i][3] = subElementObj_frequency[i-2].getAttribute("total")
        transition_name[i] = subElementObj_node[i-2].getAttribute("activity")

    # arc_info :x_position,y_position
    w, h = 2, num_arc
    arc_info = [[0 for x in range(w)] for y in range(h)]
    for i in range(0, num_arc):
        arc_info[i][0] = subElementObj_edge[i].getAttribute("sourceIndex")
        arc_info[i][1] = subElementObj_edge[i].getAttribute("targetIndex")

    #duration_info
    w, h = 1, num_arc
    duration_info = [[0 for x in range(w)] for y in range(h)]
    for i in range(0, num_arc):
        duration_info[i] = subElementObj_duration[i+num_transition].getAttribute("mean")
    #print("duration_info")
    print(duration_info)

    #transitoin_
    return transition_info,transition_name,arc_info,duration_info