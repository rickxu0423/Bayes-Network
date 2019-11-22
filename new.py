import xml.etree.ElementTree as ET, sys
from graph import Graph

e = []
varS = []
bn = Graph()

if len(sys.argv) < 3:
    print("Invalid argv: Less Than 2 argvs!")
    sys.exit()
if len(sys.argv) > 3:
    if len(sys.argv) % 2 != 1:
        print("Invalid argv: Wrong Format!")
        sys.exit()

file = sys.argv[1]
X = sys.argv[2]
varS.append(sys.argv[2])
try:
    tree = ET.parse(file)
except:
    print("File does not exists!")
    sys.exit()
if len(sys.argv) != 3:
    i = 3
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
print(varS)

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
print(newDict)

def finde(var, e):
    if var in e:
        return var
    elif "!" + var in e:
        return "!" + var
    else:
        return None

def findParent(parent, e):
    i = 0
    while i < len(parent):
        if parent[i] not in e:
            parent[i] = "!" + parent[i]
        i += 1
    return parent


def findp(Y, parent):
    return newDict[frozenset([Y]+parent)]


def enumerateAll(varS, e):
    if len(varS) == 0:
        return 1.0
    Y = varS.pop(0)
    parent = list(bn.findParent(Y))
    parent = findParent(parent, e)
    y = finde(Y, e)
    if y:
        varS1 = list(varS)      
        return findp(y, parent) * enumerateAll(varS1, e)
    else:
        varS2, varS3 = list(varS), list(varS)
        return findp(Y, parent) * enumerateAll(varS2, e+[Y]) + findp("!"+Y, parent) * enumerateAll(varS3, e+["!"+Y])

def normalize(Q):
    List1 = []
    List2 = []
    for key, val in Q.items():
        List1.append(key)
        List2.append(val)
    alpha = 1/(List2[0]+List2[1])
    Q[List1[0]] = alpha*List2[0]
    Q[List1[1]] = alpha*List2[1]
    return Q

def enumerationAsk(X, varS, e):
    Q = dict()
    Q[X] = enumerateAll(list(varS), e+[X])
    Q["!"+X] = enumerateAll(list(varS), e+["!"+X])
    return normalize(Q)


print(enumerationAsk(X, varS, e))