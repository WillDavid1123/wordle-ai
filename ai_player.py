from asyncio.windows_events import NULL
import pdb
import random
import utils

def makeguess(wordlist, guesses=[], feedback=[]):
    """Guess a word from the available wordlist, (optionally) using feedback 
 from previous guesses.
 
 Parameters
 ----------
 wordlist : list of str
 A list of the valid word choices. The output must come from this list.
 guesses : list of str
 A list of the previously guessed words, in the order they were made, 
 e.g. guesses[0] = first guess, guesses[1] = second guess. The length 
 of the list equals the number of guesses made so far. An empty list 
 (default) implies no guesses have been made.
 feedback : list of lists of int
 A list comprising one list per word guess and one integer per letter 
 in that word, to indicate if the letter is correct (2), almost 
 correct (1), or incorrect (0). An empty list (default) implies no 
 guesses have been made.
 Output
 ------
 word : str
 The word chosen by the AI for the next guess.
 """

    #Variables
    wordKnowledge = ['?','?','?','?','?'] #What we for sure know about the word
    bannedLetters = [] #What letters are not in the word
    keepLetters = [] #What letters are in the word
    bannedWords = [] #What words cannot be the secret word
    possWords = []  #What words are possibly the secret word

    #Hard-coded guesses
    if len(guesses) == 0: 
        return "ADIEU"
    elif len(guesses) == 1:
        return "SNORT"
    else: 

        #Loops that run through every guess, its feedback, and appropriate actions and manipulations to our wordbank
        for i in range(len(guesses)):

            for j in range(5): 

                #If the current letter is grey and not already a letter in the word (for double letters)
                if feedback[i - 1][j] == 0 and not (keepLetters.__contains__(guesses[i - 1][j])): 
                    bannedLetters.append(guesses[i - 1][j])

                #If the letter is in the word
                elif feedback[i - 1][j] != 0:
                    keepLetters.append(guesses[i - 1][j])

                    #If the letter is not in the right spot
                    if feedback[i - 1][j] == 1:
                        wordlist = switchPlaces(wordlist, guesses[i - 1][j], j)

                    #If the letter is in the right spot
                    if feedback[i - 1][j] == 2:
                        wordKnowledge[j] = guesses[i - 1][j]


        bannedLetters = list(set(bannedLetters) - set(keepLetters)) 

        #Loop through each banned letter and remove any words with that letter 
        for j in range(len(bannedLetters)): 
            bannedWords = notInWord(wordlist, bannedWords, bannedLetters[j]) 
            
        bannedWords += guesses
        wordlist = list(set(wordlist) - set(bannedWords)) #Adapt word list to not incluse any banned words
        wordlist = possibleWords(wordlist, wordKnowledge, possWords) 

        #If there are letters we know are in the word, adapt the word list to only have words with that letter
        if len(keepLetters) > 0:
            wordlist = changeLetters(wordlist, keepLetters)

        #Start of guess conditionals
        if len(set(keepLetters)) >= 5: #If all of the letters are known
            return wordlist[random.randint(0, len(wordlist)-1)] #Return a new word to guess
        elif len(guesses) == 2 and keepLetters.__contains__("A"):
            return "AMPLY"
        elif len(guesses) == 2 and keepLetters.__contains__("E"):
            return "CLYPE"
        elif len(guesses) == 2 and keepLetters.__contains__("I"):
            return "IMPLY"
        elif len(guesses) == 2 and keepLetters.__contains__("U"):
            return "CLUMP"
        elif len(guesses) == 2 and keepLetters.__contains__("T"):
            return "FETCH"
        elif len(guesses) == 2 and keepLetters.__contains__("O"):
            return "CYMOL"
        elif len(guesses) == 3 and len(keepLetters) <= 3:
            if keepLetters.__contains__("A"):
                return "BALKY"
            elif keepLetters.__contains__("I"):
                return "CHALK"

    return wordlist[random.randint(0, len(wordlist)-1)] #Return a new word to guess


def notInWord(wordlist, bannedWords, letter):
    '''Function that finds words with the given letter and adds them to a banned words list'''
    for j in range(len(wordlist)): 
        for k in range(5): 
            if wordlist[j][k] == letter: 
                bannedWords.append(wordlist[j])
                continue 
    return bannedWords


def possibleWords(wordlist, wordKnowledge, possWords):
    '''Function that finds words that fit the current known knowledge of letter position and adds them to a keep list'''
    for i in range(len(wordlist)):
        working = True 
        for j in range(5): 
            if wordlist[i][j] != wordKnowledge[j] and wordKnowledge[j] != '?': 
                working = False
                continue
        if working:
            possWords.append(wordlist[i])
    return possWords



def changeLetters(wordlist, keepLetters):
    '''Function that finds words with known letters (position known or not) and puts them in a keep list'''
    temp = []
    for i in range(len(wordlist)):
        working = True
        for j in range(len(keepLetters)):
            if not wordlist[i].__contains__(keepLetters[j]): #If the letter isn't in the word
                working = False
                continue
        if working:
            temp.append(wordlist[i])
    return temp


def switchPlaces(wordlist, letter, position):
    '''Function that takes letters that are in the word but not in the right position and adds words with the letter in a different position in a keep list'''
    temp = []
    working = False
    for i in range(len(wordlist)):
        if wordlist[i].__contains__(letter):
            working = True
            if wordlist[i][position] == letter:
                working = False
        if working:
            temp.append(wordlist[i])
    return temp

if __name__ == "__main__":
    wordlist = utils.readwords("allwords5.txt")
    print(f"AI: 'My next choice would be {makeguess(wordlist)}'")