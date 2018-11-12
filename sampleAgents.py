# sampleAgents.py
# parsons/07-oct-2017
#
# Version 1.1
#
# Some simple agents to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agents here are extensions written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

# RandomAgent
#
# A very simple agent. Just makes a random pick every time that it is
# asked for an action.
class RandomAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# RandomishAgent
#
# A tiny bit more sophisticated. Having picked a direction, keep going
# until that direction is no longer possible. Then make a random
# choice.
class RandomishAgent(Agent):

    # Constructor
    #
    # Create a variable to hold the last action
    def __init__(self):
         self.last = Directions.STOP

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it. Otherwise make a
        # random choice.
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.last = pick
            return api.makeMove(pick, legal)

# SensingAgent
#
# Doesn't move, but reports sensory data available to Pacman
class SensingAgent(Agent):

    def getAction(self, state):

        # Demonstrates the information that Pacman can access about the state
        # of the game.

        # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)

        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)

        # getAction has to return a move. Here we pass "STOP" to the
        # API to ask Pacman to stay where they are.
        return api.makeMove(Directions.STOP, legal)

class BreadthSearchAgentSimple(Agent):



    def breadth_first_search(self, wall_locations, food_positions, ghost_locations, pacman):

        #check locations
        Grid = [(0,1), (0,-1), (1,0), (-1,0)]
        # check nodes
        # for x, y in Grid:
        #     if (x + pacman[0], y + pacman[1]) in api.walls(state):
        #
        # a FIFO Queue
        my_queue = util.Queue()
        # an empty set to maintain visited nodes
        visited = set()
        # a dictionary to maintain meta information (used for path formation)
        # key -> (parent state, action to reach child)
        my_path = dict()
        # initialize

        my_queue.push(pacman)
        visited.add(pacman)
        # (None,None) because it is the root
        my_path[pacman] = (None, None) #meta[child]=parent or meta[child]= subtree_root

    #   as long as there are nodes in the queue, keep exploring
        while not my_queue.isEmpty():
            node_location = my_queue.pop()
            if node_location in food_positions:
                return self.construct_path(my_path, node_location)
            for g in Grid:
                next_node = (node_location[0] + g[0], node_location[1] + g[1])
                if next_node in wall_locations:
                    continue
                if next_node in visited:
                    continue
                if next_node in ghost_locations:
                    continue
                my_queue.push(next_node)
                visited.add(next_node)
                my_path[next_node] = node_location



    def construct_path(self, my_path, food_node):

        action_list = list()
        # Continue until you reach root meta data (i.e. (None, None))
        while not my_path[food_node] == (None,None):

            action_list.append(food_node)
            food_node = my_path[food_node]

        return action_list[-1]

    def getAction(self, state):
        food_positions = api.food(state)
        wall_locations = api.walls(state)
        pacman = api.whereAmI(state)
        capsule_locations = api.capsules(state)
        ghost_locations = api.ghosts(state)
        move = self.breadth_first_search(wall_locations, food_positions, ghost_locations, pacman)
        print("Ghost locations:", ghost_locations)
        print("Move:", move)
        print("Pacman:", pacman)
        print("capsule_locations:", capsule_locations)
        Grid = [(0,1), (0,-1), (1,0), (-1,0)]

        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)


        if move[0] > pacman[0]:
            return api.makeMove(Directions.EAST, legal)
        if move[0] < pacman[0]:
            return api.makeMove(Directions.WEST, legal)
        if move[1] > pacman[1]:
            return api.makeMove(Directions.NORTH, legal)
        if move[1] < pacman[1]:
            return api.makeMove(Directions.SOUTH, legal)
        else:
            pick = random.choice(legal)
            return api.makeMove(pick, legal)


class BreadthSearchAgentGhosts(Agent):

    # Create variables to remember way points pacman has not visited before
    def __init__(self):
        self.way_points = []
    def final(self,state):
        self.way_points=[]
        self.visited_list=[]
# """This is the first BFS which is only active when a ghost is either visible or in hearing range. The BFS takes the coordinates of walls, ghosts and pacman from the api.
#     Then instead of aiming for the ghost node, I remove the direction leading to the ghost from the legal actions and instruct pacman to move into either the opposite or
#     or diagonal opposite direction, depending on if the ghost shares an axis with pacman."""


    def breadth_first_search_ghost(self, wall_locations, ghost_locations, pacman):

        #check locations
        grid = [(0,1), (0,-1), (1,0), (-1,0)]
        # a first in first out queue (FIFO)
        my_queue = util.Queue()
        # an empty set to maintain visited nodes in order to only visit nodes that have not been visited before
        visited = set()
        # a dictionary to maintain meta information (used for path formation)
        # key -> (parent state, action to reach child)
        my_path = dict()
        # initialize the queue
        my_queue.push(pacman)
        visited.add(pacman)
        #(None,None) because it is the root
        my_path[pacman] = (None, None)
        #as long as there are nodes in the queue, keep exploring surrounding nodes
        while not my_queue.isEmpty():
            # following the principle of FIFO the first node gets popped out of the queue.
            node_location = my_queue.pop()
            # if the closest node is in the reach of an ghost the BFS emidiately returns the node to my path construction function
            if node_location in ghost_locations:
                return self.construct_path(my_path, node_location)
            #loop through surrounding nodes
            for g in grid:
                next_node = (node_location[0] + g[0], node_location[1] + g[1])
                # if next node in a wall or has been visited before, skip the node
                if next_node in wall_locations:
                    continue
                if next_node in visited:
                    continue
                my_queue.push(next_node)
                visited.add(next_node)
                my_path[next_node] = node_location

