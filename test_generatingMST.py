from Graph import Graph
from MST import MST
import matplotlib.pyplot as plt
import numpy as np 
from scipy.optimize import curve_fit
from timeit import default_timer as timer 
import random
# graph = Graph() 
# graph.addEdge(0, 1, 4) 
# graph.addEdge(0, 7, 12) 
# graph.addEdge(1, 2, 8) 
# graph.addEdge(1, 7, 11) 
# graph.addEdge(2, 3, 7) 
# graph.addEdge(2, 8, 2) 
# graph.addEdge(2, 5, 4) 
# graph.addEdge(3, 4, 9) 
# graph.addEdge(3, 5, 14) 
# graph.addEdge(4, 5, 10) 
# graph.addEdge(5, 6, 2) 
# graph.addEdge(6, 7, 1) 
# graph.addEdge(6, 8, 6) 
# graph.addEdge(7, 8, 7) 
# graph.show()
# mst=MST(graph)
# res = mst.Boruvka()
# res.show()
# res = mst.Prim()
# res.show()

def random_mst(n):

    # build the mst 
    graph = Graph()
    unvisited = set(range(0,n))
    visited = set()
    

    s = unvisited.pop()
    visited.add(s)
    
    # create a set contain all edges that not belong to mst
    edgeSet=set()
    for i in range(0,n):
        for j in range(0,i):
            edgeSet.add((j,i))
    i = 0
    while i < n - 1:
        s = random.choice(tuple(unvisited))
        # s = unvisited.pop()
      
        
       
        w = random.randint(1,10)
        # t = visited.pop()
        # visited.add(t)

        t = random.choice(tuple(visited))
        

        graph.addEdge(s,t,w)
        unvisited.discard(s)
        # unvisited.discard(t)

        i = i + 1
        visited.add(s)
        # else:
        #     continue
        if s > t:
            edgeSet.remove((t,s))
        else:
            edgeSet.remove((s,t))


    return graph,edgeSet

# increase the density

def random_graph(mst,m, edgeSet):
    '''
        each mst has n-1 edges and n vertices, to increase the density of the network, we can add edges to the mst.
        The maximum number of edges is m = (n-1)n/2. To investigate the time complexity - density relationship we can 
        use several density of graph, like [1n,2n, 4n, 8n, 16n, 32n]
    '''
    cur = mst.number_of_edges()
    n = mst.number_of_nodes()
    while cur < m*(n*(n-1))/2.0:
        #s= random.randint(0,n-1)
        #s_degree = sum(1 for _ in mst.neighbors(s))
        # check if the degree of s is already n-1 
        #while s_degree == n-1:
            #s = random.randint(0,n-1)
            #s_degree = sum(1 for _ in mst.neighbors(s))
        # check if t is already connected with s
        #t= random.randint(0,n-1)
        #while t in mst.neighbors(s):
            #t = random.randint(0,n-1)
        # connect s & t with weight w
 
        edge = edgeSet.pop()

        # edge = random.choice(tuple(edgeSet))
        # edgeSet.remove(edge)
        # edge = random.sample(edgeSet,1)[0]
        # edgeSet.remove(edge)

        w = random.randint(11, 30)
        mst.addEdge(edge[0], edge[1], w)
        cur += 1
    return mst, edgeSet

# def func(x,k,c):
#    return k * ((x-1)*x/2.0) * np.log2(x) + c

def func(x,k):
    return k * ((x-1)*x/2.0) * np.log2(x)



if __name__ == '__main__':
    # plt.switch_backend('agg')
   
    sizes = [10]
   
    density = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

    times_Boruvka = []
    times_Prim =[]
    for n in sizes:
        mst,edgeSet= random_mst(n)
        mst.show()
        for m in density:
            
            
            graph, edgeSet = random_graph(mst, m, edgeSet)
            graph.show()
            res = MST(graph)
           
            start = timer()
            fig=res.Boruvka()
    
            end = timer()
            cost = end - start 
            fig.show()
            times_Boruvka.append(cost)
            print("Boruvka: ", "size: ", n, " ", 'density: ', m, 'time:',' ', cost, "s")

            start = timer()
            fig=res.Prim()
        
            end = timer()
            cost = end - start

            fig.show()
            times_Prim.append(cost)
            print("Prim: ", "size: ", n, " ", 'density: ', m, 'time:',' ', cost, "s")
    
   
