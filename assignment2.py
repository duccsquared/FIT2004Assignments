"""
Assignment 2 FIT2004
By: Mario Susanto
"""

class MinHeap:
    def __init__(self,maxLen,getVal = lambda x:x, getHeapIndex = lambda x:0, setHeapIndex = lambda x,y:0):
        """
        Instantiates the MinHeap class, which allows for storing items and accessing the smallest item in O(1) time
        :Input:
            maxLen:
                The maximum number of items that the MinHeap can store
            getVal:
                A function to obtain the value of the item with which to sort. Accepts the item as an input
            getHeapIndex:
                A function to obtain the index of the heap dataList at which the item is stored. Accepts the item as an input
            setHeapIndex:
                A function to set the index of the heap dataList at which the item is stored into the item. Accepts the item and index as inputs            
        :Time complexity:
            O(N) where N = maxLen
        :Aux space complexity:
            O(N) where N = maxLen
        """
        self.data = [None] * maxLen 
        self.dataLen = 0
        # function to extract the value to sort by from the item
        self.getVal = getVal 
        # function to extract the index of the item from 
        self.getHeapIndex = getHeapIndex 
        # function to set the index that the item is at into the item
        self.setHeapIndex = setHeapIndex 


    def __len__(self):
        """
        gets the number of items in the heap
        :Output, return or postcondition:
            the number of items in the heap
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        return self.dataLen
    def swap(self,i,j):
        """
        swaps the positions of the items at index i and j in the heap
        :Input:
            i:  
                index of the first item to swap
            j:
                index of the second item to swap            
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        # switch locations of items
        temp = self.data[i]
        self.data[i] = self.data[j]
        self.data[j] = temp
        # set heap index into switched items
        self.setHeapIndex(self.data[i],i)
        self.setHeapIndex(self.data[j],j)
    def parent(self,index):
        """
        a function that obtains the index of the parent of an item within the heap based on the index
        :Input:
            index:
                the index of the item
        :Output, return or postcondition:
            the index of the parent of the item, or None if the parent doesn't exist
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        parentIndex = index//2
        if(parentIndex!=index):
            return parentIndex 
        else:
            return None
    def smallestChild(self,index):
        """
        a function that obtains the index of the smallest child of an item within the heap based on the index
        :Input:
            index:
                the index of the item
        :Output, return or postcondition:
            the index of the smallest child of the item, or None if no child exists
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        # get the left child
        childIndex = 2*index+1 
        # if the right child is smaller than the left child, go right instead
        if childIndex < len(self)-1 and self.getVal(self.data[childIndex+1]) < self.getVal(self.data[childIndex]):
            childIndex += 1
        if(childIndex<len(self)):
            return childIndex 
        else:
            return None 
    def rise(self,index):
        """
        Moves the item at the index upwards through the heap until the item's parent is smaller than the item
        :Input:
            index:
                the index of the item that should rise through the heap
        :Time complexity:
            O(log N) where N is the number of items in the heap
        :Aux space complexity:
            O(1)
        """
        # if the index is negative, account for it accordingly
        if(index<0):
            index += len(self)
        # get parent of rising item
        parent = self.parent(index)
        # while the top of the heap hasn't been reached and while the rising item isn't at the correct position
        while parent != None:
            # if the parent item is larger than the rising item, swap
            if(self.getVal(self.data[parent]) > self.getVal(self.data[index])): 
                self.swap(parent,index)
                index = parent
                parent = self.parent(index)
            else: # otherwise the item is in the correct position, exit loop
                break     

    def fall(self,index):
        """
        Moves the item at the index downard through the heap until the item's children are larger than the item
        :Input:
            index:
                the index of the item that should rise through the heap
        :Output, return or postcondition:
        :Time complexity:
            O(log N) where N is the number of items in the heap
        :Aux space complexity:
            O(1)
        """
        # if the index is negative, account for it accordingly
        if(index<0):
            index += len(self)
        # get smallest child of falling item
        child = self.smallestChild(index)
        # while a leaf node hasn't been reached and while the falling item isn't at the correct position
        while child != None:
            # if the falling item is smaller than the child item, swap
            if(self.getVal(self.data[index]) > self.getVal(self.data[child])): 
                self.swap(index,child)
                index = child
                child = self.smallestChild(index)
            else: # otherwise the item is in the correct position, exit loop
                break
    def serve(self):
        """
        gets the smallest item in the heap, replaces its position with another node, and returns the smallest item
        :Output, return or postcondition:
            the smallest item in the heap
        :Time complexity:
            O(log N) where N is the number of items in the heap
        :Aux space complexity:
            O(1)
        """
        if(len(self)==0): # if heap is empty return None
            return None 
        else:
            # get smallest item
            item = self.data[0]
            # decrement data length
            self.dataLen -= 1
            if(len(self)==0): # if after removing the smallest item there is nothing left
                self.data[0] = None 
            else:
                # move last item to the front
                self.data[0] = self.data[len(self)]
                self.setHeapIndex(self.data[0],0)
                self.data[len(self)] = None 
                # make the moved item fall so that it gets to the correct position
                self.fall(0)
                # return
            return item  
    def append(self,item):
        """
        adds an item into the heap
        :Input:
            item: the item to add into the heap
        :Time complexity:
            O(log(N)) where N is the number of items in the heap
        :Aux space complexity:
            O(1)
        """
        # set item at furthest position and increment
        self.data[len(self)] = item
        self.setHeapIndex(item,len(self))
        self.dataLen += 1
        # move item up until it is at the correct position
        self.rise(len(self)-1)
    def update(self,item):
        """
        if the value of the item has been changed, this function can update the position of the item
        :Input:
            item:
                the item in the heap to be updated
        :Time complexity:
            O(log(N)) where N is the number of items in the heap
        :Aux space complexity:
            O(1)
        """
        # move item up until it is at the correct position based on its index
        self.rise(self.getHeapIndex(item))
    def notEmpty(self):
        """
        returns a boolean determining if the heap isn't empty
        :Output, return or postcondition: 
            a boolean signifying whether the boolean isn't empty
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        return len(self) > 0

class DjikData():
    def __init__(self):
        """
        Instantiates the DjikData class, which stores information relevant to djikstra for a vertex
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        self.dist = float('inf') # distance from the start vertex of djikstra
        self.prev = None # previous vertex
        self.discovered = False # has this vertex been discovered by a neighbouring vertex?
        self.heapIndex = None # position of the vertex within the heap

