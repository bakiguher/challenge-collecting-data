<<<<<<< Updated upstream
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
=======
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from dataclasses import dataclass



driver = webdriver.Chrome(executable_path="chromedriver.exe")


class HouseData:
    link: str
    price: str  #float
    adress= str
    type_of_property=str  #enum
    subtype_of_property=str #enum
    number_of_rooms=str   #int
    area=str       #float
    fully_equipped_kitchen= str #yes no (no data) int  
    furnished=str    #int yes no no data
    open_fire=str
    terrace=str
    terrace_area=str
    garden=str
    garden_area=str
    surface_land=str
    surface_plot_land=str
    number_of_facades=str
    swimmin_pool=str
    state_of_building= str

    
# for each house go bring data put this under a thread
def scrape_house(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    
    h_data = HouseData()
    h_data.link=url

    for elem in soup.find_all("script")[2]:
        print(elem)
>>>>>>> Stashed changes
