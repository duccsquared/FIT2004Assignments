from queue import Queue
import math


class Vertex:
    def __init__(self,vertexId):
        """
        Initializes the Vertex class, which represents a vertex within a circulation flow graph that can
        have a demand
        :Input:
            vertexId:
                the index of the vertex within the graph's vertexList
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        self.id = vertexId 
        self.edges = [] 
        self.sourceEdge = None # an edge from the source to this vertex
        self.sinkEdge = None # an edge from this vertex to the sink
        self.discovered = False # has this vertex been discovered this iteration?
        self.prevEdge = None # previous edge in a ford-fulkerson path
    def getDemand(self):
        """
        Obtains the demand of the vertex
        :Output, return or postcondition:
            the numeric demand of the vertex
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        # more flowing in = positive, more flowing out = negative
        return self.sinkEdge.capacity - self.sourceEdge.capacity
    def setDemand(self,demand):
        """
        Sets the demand of the vertex
        :Input:
            demand:
                The new demand of the vertex
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        self.sourceEdge.setCapacity(abs(min(0,demand)))
        self.sinkEdge.setCapacity(abs(max(0,demand)))
    def changeDemand(self,demand,modifyFlow=False):
        """
        Modifies the demand by a value, and optionally modifies the flow accordingly
        :Input:
            demand:
                A number representing the change in the demand of the vertex
            modifyFlow:
                A boolean for whether to modify the flow based on the change in demand
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        # modify demand
        self.setDemand(self.getDemand()+demand)
        # should the flow also be modified?
        if(modifyFlow):
            # modify flow accordingly
            self.sourceEdge.setFlow(min(self.sourceEdge.capacity,max(0,self.sourceEdge.flow + demand * -1)))
            self.sinkEdge.setFlow(min(self.sinkEdge.capacity,max(0,self.sinkEdge.flow + demand)))

