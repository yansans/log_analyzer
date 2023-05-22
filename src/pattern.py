import re

def KMP(pattern: str, text: str) -> int:
    """
    KMP algorithm for pattern searching in a text
    return index of pattern in text if found else -1
    """
    # Preprocessing
    lps = border_function(pattern) # longest prefix suffix

    # Searching
    i = 0
    j = 0
    while i < len(text) and j < len(pattern):
        if text[i] == pattern[j]: # if match
            # continue next character
            i += 1
            j += 1
        else: # if not match
            if j != 0: # if not at the beginning of pattern
                j = lps[j - 1] # jump to the last prefix
            else:
                i += 1 # continue next character

    if j == len(pattern): # if found
        return i - j 
    else: # if not found
        return -1

def border_function(pattern: str) -> list:
    """
    Preprocesses pattern for KMP algorithm
    """
    lps = [0] * len(pattern) # init all length of prefix suffix to 0
    i = 1
    j = 0
    while i < len(pattern):
        if pattern[i] == pattern[j]: # if match
            lps[i] = j + 1 # set length of prefix suffix
            # continue next character
            i += 1
            j += 1
        else: # if not match
            if j != 0: # if not at the beginning of pattern
                j = lps[j - 1] # jump to the last prefix
            else: 
                lps[i] = 0 # set length of prefix suffix to 0
                i += 1 # continue next character
    return lps

def BM(pattern: str, text: str) -> int:
    """
    BM algorithm for pattern searching in a text
    return index of pattern in text if found else -1
    """
    # Preprocessing
    last = last_occurance(pattern) # last occurance of each character in pattern

    # Searching
    i = len(pattern) - 1
    j = len(pattern) - 1
    while i < len(text):
        if text[i] == pattern[j]: # if match
            if j == 0: # if found
                return i 
            else: # if not found
                # continue before character
                i -= 1 
                j -= 1
        else:
            # jump to the last occurance of character in pattern or move to the right of pattern once
            i += len(pattern) - min(j, 1 + last[ord(text[i])])
            j = len(pattern) - 1 # reset j to the end of pattern

    return -1

def last_occurance(pattern: str) -> list:
    """
    Preprocesses pattern for BM algorithm
    """
    last = [-1] * 256 # init all (ASCII) last occurance to -1
    for i in range(len(pattern)):
        last[ord(pattern[i])] = i # set last occurance of character in pattern
    return last

def regex(pattern: str, text: str) -> int:
    """
    Regex algorithm for pattern searching in a text
    return index of pattern in text if found else -1
    """
    # search for pattern in text with case insensitive
    match = re.search(pattern, text, re.IGNORECASE) 
    if match:
        return match.start()
    else:
        return -1


if __name__ == "__main__":
    text = "Aug  1 18:30:24 knight sshd[20484]: Failed password for root from 218.49.183.17 port 54078 ssh2"
    pattern = "Failed password for"
    print(KMP(pattern, text))

    text = "Aug Failed password for knight sshd[20488]: Illegal user test from 218.49.183.17"
    pattern = "Failed password for"
    print(BM(pattern, text))
