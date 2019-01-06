import pickle #for pickling
import marshal
import csv
import os
from functools import lru_cache
from .constants import MAX
LIM = 25



class Node(object):
    def __init__(self,val=''):
        self.val = val
        self.children = {}

    def add(self,ch):  #add a new child
        node = self.children.get(ch,None)
        if not node:
            node = Node(ch)
            self.children[ch] = node

        return node

#https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
#single instance, so object is not created again and again
def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance

    
#better to use supressed Suffix tree
class SuffixTree(object):

    def __init__(self, word):
        self.root = Node()
        self.name = word
        for i in range(len(self.name)):
            self.add_str(self.name[i:])

    def add_str(self,str):
        if not str:
            return
        node = self.root
        for i in str:
            node = node.add(i)

    def find(self,pat):
        if not pat:
            return None
        pat = pat.lower()
        node = self.root
        for i in pat:
            n = node.children.get(i,None)
            if not n:
                return None
            node = n
        return self.name

#single 
@singleton
class FastLooker:
    def __init__(self, filename):
        self.filename = filename
        self.w = {}
        self.SUFFTREE = []
        with open(self.filename) as f:
            reader = csv.reader(f,delimiter='\t')
            for i,row in enumerate(reader):
                self.w[row[0]]=int(row[1])
                if i==MAX:
                    break
        self.load()

    #use memoize for caching previous calls
    #https://stackoverflow.com/questions/1988804/what-is-memoization-and-how-can-i-use-it-in-python
    @lru_cache(maxsize=None)
    def getMatches(self, word):
        matches=[]
        for i in range(len(self.w)):
            st = self.SUFFTREE[i]
            match = st.find(word)
            if match:
                matches.append([match,self.w[match]])
        # return matches
        matches = sorted(matches, key=lambda x: (len(x[0]),-x[1])) #according to criteria, shortest first, and then sort by frequency
        matches = [i[0] for i in matches[:LIM]]
        return matches[:LIM] #retuurn the top 25

    def load(self):
        #try pickled
        try:
            with open(f'{self.filename.split(".")[0]}_pickled.p', 'rb') as f:
                self.SUFFTREE = pickle.load(f)
        #else rebuild
        except:
            self.build()
            with open(f'{self.filename.split(".")[0]}_pickled.p', 'wb') as f:
                pickle.dump(
                    self.SUFFTREE,
                    f,
                    protocol=pickle.HIGHEST_PROTOCOL)
    
    def build(self):
        print(f'Total: {len(self.w)}')
        for j,word in enumerate(self.w):
            print(f'building {j}:{word}')
            self.SUFFTREE.append(SuffixTree(word))