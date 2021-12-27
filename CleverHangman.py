import random


def handleUserInputDebugMode():
    '''
        Prompt the user if they wish to play in debug mode. True is returned
        if the user enters the letter “d”, indicating debug mode was chosen;
        False is returned otherwise.
    '''
    ans = input("Which mode do you want: (d)ebug or (p)lay:")

    if ans == "d":
        return True
    else:
        return False


def handleUserInputDifficulty():
    '''
    This function asks the user if they would like to play the game in (h)ard or (e)asy mode, then returns the
    corresponding number of misses allowed for the game.
    '''

    ans = input("How many misses do you want? Hard has 8 and Easy has "
                "12.  \n" + "(h)ard or (e)asy>")

    if ans == 'e':
        print("you have 12 misses to guess word")
        return 12
    else:
        print("you have 8 misses to guess word")
        return 8


def handleUserInputWordLength():
    '''
        Asks user how long secretWord should be. User will input
        number between 5 and 10.
    '''

    ans = input("How many letters in the word you'll guess: ")
    return int(ans)


def createTemplate(currTemplate, letterGuess, word):
    '''
    This will create a new template for the secret word that the user will see.
    '''


    #print(currTemplate)
    #new template as a list

    ctemplatelist = list(currTemplate)
    newtemplist = []

    for i in range(len(ctemplatelist)):
        #print("ct " + currTemplate)
        #print("cti " + currTemplate[i])
        if ctemplatelist[i] == "_" and word[i] == letterGuess:
            ctemplatelist[i] = letterGuess

    string2 = "".join(ctemplatelist)

    newtemp = string2

    return newtemp


def getNewWordList(currTemplate, letterGuess, wordList, debug):
    '''
    Constructs a dictionary of strings as the key to lists as the value. I
    '''
    dict1 = {}

    for w in wordList:
        temp = createTemplate(currTemplate, letterGuess, w)

        if temp not in dict1:
            dict1[temp] = [w]

        else:
            dict1[temp] = dict1[temp] + [w]



    sorteddict = sorted(dict1.items(), key=lambda x: (len(x[1]),
                                                      x[0].count("_")))

    first = sorteddict[-1][0]
    second = dict1[first]
    tuple1 = (first, second)


    if debug == True:
        dict2 = {}

        for k in dict1:
            dict2[k] = len(dict1[k])



        debugdict = sorted(dict2.items())

        for key in debugdict:
            print(key[0] + " : " + str(key[1]))

        print("# keys = " + str(len(debugdict)))

    return tuple1




def processUserGuessClever(guessedLetter, hangmanWord, missesLeft):
    '''
    Takes user's guess, the user's current progress on the word, and the number of misses left;
updates the number of misses left and indicates whether the user missed.
    '''

    list1 = []

    if guessedLetter in hangmanWord:
        list1.append(missesLeft)
        list1.append(True)
    else:
        missesLeft -= 1
        list1.append(missesLeft)
        list1.append(False)

    return list1

def createDisplayString(lettersGuessed, missesLeft, hangmanWord):
    '''
    Creates the string that will be displayed to the user, using the information in the parameters.
    '''

    alphabet = list("abcdefghijklmnopqrstuvwxyz")

    #not yet guessed letter list
    notguessedlist = []

    for i in range(len(alphabet)):
        if alphabet[i] in lettersGuessed:
            notguessedlist.append(" ")
        else:
            notguessedlist.append(alphabet[i])

    newalphabet = "".join(notguessedlist)

    return "letters not yet guessed: " + newalphabet + "\n" + "misses remaining = " + \
           str(missesLeft) + "\n" + " ".join(hangmanWord)


def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if it is a repeated letter.
    '''

    print(displayString)

    while True:
        letInput = input("letter> ")
        if letInput not in lettersGuessed:
            return letInput
        else:
            print("you already guessed that")




def runGame(filename):
    '''
    This function sets up the game, runs each round, and prints a final message on whether or not the user won.
    True is returned if the user won the game. If the user lost the game, False is returned.
    '''

    # original text file list
    textfilelist = []

    # actual wordlist
    thewordlist = []

    f = open(filename).readlines()
    for word in f:
        textfilelist.append(word[:len(word)-1])

    # which mode do you want:
    debug = handleUserInputDebugMode()

    # how many letters
    length = handleUserInputWordLength()

    # how many misses do you want
    missesLeft = handleUserInputDifficulty()
    initial = missesLeft

    for w in textfilelist:
        if len(w) == length:
            thewordlist.append(w)

    sword = thewordlist[random.randint(0, len(thewordlist) - 1)]

    # hangmanword (comprised of underscores and letters)
    hangmanlist = []


    for c in range(len(sword)):
        hangmanlist.append("_")

    hangmanstring = "".join(hangmanlist)


    lguessed = []

    while missesLeft > 0 and "_" in hangmanlist:

        hui = handleUserInputLetterGuess(lguessed,
                                         createDisplayString(
                                             lguessed, missesLeft,
                                             hangmanlist))

        if debug:
            print("(word is " + sword + ")")
            print("# possible words: ", len(thewordlist))


        #ct = createTemplate(hangmanstring, hui, sword)

        tuple2 = getNewWordList(hangmanlist, hui, thewordlist, debug)



        hangmanlist = list(tuple2[0])
        hangmanstring = "".join(hangmanlist)

        thewordlist = tuple2[1]


        sword = thewordlist[random.randint(0, len(thewordlist) - 1)]
        lguessed.append(hui)

        valueofguess = processUserGuessClever(hui, hangmanlist, missesLeft)



        missesLeft = valueofguess[0]
        didnotfail = valueofguess[1]

        if didnotfail == False:
            print("you missed: " + hui + " not in word" + "\n")

    # count win and loss stats

    if "_" not in hangmanlist:
        print("You guessed the word: " + sword)
        print("you made " + str(len(lguessed)) + " guesses with " +
              str(initial - missesLeft) + " misses")
    elif "_" in hangmanlist and missesLeft == 0:
        print("You're hung!!" + "\n" + "word is " + sword)
        print("you made " + str(len(lguessed)) + " guesses with " +
              str(initial - missesLeft) + " misses")

    if "_" not in hangmanlist:
        return True
    else:
        return False


if __name__ == "__main__":
    '''
    Running Hangman.py should start the game, which is done by calling runGame, therefore, we have provided you this code below.
    '''

    summary = []

    playagain = 'y'

    while playagain == 'y':
        summary.append(runGame('lowerwords.txt'))
        playagain = input("Do you want to play again? y or n>")

    print("You won " + str(summary.count(True)) + " games and lost " + str(
        summary.count(False)))


