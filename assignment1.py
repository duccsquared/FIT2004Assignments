"""
Assignment 1 FIT2004
By: Mario Susanto
"""

def alphabetVal(chr):
    """
    description:
        obtains a value based on ASCII values where @=0, A=1, B=2, etc
    input parameters:
        chr - a character
    outputs:
        an integer based on the ASCII value of chr
    worst case space and time complexity:
        time complexity - O(1)
        aux space complexity - O(1)
        explanation:
            this function involves no looping and no list creation,
            resulting in a constant time and space complexity
    """
    return ord(chr) - 64

def getItemFromResultsItem(item,resultsIndex):
    """
    description:
        a function that obtains a value from an array or a string based on its index and resultsIndex
    input parameters:
        item - an array containing a value or a value
        resultsIndex - -1 if item shouldn't be subscripted, index of array if item is an array
    outputs:
    worst case space and time complexity:
        time complexity - O(1)
        aux space complexity - O(1)
        explanation:
            this function involves no looping and no list creation,
            resulting in a constant time and space complexity
    """
    if(resultsIndex==-1):
        return item # returns either an integer or a string
    else:
        return item[resultsIndex] # from an item with the format (team1,team2,score), return an integer or string
def getLetterFromResultsItem(item,index,resultsIndex):
    """
    description:
        a function that obtains a letter from an array or a string based on its index and resultsIndex
    input parameters:
        item - an array containing a string or a string
        index - index of the string
        resultsIndex - -1 if item is a string, index of array if item is an array
    outputs:
        a character from item
    worst case space and time complexity:
        time complexity - O(1)
        aux space complexity - O(1)
        explanation:
            this function involves no looping and no list creation,
            resulting in a constant time and space complexity
    """
    return getItemFromResultsItem(item,resultsIndex)[index] # from a string return a character
     
def countingSortAlpha(arr,index=0,resultsIndex=-1,reverse=False):
    """
    description:
        a function that sorts characters in string in an array using counting sort
        with specific support for results
    input parameters:
        arr - the array to be sorted
        index - the position of the string at which to sort
        resultsIndex - index if using results as an input, or -1 otherwise
        reverse - a boolean stating whether to sort in descending alphabetical order
    outputs:
        a sorted array
    worst case space and time complexity:
        time complexity - O(N)
        aux space complexity - O(MN)
        where:
            N is the length of the array
            M is the number of characters in each team if arr is results
        explanation:
            The function iterates through the input list a constant number of times,
            but a duplicate of the list (which may be the results list) is created 

    """
    base = 27 # 26 for alphabet + 1 for padding
    # calculate frequency of each character
    countList = [0] * base 
    for item in arr: 
        letterIndex = ord(getLetterFromResultsItem(item,index,resultsIndex)) - 64
        if(reverse): letterIndex = base - 1 - letterIndex #reverse order
        countList[letterIndex] += 1 
    # calculate starting indexes of each character based on the count list
    posList = [0] * base 
    for i in range(1,base): 
        posList[i] = posList[i-1] + countList[i-1]
    # add items to position based on the position list
    resultList = [None] * len(arr)
    for item in arr:
        letterIndex = ord(getLetterFromResultsItem(item,index,resultsIndex)) - 64
        if(reverse): letterIndex = base - 1 - letterIndex
        resultList[posList[letterIndex]] = item
        posList[letterIndex] += 1
    return resultList

def countingSortResultsNumeric(arr,base=10,resultsIndex=-1): # time: O(kN), space: O(N)
    """
    description:
        a function that sorts numbers using counting sort, with specific support for results
    input parameters:
        arr - the array to be sorted
        base - the largest digit of the values that are to be sorted
        resultsIndex - index if using results as an input, or -1 otherwise
    outputs:
        a sorted array
    worst case space and time complexity:
        time complexity - O(N)
        aux space complexity - O(MN)
        where:
            N is the length of the array
            M is the number of characters in each team if arr is results
        explanation:
            The function iterates through the input list a constant number of times,
            but a duplicate of the list (which may be the results list) is create
    """
    u = base 
    # calculate frequency of each digit
    countList = [0] * u 
    for item in arr:  
        it = getItemFromResultsItem(item,resultsIndex)
        countList[it] += 1 
    posList = [0] * u 
    # calculate starting indexes of each digit based on the count list
    for i in range(1,u):
        posList[i] = posList[i-1] + countList[i-1]
    resultList = [None] * len(arr)
    # add items to position based on the position list
    for item in arr: 
        it = getItemFromResultsItem(item,resultsIndex)
        resultList[posList[it]] = item 
        posList[it] += 1 
    return resultList

def radixSortResults(results):
    """
    description:
        a function that sorts results using radix sort
        with score being most important, followed by team1, then team2
    input parameters:
        results - a list of matches between 2 teams represented as strings, and the resulting score for each match
    outputs:
        a sorted version of results
    worst case space and time complexity:
        time complexity - O(MN)
        aux space complexity - O(MN)
        where:
            N is the number of matches in results
            M is the number of characters in each team
        explanation:
            counting sort (O(N) time) is iterated through M times,
            and counting sort has a space complexity of O(MN)
    """
    # get maximum string length
    maxLen = 0
    for (team1,team2,score) in results:
        if(len(team1)>maxLen):
            maxLen = len(team1)
        if(len(team2)>maxLen):
            maxLen = len(team2)
    # pad string to ensure the same length
    # (@ is used because it is the ASCII letter before A, which makes counting sort more straightfoward)
    for i in range(len(results)):
        results[i][0] = results[i][0] + "@" * (maxLen - len(results[i][0]))
        results[i][1] = results[i][1] + "@" * (maxLen - len(results[i][0]))
    # sort team2, then team1
    for resultsIndex in [1,0]:
        # go through each letter and sort in reverse alphabetical order
        for i in range(maxLen-1,-1,-1):
            results = countingSortAlpha(results,i,resultsIndex,True)
    # sort by score
    results = countingSortResultsNumeric(results,101,2)
    # remove all padding and return sorted results
    return [[team1.replace("@",""),team2.replace("@",""),score] for (team1, team2, score) in results]

