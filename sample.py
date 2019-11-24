import xml.etree.ElementTree as ET, sys, random
from graph import Graph
from time import time

e = []
varS = []
N = None
bn = Graph()

if len(sys.argv) < 4:
    print("Invalid argv: Less Than 2 argvs!")
    sys.exit()
if len(sys.argv) > 4:
    if len(sys.argv) % 2 != 0:
        print("Invalid argv: Wrong Format!")
        sys.exit()

file = sys.argv[2]
X = sys.argv[3]
try:
    N = int(sys.argv[1])
except:
    print("Invalid argv: Wrong Sample Number")
    sys.exit()
varS.append(sys.argv[3])
try:
    tree = ET.parse(file)
except:
    print("File does not exists!")
    sys.exit()
if len(sys.argv) != 4:
    i = 4
    while i < len(sys.argv):
        if sys.argv[i+1].lower() == "true":
            varS.append(sys.argv[i])
            e.append(sys.argv[i])
            i += 2
        elif sys.argv[i+1].lower() == "false":
            varS.append(sys.argv[i])
            e.append("!"+sys.argv[i])
            i += 2
        else:
            print("Invalid argv: Wrong Format!")
            sys.exit()

root = tree.getroot()

varList = []
fgList = []
defList = []

for i in range(len(root[0])):
    tem = root[0][i]
    if tem.tag == 'VARIABLE':
        varList += tem[0].text.split(' ')
    elif tem.tag == 'DEFINITION':
        
        for stuff in tem:
            if stuff.tag == 'FOR':
                node = stuff.text
                temList_1 = [stuff.text]
            elif stuff.tag == 'GIVEN':
                temList_1 += [stuff.text]
                bn.addEdge((node, stuff.text))
            elif stuff.tag == 'TABLE':
                temList = stuff.text.replace('\n','').replace('\t','').strip().split(' ')
                j = 0
                while j < len(temList):
                    if not temList[j]:
                        temList.pop(j)
                    else:
                        temList[j] = float(temList[j])
                        j += 1
                defList.append(temList)
        fgList.append(temList_1)

j = 0
while j < len(varS):
    tem = bn.findParent(varS[j])
    for var in list(tem):
        if var in varS:
            tem.remove(var)
    if len(tem) > 0:
        for stuff in tem:
            varS.insert(1,stuff)
            j = 0
    j += 1

# sort the list topologically
i = 0
while 1:
    flag = 0
    while i < len(varS) - 1:
        var = bn.findParent(varS[i])
        if var:
            for stuff in var:
                if stuff not in varS[:i]:
                    varS[i], varS[i+1] = varS[i+1], varS[i]
                    flag += 1      
                    break
            i += 1
        else:
            i += 1
    if flag == 0:
        break

newDict = dict()
for i in range(len(fgList)):
    counter = 2 ** len(fgList[i])  
    j = 0
    while j < counter:
        k = 0
        List = []
        a = "" if j % 2 == 0 else "!"
        b = "" if j < 0.5 * counter else "!"
        c = "" if j % 4 == 0 or (j - 1) % 4 == 0 else "!"
        while k < len(fgList[i]):
            if k == 0:
                List.append(a+fgList[i][k])
            elif k == 1:
                List.append(b+fgList[i][k])
            elif k == 2:
                List.append(c+fgList[i][k])
            k += 1
        newDict[frozenset(List)] = defList[i][j]
        j += 1
    i += 1

def priorSample(sortedGraph):
    sample = []
    while sortedGraph:
        Y = sortedGraph.pop(0)
        parent = findParent(list(bn.findParent(Y)), sample)
        parent += [Y]
        if random.random() <= newDict[frozenset(parent)]:
            sample.append(Y)
        else:
            sample.append("!"+Y)
    return sample


def findParent(parent, e):
    i = 0
    while i < len(parent):
        if parent[i] not in e:
            parent[i] = "!" + parent[i]
        i += 1
    return parent

def consistent(sample, e):
    for var in sample:
        if "!" + var in e:
            return False
    for evidence in e:
        if "!" + evidence in sample:
            return False
    return True

def normalize(Q):
    List1 = []
    List2 = []
    for key, val in Q.items():
        List1.append(key)
        List2.append(val)
    if len(List1) == 1:
        Q[List1[0]] = 1
        if len(List1[0]) == 1:
            Q["!"+List1[0]] = 0
        elif len(List1[0]) == 2:
            Q[List1[0][1:]] = 0       
        return "Sample Not Enough"
    elif len(List1) == 0:
        return Q
    alpha = 1/(List2[0]+List2[1])
    Q[List1[0]] = alpha*List2[0]
    Q[List1[1]] = alpha*List2[1]
    return Q

def rejectionSampling(X, e, sortedGraph, N):
    Q = {}
    reject = 0
    accept = 0
    for i in range(1, N + 1):
        sample = priorSample(list(sortedGraph))
        if not consistent(sample, e):
            reject += 1
            continue
        if X in sample:
            Q[X] = Q.get(X,0) + 1
            accept += 1
        elif "!"+X in sample:
            Q["!"+X] = Q.get("!"+X,0) + 1
            accept += 1
    return normalize(Q), accept, reject

t = time()
result = rejectionSampling(X, e, list(varS), N)
print("")
print("Result:", result[0])
rate = result[1] / (result[1] + result[2])
print("Accept:", result[1], "Reject:", result[2])
print("Acception Rate:", rate)
print("Calculated in %.1fs" % (time() - t))
print("")


