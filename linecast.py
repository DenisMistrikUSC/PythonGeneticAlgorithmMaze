#for casting a line segment across a space and see if it intersects with axis aligned bounding boxes (AABB collision)
import numpy as np
import shapely
from shapely.geometry import LineString, Point


#given a certain length of line cast, return the end point given its direction and length
def get_line_endpoint(start_position : np.ndarray, direction : np.ndarray, length) -> np.ndarray:
    end_pos = start_position + (direction * length)
    return end_pos

#from the AABB points, get each edge of the rectangle obstacle format will be 2d numpy array
def get_rect_edges(top_left : np.ndarray, bottom_right : np.ndarray) -> np.ndarray:
    
    top = np.array([top_left, np.array([bottom_right[0], top_left[1]])])
    left = np.array([top_left, np.array([top_left[0], bottom_right[1]])])
    right = np.array([np.array([bottom_right[0], top_left[1]]), bottom_right])
    bottom = np.array([np.array([top_left[0], bottom_right[1], bottom_right])])

    return np.array([top,left,right,bottom])

def line_intersection(p1 : np.ndarray, p2 : np.ndarray, p3 : np.ndarray, p4 : np.ndarray) -> Point:
    line1 = LineString((p1[0], p1[1]),(p2[0], p2[1]))
    line2 = LineString((p3[0], p3[1]),(p4[0], p4[1]))

    intersection = line1.intersection(line2)
    #need to check the various cases for intersection, ie parallel lines, multiple points etc. we only want to deal with single intersects
    #there will be no complex intersects as the lines will be straight and parallels will be treated as misses for the sake of simplicity, 
    if intersection.geom_type == Point:
        return intersection
    else:
        return None

#this will be called in the new genetic agent, cast a line of a certain direction and length, compare against all obstacles, return the distance between
#nearest collision
#obstacles list is a list of np arrays of size 2 which hold 2d vector np arrays ie [[1.0,2.0], [2.0,3.0]] top_left is element 0, bot right is element 1
def cast_line(start_position : np.ndarray, direction : np.ndarray, length : float, obstacles : list[np.ndarray]) -> float:
    
    endpoint = get_line_endpoint(start_position=start_position, direction=direction, length=length)
    least_distance = length #if no collisions are detected simply return the length of the line segment
    for edge in (edge for obstacle in obstacles for edge in get_rect_edges(obstacle[0], obstacle[1])):
        intersect = line_intersection(start_position, endpoint, edge[0], edge[1])
        if intersect is not None:
            distance_to_collision = shapely.distance(Point(start_position[0], start_position[1]), intersect)
            if distance_to_collision < least_distance:
                least_distance = distance_to_collision
    
    return least_distance