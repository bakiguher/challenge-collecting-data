from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import re

f = open("property.txt", "a")

mainUrl = 'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page=1&orderBy=relevance'

# Opens up the connection and gets the html page from it
uClient = uReq(mainUrl)
pageHtml = uClient.read()

# Closes the connection
uClient.close()

pageSoup = soup(pageHtml.decode('utf-8', 'ignore'), 'html.parser')


allURLs = []

for row in allRows:
    if row.find('tr', attrs={'style': 'height: 46px;'}):
        continue
    cells = row.findAll('td')
    for cell in cells:
        href = cell.find('a')
        if href is None:
            continue
        allURLs.append(str(href.get('href')))