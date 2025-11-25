#!/usr/bin/python3
import sys
# This function uses the index of coincidence(what is the probability of picking two identical letters like 'aa' from the cipher text).
# This test is used to quantify how well the ciphertext 'fits' into columns.
# More specifically, this function uses the index of coincidence on each column and then gets the mean of all of the columns' index of coincidence
# Ex:
# ciphertext = ABCDEFGHI
# columns of two: AB
#                 CD
#                 EF
#                 ..
#The column number that gets a index of coindicence close to .067 is likely the number describing the length of the secret key
def keyLength(text):
    coincidenceList = []
    textlength = len(text)

    for columns in range(1,15): #goes from 1 -> 14 so that even 2 & 13 can have a delta with numbers on either side of them
        columnLen = textlength/columns
        coincidenceSum = 0

        for i in range(0,columns):
            ciphertextColumn=""

            for x in range(i,textlength,columns): #find the letters that go into specific column by stepping by the columns
                ciphertextColumn+= text[x:x+1]
            letterFreq = {} #stores how many times a letter occured in the ciphertextColumn

            for letter in ciphertextColumn:
                if letter in letterFreq:
                    letterFreq[letter] += 1
                else:
                    letterFreq[letter] = 1
            columnLenLessOne = columnLen-1
            coincidence = sum([ ( (letterFreq[key]/columnLen) * ((letterFreq[key]-1)/ columnLenLessOne) ) for key in letterFreq.keys()]) # calculating the index of coincidence for certain column arrangment
            coincidenceSum += coincidence
        coincidenceList.append(coincidenceSum/columns) #adding the mean index of coincidence for certain column arrangment
    
    for index in range(0,len(coincidenceList),2):
        currentCoincidence = coincidenceList[index]
        futureCoincidence = coincidenceList[index+1]
        delta = (futureCoincidence - currentCoincidence) ** 2 # squared becasue only the magnitude maters
        if(delta > .0002):
            # if the mean index of coincidence is above .06 and there was a noticable delta then that is probably the length of the secret key. For a secret key of 5, the mean index of coincidence will spike at 5 and multipules of 5
            if(futureCoincidence >= .06):
                return (index+2)
            elif(currentCoincidence >= .06):
                return (index+1)
# This function preforms a Ceaser cipher decryption of text
# IMPORTANT this function only accepts ONE CHAR for arg. key
def decrypt(text,key,letterToNum,numToLetter):
    return ''.join( [ numToLetter[ ((letterToNum[letter] - letterToNum[key]) % 26) + 1 ] for letter in text] )

# This function  takes ciphertext as the argument and then preforms three main staps:
# 1. Find Secret Length by calling keyLength
# 2. break ciphertext input columns and call decrypt(text) to run Ceaser cipher on columns
# 3. Find the Ceaser cipher keys that create the best corolation using the Chi-square test and put all of these one character keys together to form the secret key
def findKey(text):
    RELATIVE_FEQ = { "a": .08167, "b": .01492, "c": .02782, "d": .04253, "e": .12702, "f": .02228,
    "g": .02015, "h": .06094, "i": .06996, "j": .00153, "k": .00772, "l": .04025,
    "m": .02406, "n": .06749, "o": .07507, "p": .01929, "q": .00095, "r": .05987,
    "s": .06327, "t": .09056, "u": .02758, "v": .00978, "w": .02360, "x": .00150,
    "y": .01974, "z": .00074 }
    #################################################### For calling decrypt
    text = text.lower() # Critical inorder to avoid conflicts between upper and lower case letters
    letters = "abcdefghijklmnopqrstuvwxyz"
    letterToNum = {}
    numToLetter = {}
    count = 1

    for letter in letters:
        letterToNum[letter] = count
        numToLetter[count] = letter
        count+=1
    #################################################### For calling decrypt
    textlength = len(text)
    columns = keyLength(text)
    columnLen = textlength/columns
    finalKey = ""

    for col in range(0,columns):
        corolationColumnList = []

        for letterIndex in range(1,27):
            ciphertextColumn = ""

            for x in range(col,textlength,columns):
                ciphertextColumn+= text[x:x+1]
            columnDecrypt = decrypt(ciphertextColumn,numToLetter[letterIndex],letterToNum,numToLetter)
            letterFreq = {}

            for x in columnDecrypt:
                if x in letterFreq:
                    letterFreq[x] += 1
                else:
                    letterFreq[x] = 1
            totalCorolation = 0

            for key in letterFreq.keys():
                totalCorolation += (letterFreq[key]/columnLen) * RELATIVE_FEQ[key]
                    # Using the idea of multiplying observed by actual frequency of occurance for english letters
                    # This rewards matches between high-freq. letters in english and cipher text
                    # The largest sum means that all the largest peaks like the frequency of 'e' matched
            corolationColumnList.append(totalCorolation)
        highest = 0
        part = ""

        for index in range(0,26):
            if(corolationColumnList[index] > highest):
                part = numToLetter[index+1]
                highest = corolationColumnList[index]
        finalKey+=part
    print(finalKey.upper())

if __name__ == "__main__":
    # Read ciphertext from stdin
    # Ignore line breaks and spaces, convert to all upper case
    #print("Enter Text Here. Press CTRL+D When Finished.")
    cipher = sys.stdin.read().replace("\n", "").replace(" ", "")
    findKey(cipher)

    #################################################################
    # Your code to determine the key and decrypt the ciphertext here
