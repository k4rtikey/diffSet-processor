import itertools

def integerize(strInputList):
    for i in range(len(strInputList)):
        strInputList[i] = int(strInputList[i])
    indexList = strInputList
    return indexList

# Step 2. Obtain a properly formatted list of range(n) for every n in indexList. This will be done by the following steps:
    # Step 2.1. (fruitful) Obtain a list of ranges
def ranginate(indexList):
    rangesList = []
    for i in indexList:
        residueList = []
        for j in range(i):
            residueList.append(j)
        rangesList.append(residueList)
    return rangesList

    # Step 2.2. (fruitless) Make list format compatible with the concatenator (designed in Step 4.). Takes a list [0,1] and converts it to [[0],[1]]. This will be used as the bracketedList parameter in concatenate().
def bracketize(rangesList):
    for i in range(len(rangesList)):
        entry = []
        entry.append(rangesList[i])
        rangesList[i] = entry

# Step 3. Generate ordered n-tuples from this. This will be done by the following steps:
    # Step 3.1. (fruitful) Define a function which takes as parameters two lists of any length, and outputs a list containing concatenated entries of the two lists. Note that the parameter bracketedList must be bracketed in the sense of the bracketize function above.
def concatenate(bracketedList,list2):
    concatList = []
    for i in bracketedList:
        for j in list2:
            # the [:] ensures that iCopy is a new copy of i, instead of just a reference to i.
            iCopy = i[:]
            iCopy.append(j)
            concatList.append(iCopy)
    return concatList

    # Step 3.2. (fruitful) Chain the concatenate function so that you can get all group entries. The output of last concatenate operation should be the input (parameter bracketedList) of the next concatenate operation.
def getElements(strInputList):
    indexList = integerize(strInputList)
    rangesList = ranginate(indexList)
    bracketize(rangesList[0])
    runningOutput = concatenate(rangesList[0], rangesList[1])
    i = 2
    while (i < len(rangesList)):
        runningOutput = concatenate(runningOutput, rangesList[i])
        i = i+1
    return runningOutput
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PART 2: INCIDENCE MATRIX AND OPERATIONS ON IT
    # PART 2.1: GENERATING AN INCIDENCE MATRIX
# Step 1. (fruitful) Addition modulo m and n
def modAdd(summand1, summand2, group):
    result = []
    for i in range(len(group)):
        sum = (summand1[i]+summand2[i]) % group[i]
        result.append(sum)
    return result

def linCombo(listOfArr, group):
    sum = listOfArr[0]
    i = 1
    while (i < len(listOfArr)):
        sum = modAdd(sum, listOfArr[i], group)
        i = i+1
    return sum


# Step 2. (fruitful) Take a group, and a difference set, and output the requisite incidence matrix. Element list must be ordered. Also note that modList requirement can be removed from this using OOP. Also, your matrix's rows aren't in the right order for some reason.
def matrix(group, diffSet):
    outMatrix = []
    elementList = getElements(group)
    for e in elementList:
        row = []
        for e2 in elementList:
            if (modAdd(e2,e, group) in diffSet):
                row.append(1)
            else: row.append(0)
        outMatrix.append(row)
    return outMatrix

    # PART 2.2: BINARIZED ELEMENTARY ROW OPERATIONS
# Step 1. (fruitful) Method to make all single element addition binary. For such limited purposes, equivalent to addition modulo 2. However, accuracy may not persist if you do a series of arithmetic manipulations and then just mod that. Make sure to use this operation wherever you would use
# ordinary addition. Also make sure to not have parameters x or y NOT equal to 0 or 1.
def add(x,y):
    c = (x+y)%2
    return c

# Step 2. (fruitless) Method to exchange two rows
# Obsolete: remove in next iteration
def exchange(list2d, row1, row2):
    temp = list2d[row1]
    list2d[row1] = list2d[row2]
    list2d[row2] = temp

