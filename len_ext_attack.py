#!/usr/bin/python3

import sys
from urllib.parse import quote, urlparse
from pymd5 import md5, padding

#MD5(secret 8-byte password || the portion of the URL starting from the first command= )

if __name__ == '__main__':
    if len(sys.argv) < 2: #sys.argv will always have one item which is the programs name
        print(f"usage: {sys.argv[0]} URL_TO_EXTEND", file=sys.stderr)
        sys.exit(-1)

    # Get url from command line argument (argv)

    url = sys.argv[1]
    res = urlparse(url)
    firstCommand = res.query.find("&")
    token = (res.query[6:firstCommand])
    tokenLen = 8 + len(res.query[firstCommand+1:]) # The secret password may be different than in the examples, but it will always be 8 bytes long, The plus one is to remove the & so that the string starts from "command="
    lenBytes = ( len(padding((tokenLen) * 8)) + (tokenLen)) #account for bytes from original message as well as original message padding
    h = md5(state = bytes.fromhex(token), count = lenBytes * 8)
    h.update("&command=UnlockSafes") ##Important
    modifiedToken = h.hexdigest()
    print(url[:url.find("token=") + 6] + modifiedToken + res.query[firstCommand:] + quote(padding((tokenLen*8))) + "&command=UnlockSafes") #"&command=UnlockSafes" needs to be added on last
    sys.exit(0) #successful termination
    #Token is invalid or does not match the given commands
    #Enter Url with quotes so that the shell does not mistake '&' for a special character