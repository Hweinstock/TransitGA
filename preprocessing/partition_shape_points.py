from typing import List 

from transit_network.shapes import ShapePoint
from transit_network.stops import Stop 

from root_logger import RootLogger

def closest_shape_point_index(cur_stop: Stop, shape_points: List[ShapePoint]) -> int: 

    min_index = -1 
    min_distance = float('inf')
    for index, shape_pt in enumerate(shape_points):
        cur_dist = cur_stop.distance_to_point(shape_pt)
        if cur_dist < min_distance:
            min_index = index 
            min_distance = cur_dist 
    
    return min_index

def partition_shape_points(shape_points: List[ShapePoint], stops: List[Stop]) -> List[List[ShapePoint]]:
    partition = []
    cur_shape_points = [pt for pt in shape_points]
    num_stops = len(stops)
    for stop_index, stop in enumerate(stops):
        if cur_shape_points == []:
            RootLogger.log_error(f'Ran out of shapes to assign. On stop {stop_index} of {num_stops}.')
        closest_index = closest_shape_point_index(stop, cur_shape_points)
        cur_partition = cur_shape_points[:closest_index]
        cur_shape_points = cur_shape_points[closest_index:]
        partition_len = len(cur_partition)
        
        RootLogger.log_debug(f'Assigning {partition_len} shapes points to stop {stop.id}, {len(cur_shape_points)} left to assign.')
        partition.append(cur_partition)
    
    if cur_shape_points != []:
        RootLogger.log_warning(f'Failed to assign all shape points, {len(cur_shape_points)} remaining.')
        partition[-1] += cur_shape_points

    return partition


def old_partition_shape_points(shape_points: List[ShapePoint], stops: List[Stop]) -> List[List[ShapePoint]]:
    partition = []
    cur_stop_points = []

    num_stops = len(stops)
    num_points = len(shape_points)

    cur_closest_stop_index = 0
    prev_dist_to_stop = 0

    local_min = float('inf')
    for point in shape_points:
        # Current stop that is closest
        closest_stop = stops[cur_closest_stop_index]

        # Distance from stop to ShapePoint 
        cur_dist_to_cur_stop = closest_stop.distance_to_point(point)
        local_min = min(local_min, cur_dist_to_cur_stop)
        if cur_dist_to_cur_stop == 0.0:
            RootLogger.log_debug(f'Found shape point on top of stop!')

        # If this distance is increasing i.e. we are moving away from stop, move to next stop. 
        if cur_dist_to_cur_stop > prev_dist_to_stop:
            partition.append(cur_stop_points)

            cur_stop_points = []
            cur_closest_stop_index += 1
            if cur_closest_stop_index == num_stops:
                cur_closest_stop_index -= 1
                RootLogger.log_warning(f'Hit final stop, but at point {point.sequence_num} out of {num_points}. \
                    decrementing cur_closest_stop_index')

            closest_stop = stops[cur_closest_stop_index]
            cur_dist_to_cur_stop = closest_stop.distance_to_point(point)

        prev_dist_to_stop = cur_dist_to_cur_stop
        cur_stop_points.append(point)
    
    # Add final stop
    partition.append(cur_stop_points)
    cur_closest_stop_index += 1
    RootLogger.log_debug(f'Found minimum distance: {local_min}')
    if cur_closest_stop_index < num_stops:
        RootLogger.log_error(f'Invalid partition generated for stops. Made it to stop {cur_closest_stop_index} out of {num_stops}')
    return partition