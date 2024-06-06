"""
Title: 			Basic_Stats.py
Date:  			4/17/24
Author:  		Vincent Bertolino
Language:		Python 	Version: 3.10.12
Description:    Basic statistics on text files in a directory
"""

import os
import re
import csv
import statistics
import matplotlib.pyplot as plt

#   set file path

path = ("C://Users//compaq//Documents//Python Scripts//DATA532-Code//DATA532-Code//data")

dir_list = os.listdir(path)

#   read each bible file in the directory and add stats to a dictionary

bookStats = {}
plotWords = {}
plotMeans = {}
plotVariance = {}
plotSDv = {}

for file in dir_list:
    book = path + "//" + file
    with open(book, 'r', encoding="utf8") as f:
        text = f.read()

        #   clear the text of punctuation, etc.

        cleanedText = re.sub(r'[.,\'"-_;’:?!()|“”‘§\n\d]+',' ', text)

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
    data = bookStats.__getitem__(key)
    countr += 1
    plotWords[countr] = data[0]
    plotMeans[countr] = data[1]
    plotVariance[countr] = data[2]
    plotSDv[countr] = data[3]

#   Plot Statistics in a bar graph

plt.bar(*zip(*plotWords.items()))
plt.xlabel("Words in Each Text")
plt.show()
plt.bar(*zip(*plotMeans.items()))
plt.xlabel("Mean Word Size for Each Text")
plt.show()
plt.bar(*zip(*plotVariance.items()))
plt.xlabel("Variance of Word Size for Each Text")
plt.show()
plt.bar(*zip(*plotSDv.items()))
plt.xlabel("Standard Deviation of Word Size for Each Text")
plt.show()
year = [1866,1881,1901,1901,1769,1965,2010,1889,1890,1961,1752,2006,2001,0000,1599,1995,2003,2005,2006,1989,2010,2020,2016,0000,1982,1996,1913,1833,2020,1889,1989,1895,1984,2014,1924,1992,2002,2008,1534,1530,2017,2014,2013]
means = []
means = list(plotMeans.values())
year.pop(23)
year.pop(13)
year.pop(7)
means.pop(23)
means.pop(13)
means.pop(7)
plt.scatter(year, means)
plt.show()

head = ["Text", "Word Count", "Mean Word Length", "Variance", "STDev", "Z-Score"]

#   save the stats csv 

