import networkx as nx 

class Graph():
    '''
    my own Graph class for MST
    '''

    def __init__(self):
        # we just consider undirected _graph
        self._graph = nx.Graph()
        #super(Graph).__init__()

    @property
    def adj(self):
        return self._graph.adj

    def addEdge(self,src, dest, weight=1):
        self._graph.add_edge(src, dest, weight=weight)
        #super().add_edge(src,dest,weight=weight)
    def removeEdge(self, src, dest):
        self._graph.remove_edge(src, dest)
        #super().remove_edge(src,dest)

    def readEdgeList(self, path, comments='#', delimiter=None, nodetype=None):
        self._graph = nx.read_weighted_edgelist(path, comments=comments, \
        delimiter=delimiter, create_using=None, nodetype=nodetype, encoding='utf-8')
    
    def clear(self):
        self._graph.clear()
        #super().clear()

    def edges(self):
        return self._graph.edges(data=True)
    
    def number_of_nodes(self):
        return self._graph.number_of_nodes()
    
    def number_of_edges(self):
        return self._graph.number_of_edges()

    def neighbors(self, n):
        return self._graph.neighbors(n)
    

    # draw the _graph
    def show(self):
        import matplotlib.pyplot as plt 
        plt.figure(figsize=(8, 8))
        plt.axis('off')
        pos=nx.spring_layout(self._graph)
        #pos=nx.spring_layout(self)
        edge_labels=dict([((u,v,),d['weight'])
             for u,v,d in self._graph.edges(data=True)])
             #for u,v,d in self.edges(data=True)])
        nx.draw_networkx(self._graph,pos)
        nx.draw_networkx_edge_labels(self._graph,pos,edge_labels=edge_labels)
        #nx.draw_networkx(self,pos)
        #nx.draw_networkx_edge_labels(self,pos,edge_labels=edge_labels)
        plt.show()

    