# """This BFS is active when a food node is in reach. Otherwise identical to the ghost BFS. Coordinates for ghosts, food, walls, capsules and pacman come from the api.
#     Leaving searching for ghosts in the nodes should be unnecessary as the ghost BFS gets active when a ghost is visible or audible but I thought 'better be safe than sorry'."""

    def breadth_first_search(self, wall_locations, food_positions, ghost_locations, capsule_locations, pacman):

        #check locations
        grid = [(0,1), (0,-1), (1,0), (-1,0)]
        # a first in first out queue (FIFO)
        my_queue = util.Queue()
        # an empty set to maintain visited nodes in order to only visit nodes that have not been visited before
        visited = set()
        # a dictionary to maintain meta information (used for path formation)
        # key -> (parent state, action to reach child)
        my_path = dict()
        # initialize
        my_queue.push(pacman)
        visited.add(pacman)
        #(None,None) because it is the root
        my_path[pacman] = (None, None)
        #as long as there are nodes in the queue, keep exploring
        while not my_queue.isEmpty():
            node_location = my_queue.pop()
            if node_location in food_positions or capsule_locations:
                return self.construct_path(my_path, node_location)
            for g in grid:
                next_node = (node_location[0] + g[0], node_location[1] + g[1])
                if next_node in wall_locations:
                    continue
                if next_node in visited:
                    continue
                if next_node in ghost_locations:
                    continue
                my_queue.push(next_node)
                visited.add(next_node)
                my_path[next_node] = node_location

# """This BFS taps into the saved the all the available coordinates that are not in a wall and have not been visited before. Should Pacman run out of
#     food nodes to visit, BFS_waypoints will get active by constructing a path to the nearest 'virgin' node."""

    def breadth_first_search_way_points(self, wall_locations, waypoints, ghost_locations, pacman):

        #check locations
        grid = [(0,1), (0,-1), (1,0), (-1,0)]
        # a FIFO Queue
        my_queue = util.Queue()
        # an empty set to maintain visited nodes
        visited = set()
        # a dictionary to maintain meta information (used for path formation)
        # key -> (parent state, action to reach child)
        my_path = dict()
        # initialize
        my_queue.push(pacman)
        visited.add(pacman)
        # (None,None) because it is the root
        my_path[pacman] = (None, None)
        #as long as there are nodes in the queue, keep exploring
        while not my_queue.isEmpty():
            node_location = my_queue.pop()
            if node_location in waypoints:
                return self.construct_path(my_path, node_location)
            for g in grid:
                next_node = (node_location[0] + g[0], node_location[1] + g[1])
                if next_node in wall_locations:
                    continue
                if next_node in visited:
                    continue
                if next_node in ghost_locations:
                    continue
                my_queue.push(next_node)
                visited.add(next_node)
                my_path[next_node] = node_location

# """The construct path function takes the node and my_path dictionary returned by one of the three BFS functions and returns the first action"""

    def construct_path(self, my_path, food_node):
        # initializeempty action list
        action_list = list()
        # Continue until you reach root meta data (i.e. (None, None))
        while not my_path[food_node] == (None,None):
            action_list.append(food_node)
            food_node = my_path[food_node]
        # reverse action list to get the first action
        action_list = action_list[::-1]
        # to not crash the code in case a certain BFS returns an empty list which creates errors when indexing
        if action_list:
            return action_list[0]
        if not action_list:
            return None

# """The getAction function containing the movement conditions for the returned path, calling the api for information on food, walls, capsules, ghosts
#     and Pacman."""

    def getAction(self, state):
        # Below i call the api for all the information Pacman needs to navigate and (hopefully) succeed in this world
        food_positions = api.food(state)
        capsule_locations = api.capsules(state)
        wall_locations = api.walls(state)
        pacman = api.whereAmI(state)
        ghost_locations = api.ghosts(state)
        # I store the waypoints for Pacman to visit them later when he has run out of visible food nodes
        waypoints = self.way_points
        # ghost_move refers to the BFS that is active when a ghost is visible or audibl
        ghost_move = self.breadth_first_search_ghost(wall_locations, ghost_locations, pacman)
        # move refers to the BFS that is active when a food node or capsule is in reach
        move = self.breadth_first_search(wall_locations, food_positions, ghost_locations, capsule_locations, pacman)
        # move2 refers to the BFS that is active when no food nodes, capsules or ghosts are in reach, so Pacman instead moves to an previously unvisited way point
        move2 = self.breadth_first_search_way_points(wall_locations, waypoints, ghost_locations, pacman)

        grid = [(0,1), (0,-1), (1,0), (-1,0)]
