"""
Title: 			All_Words.py
Date:  			4/18/24
Author:  		Vincent Bertolino
Language:		Python 	Version: 3.10.12
Description:    Makes a dict of all words from all version files .
"""

import os
import re
import pickle

#   set file path

path = ("//home//catdaddy//Documents//CCSU//DATA532//Project//DataSets")
dir_list = os.listdir(path)

#   read each bible file in the directory, record the sequence of books read,
#   then record words found with their frequency by bible file read.

whichBook = {}
allWords = {}
countr = 0
zeroWordList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

for file in dir_list:
    book = path + "//" + file
    countr += 1
    with open(book, 'r') as f:
        text = f.read()

        #   record the version read in sequence to a dictionary

        key = countr
        whichBook[key] = file

        #   clear the text of punctuation

        cleanedText = re.sub(r'[.,\'"-_;’:?!()|“”‘§\n]+',' ', text)

        #   add new words to dictionary

        wordList = re.findall(r'\w+', cleanedText)
        for word in wordList:
            if word not in allWords.keys():
                allWords[word] = zeroWordList

#   Save dictionaries for next steps

with open('allWords.pkl', 'wb') as f:
    pickle.dump(allWords, f)

with open('whichBook.pkl', 'wb') as f:
    pickle.dump(whichBook, f)
