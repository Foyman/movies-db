from lxml import etree, html
import requests
import csv
import time
import re

lengthNULL = 0
yearNULL = 0
genreNULL = 0
errorCount = 0
genreList = []

def xstr(s):
    return s if s is not None else str(s)

def checkLength (itemL):
    "This makes sure there is an entry, then shortens it to only the minutes"
    movieLength = 0
    global lengthNULL
    if not itemL:
        movieLength = 0
        lengthNULL += 1
    else:
        contents = xstr(itemL[0].text).split( )
        if(contents[0] == "None"):
            contents[0] = 0
        try:
            movieLength = int(contents[0])
        except ValueError:
            movieLength = 0
            lengthNULL += 1
    return movieLength

def checkYear (itemY):
    "This makes sure there is an entry, then shortens the value to only the year"
    movieYear = 0
    global yearNULL
    if not itemY:
        movieYear = 0
        yearNULL += 1
    else:
        contents = xstr(itemY[0].text).split( )
        try:
            movieYear = int(contents[2])
        except IndexError:
            movieYear = 0
            yearNULL += 1
    return movieYear

def checkWinner(movie_title, doc):
    "This checks if the movie won Best Picture"
    win = 0
    movie = doc.xpath('//table[@class="wikitable"]/tr[@style="background:#FAEB86"]/td/i/b/a[text()="%s"]' % movie_title)
    if movie:
        win = 1
    return win

def findGenre(x):
    "Looks at the word and compares it to the genre table"
    foundGenre = ''
    tempWord = x.lower()
    for i in genreList:
        for j in range(1, len(i)):
            if i[j] in x:
                foundGenre = i[0]
    if foundGenre == "WAR" and x != "war":
            foundGenre = ''
            #print x
    #if foundGenre:
        #print "%s: %s" % (x, foundGenre)
    return foundGenre

def getWords(lineText):
    genres = ""
    words = re.split('-| ', lineText.lower())
    for i in words:
        tempGenre = findGenre(i)
        if tempGenre not in genres:
            if genres and tempGenre:
                genres += "/"
            genres += tempGenre
    return genres

def checkGenre (movie_title, htmlDoc):
    "This gets the movie's genre and prints the results"
    global genreNULL
    global errorCount
    movies_genres = ""
    newText = ''
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
        print err
        errorCount += 1
        pass
    if not movies_genres:
        genreNULL += 1
        movies_genres = "NULL"
        #print "%s%s\n" % (movie_title, newText)
    #else:
        #print "%s %s\n" % (movie_title, movies_genres)
    return movies_genres

def getMovieInfo (movie_title, movie_link, winner):
    "This gets the movie's length and year from its wiki page and prints the results"
    request = requests.get('https://en.wikipedia.org'+ movie_link)
    document = etree.fromstring(request.text)
    htmlDoc = html.fromstring(request.text)

    year = document.xpath('//table[@class="infobox vevent"]/tr[th/div/text()="Release date"]/td/div/ul/li')
    if not year:
        year = document.xpath('//table[@class="infobox vevent"]/tr[th/div/text()="Release date"]/td')

    length = document.xpath('//table[@class="infobox vevent"]/tr[th/div/text()="Running time"]/td/div/ul/li')
    if not length:
        length = document.xpath('//table[@class="infobox vevent"]/tr[th/div/text()="Running time"]/td')

    if isinstance(movie_title, str):
        movie_title = unicode(movie_title, "utf-8")
    resultList = [movie_title.encode('utf-8'), checkYear(year), checkLength(length), checkGenre(movie_title, htmlDoc), winner]
    return resultList

#Main Function
start_time = time.time()

genre_table = open('../text/genres_table.txt', 'r')
for line in genre_table.readlines():
    genreList.append((line.rstrip('\n')).split(','))
genre_table.close()

r = requests.get('https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture')
doc = etree.fromstring(r.text)
movies = doc.xpath('//table[@class="wikitable"]//tr/td[1][not(@rowspan)]//a') #all?
links =  doc.xpath('//table[@class="wikitable"]//tr/td[1][not(@rowspan)]//a/@href')

with open('../csv/best_picture.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Movie', 'Year', 'Length', 'Genre', 'Winner'])
    for i in range(len(movies)):
        movieInfo = getMovieInfo(movies[i].text, links[i], checkWinner(movies[i].text, doc))
        filewriter.writerow(movieInfo)
csvfile.close()

print "DONE"
print "lengthNULL: ", lengthNULL
print "yearNULL: ", yearNULL
print "genreNULL: ", genreNULL
print "errorCount: ", errorCount
print ("--- %s ---" % (time.time() - start_time))