fields = ['Book', 'Word Count', 'Mean Word Size', 'Variance','STDv'] 
path = ("C://Users//compaq//Documents//Python Scripts//DATA532-Code//DATA532-Code//stats.csv")
with open(path, 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in bookStats.items():
       writer.writerow([key, value])

"""
Title: 			Data532Main.py
Date:  			4/18/24
Author:  		Vincent Bertolino
Language:		Python 	Version: 3.10.12
Description:    Makes a list of unique words in all 48 texts and counts them 
                into a matrix. Calculates the cosine of similarity, sentiment,
                polarity and subjectivity.
                
"""

import os
import re
# import csv
import datetime
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from textblob import TextBlob
from afinn import Afinn

    
#   set file path

path = ("C://Users//compaq//Documents//Python Scripts//DATA532-Code//DATA532-Code//data")
dir_list = os.listdir(path)

#   read each bible file in the directory, record the sequence of books read,
#   then record words found with their frequency by bible file read.

whichBook = {}
allWords = {}
WordList = []

#   get a list of unique words in the 48 texts

nFiles = 43

for file in dir_list:
    book = path + "//" + file
    print(file)
    with open(book, 'r', encoding="utf8") as f:
        text = f.read()
        cleanedText = re.sub(r'[.,\'"-_;’:?!()|“”‘§\n\d]+',' ', text)
        for word in cleanedText.split():
            WordList.append(word)
        
        
WordList = list(set(WordList))

#   Build the term frequency matrix

tf_Matrix = np.zeros((len(WordList), nFiles), dtype = int)
countr = -1
for file in dir_list:
    book = path + "//" + file
    now = datetime.datetime.now()
    print(now)
    print(file)
    with open(book, 'r', encoding="utf8") as f:
        text = f.read()
        countr += 1
        cleanedText = re.sub(r'[.,\'"-_;’:?!()|{}“”‘§\n\d]+',' ', text)
        for n, word in enumerate(WordList):
            tf_Matrix[n,countr] = cleanedText.count(word)
                    
#   Compute and normalize the TF-IDF Matrix

TfIDF_Matrix = np.zeros((len(WordList), nFiles), dtype = float)
for n in range(len(WordList)):
    df = 0
    for m in range(nFiles):
        if tf_Matrix[n,m] > 0: 
            df += 1
            
            
    for m in range(nFiles):   
        TfIDF_Matrix[n,m] = float(tf_Matrix[n,m]) * (1 + np.log(((nFiles +1)/float(df+1))))


TfIDF_Matrix_normed = TfIDF_Matrix / TfIDF_Matrix.max(axis = 0)

#   generate cosine matrix

cosMatrix = np.zeros((nFiles,nFiles),dtype = float)
cosMatrix = cosine_similarity(np.transpose(TfIDF_Matrix_normed))

#   plot cosines

cosLst = []
for i in range(nFiles):
    for j in range(nFiles):
        if cosMatrix[i,j] < 1:
            cosLst.append(cosMatrix[i,j])
            
plt.hist(cosLst, density=True, bins=100)
plt.title("Distribution of Cosines of Similarity")
plt.show()
    
plt.matshow(cosMatrix)
plt.title("Cosine of Similarity Matrix Colormap")
plt.show()

#   Analyze new testaments for sentiment measures

subjectivityData = []
polarityData = []
sentimentData = []
dataLabels = []
year = [1866,1881,1901,1901,1769,1965,2010,1889,1890,1961,1752,2006,2001,0000,1599,1995,2003,2005,2006,1989,2010,2020,2016,0000,1982,1996,1913,1833,2020,1889,1989,1895,1984,2014,1924,1992,2002,2008,1534,1530,2017,2014,2013]

afinn = Afinn()
for file in dir_list:
    book = path + "//" + file
    with open(book, 'r', encoding="utf8") as f:
        text = f.read()
        textSent = TextBlob(text)
        x = textSent.sentiment.subjectivity
        print(x)
        y = textSent.sentiment.polarity
        print(y)
        print(file)
        z = afinn.score(text)
        print(z)
        dataLabels.append(file)
        subjectivityData.append(x)
        polarityData.append(y)
        sentimentData.append(z)

psTitle = "Polarity vs. Subjectivity " + str(len(subjectivityData)) +  " Texts"
plt.scatter(subjectivityData, polarityData)
plt.ylabel("polarity")
plt.xlabel("subjectivity")
plt.title(psTitle)
plt.show()

saTitle = "Sentiment Analysis " + str(len(sentimentData)) +  " Texts"
plt.hist(sentimentData,bins=100)    
plt.title(saTitle)
plt.show()

#   save data to csv table - uncomment and correct the target directory
#   but don't use the data directory as a target
#   also, uncomment import csv

"""
fields = ['Book', 'Polarity', 'Subjectivity', 'Sentiment','Year'] 
path = ("C://Users//compaq//Documents//Python Scripts//DATA532-Code//DATA532-Code//results.csv")
with open(path, 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    for i in range(nFiles):
        write.writerow([dataLabels[i], polarityData[i], subjectivityData[i], sentimentData[i], year[i]])
"""

#   remove two data points where publication date was not known

sentimentData.pop(23)
year.pop(23)
sentimentData.pop(13)
year.pop(13)

svyTitle = "Sentiment vs. Publication Year " + str(len(sentimentData)) +  " Texts"
plt.scatter(sentimentData, year, vmin=1500)
plt.ylabel("Copyright Year")
plt.xlabel("Sentiment")
plt.title(svyTitle)
plt.show()


