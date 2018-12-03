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
    #import sys
    #weight = [sys.maxsize]*n
    s = unvisited.pop()
    visited.add(s)
    
    # create a set contain all edges that not belong to mst
    edgeSet=set()
    for i in range(0,n):
        for j in range(0,i):
            edgeSet.add((j,i))
    i = 0
    while i < n - 1:
        # s = random.choice(tuple(unvisited))
        s = unvisited.pop()
      
        
        # if s in unvisited or t in unvisited and s != t:
        w = random.randint(0,10)
        t = visited.pop()
        visited.add(t)
        # t = random.choice(tuple(visited))
        #t = random.sample(visited,1)[0]
        #weight[s]=min(w,weight[s])
        #weight[t]=min(w.weight[t])

        graph.addEdge(s,t,w)
        # unvisited.discard(s)
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

def func2(x,k,c):
    return k * ((x-1)*x/2.0) * np.log2(x) + c

def func1(x,k):
    return k * ((x-1)*x/2.0) * np.log2(x)

def func3(x,k,b,c):
    return k * ((x-1)*x/2.0) * np.log2(x) + b*x + c


if __name__ == '__main__':
    plt.switch_backend('agg')
    # some test function 
    # sizes = [10000, 20000, 40000, 80000, 160000, 320000]
    # sizes = [100, 200, 400, 800,1600,3200,6400,12800]
    # sizes = [100, 200,400,600,800,1000]
    sizes =   [200*i for i in range(5,31)]
    # density = [1, 2, 4, 8, 16, 32]
    density = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    # density = [0.1]
    times_Boruvka = []
    times_Prim =[]
    for n in sizes:
        mst,edgeSet= random_mst(n)
        for m in density:
            
            
            graph, edgeSet = random_graph(mst, m, edgeSet)
            res = MST(graph)

            start = timer()
            res.Boruvka()
            end = timer()
            cost = end - start
            times_Boruvka.append(cost)
            print("Boruvka: ", "size: ", n, " ", 'density: ', m, 'time:',' ', cost, "s")

            start = timer()
            res.Prim()
            end = timer()
            cost = end - start
            times_Prim.append(cost)
            print("Prim: ", "size: ", n, " ", 'density: ', m, 'time:',' ', cost, "s")
    
    times_Boruvka = np.array(times_Boruvka).reshape((len(sizes), len(density)))
    
    times_Prim = np.array(times_Prim).reshape((len(sizes), len(density)))

    for i in range(0, len(density)):
        vertices = sizes
        plt.figure(figsize=(17,10))
        
        plt.plot(vertices, times_Prim[:,i], 'o', label = 'Prim')
        
        xdata=np.linspace(vertices[0],vertices[-1],50)

        popt1, pcov1 = curve_fit(func1, np.array(vertices), times_Prim[:,i])
        dev1 = sum(np.square(func1(np.array(vertices),*popt1) - times_Prim[:,i]))
        popt_1=np.append(popt1,dev1)
        plt.plot(xdata, func1(xdata, *popt1), 'r-', label = 'Prim: fit: k=%10.8f, dev=%f' % tuple(popt_1))

        popt3, pcov3 = curve_fit(func3, np.array(vertices), times_Prim[:,i])
        dev3 = sum(np.square(func3(np.array(vertices),*popt3) - times_Prim[:,i]))
        popt_3=np.append(popt3,dev3)
        plt.plot(xdata, func3(xdata, *popt3), 'g-', label = 'Prim: fit: k=%15.13f, b=%15.13f, c=%5.3f, dev=%f' % tuple(popt_3))

        popt2, pcov2 = curve_fit(func2, np.array(vertices), times_Prim[:,i])
        dev2 = sum(np.square(func2(np.array(vertices),*popt2) - times_Prim[:,i]))
        popt_2=np.append(popt2,dev2)
        plt.plot(xdata, func2(xdata, *popt2), 'b-', label = 'Prim: fit: k=%15.13f,c=%5.3f,dev=%f' % tuple(popt_2))
        # plt.xlabel('nodes')
        #plt.ylabel('time')
        #plt.legend()
        #plt.title('Prim: density='+str(density[i]))
        #plt.savefig('Prim: density='+str(density[i])+'.png')
        #plt.close()    
        # for Boruvka
        #plt.figure()
        plt.plot(vertices, times_Boruvka[:,i], 'ro',label = 'Boruvka')
        
        popt1, pcov1 = curve_fit(func1, np.array(vertices), times_Boruvka[:,i])
        dev1 = sum(np.square(func1(np.array(vertices),*popt1) - times_Boruvka[:,i]))
        popt_1=np.append(popt1,dev1)
        plt.plot(xdata, func1(xdata, *popt1), 'r-', label = 'Boruvka: fit: k=%10.8f,dev=%f' % tuple(popt_1))
        
        popt3, pcov3 = curve_fit(func3, np.array(vertices), times_Boruvka[:,i])
        dev3 = sum(np.square(func3(np.array(vertices),*popt3) - times_Boruvka[:,i]))
        popt_3=np.append(popt3,dev3)
        plt.plot(xdata, func3(xdata, *popt3), 'g-', label = 'Boruvka: fit: k=%15.13f, b=%15.13f, c=%5.3f,dev=%f' % tuple(popt_3))

        popt2, pcov2 = curve_fit(func2, np.array(vertices), times_Boruvka[:,i])
        dev2 = sum(np.square(func2(np.array(vertices),*popt2) - times_Boruvka[:,i]))
        popt_2=np.append(popt2,dev2)
        plt.plot(xdata, func2(xdata, *popt2), 'b-', label = 'Boruvka: fit: k=%15.13f, c=%5.3f,dev=%f' % tuple(popt_2))
        
        plt.xlabel('nodes')
        plt.ylabel('time')
        plt.legend()
        # plt.title('Boruvka: density='+str(density[i]))
        # plt.savefig('Boruvka: density='+str(density[i])+'.png')
        plt.title('density='+str(density[i]))
        # plt.savefig('density='+str(density[i])+'.png')
        # plt.savefig('results/fit:[k,b,c]/1000-6000nodes/density='+str(density[i])+'.png')
        # plt.savefig('results/fit:[k,b,c]/max12800nodes/density='+str(density[i])+'.png')

        # plt.savefig('results/fit:[k,c]/1000-6000nodes/density='+str(density[i])+'.png')
        # plt.savefig('results/fit:[k,c]/max12800nodes/density='+str(density[i])+'.png')

        plt.savefig('results/fit_compare/1000-6000nodes/density='+str(density[i])+'.png')
        # plt.savefig('results/fit_compare/max12800nodes/density='+str(density[i])+'.png')
        plt.close()    
    # for i in range(0, len(sizes)): 
    #    vertices = [dense * sizes[i] for dense in density]
    #    plt.figure()
    #    plt.plot(vertices, times_Prim[i], 'o')
       
    #    popt, pcov = curve_fit(func, np.array(vertices), times_Prim[i])
    #    plt.plot(vertices, func(np.array(vertices), *popt), 'r-', label = 'fit: k=%5.3f, c=%5.3f' % tuple(popt))
    #    plt.xlabel('nodes')
    #    plt.ylabel('time')
    #    plt.legend()
    #    plt.title('sizes:'+str(sizes[i])+'with different density')
        # plt.show()
    #    plt.savefig('sizes:'+str(sizes[i])+'.png')
    #    plt.close()
