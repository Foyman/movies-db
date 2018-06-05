from lxml import etree
from lxml import html
import requests
import csv
import time
import re

genreNULL = 0
errorCount = 0
genreList = []

def genreDict(dic_file):
    global genreList
    for line in dic_file.readlines():
        genreList.append((line.rstrip('\n')).split(','))
    return

def checkGenre(x):
    foundGenre = ''
    tempWord = x.lower()
    for i in genreList:
        for j in range(1, len(i)):
            if i[j] in x:
                foundGenre = i[0]
    if foundGenre == "WAR" and x != "war":
            foundGenre = ''
            #print x
    if foundGenre:
        #print "%s: %s" % (x, foundGenre)
    return foundGenre

def getWords(lineText):
    movies_genres = ""
    words = re.split('-| ', lineText.lower())
    for i in words:
        tempGenre = checkGenre(i)
        if tempGenre not in movies_genres:
            if movies_genres and tempGenre:
                movies_genres += "/"
            movies_genres += tempGenre
    return movies_genres

def getMovieInfo (movie_title, movie_link):
    "This gets the movie's genre and prints the results"
    global genreNULL
    global errorCount
    movies_genres = ""
    newText = ''
    request = requests.get('https://en.wikipedia.org'+ movie_link)
    document = etree.fromstring(request.text)
    htmlDoc = html.fromstring(request.text)
    test = htmlDoc.xpath('//div[@class="mw-parser-output"]/p[1]')
    #print test.text_content()
    try:
        text = test[0].text_content().split(movie_title, 1)[1]
        if ')' in text:
            newText = text.split(')', 1)[1]
        for i in range(0,2):
            newText = text.split('.', 1)[i]
            movies_genres = getWords(newText)
            if movies_genres:
                break
    except Exception as err:
        #print err
        errorCount += 1
    if not movies_genres:
        genreNULL += 1
        #print "%s%s\n" % (movie_title, newText)
    else:
        #print "%s %s\n" % (movie_title, movies_genres)
    return movies_genres

#Main Function
start_time = time.time()

#create genre table
genre_table = open('../text/genres_table.txt', 'r')
for line in dic_file.readlines():
    genreList.append((line.rstrip('\n')).split(','))

#connect to wikipedia for movies
r = requests.get('https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture')
doc = etree.fromstring(r.text)
movies = doc.xpath('//table[@class="wikitable"]//tr/td[1][not(@rowspan)]//a') #all?
links =  doc.xpath('//table[@class="wikitable"]//tr/td[1][not(@rowspan)]//a/@href')

for i in range(len(movies)):
    #print "%s %s" % (movies[i].text, getMovieInfo(movies[i].text, links[i]))
    getMovieInfo(movies[i].text, links[i])

print "DONE"
print len(movies)
print "NULL Genres: %s" % (genreNULL)
print "Error Count: %s" % (errorCount)
print ("--- %s ---" % (time.time() - start_time))