# Step 3. (fruitless) Method to replace a row by the sum of that row and another row
def rowSum(row1, row2):
    result = []
    for i in range(len(row1)):
        summation = (row1[i]+row2[i])%2
        result.append(summation)
    return result

# Step 4. (fruitful) Row reduction algorithm designed to work in binary; jerry-rigged version of algorithm from zhuowei (in public domain). URL: https://gist.github.com/zhuowei/7149445
def rowReducev1(mat):
	# Let's do forward step first.
	# at the end of this for loop, the matrix is in row-echelon format.
	for i in range(len(mat)):
		# every iteration, ignore one more row and column
		for r in range(i, len(mat)):
			# find the first row with a nonzero entry in first column
			if mat[r][i] == 0:
				continue
			# swap current row with first row
			temp = mat[i]
			mat[i] = mat[r]
			mat[r]= temp
			# add multiples of the new first row to lower rows so lower
			# entries of first column is zero
			for r in range(i+1, len(mat)):
			    if(mat[r][i] == 1):
			        rowSum(mat[i],mat[r])
			break
	# At the end of the forward step
	return mat

# new and improved bespoke row reduction, which works for arbitrary mod 2 m x n matrices.

def rowReducev2(mat):
    for i in range(min(len(mat),len(mat[0]))):
        subMat = mat[i:]
        # find ith pivot
        pivotIndex = -1
        pivotCol = []
        for j in range(len(mat[0])):
            col = [x[j] for x in subMat]
            if (1 in col):
                pivotIndex = j
                pivotCol = col
                break
        if (pivotIndex == -1):
            break
        mat[i], mat[pivotCol.index(1)+i] = mat[pivotCol.index(1)+i], mat[i]
        #it's alive!
        for k in range(i+1, len(mat)):
            if(mat[k][pivotIndex] == 1):
                mat[k] = rowSum(mat[i],mat[k])
    return mat

# Step 5. Method to multiply two rows. Used in next step.
def rowMultiply(row1,row2):
    newRow = []
    for i in range(len(row1)):
        product = (row1[i]*row2[i])
        newRow.append(product)
    return newRow

# non-fruitful
def extendMatrix(matrix):
    newRowList = []
    for i in range(len(matrix)):
        for j in range(i+1, len(matrix)):
            newRowList.append(rowMultiply(matrix[i],matrix[j]))
    matrix.extend(newRowList)

def rank(reducedMatrix):
    # count number of all-zeroes rows, and subtract that from total number of columns to get the rank
    counter = 0
    for i in reducedMatrix:
        sum = 0
        for j in range(len(i)):
            sum = sum + i[j]
        if (sum != 0):
            counter = counter+1
    return (counter)

# HYPERPLANE FUNCTIONS

# jerry-rigged version of code by hughdbrown at https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
def powerset(s):
  out = []
  x = len(s)
  masks = [1 << i for i in range(x)]
  for i in range(1,1 << x):
    it = [ss for mask, ss in zip(masks, s) if i & mask]
    out.append(it)
  return out

def genHyperplanes(generatorList, group):
    out = []
    for g in generatorList:
        p = powerset(g)
        toAppend = [[0]*len(group)]
        for thing in p:
            toAppend.append(linCombo(thing, group))
        out.append(toAppend)
    return out

def hpTranslate(hyp, cosRep, group):
    newhp = []
    for h in hyp:
        new = modAdd(h, cosRep, group)
        newhp.append(new)
    return newhp

def genDiffSet(hypList, cosRepList, group):
    newHypList = []
    for i in range(len(hypList)):
        new = hpTranslate(hypList[i], cosRepList[i], group)
        newHypList.append(new)
    diffSet = []
    for j in range(len(hypList)):
        diffSet.extend(newHypList[j])
    return diffSet