class Edge:
    def __init__(self,u,v,capacity,flow=0,isInverse=False,lowerBound=0):
        """
        Instantiates the Edge class, which represents connections within a circulation graph
        that allow for flow bounded by a lower and higher bound
        :Input:
            u:
                the vertex at which the edge starts
            v:
                the vertex at which the edge ends
            capacity:
                the maximum flow that can go through the edge
            flow:
                the value being transferred from the starting vertex to the ending vertex
            isInverse:
                a boolean representing whether the current edge is a residual edge
            lowerBound:
                the minimum flow that has to flow through the edge after the network flow is calculated            
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        self.u = u
        self.v = v 
        self.flow = flow
        self.capacity = capacity # highest flow allowed
        self.isInverse = isInverse # boolean to check if this is an inverse edge
        self.invEdge = None # this edges' counterpart
        self.lowerBound = lowerBound # lowest flow allowed
    def setCapacity(self,capacity):
        """
        sets the capacity of the edge, along with the inverse edge's capacity
        :Input:
            capacity:
                the new capacity for the current and inverse edge
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        self.capacity = capacity
        self.invEdge.capacity = self.capacity 
    def getResidual(self):
        """
        obtains the residual of the edge (ie how much more flow can be pushed in)
        :Output, return or postcondition:
            the residual of the edge
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        return  self.capacity - self.flow
    def setFlow(self,flow):
        """
        sets the flow of the edge, along with the inverse edge's flow
        :Input:
            flow:
                the new flow for the edge
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        self.flow = flow 
        self.invEdge.flow = self.getResidual()
    def changeFlow(self,flow):
        """
        modifies the flow of the edge, along with the inverse edge's flow
        :Input:
            flow:
                the change in flow for the edge
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        self.setFlow(self.flow+flow)


class CirculationGraph:
    def __init__(self,vertexCount):
        """
        Instantiates a CirculationGraph class, which represents a group of vertexes and edges that
        can be used to calculate a circulation flow
        :Input:
            vertexCount:
                the integer number of vertexes that the circulation graph should have
        :Time complexity:
            O(V+E) where V is the number of vertexes and E is the number of edges
        :Aux space complexity:
            O(V+E) where V is the number of vertexes and E is the number of edges
        
        """
        # setup vertexes
        self.vertexes = [Vertex(i) for i in range(vertexCount)]
        # get source and sink
        self.source = Vertex(vertexCount)
        self.sink = Vertex(vertexCount+1)
        # add source and sink to the list of vertexes
        self.vertexes.append(self.source)
        self.vertexes.append(self.sink)
        # connect vertexes to sources and sinks
        for u in self.vertexes:
            u.sourceEdge = self.addEdge(self.source,u,0,0)
            u.sinkEdge = self.addEdge(u,self.sink,0,0)  

    def addEdge(self,u,v,capacity,flow=0,lowerBound=0):
        """
        Creates an edge along with its inverse edge and adds them to the vertexes accordingly
        :Input:
            u:
                the vertex at which the edge starts
            v:
                the vertex at which the edge ends
            capacity:
                the maximum flow that can go through the edge
            flow:
                the value being transferred from the starting vertex to the ending vertex
            lowerBound:
                the minimum flow that has to flow through the edge after the network flow is calculated  
        :Output, return or postcondition:
            the edge that was created
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        # create edge and inverse edge
        edge = Edge(u,v,capacity,flow=flow,lowerBound=lowerBound)
        invEdge = Edge(v,u,capacity,flow=capacity-flow,isInverse=True,lowerBound=lowerBound)
        # pair together edges
        edge.invEdge = invEdge 
        invEdge.invEdge = edge 
        # add edge and inverse edges to the vertexes
        u.edges.append(edge)
        v.edges.append(invEdge)
        # return edge
        return edge
    def __len__(self):
        """
        Obtains the number of vertexes within the graph
        :Output, return or postcondition:
            The number of vertexes within the graph
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        return len(self.vertexes)
    def __getitem__(self,i):
        """
        Returns a vertex within the graph
        :Input:
            i:
                The indice of the vertex list to be acccessed
        :Output, return or postcondition:
            A vertex at the position specified by the parameter
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        return self.vertexes[i]
    def reduceLowerBounds(self):
        """
        Modifies the edges and vertexes of the graph to account for the lower bound of the edges 
        :Time complexity:
            O(V + E) where V is the number of vertexes and E is the number of edges
        :Aux space complexity:
            O(1)
        """
        # loop through each edge
        for u in self.vertexes:
            for edge in u.edges:
                # update if the edge isn't an inverse and has no lower bound
                lowerBound = edge.lowerBound
                if(lowerBound!=0 and not edge.isInverse):
                    # reduce capacity
                    edge.setCapacity(edge.capacity-lowerBound)
                    # reduce flow
                    edge.setFlow(max(edge.flow - lowerBound,0))
                    # modify demand to account for the changes
                    edge.u.changeDemand(lowerBound)
                    edge.v.changeDemand(-lowerBound)


    def restoreLowerBounds(self):
        """
        Reverses the effects of reducing the lower bounds
        :Time complexity:
            O(V + E) where V is the number of vertexes and E is the number of edges
        :Aux space complexity:
            O(1)
        """
        # loop through each edge
        for u in self.vertexes:
            for edge in u.edges:
                lowerBound = edge.lowerBound
                # update if the edge isn't an inverse and has no lower bound
                if(lowerBound!=0 and not edge.isInverse):
                    # restore capacity
                    edge.setCapacity(edge.capacity+lowerBound)
                    # restore flow
                    edge.setFlow(max(edge.flow + lowerBound,0))
                    # modify demand to account for the changes
                    edge.u.changeDemand(-lowerBound,True)
                    edge.v.changeDemand(lowerBound,True)
    def findPathAndAugment(self):
        """
        Finds a valid path to push flow through from the source to the sink, and augments the path accordingly
        :Output, return or postcondition:
            whether the graph was augmented
        :Time complexity:
            O(V + E) where V is the number of vertexes and E is the number of edges
        :Aux space complexity:
            O(V) where V is the number of vertexes
        """
        # reset variables for vertexes
        for u in self.vertexes:
            u.discovered = False 
            u.prevEdge = None
        # create queue and add the source
        vertexQueue = Queue(len(self))
        vertexQueue.put((self.source,float('inf')))
        # set source as discovered with no previous edge
        self.source.discovered = True
        # keep looping until the queue runs out or the sink is found
        while True:
            # get vertex and bottleneck
            (u, bottleneck) = vertexQueue.get(timeout=6)
            # if the sink is found, set augment and exit loop
            if(u==self.sink):
                if bottleneck == float('inf') or bottleneck == 0: return False
                # backtrack through flow path and augment
                edge = self.sink.prevEdge 
                while edge != None:
                    edge.changeFlow(bottleneck)
                    edge = edge.u.prevEdge
                return True

            # for each neighbour
            for edge in u.edges:
                # check if more flow can be pushed into the edge
                if(edge.getResidual() > 0 and not edge.v.discovered):
                    # set as previous and discovered
                    edge.v.prevEdge = edge
                    edge.v.discovered = True
                    # add to queue
                    vertexQueue.put((edge.v,min(bottleneck,edge.getResidual())))
            # if there is no path, quit
            if(vertexQueue.empty()):
                return False


    def fordFulkerson(self):
        """
        calculates the flow of the circulation graph such that the largest possible flow 
        goes from the source to the sink of the graph
        :Time complexity:
            O(kE+kV) where V is the number of vertexes, E is the number of edges, and k is the number of iterations of the loop
        :Aux space complexity:
            O(V) where V is the number of vertexes
        """
        # take lower bound into account
        self.reduceLowerBounds()
        # while iterations still increase the maximum flow, augment the path
        while self.findPathAndAugment(): pass
        # undo the changes made to take the lower bound into account
        self.restoreLowerBounds()
    
