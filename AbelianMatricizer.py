# MATRICIZER
# The program takes as primary input a list of indices corresponding to the orders of the modular factors in an additive direct product group G of the form Z_m_1 x Z_m_2 x ... x Z_m_n. As output, the program:
# - generates the n-tuples corresponding to this group,
# - takes as further input a difference set corresponding to the carrier set (the elements of which are the generated n-tuples) to output an incidence matrix for G,
# - computes the rank of the incidence matrix through binary row reduction.

# FUTURE IMPROVEMENTS:
# i) Make functions modify input instead of generating output from scratch, i.e., make them fruitless functions instead of fruitful functions.
#   a) Some functions are fruitful, some are not. Will probably make it kinda confusing when the time comes to run the main method. Make up your mind.
# ii) Try and remove as many nested for-loops as possible.
# iii) Remove need for not putting spaces in input, make input more elegant.
# iv) Make variable names clearer and less redundant, i.e., name the variables better.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PART 1: OBTAINING A LIST OF GROUP ELEMENTS FOR A GIVEN GROUP

# Step 1. (fruitful) Make every entry an int instead of a list
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
# PART 2: GENERATING A MATRIX FROM A DIFFERENCE SET

    # PART 2.1: BINARIZED ELEMENTARY ROW OPERATIONS
# Step 1. (fruitful) Method to make all single element addition binary. For such limited purposes, equivalent to addition modulo 2. However, accuracy may not persist if you do a series of arithmetic manipulations and then just mod that. Make sure to use this operation wherever you would use
# ordinary addition. Also make sure to not have parameters x or y NOT equal to 0 or 1.
def add(x,y):
    c = (x+y)%2
    return c

# Step 2. (fruitless) Method to exchange two rows

# Step 3. (fruitless) Method to replace a row by the sum of that row and another row
 

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MAIN METHOD
def main():
    indexInput = input("Please enter a comma-separated list of the indices of your integer group modulo n.\nPlease do not enter any spaces Example: Z_2 x Z_4 would be entered as: 2,4. \n")
    strInputList = indexInput.split(",")
    a = getElements(strInputList)
    print(a)
main()
