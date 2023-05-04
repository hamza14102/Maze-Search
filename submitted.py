# submitted.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Kelvin Ma (kelvinm2@illinois.edu) on 01/24/2021

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# submitted should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi)


import queue


def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    path = []

    q = queue.Queue()
    q.put((maze.start, ))
    visited = set()
    visited.add((maze.start, ))
    while (not q.empty()):
        curr_path = q.get()
        pos = curr_path[-1]
        if pos == maze.waypoints[0]:
            return curr_path
        for n in maze.neighbors(pos[0], pos[1]):
            if ((n,) in visited):
                continue
            visited.add((n,))
            next_step = curr_path + (n,)
            q.put(next_step)

    return []


def astar_single(maze):
    """
    Runs A star for part 2 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    q = queue.PriorityQueue()
    dest = maze.waypoints[0]
    start = maze.start
    q.put((0, start))

    visited = set()
    visited.add((start, ))

    while (not q.empty()):
        curr_path = q.get()
        pos = curr_path[-1]
        if pos == maze.waypoints[0]:
            return curr_path[1:]

        for n in maze.neighbors(pos[0], pos[1]):
            if (n == dest):
                return curr_path[1:] + (n,)
            if ((n,) in visited):
                continue
            visited.add((n,))
            g = len(curr_path[1:])
            h = abs(dest[0] - n[0]) + abs(dest[1] - n[1])
            next_step = (g + h,) + curr_path[1:] + (n,)
            q.put(next_step)

    return []

# This function is for Extra Credits, please begin this part after finishing previous two functions


def astar_multiple(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """

    graph = {}
    for a in maze.waypoints:
        for b in maze.waypoints:
            if (a not in graph):
                graph[a] = {}
            if (b not in graph):
                graph[b] = {}
            dist = abs(a[0] - b[0]) + abs(a[1] - b[1])
            graph[a][b] = dist
            graph[b][a] = dist

    q = queue.PriorityQueue()
    q.put((0, maze.start, set(maze.waypoints)))
    prev = {}
    explored = set()
    explored.add((maze.start, len(maze.waypoints)))
    to_ret = []
    while (not q.empty()):
        f_val, pos, to_explore = q.get()
        # print(f_val, pos, to_explore, left_count)
        c = 0
        if (pos in to_explore):
            c = 1
        to_explore.discard(pos)
        if (len(to_explore) == 0):
            path = [pos]
            temp = 1
            while (prev[(pos, temp)] != (maze.start, len(maze.waypoints))):
                pos, temp = prev[(pos, temp)]
                path.append(pos)
            path.append(maze.start)
            path.reverse()
            if (len(to_ret) == 0 or len(path) < len(to_ret)):
                to_ret = path
            continue

        for neighbor in maze.neighbors(pos[0], pos[1]):
            if ((neighbor, len(to_explore)) not in explored):
                explored.add((neighbor, len(to_explore)))
                prev[neighbor, len(to_explore)] = (pos, len(to_explore) + c)

                min_dist = min(
                    abs(point[0] - neighbor[0]) + abs(point[1] - neighbor[1]) for point in to_explore)

                for waypoint in to_explore:
                    dist = abs(waypoint[0] - neighbor[0]) + \
                        abs(waypoint[1] - neighbor[1])
                    if (dist <= min_dist):
                        min_dist = dist
                        nearest_waypoint = waypoint
                        break

                h = min_dist
                for waypoint in to_explore:
                    h += graph[nearest_waypoint][waypoint]

                q.put((h, neighbor, to_explore.copy()))
    return to_ret
    # graph = {}
    # siz = 1
    # level = 1
    # for a in maze.waypoints:
    #     for b in maze.waypoints:
    #         # if a != b:
    #         if (a not in graph):
    #             graph[a] = {}
    #         if (b not in graph):
    #             graph[b] = {}
    #         dist = abs(a[0] - b[0]) + abs(a[1] - b[1])
    #         graph[a][b] = dist
    #         graph[b][a] = dist

    # q = queue.PriorityQueue()
    # prev = {}

    # q.put((0, set(maze.waypoints), maze.start, maze.start, ))
    # visited = set()
    # visited.add((maze.start, maze.start, 0))
    # while not q.empty():
    #     curr_path = q.get()
    #     pos = curr_path[-1]
    #     prv = curr_path[2]

    #     curr_path[1].discard(pos)
    #     if len(curr_path[1]) == 0:
    #         x = curr_path[0]
    #         # print(x)
    #         to_ret = [pos]
    #         while (prev[(pos, prv, x)]) != (maze.start, maze.start, 0):

    #             (pos, prv, x) = prev[(pos, prv, x)]
    #             to_ret.append(pos)
    #         to_ret.append(prv)
    #         to_ret.reverse()

    #         return to_ret

    #     for n in maze.neighbors(pos[0], pos[1]):
    #         if ((n, pos, curr_path[0]) in visited):
    #             continue
    #         visited.add((n, pos, curr_path[0]))

    #         # g = len(curr_path[1:])

    #         min_dist = min(
    #             abs(point[0] - n[0]) + abs(point[1] - n[1]) for point in curr_path[1])

    #         for waypoint in curr_path[1]:
    #             dist = abs(waypoint[0] - n[0]) + abs(waypoint[1] - n[1])
    #             if (dist <= min_dist):
    #                 min_dist = dist
    #                 nearest_waypoint = waypoint
    #                 break

    #         h = min_dist
    #         for waypoint in curr_path[1]:
    #             h += graph[nearest_waypoint][waypoint]
    #         h += (abs(n[0] - pos[0]) + abs(n[1] - pos[1])) + level
    #         cp = curr_path[1].copy()
    #         if ((n, pos, h) not in prev):

    #             prev[(n, pos, h)] = (pos, prv, curr_path[0])
    #             next_step = (h, cp, pos, n)

    #             q.put(next_step)

    #     siz -= 1
    #     if (siz == 0):
    #         siz = q.qsize()
    #         level += 1

    # return []
