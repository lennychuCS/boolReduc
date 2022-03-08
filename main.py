import numpy as np
import pandas as pd
np.set_printoptions(threshold=np.inf)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
global cols

segMap = {
            "A":10,
            "B":11,
            "C":12,
            "D":13,
            "E":14,
            "F":15,
            "G":16,
            "H":17,
            "I":18,
            "J":19,
            "K":20,
            "L":21,
            "M":22,
            "N":23,
            "O":24,
            "P":25,
            "DP":26

        }

with open("./tTable.csv") as file_name:
    data = np.loadtxt(file_name, delimiter=",", dtype="str")

def compileTerms(seg):
    index = segMap[seg]
    matchedTerms = []
    for term in data:
        #Term Index, Term Char, Number of Ones, Binary for Term
        term_info = term[0:10].tolist()
        if term[index] == "1":
            matchedTerms.append(term_info)
    return matchedTerms

def compareBinary(one, two):
    differences = 0
    newTerm = [one[0] + "," + two[0], (one[1] + "," + two[1]), "0"]
    for i in range(7):
        if one[i+3]==two[i+3]:
            newTerm.append(one[i+3])
            if one[i+3] == "1":
                newTerm[2] = str(int(newTerm[2]) + 1)
        else:
            newTerm.append("-")
            differences += 1
    temp = newTerm[0].split(",")
    for i in range(len(temp)):
        temp[i] = int(temp[i])
    temp.sort()
    for i in range(len(temp)):
        temp[i] = str(temp[i])

    newTerm[0] = ",".join(temp)

    if differences == 1:
        return newTerm

def combineTerms(termList):
    inputTerms = termList
    reducedTerms = []
    for termOne in inputTerms:
        for termTwo in inputTerms:
            if termOne[2] < termTwo[2]:
                newTerm = compareBinary(termOne,termTwo)
                if newTerm != None:
                    reducedTerms.append(newTerm)
    reducedTerms = [list(t) for t in set(tuple(element) for element in reducedTerms)]
    rlist = []
    indexesAccounted = []
    for term in reducedTerms:
        if term[0] not in indexesAccounted:
            rlist.append(term)
            indexesAccounted.append(term[0])
    return rlist

def showIncludedTerms(allTerms, data):
    global cols
    cols = ["Indexes"]
    out = []
    for term in data:
        info = [term[0]]
        for i in range(len(allTerms)):
            if allTerms[i][0] in term[0].split(","):
                info.append("✔")
            else:
                info.append("-")
        out.append(info)
    for i in range(len(allTerms)):
        cols.append(allTerms[i][0])
    return out

segment = "A"
segmentTerms = compileTerms(segment)
#print(np.array(combineTerms(segmentTerms)))
#print(np.array(combineTerms(combineTerms(segmentTerms))))
#print(np.array(combineTerms(combineTerms(combineTerms(segmentTerms)))))
#print(np.array(combineTerms(combineTerms(combineTerms(combineTerms(segmentTerms))))))
try:
    output = np.array(showIncludedTerms(segmentTerms, combineTerms(combineTerms(combineTerms(segmentTerms)))))
    output = np.vstack([output, np.array(showIncludedTerms(segmentTerms, combineTerms(combineTerms(segmentTerms))))])
    output = np.vstack([output, np.array(showIncludedTerms(segmentTerms, combineTerms(segmentTerms)))])
    output = np.vstack([output, np.array(showIncludedTerms(segmentTerms, segmentTerms))])
except:
    try:
        output = np.array(showIncludedTerms(segmentTerms, combineTerms(combineTerms(segmentTerms))))
        output = np.vstack([output, np.array(showIncludedTerms(segmentTerms, combineTerms(segmentTerms)))])
        output = np.vstack([output, np.array(showIncludedTerms(segmentTerms, segmentTerms))])
    except:
        output = np.array(showIncludedTerms(segmentTerms, combineTerms(segmentTerms)))
        output = np.vstack([output, np.array(showIncludedTerms(segmentTerms, segmentTerms))])

df = pd.DataFrame(output)
df.columns = cols
print(df)

#### You could reduce the gates shown above, but I'm not sure the best way
#### Below is where gates will be selected
valuesToCover = cols[1:]