class TopoData():
    def __init__(self):
        """
        Instantiates the TopoData class, which stores information relevant to djikstra for a vertex
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        self.visited = False # has this vertex been visited?
        self.score = -float('inf') # score when going from the start to here
        self.prev = None 

class Vertex:
    def __init__(self,vertexId):
        """
        Instantiates the Vertex class, which represents nodes in a graph
        :Input:
            vertexId:  
                an integer representing the index at which the vertex is stored within the Graph
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        self.id = vertexId 
        self.edges = [] # outgoing edges
        self.oppEdges = [] # incoming edges
        self.dataList = [] # record of data related to djikstra or topographical sort


class Edge:
    def __init__(self,u,v,w):
        """
        Instantiates the Edge class, which represents connections in a graph
        :Input:
            u: the starting vertex
            v: the ending vertex
            w: the weight of the edge
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        self.u = u # start vertex
        self.v = v # end vertex
        self.w = w # weight

class Graph:
    def __init__(self,vertexPairsWithWeight):
        """
        Instantiates the Graph class
        :Input:
            vertexPairsWithWeight:
                a list of tuples with three items each:
                    an integer representing the start vertex
                    an integer representing the end vertex
                    the weight        
        :Time complexity:
            O(V + E) where V is the number of vertexes and E is the number of edges
        :Aux space complexity:
            O(V + E) where V is the number of vertexes and E is the number of edges
        """
        # get the largest vertex ID to figure out how many vertexes there are
        maxID = 0
        for (u,v,w) in vertexPairsWithWeight:
            maxID = max(u,v,maxID)
        # instantiate vertexes
        self.vertexes = [Vertex(i) for i in range(maxID+1)] 
        # add edges
        self.addEdgesByIndex(vertexPairsWithWeight)
    def addEdgeByIndex(self,uIndex,vIndex,w=1):
        """
        adds an edge between two vertexes
        :Input:
            u: an integer representing the starting vertex
            v: an integer representing the ending vertex
            w: the weight of the edge
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        # get vertexes
        u = self.vertexes[uIndex]; v = self.vertexes[vIndex]
        # add edge
        edge = Edge(u,v,w) 
        u.edges.append(edge)
        # add the inverse edge
        v.oppEdges.append(Edge(v,u,w))

    def addEdgesByIndex(self,indexPairWithWeightList):
        """
        adds multiple edges between vertexes
        :Input:
            vertexPairsWithWeight:
                a list of tuples with three items each:
                    an integer representing the start vertex
                    an integer representing the end vertex
                    the weight        
        :Time complexity:
            O(E) where E is the number of edges
        :Aux space complexity:
            O(E) where E is the number of edges
        """
        for (uIndex,vIndex,w) in indexPairWithWeightList:
            self.addEdgeByIndex(uIndex,vIndex,w)

    def __len__(self):
        """
        returns the number of vertexes in the graph
        :Output, return or postcondition:
            the number of vertexes in the graph
        :Time complexity:
            O(1)
        :Aux space complexity:
            O(1)
        """
        return len(self.vertexes)

