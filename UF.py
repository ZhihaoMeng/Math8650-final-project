# union and find

class UF:

    def __init__(self, N):
        self._count = N
        self._parent=list(range(N))
        self._rank=[0]*N

# instance method : find the set of a node
    # with path compression
    # def find(self, _parent, i):
    #     if _parent[i] == i:
    #         return _parent[i]
    #     _parent[i] = self.find(_parent, _parent[i])

    def find(self, i):
        if self._parent[i] == i:
            return self._parent[i]
        self._parent[i] = self.find(self._parent[i])
        return self._parent[i]
    # instance method : union two node if they belong to 2 components 
    # union by _rank to make the tree more balanced

    # def union(self, _parent, _rank, src, dest):
    #     srcRoot = self.find(_parent, src)
    #     destRoot = self.find(_parent, dest)

    #     # return if they are same component and print warning
    #     if srcRoot == destRoot:
    #         print('they blong to same component!')
    #         return 
        
    #     # union them by _rank: low _rank one is attached to high _rank one
    #     if _rank[srcRoot] < _rank[destRoot]:
    #         _parent[srcRoot]=destRoot
    #     elif _rank[srcRoot] > _rank[destRoot]:
    #         _parent[destRoot]=srcRoot
    #     else:
    #         _parent[destRoot]=srcRoot
    #         _rank[srcRoot] += 1

    def union(self,src, dest):
        srcRoot = self.find(src)
        destRoot = self.find(dest)

        # return if they are same component and print warning
        if srcRoot == destRoot:
            # print(str(src)+':'+ str(dest)+ '   ' +'they blong to same component!')
            return 
        
        # union them by _rank: low _rank one is attached to high _rank one
        if self._rank[srcRoot] < self._rank[destRoot]:
            self._parent[srcRoot]=destRoot
        elif self._rank[srcRoot] > self._rank[destRoot]:
            self._parent[destRoot]=srcRoot
        else:
            self._parent[destRoot]=srcRoot
            self._rank[srcRoot] += 1

        self._count -= 1

    def connected(self, src, dest):
        return self.find(src) == self.find(dest)
    
    def numTrees(self):
        return self._count