class Day:
    def __init__(self,g,dayAvailability,start,housemates,restaurant,meals,end):
        """
        Creates an instance of the Day class, which manages which housemates (or restaurant) prepares
        the meals for a single day. this is represented in a form akin to a bipartite graph, with the 
        start and the end vertexes representing the "source" and the "sink"
        :Input:
            g:
                the circulation graph that contains housemates and meals that need to be set up 
            dayAvailability:
                a list with 5 items with each item being an integer corresponding to housemates based on these values:
                    0 = the housemate can't prepare any meals for this day
                    1 = the housemate can only prepare meals for breakfast
                    2 = the housemate can only prepare meals for dinner
                    3 = the housemates can prepare meals for either breakfast or dinner
            start:
                a vertex representing where flow starts within the day
            housemates:
                a list of five vertexes representing the housemates that could potentially cook a meal
            restaurant:
                a vertex representing ordering out from a restaurant
            meals:
                a list of two vertexes representing the breakfast and dinner meals
            end:
                a vertex representing where flow ends within the day
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        self.dayAvailability = dayAvailability
        self.start = start
        self.start.setDemand(-12) # allow a full flow to each housemate and restaurant
        self.housemates = housemates 
        self.restaurant = restaurant 
        self.mealMakers = self.housemates + [self.restaurant]
        self.meals = meals 
        self.end = end  
        self.end.setDemand(2) # 2 meals
        self.breakfastEdgeList = [None] * 6
        self.dinnerEdgeList = [None] * 6
        self.setupData(g)

    def setupData(self,g):
        """
        Connects the vertexes of the day together
        :Input:
            g:
                the circulation graph that contains housemates and meals that need to be set up 
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        # start to housemates + restaurant
        for u in self.mealMakers:
            g.addEdge(self.start,u,2) 
        # for each housemate
        for i in range(len(self.housemates)):
            # if they are available for breakfast, add edge
            if(self.dayAvailability[i] in (1,3)):
                edge = g.addEdge(self.housemates[i],self.meals[0],1) 
                self.breakfastEdgeList[i] = edge
            # if they are available for dinner, add edge
            if(self.dayAvailability[i] in (2,3)):
                edge = g.addEdge(self.housemates[i],self.meals[1],1)  
                self.dinnerEdgeList[i] = edge
        # allow the possibility of eating out for breakfast and dinner
        self.breakfastEdgeList[5] = g.addEdge(self.restaurant,self.meals[0],1)
        self.dinnerEdgeList[5] = g.addEdge(self.restaurant,self.meals[1],1)
        # connect meals to the end
        g.addEdge(self.meals[0],self.end,1)
        g.addEdge(self.meals[1],self.end,1)

    def getBreakfast(self):
        """
        obtains the housemate/restaurant that is preparing breakfast for the day
        :Output, return or postcondition:
            An integer between 0 - 5 representing the housemate/restaurant that is preparing breakfast
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        # try to find an edge entering breakfast that has a flow
        for (index,edge) in enumerate(self.breakfastEdgeList):
            # return the housemate/restaurant that will handle breakfast for the day
            if(edge!=None and edge.flow==edge.capacity):
                return index 
    def getDinner(self):
        """
        obtains the housemate/restaurant that is preparing dinner for the day
        :Output, return or postcondition:
            An integer between 0 - 5 representing the housemate/restaurant that is preparing dinner
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        # try to find an edge entering dinner that has a flow
        for (index,edge) in enumerate(self.dinnerEdgeList):
            # return the housemate/restaurant that will handle dinner for the day
            if(edge!=None and edge.flow==edge.capacity):
                return index 