def alphabeticalOrder(strVal):
    """
    description:
        sorts a string in alphabetical order
    input parameters:
        strVal - a string comprized of alphabetic capital letters
    outputs:
        an alphabetically ordered string
    worst case space and time complexity:
        time complexity - O(M)
        aux space complexity - O(M)
        where:
            M is the length of the string
        explanation:
            It requires O(M) time to combine a list of length M back into a string,
            and counting sort in the context of a list of characters would require O(M) space
    """
    # do counting sort and revert output back to a string
    return "".join(countingSortAlpha(strVal))

def removeDuplicatesFromSorted(arr,key=lambda x:x):
    """
    description:
        a function that removes identical items from an array
    input parameters:
        arr - a sorted array
        key - a function used to extract the value to compare duplicates with
    output:
        a sorted array without any duplicates
    worst case space and time complexity:
        time complexity - O(N)
        aux space complexity - O(MN)
        where:
            N is the length of arr
        explanation:
            O(N) time because looping through a list occurs
            and O(MN) space because a new (results) array identical to the previous array is created
    """
    current = None 
    newArr = [] 
    for item in arr:
        if(key(item)!=key(current)): # if next item is different from the current item
            newArr.append(item) 
            current = item # for subsequent iterations, check for this item
    return newArr 

def binarySearch(arr,value,key=lambda x:x):
    """
    description:
        function that searches for the index of a value within a sorted array
        if the value isn't found, the next largest value is returned
    input parameters:
        arr - a sorted list
        value - the value to search for
        key - a function used to extract the value that can be compared with the value parameter
    output: 
        the index of the value, or the next largest value if not found
    worst case space and time complexity:
        time complexity - O(log(N))
        aux space complexity - O(1)
        where:
            N is the length of arr
        explanation:
            O(log(N)) time because the range between lo and hi halves every iteration
            this algorithm does not create new lists so it is in-place
    """
    # handle edge case if the value is larger than any value in the array
    if(value>key(arr[-1])):
        return len(arr)-1, None
    # set boundaries
    lo = 0
    hi = len(arr)-1
    mid = None
    # loop until value or next highest value is found
    while(lo <= hi):
        mid = (lo+hi)//2
        k = key(arr[mid])
        if(value==k):
            break
        elif(mid>0 and value<k and value>key(arr[mid-1])): # if mid is pointing to the next largest value
            break
        elif(value<k):
            hi = mid - 1
        else:
            lo = mid + 1
    return mid, key(arr[mid])

def analyze(results, roster, score):
    """
    description:
        function that finds the top 10 scores from a list of matches, along with a list of
        matches that have a score equal to a particular score
    input parameters:
        results - a list of matches between 2 teams represented as strings, and the resulting score for each match
            format: [(team1,team2,score),(team1,team2,score),...]
        roster - the number of possible characters that could show up in results (eg A, B, and C are possible when roster = 3)
        score - the score to search for in results
    outputs:
        top10matches - 10 unique matches with the highest score for the winning team
        searchedMatches - every match that either resulted in the same score as score, or the next highest score
    worst case space and time complexity:
        time complexity - O(MN)
        aux space complexity - O(MN)
        where:
            N is the number of matches in results
            M is the number of characters in each team
        explanation:
            this algorithm conducts radix sort, which takes O(MN) time
            and this algorithm creates duplicate arrays, which takes O(MN) space
    """
    top10matches = []
    searchedMatches = [] 
    # add all the inverses of each match to the results (aka team2 vs team1 instead of team1 vs team2)
    startLen = len(results)
    results += [[results[i][1], results[i][0], 100 - results[i][2]] for i in range(startLen)]
    # ensure that every string in results is ordered alphabetically
    for i in range(len(results)):
        results[i][0] = alphabeticalOrder(results[i][0]) 
        results[i][1] = alphabeticalOrder(results[i][1]) 
    # radix sort results
    results = radixSortResults(results)
    # remove any duplicates
    results = removeDuplicatesFromSorted(results,lambda x:x)
    # get the top 10 matches
    top10matches = results[-min(len(results),10):]
    top10matches.reverse()
    # get the index of the score (or the next highest score if not available)
    scoreIndex, score = binarySearch(results,score,lambda x:x[2])
    # if there are multiple matches with the searched score, find the rightmost item
    while(scoreIndex<len(results)-1 and results[scoreIndex+1][2]==score):
        scoreIndex += 1
    # add every match equal to the score into the searchedMatches array
    if(scoreIndex!=None):
        while(scoreIndex>=0 and results[scoreIndex][2]==score):
            searchedMatches.append(results[scoreIndex])
            scoreIndex -= 1
    # return results
    return [top10matches, searchedMatches]