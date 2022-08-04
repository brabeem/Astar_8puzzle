from cmath import inf
import copy
# from sre_parse import State


initial_state = [
                    [5,4,8],
                    [3,7,6],     
                    [2,1,0], ]  ##initial board state,unorganized state ##here 0 represents empty box in the puzzle

goal_state =    [
                    [1,2,3],
                    [4,5,6],
                    [7,8,0],
                            ]
                              ## arrangement of numbers for the final state we want to reach##
goal_positions = [(2,2),(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1)]
exploredList = []

###class related to game mechanics of the 8 puzzle                              
class game_kanda():
    def actions(self,state):
        ##return all the possible actions given a state
        where = self.where(state)
        allActions = [(1,0),(-1,0),(0,1),(0,-1)] ##relative possible movement for the zero block
        for i in range(len(allActions)):
            allActions[i] = (allActions[i][0] + where[0],allActions[i][1] + where[1])
        ## now allActions contain the actual position of O block ##

        validActions = []
        for el in allActions:
            if self.isValidAction(el):
                validActions.append(el)
        return validActions

    ###where does the empty box lie
    def where(self,state):
        where = (0,0)
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 0:
                    return (i,j)
        ###found the position of zero in the block

    
                     

    def isValidAction(self,action):
        ##check if the action is a valid action since any action could exceed the board size
        if action[0] <= 2 and action[0] >= 0:
            if action[1] <= 2 and action[1] >= 0:
                return True
    



    def isGoalState(self,state):
        ##check if the given state is the goal state##
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] != goal_state[i][j]:
                    return False
        return True
                

    def result(self,state,action):
        ##Since you dont wanna modify the original state create a copy of the state and work with that
        ##what is the resulting state as a result of taking the given action in the given state##
        state = copy.deepcopy(state)
        where = self.where(state)##where 0 is 
        ##action = where we want 0 to be
        value_to_be_exchanged = state[action[0]][action[1]]
        state[action[0]][action[1]] = 0
        state[where[0]][where[1]] = value_to_be_exchanged
        return state
        ##This returns a brand new version of the state     


class Node():
    def __init__(self,parent=None,state=None,action=None):
        self.parent = parent
        self.state = state
        self.action = action
        self.hn = 0
        self.gn = 0
        if self.parent != None:
            self.gn = self.parent.gn + 1
        # print(self.gn)
        self.total_cost = 0
        self.calcTotal_cost()
    

    def calcHeuristic(self):
        ##calculate the heuristic value (How close to the goal state)
        manhattan_dist  = 0
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                    position = goal_positions[self.state[i][j]]
                    manhattan_dist += (abs(position[0]- i) + abs(position[1]-j))  
        self.hn = manhattan_dist
       

    def calcTotal_cost(self):
        ##calculate the total cost from the intital point to the goal state 
        self.calcHeuristic()
        self.total_cost = self.hn + self.gn


class frontier():
    def __init__(self):
        self.theList = []
        self.theList.append(Node(state=initial_state))

    def add(self,node):
        ##add a node to the frontier
        self.theList.append(node)


    def remove(self):
        ##remove a node from the frontier on the basis of A*
        min = inf
        for el in self.theList:
            ##find the node with the minimum totalPathCost
            if el.total_cost < min:
                min = el.total_cost
                minNode = el
        self.theList.remove(minNode)
        return minNode
    ##returns the best node from the frontier



    def inFrontier(self,node):
        ##check if the node is already in the frontier
        for n in self.theList:
            if self.areMatched(node,n):
                return True
        return False


    def areMatched(self,node1,node2):
        ##check of two nodes are same
        for i in range(len(node1.state)):
            for j in range(len(node1.state[i])):
                if node1.state[i][j] != node2.state[i][j]:
                    return False
        return True





##NOW the actual code to perform A* algorithm
##Create a frontier with the node belonging to initial state
F = frontier()
G = game_kanda()

def inExplored(node):
    ##check if the node in already explored
    ##check from the exploredList for the given node
    for n in exploredList:
        if F.areMatched(node,n):
            return True
    return False



##backtrack from the goal state to find out the sequences of actions##
actions_to_goal = []##sequences of actions to goal


def backtrack(node):
    if node.parent == None:
        return ##return if the parent is None##
    actions_to_goal.append(node.action)
    return backtrack(node.parent)



#In a loop
while(1):
    # Remove a node 
    removedNode = F.remove()
    ##mark this node as  an explored node#
    exploredList.append(removedNode)
    ##if no node to remove
    if removedNode == None:
        print("There solution is not possible")
        break

    ##check if the removed node is the goal node
    if G.isGoalState(removedNode.state):
        ##backtrack the nodes to the initial state and find the sequence of actions that led to the goal
        backtrack(removedNode)
        actions_to_goal.reverse()##list reversed
        ##show all the actions and reach the goal in the actual puzzle##
        state = initial_state
        print(state)
        for action in actions_to_goal:
            state = G.result(state=state,action=action)
            print(state)
        break
    ##not a goal state
    else:
        ##find all the possible nodes reacheable from this node and expand the tree
        actions = G.actions(removedNode.state)
        for action in actions:
            newstate = G.result(removedNode.state,action)
            newNode = Node(removedNode,newstate,action)
            if not (F.inFrontier(newNode) or inExplored(newNode)):
                ##if not found in both then only add the newNode to the frontier
                F.add(newNode)
        ##we are done








