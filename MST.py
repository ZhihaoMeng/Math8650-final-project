# implementation of Prim's and Boruvka's algorithm

import networkx as nx 
from Graph import Graph

class MST:

    def __init__(self, graph):
        self._graph = graph

        self._nNodes = graph.number_of_nodes()
        self._edges = list(graph.edges())
        self._nEdges = graph.number_of_edges()
        self._mst = Graph()


    # construct MST using boruvka's algorithm
    def Boruvka(self):
        # to build the MST, results represented by _mst
        self._mst.clear()
        # load UF  class for union and find
        from UF import UF
        
        uf = UF(self._nNodes)

        # let's start the algorithm
        
        # store the cheapest edge of subset
        cheapest = [-1]*self._nNodes

        # union components until there are only one component

        while uf.numTrees() > 1:
            
            # update cheapest edges

            for i in range(self._nEdges):

                # find components of two ends of an edge
                src, dest, w = self._edges[i][0:3]
                w = w['weight']
                srcTree = uf.find(src)
                destTree = uf.find(dest)

                # if they are not unioned by now, update the cheapest edge

                if srcTree != destTree:
                    if cheapest[srcTree] == -1 or cheapest[srcTree][2] > w :
                        cheapest[srcTree] = [src, dest, w]
                    
                    if cheapest[destTree] == -1 or cheapest[destTree][2] > w :
                        cheapest[destTree] = [src, dest, w]

            # add the cheapest edges to current MST
            for node in range(self._nNodes):

                # find two disjointed trees and union them
                if cheapest[node] != -1:
                    # after above step, only cheapest[treeRoot] is not equal to -1, and they contain the cheapest edge for tree root
                    src, dest, w = cheapest[node]
                    uf.union(src, dest)
                    self._mst.addEdge(src, dest, w)
                    # srcTree = uf.find(src)
                    # destTree = uf.find(dest)

                    # if srcTree != destTree:
                    #     uf.union(srcTree, destTree)
                    #     # build the _mst
                    #     _mst.addEdge(src, dest, w)


            # reset the cheapest edges for next level union
            cheapest = [-1] * self._nNodes

        return self._mst

    def Prim(self):
        from PriorityQueue import PriorityQueue
        import sys

        pq = PriorityQueue()

        # put all nodes in the pq
        for i in range(self._nNodes):
            pq.push((sys.maxsize,i))

        # used to store the results    
        start = [-1] * self._nNodes
        
        weight = [sys.maxsize] * self._nNodes 
        # to save memory  self._graph.adj[start[dest]][dest]['weight']

        # the first node should be added to _mst anyhow
        pq.decrease_priority(0, 0)
        weight[0] = 0
        
        # grow the _mst until there is no vertice in pq
        while pq.size() > 0:


            # get the cheapest node
            src = pq.pop()[1]

            for dest in list(nx.neighbors(self._graph, src)):
                if pq.contain(dest) and pq.priority(dest) > self._graph.adj[src][dest]['weight']:
                    weight[dest] = self._graph.adj[src][dest]['weight']
                    start[dest] = src
                    pq.decrease_priority(dest, weight[dest])

        self._mst.clear()
        # print(list(self._mst.edges()))
        for dest in range(self._nNodes):
            if start[dest] != -1:
                self._mst.addEdge(start[dest], dest, weight[dest])
        return self._mst




