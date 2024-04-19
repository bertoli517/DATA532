"""
Title: 			Basic_Stats.py
Date:  			4/17/24
Author:  		Vincent Bertolino
Language:		Python 	Version: 3.10.12
Description:    Basic statistics on text files in a directory
Requires:       PyQT5
"""

import os
import re
import statistics
import matplotlib.pyplot as plt

#   set file path

path = ("//home//catdaddy//Documents//CCSU//DATA532//Project//DataSets")
dir_list = os.listdir(path)

#   read each bible file in the directory and add stats to a dictionary

bookStats = {}
plotWords = {}
plotMeans = {}
plotVariance = {}
plotSDv = {}

for file in dir_list:
    book = path + "//" + file
    with open(book, 'r') as f:
        text = f.read()

        #   clear the text of punctuation

        cleanedText = re.sub(r'[.,\'"-_;’:?!()|“”‘§\n]+',' ', text)

        #   compute stats and add dictionary entry

        nWords = len(cleanedText.split())
        data = []
        for word in cleanedText.split():
            data.append(len(word))

        #   z-score on four-letter words

        z = (4-statistics.mean(data))/statistics.stdev(data)
        key = file
        bookStats[key] = nWords, statistics.mean(data), statistics.variance(data), statistics.stdev(data), z

#   generate outputs

countr = 0
for key in bookStats:

    #   print the stats table in table 1

    print(key, bookStats[key])

    data = bookStats.__getitem__(key)
    countr += 1
    plotWords[countr] = data[0]
    plotMeans[countr] = data[1]
    plotVariance[countr] = data[2]
    plotSDv[countr] = data[3]

#   Plot Statistics in a bar graph

plt.bar(*zip(*plotWords.items()))
plt.show()
plt.bar(*zip(*plotMeans.items()))
plt.show()
plt.bar(*zip(*plotVariance.items()))
plt.show()
plt.bar(*zip(*plotSDv.items()))
plt.show()