class RoadGraph(Graph):
    def __init__(self,roads,cafes):
        """
        Instantiates the RoadGraph class, which is a subclass of Graph that also stores a list of cafes, along with a routing function
        :Input:
            roads:
                a list of tuples with three items each:
                    an integer representing the start vertex
                    an integer representing the end vertex
                    the time taken to go from the start and end vertexes    
            cafes:
                a list of tuples with two items each:
                    an integer representing a vertex with a cafe
                    the time taken to order a coffee at the cafe

        :Time complexity:
            O(V + E) where V is the number of vertexes and E is the number of edges
        :Aux space complexity:
            O(V + E) where V is the number of vertexes and E is the number of edges
        """
        super().__init__(roads)
        # get all vertexes that have cafes, and assign their associated waiting time
        self.cafeList = cafes
    def backtrack(self,startVertex,getPrev):
        """
        a function that backtracks from a particular vertex until the source point
        :Input:
            startVertex:
                the vertex to backtrack from
            getPrev:
                a function to obtain the previous vertex from the vertex
        :Output, return or postcondition:
            a list of integers representing the path from the start vertex to the source vertex
        :Time complexity:
            O(V) where V is the number of vertexes
        :Aux space complexity:
            O(V) where V is the number of vertexes
        """
        path = []
        u = startVertex
        while(getPrev(u)!=None): # loop until there is no previous vertex anymore
            u = getPrev(u) # get previous vertex
            path.append(u.id)
        return path

    def routing(self,start,end):
        """
        a function that calculates the quickest path to go from the start to end with a detour to purchase a coffee
        :Input:
            start:
                an integer representing the starting vertex
            end:
                an integer representing the ending vertex
        :Output, return or postcondition:
            a list of integers representing the path taken
        :Time complexity:
            O(E log(V) + V) where V is the number of vertexes and E is the number of edges
        :Aux space complexity:
            O(E log(V) + V) where V is the number of vertexes and E is the number of edges
        """
        # if there are no vertices or there are no cafes, return None
        if(len(self)==0 or len(self.cafeList)==0): return None
        # do djikstra from start and from end
        self.djikstra(start) # resulting data from each vertex can be accessed with u.dataList[-2]
        self.djikstra(end,useOpp=True) # resulting data from each vertex can be accessed with u.dataList[-1]

        # get the cafe that provides the quickest path
        minCafe = None; minDist = float('inf')
        for (cafeIndex,waitTime) in self.cafeList:
            # get cafe vertex
            cafe = self.vertexes[cafeIndex]
            # start to cafe + cafe wait time + cafe to end
            dist = cafe.dataList[-2].dist + waitTime + cafe.dataList[-1].dist
            # update variables if the discovered path is better
            if(dist<minDist):
                minCafe = cafe; minDist = dist 
        # if there is no valid cafe, return None
        if(minCafe==None): return None
        # get the path from the cafe to the start point
        startPath = self.backtrack(minCafe,lambda u: u.dataList[-2].prev)
        # get the path from the cafe to the end point
        endPath = self.backtrack(minCafe,lambda u: u.dataList[-1].prev)
        # reverse start path so that it goes from start to cafe
        startPath.reverse()
        # concatenate paths (including the cafe itself)
        path = startPath + [minCafe.id] + endPath
        # return in the form of a list of integers
        return path

    def relax(self,edge):
        """
        finds if an edge can be used to provide a shorter path to a particular vertex
        :Input:
            edge: the edge that is being checked
        :Output, return or postcondition:
            a boolean representing if the edge was relaxed
        :Time complexity:
            O(log(V)) where V is the number of vertexes
        :Aux space complexity:
            O(1)
        """
        # current distance of v > distance of u + weight of u to v?
        if(edge.v.dataList[-1].dist>edge.u.dataList[-1].dist+edge.w):
            # if so set the edge accordingly
            edge.v.dataList[-1].dist = edge.u.dataList[-1].dist + edge.w
            edge.v.dataList[-1].prev = edge.u 
            return True 
        return False
            
    def djikstra(self,startVertexIndex,useOpp=False):
        """
        finds the distance from one vertex to every other vertex in a weighted directed graph
        :Input:
            startVertexIndex:
                the starting vertex from which the distance to every other vertex should be calculated
            useOpp:
                whether to use incoming edges instead of outgoing edges 
        :Time complexity:
            O(E log(V) + V) where V is the number of vertexes and E is the number of edges
        :Aux space complexity:
            O(E + V) where V is the number of vertexes and E is the number of edges
        """
        # create empty DjikData instances for storing djikstra related information
        for u in self.vertexes:
            u.dataList.append(DjikData())
        # set starting vertex to zero
        self.vertexes[startVertexIndex].dataList[-1].dist = 0
        self.vertexes[startVertexIndex].dataList[-1].discovered = True
        # create a min heap and input starting vertex 
        def setHeapIndex(u,val): # function for setting the heap index, passed as an argument into MinHeap, O(1) time and aux space complexity
            u.dataList[-1].heapIndex = val
        minHeap = MinHeap(len(self),lambda u: u.dataList[-1].dist,lambda u: u.dataList[-1].heapIndex,setHeapIndex)
        minHeap.append(self.vertexes[startVertexIndex])
        # loop until empty
        while(minHeap.notEmpty()):
            # get vertex
            u = minHeap.serve()
            # loop through adjacent edges (either using normal edges or opposite edges)
            adjacent = u.oppEdges if useOpp else u.edges
            for edge in adjacent:
                v = edge.v
                # add to queue if not visited 
                if(not v.dataList[-1].discovered):
                    v.dataList[-1].discovered = True # set as discovered
                    minHeap.append(v)
                # relax edge
                updated = self.relax(edge)
                # if the vertex distance was modified, update
                if(updated):
                    minHeap.update(edge.v)