def prodConstruction(diffSet1, group1):
    diffSet1comp = []
    elements = getElements(group1)
    for i in elements:
        if (i not in diffSet1):
            diffSet1comp.append(i)
    compCopy1 = diffSet1comp[:]
    for i in compCopy1:
        i.append(0)
    part1 = diffSet1[:]
    part2 = diffSet1[:]
    part3 = diffSet1[:]
    part1.append(1)
    part2.append(2)
    part3.append(3)
    compCopy1.extend(part1)
    compCopy1.extend(part2)
    compCopy1.extend(part3)
    return compCopy1
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MAIN METHOD
def main():
    #a = genDiffSet(genHyperplanes([[[4,0,0,0],[0,2,0,0],[0,0,2,0]],[[0,2,0,0],[0,0,2,0],[0,0,0,1]],[[0,0,2,0],[0,0,0,1],[4,2,0,0]],[[0,0,0,1],[4,2,0,0],[0,2,2,0]],[[4,2,0,0],[0,2,2,0],[0,0,2,1]],[[0,2,2,0],[0,0,2,1],[4,2,0,1]],[[0,0,2,1],[4,2,0,1],[4,0,2,0]],[[4,2,0,1],[4,0,2,0],[0,2,0,1]],[[4,0,2,0],[0,2,0,1],[4,2,2,0]],[[0,2,0,1],[4,2,2,0],[0,2,2,1]],[[4,2,2,0],[0,2,2,1],[4,2,2,1]],[[0,2,2,1],[4,2,2,1],[4,0,2,1]],[[4,2,2,1],[4,0,2,1],[4,0,0,1]],[[4,0,2,1],[4,0,0,1],[4,0,0,0]],[[4,0,0,1],[4,0,0,0],[0,2,0,0]]],[8,4,4,2]), [[2,0,0,0],[1,0,0,0],[3,0,0,0],[1,1,0,0],[3,1,0,0],[0,1,0,0],[1,0,1,0],[0,0,1,0],[3,0,1,0],[1,1,1,0],[2,1,0,0],[2,0,1,0],[3,1,1,0],[0,1,1,0],[2,1,1,0]],[8,4,4,2])

    #mat2 = matrix([8,4,4,2], a)
    #extendMatrix(mat2)
    #mat = rowReducev2(mat2)

    #print(rank(mat))

    hypList = [[[0,0,0],[4,0,0],[0,2,0],[4,2,0]],[[0,0,0],[0,2,0],[0,0,1],[0,2,1]],[[0,0,0],[0,0,1],[4,2,0],[4,2,1]],[[0,0,0],[4,2,0],[0,2,1],[4,0,1]],[[0,0,0],[0,2,1],[4,2,1],[4,0,0]],[[0,0,0],[4,2,1],[4,0,1],[0,2,0]],[[0,0,0],[4,0,1],[4,0,0],[0,0,1]]]
    cosRepList = [[1,0,0],[2,0,0],[3,0,0],[0,1,0],[1,1,0],[2,1,0],[3,1,0]]
    cosetPermList = []
    print("Program has started")
    for i in list(itertools.permutations(cosRepList)):
        cosetPermList.append(list(i))
    for i in cosetPermList:
        mat = matrix([8,4,2], genDiffSet(hypList,i,[8,4,2]))
    #mat = matrix([8,4,2], [[0,0,0],[1,0,0],[0,0,1],[4,0,0],[1,0,1],[0,1,1],[2,1,0],[0,3,0],[2,0,1],[4,0,1],[6,0,0],[1,1,1],[3,0,1],[3,2,0],[7,0,0],[5,2,0],[2,1,1],[4,1,1],[2,3,0],[4,3,0],[2,2,1],[6,2,0],[1,3,1],[5,1,1],[5,2,1],[2,3,1],[5,3,1],[7,2,1]])
        extendMatrix(mat)
        redMat = rowReducev2(mat)
        if (rank(redMat) == 29):
            print("DiffSet: ")
            print(genDiffSet(hypList, i,[8,4,2]))
    

main()