def createGraph(days):
    """
    Calculates the size of the graph and creates a graph
    :Input:
        days: 
            the number of days to allocate meals for
    :Output, return or postcondition:
        g:
            the graph containing the scheduling circulation graph
        vertexesPerDay:
            the number of vertexes that go into each day (increases linearly with the number of days)
        constantVertexes:
            the base number of vertexes when there are no days
        graphSize:
            the size of the graph
    :Time complexity:
        O(1)
    :Aux space complexity:
        O(1)
    """
    # calculate the size of the graph
    vertexesPerDay = 2+2+6
    constantVertexes = 1+6
    graphSize = constantVertexes + days * vertexesPerDay
    # create graph
    g = CirculationGraph(graphSize)
    return g, vertexesPerDay, constantVertexes, graphSize
def processGraphIntoVariables(g,availability,days,vertexesPerDay,constantVertexes,graphSize):
    """
    Segments the vertexes within the graph into variables and classes, and returns the data
    :Input:
        g:
            the graph containing the scheduling circulation graph
        availability:
            a list of sublists of length 5 designating when each housemate can cook meals
        days: 
            the number of days to allocate meals for
        vertexesPerDay:
            the number of vertexes that go into each day (increases linearly with the number of days)
        constantVertexes:
            the base number of vertexes when there are no days
        graphSize:
            the size of the graph
    :Output, return or postcondition:
        overflowEnd:
            the end point for the overflows of the graph
        overflowList:
            a list of overflows corresponding to the housemates and the restaurant
        dayList:
            a list of day objects
    :Time complexity:
        O(N) where N is the number of days
    :Aux space complexity: 
        O(N) where N is the number of days
    """
    # setup the start/end vertex positions, along wih their associated demands
    # 0: overflow end
    # 1 - 6: overflow sums
    overflowEnd = g[0]
    overflowEnd.setDemand(10*days)
    overflowList = [g[i] for i in range(1,6+1)]

    # create Days (ie bipartite graphs between housemates/restaurant and meals)
    dayList = []
    for (index,i) in enumerate(range(constantVertexes,graphSize,vertexesPerDay)):
        # construct day (relative to i)
        #0: start
        #1 - 5: housemates
        #6: restaurant
        #7 - 8: meals
        #9: end
        dayList.append(Day(g,availability[index],g[i+0],g[i+1:i+5+1],g[i+6],g[i+7:i+8+1],g[i+9]))
        # add to the daylist
    return overflowEnd, overflowList, dayList

def connectToOverflowSums(g,days,dayList,overflowList):
    """
    Connects all the housemates to the overflow sums
    :Input:
        g:
            the graph containing the scheduling circulation graph
        days: 
            the number of days to allocate meals for
        overflowList:
            a list of overflows corresponding to the housemates and the restaurant
        dayList:
            a list of day objects
    :Time complexity:
        O(N) where N is the number of days
    :Aux space complexity:
        O(N) where N is the number of days
    """
    # connect overflows to each other
    for i in range(days):
        for j in range(len(dayList[i].housemates)):
            g.addEdge(dayList[i].housemates[j],overflowList[j],2,lowerBound=1)
        g.addEdge(dayList[i].restaurant,overflowList[-1],2)