class SkiGraph(Graph):
    """
        SkiGraph is a subclass of Graph that has a topological sort and a routing function
        It does not have a constructor, so constructing the SkiGraph requires a time and space complexity
        that is equivalent to Graph's time and space complexity
    """
        
    def partialTopologicalSort(self,start,finish):
        """
        sorts part of a directed acyclic graph such that the path from start to finish will be included
        :Input:
            start:
                an integer representing the starting vertex
            finish:
                an integer representing the finishing vertex
        :Output, return or postcondition:
            the topological order of some of the vertexes with start and finish included
        :Time complexity:
            O(E + V)  where V is the number of vertexes and E is the number of edges
        :Aux space complexity:
            O(V)  where V is the number of vertexes
        """
        # add storage for topographical sort into vertexes
        for u in self.vertexes:
            u.dataList.append(TopoData())
        # process from starting position
        order = []
        self.processNeighbours(order,self.vertexes[start],finish)
        # reverse so that the starting vertex is first
        order.reverse()
        return order
    def processNeighbours(self,order,u,finish):
        """
        function that recursively processes the neighbours of a vertex, and adding it to a list afterwards
        :Input:
            order:
                an array storing the topological order
            u:
                the vertex to process
            finish:
                an integer. if the vertex corresponds to it, the recrusion should terminate early
        :Time complexity:
            O(E + V)  where V is the number of vertexes and E is the number of edges
        :Aux space complexity:
            O(V)  where V is the number of vertexes
        """
        # this vertex has been visited
        u.dataList[-1].visited = True 
        # if the finishing vertex is reached, there isn't a need to check subsequent vertexes
        if(u.id==finish):
            order.append(u)
            return 
        # loop through adjacent vertexes
        for edge in u.edges:
            # if this vertex hasn't been visited yet, process it
            v = edge.v 
            if(not v.dataList[-1].visited):
                self.processNeighbours(order,v,finish)
        # after all child vertexes have been visited, add to order
        order.append(u)

    def routing(self,start,finish):
        """
        Finds the path from the start to the finish that provides the highest score
        :Input:
            start:
                integer that corresponds to a vertex in the graph
            finish:
                integer that corresponds to a vertex in the graph
        :Output, return or postcondition:
            a list of scores and a list of previous vertexes
        :Time complexity:
            O(V + E)  where V is the number of vertexes and E is the number of edges
        :Aux space complexity:
            O(V + E)  where V is the number of vertexes and E is the number of edges
        """
        # get the order to loop through
        order = self.partialTopologicalSort(start,finish)
        # start at start where score = 0
        self.vertexes[start].dataList[-1].score = 0
        # for each vertex in order loop through their adjacencies
        for u in order:
            for edge in u.edges:
                # calculate the score at v if the current edge is used
                v = edge.v 
                newScore = edge.w + u.dataList[-1].score
                # is this better than the existing score? (or is this the first time this vertex is reached?)
                if(newScore>v.dataList[-1].score):
                    # update accordingly
                    v.dataList[-1].score = newScore
                    v.dataList[-1].prev = u
        
def optimalRoute(downhillScores,start,finish):
    """
    function that calculates the best route from start to finish
    :Input:
        downhillScores:
            a list of tuples with three items each:
                an integer representing the start vertex
                an integer representing the end vertex
                the score earned for going directly from the start vertex to the end vertex
    :Output, return or postcondition:
        A list of integers that represent the path taken from the start to the end
    :Time complexity:
        O(V + E)  where V is the number of vertexes and E is the number of edges
    :Aux space complexity:
        O(V + E)  where V is the number of vertexes and E is the number of edges
    """
    # instantiate graph
    g = SkiGraph(downhillScores)
    # calculate route
    g.routing(start,finish)
    # find path
    path = []
    previous = g.vertexes[finish] 
    while(not previous in [g.vertexes[start],None]): # loop until the start vertex has been found
        path.append(previous.id)
        previous = g.vertexes[previous.id].dataList[-1].prev # get previous vertex
    # no valid path to start? then return None
    if(previous==None): return None 

    # add the starting vertex itself
    path.append(previous.id) 
    # make it so that the path starts at start
    path.reverse() 
    return path