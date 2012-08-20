#! /usr/bin/python
import re
import random
import sys
import copy
allWords = "/usr/share/dict/words"
wordList = "wordList"

template = [[0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,1,1,0,0,0,0,0,1],
            [0,0,0,0,0,0,1,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,1,0,0,0,0,1,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,1,0,0,0,0,1,0,0,0,0,0],
            [1,1,1,0,0,0,0,0,1,0,0,0,0,0,0],
            [1,0,0,0,0,0,1,1,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0]]

template2 = [[0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
             [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
             [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [1,1,1,0,0,0,1,0,0,0,1,0,0,0,0],
             [0,0,0,0,1,0,0,0,0,1,0,0,0,1,1],
             [0,0,0,1,0,0,0,0,1,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,1,0,0,0,0,1,0,0,0],
             [1,1,0,0,0,1,0,0,0,0,1,0,0,0,0],
             [0,0,0,0,1,0,0,0,1,0,0,0,1,1,1],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
             [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
             [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0]]

template3 = [[0,0,0],
             [0,0,0],
             [0,0,0]]

def crossword(template,wordList):
    f = open(wordList)
    lines = f.readlines()
    words = dict()
    for line in lines:
        #print line
        if "'" not in line:
            if len(line)-1 not in words:
                words[len(line)-1] = list()
            words[len(line)-1].append(line.upper()[:-1])

    def printCrossword(grid):
        for row in range(0,len(grid)):
            print "+-"*len(grid)+"+"
            for column in range(0,len(grid)):
                if grid[row][column] == 1:
                    sys.stdout.write(u"|\u2588")
                else:
                    sys.stdout.write("|"+str(grid[row][column]))
            sys.stdout.write("|\n")
        print "+-"*len(grid)+"+"
    def crosswordAux(grid,words):
        # find next empty down index
        index = (-1,-1)
        for i in [(row,column) for row in range(0,len(grid)) for column in range(0,len(grid))]:
            if grid[i[0]][i[1]] == 0 and (i[0] == 0 or grid[i[0]-1][i[1]] == 1):
                index = i
                break
        #print index
        #printCrossword(grid)
        if index == (-1,-1): # no next index was found, must be done
            printCrossword(grid)
            return True

        # get length of this word
        wordLength = 0
        for i in range(0,len(grid)-index[0]):
            if grid[index[0]+i][index[1]] == 1:
                wordLength = i
                break
        else:
            wordLength = len(grid)-index[0]
        if wordLength not in words: return False
        
        # iterate through possible words
        shuffledWords = list(words[wordLength])
        random.shuffle(shuffledWords)
        badWords = set() # store list of words that cause conflicts
        for word in shuffledWords:
            if word in badWords: continue # don't try a word that causes a conflict
            gridCopy = copy.deepcopy(grid) # make a copy for editing & recursion
            # insert word and check for conflicts
            for i in range(0,wordLength):
                gridCopy[index[0]+i][index[1]] = word[i]

                #find across word that this letter is part of
                indexCopy = (index[0]+i,index[1])
                # go back to filled square or beginning of line
                while indexCopy[1] > 0 and gridCopy[indexCopy[0]][indexCopy[1]-1] != 1:
                    indexCopy = (indexCopy[0],indexCopy[1]-1)
                expression = "^"
                # iterate across line until filled square is found, adding to a regular expression
                acrossWordLength = 0
                while indexCopy[1] < len(grid) and gridCopy[indexCopy[0]][indexCopy[1]] != 1:
                    if gridCopy[indexCopy[0]][indexCopy[1]] == 0:
                        expression = expression + "\w" # add wildcard
                    else:
                        expression = expression + gridCopy[indexCopy[0]][indexCopy[1]] # add letter in square
                    indexCopy = (indexCopy[0],indexCopy[1]+1)
                    acrossWordLength += 1
                # check for conflicts
                doContinue = False
                #printCrossword(gridCopy)
                if not any(re.search(expression,s) is not None for s in words[acrossWordLength]):
                    doContinue = True
                    toRemove = set(filter(lambda x:re.match("\w{"+str(i)+"}"+word[i],x) is not None,shuffledWords))
                    #print toRemove
                    badWords = badWords.union(toRemove)
                    break
            if doContinue:
                continue
            #printCrossword(gridCopy)
            if crosswordAux(gridCopy,words): return True
        return False
    crosswordAux(template,words)
    

if __name__ == "__main__": 
    t = sys.argv[1]
    if t == "template":
        crossword(template,sys.argv[2])
    elif t == "template2":
        crossword(template2,sys.argv[2])
    elif t == "template3":
        crossword(template3,sys.argv[2])
    else:
        crossword(template,sys.argv[2])
    #crossword(template2,allWords)
