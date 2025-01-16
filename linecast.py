#for casting a line segment across a space and see if it intersects with axis aligned bounding boxes (AABB collision)
import numpy as np
import shapely
from shapely.geometry import LineString, Point


def get_line_endpoint():
    pass

def get_rect_edges():
    pass

def line_intersection(p1, p2, p3, p4):
    line1 = LineString((p1[0], p1[1]),(p2[0], p2[1]))
    line2 = LineString((p3[0], p3[1]),(p4[0], p4[1]))

    intersection = line1.intersection(line2)
    #need to check the various cases for intersection, ie parallel lines, multiple points etc. we only want to deal with single intersects
    #there will be no complex intersects as the lines will be straight and parallels will be treated as misses for the sake of simplicity, 
    if intersection.geom_type == Point:
        return intersection
    else:
        return None


def cast_line():
    pass