def createOverflowConstraintEdges(g,days,overflowEnd,overflowList):
    """
    Creates edges in order to constrain the number of meals each housemate or restaurant can make
    :Input:
        g:
            the graph containing the scheduling circulation graph
        days: 
            the number of days to allocate meals for
        overflowEnd:
            the end point for the overflows of the graph
        overflowList:
            a list of overflows corresponding to the housemates and the restaurant
    :Time complexity:
        O(1)
    :Aux space complexity:
        O(1)
    """
    # calculate constants for boundaries
    minMeals = math.floor(0.36 * days)
    maxMeals = math.ceil(0.44 * days)
    maxMealsResto = math.floor(0.1 * days)

    # calculate lower bounds and higher bounds
    housemateLowerBound = 2 * days - maxMeals
    housemateUpperBound = 2 * days - minMeals
    restaurantLowerBound = 2 * days - maxMealsResto
    restaurantUpperBound = 2 * days

    # ensure that boundaries are met for the overflows
    for i in range(len(overflowList)-1):
        g.addEdge(overflowList[i],overflowEnd,housemateUpperBound,lowerBound=housemateLowerBound)
    g.addEdge(overflowList[-1],overflowEnd,restaurantUpperBound,lowerBound=restaurantLowerBound)

def allocate(availability):
    """
    Calculates how to allocate the meals that a group of 5 people should make based on their availability 
    :Input:
        availability:
            a list of sublists, where each sublist is:
                a list with 5 items with each item being an integer corresponding to housemates based on these values:
                    0 = the housemate can't prepare any meals for this day
                    1 = the housemate can only prepare meals for breakfast
                    2 = the housemate can only prepare meals for dinner
                    3 = the housemates can prepare meals for either breakfast or dinner
    :Output, return or postcondition:
        a tuple containing two lists:
            a list containing the roommates/restaurants that will cook breakfast for each day
            a list containing the roommates/restaurants that will cook dinner for each day
    :Time complexity:
        O(N^2) where N is the number of days
    :Aux space complexity:
        O(N) where N is the number of days
    """
    # get number of days
    days = len(availability)
    # handle edge case
    if(days==0):
        return ([],[]) 

    g, vertexesPerDay, constantVertexes, graphSize = createGraph(days)
    
    overflowEnd, overflowList, dayList = processGraphIntoVariables(g,availability,days,vertexesPerDay,constantVertexes,graphSize)
    
    connectToOverflowSums(g,days,dayList,overflowList)

    createOverflowConstraintEdges(g,days,overflowEnd,overflowList)

    # run network flow
    g.fordFulkerson()

    # if the max flow has not been achieved, return None
    for edge in g.source.edges:
        if(edge.flow<edge.capacity):
            return None 
    
    # return result
    return ([day.getBreakfast() for day in dayList],[day.getDinner() for day in dayList])

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------

def getTrieIndex(char):
    """
    converts a character into the corresponding index of a node's child list
    :Input:
        char:
            the character to be converted
    :Output, return or postcondition:
        an integer representing the index of the node's child list
    :Time complexity:
        O(1)
    :Aux space complexity:
        O(1)
    """
    # $ = 0, space = 1, a = 2, b = 3, c = 4, ..., z = 28
    return 0 if char=='$' else 1 if char==' ' else ord(char) - 97 + 2