# """Get all the floor coordinates by creating a complete grid. The complete grid is then used for the waypoints BFS which searches for
#     untouched nodes when there is no food in sight. I start by acquiring the corners."""
        corners = api.corners(state)
        x_axis = []
        y_axis = []
        # find the maximum and minimum values of the x and y axis for the complete grid.
        # minimum here not as relevant as the lowest coordinate value is 0
        for corner in corners:
            x_axis.append(corner[0])
        for corner in corners:
            y_axis.append(corner[1])
        # maximum x-axis and y-axis value
        max_X=max(x_axis)
        max_Y=max(y_axis)
        # create a complete grid
        grid_plan = []
        for x in range(max_X+1):
            for y in range(max_Y+1):
                grid_plan.append((x,y))

        #i check if the list is empty so the way points get only added once.
        if self.way_points ==[]:
            # only append to waypoints if the point is not a wall
            for grid_point in grid_plan:
                if grid_point not in wall_locations:
                    self.way_points.append(grid_point)
        # remove way points from the list once pacman has visited them
        if pacman in self.way_points:
            self.way_points.remove(pacman)
        # I leave Directions.STOP in legal as that helps prevent the code from crashing in rare scenarios
        legal = api.legalActions(state)
        # should a ghost be in reach and the bfs managed to construct a path, Pacman will move into the opposite direction of where the ghost is
        # should that not be possible, I remove the direction leading to the ghost and execute a random action
        if ghost_locations > 0 and ghost_move != None:

            print("GHOSTS ARE SOMEWHERE CLOSE", ghost_locations)
            # if the ghost and pacman share the same x-axis and the ghost has a higher y-axis value
            if ghost_move[0] == pacman[0] and ghost_move[1] > pacman[1]:
                if Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                if Directions.EAST in legal:
                    return api.makeMove(Directions.EAST,legal)
                if Directions.WEST in legal:
                    return api.makeMove(Directions.WEST,legal)
                else:
                    # remove the direction of the ghost and pick a random remaining legal direction
                    legal.remove(Directions.NORTH)
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            # if the ghost and pacman share the same x-axis and the ghost has a lower y-axis value
            if ghost_move[0] == pacman[0] and ghost_move[1] < pacman[1]:
                if Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                if Directions.EAST in legal:
                    return api.makeMove(Directions.EAST,legal)
                if Directions.WEST in legal:
                    return api.makeMove(Directions.WEST,legal)

                else:
                    legal.remove(Directions.SOUTH)
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

            if ghost_move[0] > pacman[0] and ghost_move[1] == pacman[1]:
                if Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                if Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH,legal)
                if Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH,legal)
                else:
                    legal.remove(Directions.EAST)
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

            if ghost_move[0] < pacman[0] and ghost_move[1] == pacman[1]:
                if Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                if Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH,legal)
                if Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH,legal)
                else:
                    legal.remove(Directions.WEST)
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                pick = random.choice(legal)
                return api.makeMove(pick, legal)

        # should Pacman be in reach of food, the variable "move" should not be empty and Pacman moves towards the direction of the food
        if move != None and ghost_move==None:

            print("BFS FOOD ACTIVATED")

            if move[0] > pacman[0]:
                return api.makeMove(Directions.EAST, legal)
            if move[0] < pacman[0]:
                return api.makeMove(Directions.WEST, legal)
            if move[1] > pacman[1]:
                return api.makeMove(Directions.NORTH, legal)
            if move[1] < pacman[1]:
                return api.makeMove(Directions.SOUTH, legal)
            else:
                pick = random.choice(legal)
                return api.makeMove(pick, legal)

        # should there be no food or ghost in reach, the variable "move2" should contain an action to a previously undiscovered location stored in waypoints
        if move2 != None and ghost_move==None:

            print("BFS WAYPOINTS ACTIVE")

            if move2[0] > pacman[0]:
                return api.makeMove(Directions.EAST, legal)
            if move2[0] < pacman[0]:
                return api.makeMove(Directions.WEST, legal)
            if move2[1] > pacman[1]:
                return api.makeMove(Directions.NORTH, legal)
            if move2[1] < pacman[1]:
                return api.makeMove(Directions.SOUTH, legal)
            else:
                pick = random.choice(legal)
                return api.makeMove(pick, legal)
        # should all the BFS fail, execute a random move
        else:
            print("RANDOM MOVE")
            pick = random.choice(legal)
            return api.makeMove(pick, legal)
