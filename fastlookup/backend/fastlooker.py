import pickle #for pickling
import csv
import os
from django.conf import settings

FILENAME = os.path.join(settings.BASE_DIR, 'word_search.tsv')

LIM = 25
SUFFTREE = [] #Suffix tree array



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

w = {}
with open(FILENAME) as f:
    reader = csv.reader(f,delimiter='\t')
    for i,row in enumerate(reader):
        w[row[0]]=int(row[1])
        if i==2000:
        	break

def getMatches(word):
    global SUFFTREE
    matches = []
    try:
        SUFFTREE = pickle.load(open(f"{FILENAME.split('.')[0]}_pickled.p","rb"))
        print('pickle loaded')
    except:
        build()
        pickle.dump(SUFFTREE,open(f"{FILENAME.split('.')[0]}_pickled.p","wb"))
    for i in range(len(w)):
        st = SUFFTREE[i]
        match = st.find(word)
        if match:
            matches.append([match,w[match]])
    # return matches
    matches = sorted(matches, key=lambda x: (len(x[0]),-x[1])) #according to criteria, shortest first, and then sort by frequency
    matches = [i[0] for i in matches[:LIM]]
    return matches[:LIM] #retuurn the top 25


#function to build tree
def build():
    print(f'Total: {len(w)}')
    for j,word in enumerate(w):
        print(f'building {j}:{word}')
        SUFFTREE.append(SuffixTree(word))