class Node:
    def __init__(self,char=""):
        """
        Instantiate a Node class, which is a class that represents a character or a string
        within a tree or a trie
        :Input:
            char: the character or string associated with the node
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        self.childList = [None] * 28
        self.char = char 
        self.str1Visited = False # is this node covered by the first string?
        self.str2Visited = False # is this node covered by the second string?
        self.sparseChildList = []
    def getSubstring(self):
        """
        Backtracks in order to recursively obtain the substring ending at the node
        :Output, return or postcondition:
            the substring associated with the node
        :Time complexity:
            O(N + M) where N is the length of the first string and M is the length of the second string
        :Aux space complexity:
            O(N + M) where N is the length of the first string and M is the length of the second string
        """
        if(self.parent==None):
            return ""
        else:
            return self.parent.getSubstring() + self.char

class SimilarityTree:
    def __init__(self,str1,str2):
        """
        Instantiates a SimilarityTree class, which is a tree that represents the suffixes of the two
        strings inputted into the tree
        :Input:
            str1:
                the first string to be inserted
            str2: 
                the second string to be inserted
        :Output, return or postcondition:
        :Time complexity:
            O((M+N)^2) where N is the length of the first string and M is the length of the second string
        :Aux space complexity:
            O((M+N)^2) where N is the length of the first string and M is the length of the second string
        """
        self.str1 = str1 
        self.str2 = str2 
        self.root = Node()  
        self.insertSuffixes(str1,1)
        self.insertSuffixes(str2,2)
        self.convertIntoTree()
    def insertSuffixes(self,trieString,strChoice):
        """
        Inserts a string, along with all its suffixes into the trie
        :Input:
            trieString:
                the string to be inserted
            strChoice:
                an integer (either 1 or 2) designating which string the inputted string is
        :Time complexity:
            O((N + M)^2) where N is the length of the first string and M is the length of the second string
        :Aux space complexity:
            O((N + M)^2) where N is the length of the first string and M is the length of the second string
        """
        strVal = ""
        # loop through each substring, and insert into the suffix trie
        for i in range(len(trieString)-1,-1,-1):
            self.insert(strVal,strChoice)
            strVal = trieString[i] + strVal
        self.insert(strVal,strChoice)
    def setVisited(self,node,strChoice):
        """
        Sets a node as discovered based on which string accessed it
        :Input:
            node:
                the node to be set as discovered
            strChoice:
                an integer (either 1 or 2) designating which string the inputted string is
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        if(strChoice==1):
            node.str1Visited = True 
        else:
            node.str2Visited = True   
    def insert(self,strVal,strChoice):
        """
        Inserts a string into the trie by creating associated character nodes
        :Input:
            strVal:
                the string to be added to the tire
            strChoice:
                an integer (either 1 or 2) designating which string the inputted string is
        :Time complexity:
            O(M + N) where N is the length of the first string and M is the length of the second string
        :Aux space complexity:
            O(M + N) where N is the length of the first string and M is the length of the second string
        """
        currentNode = self.root 
        self.setVisited(currentNode,strChoice)
        for char in strVal: 
            index = getTrieIndex(char)
            if(currentNode.childList[index] == None):
                node = Node(char)
                currentNode.childList[index] = node
                currentNode.sparseChildList.append(node)
            currentNode = currentNode.childList[index]
            self.setVisited(currentNode,strChoice)
        index = 0
        if(currentNode.childList[index] == None):
            node = Node("$")
            currentNode.childList[index] = node
            currentNode.sparseChildList.append(node)
        currentNode = currentNode.childList[index]
        self.setVisited(currentNode,strChoice)

    def convertIntoTree(self):
        """
        Converts the stored trie into a tree, and replaces the trie with the tree
        :Time complexity:
            O((N + M)^2) where N is the length of the first string and M is the length of the second string
        :Aux space complexity:
            O((N + M)^2) where N is the length of the first string and M is the length of the second string
        """
        root = Node("|")  
        root.str1Visited = self.root.str1Visited
        root.str2Visited = self.root.str2Visited
        self.convertIntoTreeAux(self.root,root) 
        self.root = root
    def convertIntoTreeAux(self,trieNode,treeNode):
        """
        Auxilliary function that recursively converts the stored trie into a tree
        :Input:
            trieNode:
                the node of the trie that is being used to create the treeNode
            treeNode:
                the current tree node that is being modified
        :Time complexity:
            O((N + M)^2) where N is the length of the first string and M is the length of the second string
        :Aux space complexity:
            O((N + M)^2) where N is the length of the first string and M is the length of the second string
        """
        treeNode.char += trieNode.char if trieNode.char != "$" else ""
        if(len(trieNode.sparseChildList)==0):
            return  
        elif(len(trieNode.sparseChildList)==1):
            self.convertIntoTreeAux(trieNode.sparseChildList[0],treeNode) 
        else:
            for node in trieNode.sparseChildList:
                newTreeNode = Node()
                newTreeNode.str1Visited = node.str1Visited
                newTreeNode.str2Visited = node.str2Visited
                treeNode.childList[getTrieIndex(node.char)] = newTreeNode
                treeNode.sparseChildList.append(newTreeNode)
                self.convertIntoTreeAux(node,newTreeNode)
    def __str__(self):
        return self.strAux(self.root)
    def strAux(self,node):
        result = "\n%s (%s,%s)" % (node.char,node.str1Visited,node.str2Visited)
        i = 0
        for child in node.childList:
            if(child!=None):
                result += self.strAux(child).replace("\n","\n  ")
            i += 1
        return result 
    def getLongestSubstring(self):
        """
        Obtains the longest substring that both the first and second strings contain
        :Output, return or postcondition:
            The longest shared substring
        :Time complexity:
            O(N + M) where N is the length of the first string and M is the length of the second string
        :Aux space complexity:
            O(N + M) where N is the length of the first string and M is the length of the second string
        """
        self.root.char = ""
        return self.getLongestSubstringAux(self.root)
    def getLongestSubstringAux(self,node):
        """
        Auxilliary function that recursively obtains the longest substring that both 
        the first and second strings contain
        :input:
            node:
                the node that is currently being iterated through
        :Output, return or postcondition:
            The longest shared substring of the current node
        :Time complexity:
            O(N + M) where N is the length of the first string and M is the length of the second string
        :Aux space complexity:
            O(N + M) where N is the length of the first string and M is the length of the second string
        """
        strVal = ""
        for child in node.sparseChildList:
            if(child.str1Visited and child.str2Visited):
                childStrVal = self.getLongestSubstringAux(child)
                if(len(childStrVal)>len(strVal)):
                    strVal = childStrVal
        return node.char + strVal 

