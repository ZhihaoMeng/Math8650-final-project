# PriorityQueue implemented via binary heap
# most from HW05 but important modification is self._pos which make the decease_priority operation fast

class PriorityQueue():
    '''
    The arguments passed to a PriorityQueue must consist of
    objects than can be compared using <.
    Use a tuple (priority, item) if necessary.
    '''

    def __init__(self):
        self._array = []
        self._pos ={}

    def push(self, obj):
        # append at end and bubble up
        self._array.append( obj )
        n = len(self._array)
        self._pos[obj[1]] = n - 1
        self._bubble_up(n-1)
        
    def pop(self):
        n = len(self._array)
        if n==0:
            return None
        if n==1:
            self._pos = {}
            return self._array.pop()
        
        # replace with last item and sift down:
        obj = self._array[0]
        # self.pos[obj[0]] will not be used anymore
        self._pos.pop(obj[1])

        self._array[0] = self._array.pop()
        self._pos[self._array[0][1]] = 0
        self._sift_down(0)
        return obj
    
    def _parent(self, n):
        return (n-1)//2

    def _left_child(self, n):
        return 2*n + 1

    def _right_child(self, n):
        return 2*n + 2

    def _bubble_up(self, index):
        while index>0:
            cur_item = self._array[index]
            parent_idx = self._parent(index)
            parent_item = self._array[parent_idx]
            
            if cur_item < parent_item:
                # swap with parent,  update pos
                self._array[parent_idx] = cur_item
                self._pos[cur_item[1]] = parent_idx
                self._array[index] = parent_item
                self._pos[parent_item[1]] = index
                index = parent_idx
            else:
                break
    
    def _sift_down(self,index):
        n = len(self._array)
        
        while index<n:           
            cur_item = self._array[index]
            lc = self._left_child(index)
            if n <= lc:
                break

            # first set small child to left child:
            small_child_item = self._array[lc]
            small_child_idx = lc
            
            # right exists and is smaller?
            rc = self._right_child(index)
            if rc < n:
                r_item = self._array[rc]
                if r_item < small_child_item:
                    # right child is smaller than left child:
                    small_child_item = r_item
                    small_child_idx = rc
            
            # done: we are smaller than both children:
            if cur_item <= small_child_item:
                break
            
            # swap with smallest child:
            self._array[index] = small_child_item
            self._pos[small_child_item[1]] = index
            self._array[small_child_idx] = cur_item
            self._pos[cur_item[1]] = small_child_idx
            
            # continue with smallest child:
            index = small_child_idx
        
    def size(self):
        return len(self._array)
    
    def is_empty(self):
        return len(self._array) == 0
    
    # def show(self):
    #     G = nx.Graph()
    #     nodes=[]
    #     for i in range(0,len(self._array)):
    #         if nodes.count(self._array[i])>0:
    #     # since networkx does not allow duplicated nodes, I added an suffix '_i' to nodes's name 
    #     # which i is the corresponding index 
    #             nodes.append(str(self._array[i])+'_'+str(i))
    #         else:
    #             nodes.append(self._array[i])
    #     for i in range(1,len(self._array)):
    #         G.add_edge(nodes[(i-1)//2],nodes[i])
    #     plt.figure(figsize=(12,12)) 
    #     plt.axis('off')
    #     nx.draw_networkx(G,pos = nx.nx_agraph.graphviz_layout(G, prog='dot'))
      
    
    def heapify(self, items):
        """ Take an array of unsorted items and replace the contents
        of this priority queue by them. """
       
        self._array=items
        n=len(self._array)
        start=(n-1)//2
        while start>=0:
            self._sift_down(start)
            start=start-1
            
    def decrease_priority(self, dest, weight):
        
        index = self._pos[dest]
        assert (weight < self._array[index][0])
        self._array[index] = (weight, self._array[index][1])
        self._bubble_up(index)
    
    def contain(self,v):
        return v in self._pos

    def priority(self, v):
        return self._array[self._pos[v]][0]
