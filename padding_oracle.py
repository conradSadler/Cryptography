import requests
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: %s ORACLE_URL CIPHERTEXT_HEX" % (sys.argv[0]), file=sys.stderr)
        sys.exit(-1)
    oracle_url = sys.argv[1]
    ciphertext = sys.argv[2]
    allPlaintext = []
    blockNum = int(len(ciphertext)/32) -2 # -2 becasue messing with the last block of the ciphertext will not be benifitial 
    with requests.Session() as session:
        for block in range(blockNum,-1,-1): #from blockNum(inclusive) -> -1(exclusive)
            countPadding = 1
            decrypted = []
            plaintext = ""
            lower = block*32
            upper = (block+1)*32
            ciphertextBlock = ciphertext[lower:upper] # getting the substring of 16 bytes
            cipherLen = len(ciphertextBlock)
            for i in range(0,cipherLen,2):
                correctGuess = 0

                for x in range(0,256):
                    guess = str(hex(x)[2:]) #formatting guess into hex which will be inserted into ciphertext
                    if(len(guess) < 2):
                        guess = "0"+guess

                    if(i == 0):
                        ciphertextBlock = ciphertextBlock[:cipherLen-(2)] + guess
                    else:
                        ciphertextBlock = ciphertextBlock[:cipherLen-(i+2)] + guess + ciphertextBlock[cipherLen-i:] #placing the guess inside of the ciphertext block

                    r = session.get("%s?message=%s" % (oracle_url, (ciphertext[:lower]+ciphertextBlock+ciphertext[upper:])))
                    obj = r.json()
                    if(obj['status'] == 'invalid_mac'):
                        correctGuess = x
                        break
                decrypted.append(correctGuess ^ countPadding)
                countPadding+=1
                paddingStr = ""

                for x in range(len(decrypted)-1,-1,-1): # go backwards through list and updating padding for the ciphertext block
                    byte = decrypted[x]
                    modifiedByte = byte ^ countPadding
                    truncatedMB = str(hex(modifiedByte)[2:])
                    if(len(truncatedMB) < 2):
                        truncatedMB = "0"+truncatedMB
                    paddingStr+=truncatedMB

                ciphertextBlock = ciphertextBlock[:cipherLen-(i+2)] + paddingStr #adding updated padding to the ciphertext block
            
            ciphertextCount = 0
            ciphertextBlock = ciphertext[lower:upper]
            ciphertext = ciphertext[:lower]+ciphertextBlock #leaving off the last block/blocks of the original ciphertext. As the ciphertext is decoded, it gets smaller by 16 byte blocks
            decryptedReversed = [decrypted[x] for x in range(len(decrypted)-1,-1,-1)] #reverse the list so that the last element is first
            ciphertextCount = 0

            for x in range(0,len(decryptedReversed)): #performing xor operation with deciphered ciphertext and the prodeeding ciphertext
                
                plaintext+= (int((ciphertextBlock[ciphertextCount:ciphertextCount+1] + ciphertextBlock[ciphertextCount+1:ciphertextCount+2]) ,16 ) ^ decryptedReversed[x]).to_bytes(1,byteorder='big').hex() # ordering bytes in big endian, length = 1 becasue hex byte is constrained to 0 -> 255
                ciphertextCount +=2

            allPlaintext.append(plaintext)
    plaintextString = (''.join([allPlaintext[x] for x in range(len(allPlaintext)-1,-1,-1)])) #reversing the plain text
    
    messageEnd = len(plaintextString)-((int(plaintextString[len(plaintextString)-2:],16) * 2) + 64)
    parsedPlaintext = plaintextString[:messageEnd]
    print(''.join([chr(int(parsedPlaintext[x:x+2],16)) for x in range(0,len(parsedPlaintext),2)]))