def customRound(x):
    """
    Rounds a number, with an exact value of 0.5 rounding up
    :Input:
        x:
            a numerical value
    :Output, return or postcondition:
        a rounded number
    :Time complexity:
        O(1)
    :Aux space complexity:
        O(1)
    """
    return math.floor(x) if x % 1 < 0.5 else math.ceil(x)

def compare_subs(str1,str2):
    """
    Compares two strings and calculates the longest substring and the percentage of each string that it comprises
    :Input:
        str1:   
            the first string to check
        str2:
            the second string to check
    :Output, return or postcondition:
        a list with three items:
            the longest shared substring between the two strings
            the % of the substring within the first string rounded to the nearest integer
            the % of the substring within the second string rounded to the nearest integer
    :Time complexity:
        O((N + M)^2) where N is the length of the first string and M is the length of the second string
    :Aux space complexity:
        O((N + M)^2) where N is the length of the first string and M is the length of the second string
    """
    if(len(str1)==0 or len(str2)==0):
        return ['',0,0]
    # create trie
    t = SimilarityTree(str1,str2) 
    # get longest substring
    subString = t.getLongestSubstring()
    # return substring along with corresponding stats
    return [subString,customRound(len(subString)/len(str1)*100),customRound(len(subString)/len(str2)*100)]

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------


if __name__ == "__main__":
    availability = [[2, 0, 2, 1, 2], [3, 3, 1, 0, 0],
                    [0, 1, 0, 3, 0], [0, 0, 2, 0, 3],
                    [1, 0, 0, 2, 1], [0, 0, 3, 0, 2],
                    [0, 2, 0, 1, 0], [1, 3, 3, 2, 0],
                    [0, 0, 1, 2, 1], [2, 0, 0, 3, 0]]
    results = allocate(availability)
    print(results)

    print(compare_subs("the quick brown fox jumped over the lazy dog","my lazy dog has eaten my homework"))
    print(compare_subs(
        "radix sort and counting sort are both non comparison sorting algorithms",
        "counting sort and radix sort are both non comparison sorting algorithms"))