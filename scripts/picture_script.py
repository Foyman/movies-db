import urllib
import os
import requests
import shutil
from lxml import etree

def getMoviePic(link, name):
    request = requests.get('https://en.wikipedia.org'+ link)
    document = etree.fromstring(request.text)
    #wiki_image = document.xpath('//table[@class="infobox vevent"]/tr/td/a/@href')
    wiki_image = document.xpath('//table[@class="infobox vevent"]/tr/td/a/img/@src')
    #htmlDoc = html.fromstring(request.text)
    image_url = 'https:' + wiki_image[0]
    print(image_url)

    # response = requests.session().get(image_url, stream = True)
    # if response.status_code == 200:
    # with open(name, 'wb') as f:
    #     for chunk in response.iter_content(1024):
    #         f.write(chunk)

    image = requests.get(image_url, stream = True)
    if image.status_code == requests.codes.ok:
        with open(name, 'wb') as image_file:
            shutil.copyfileobj(image.raw, image_file)
            print("Done with %s" % name)
    else:
        print("ERROR with %s" % name)

    return

#Main
retval = os.getcwd()
print ("Current working directory %s" % retval)
r = requests.get('https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture')
doc = etree.fromstring(r.text)
#movies = doc.xpath('//table[@class="wikitable"]//tr/td[1][not(@rowspan)]//a') #all?
links =  doc.xpath('//table[@class="wikitable"]//tr/td[1][not(@rowspan)]//a/@href')
for i in range(len(links)):
    index = i + 1
    os.chdir('/home/senior/movie-db/python_webapp/moviesite/movies/static/images')
    name = str(index) + '.jpg'
    movieInfo = getMoviePic(links[i], name)
