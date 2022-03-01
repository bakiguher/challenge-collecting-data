import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from dataclasses import dataclass
import os
from threading import Thread, RLock
import numpy as np
import glob, os


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


from selenium import webdriver
from selenium.webdriver import FirefoxOptions


def read_txt_files():
    urls=[]
    txtFiles = glob.glob('*.txt')
    for a in txtFiles:
        file1 = open(a, 'r')
        lines = file1.readlines()
        urls.append(lines)
        file1.close()

    return urls        
    #print(txtFiles)

def write_all_urls_to_txt(urlist:list):
    file1 = open("all_urls.txt",'w')
    file1.write(urlist)
    file1.close()
    


class HouseData:
    link: str
    price: str  # float
    adress = str  # post code and municipality
    type_of_property = str  # enum    from url 5th one when we split
    subtype_of_property = str  # enum   WE DONT HAVE THIS
    number_of_rooms = str  # int
    area = str  # float
    fully_equipped_kitchen = str  # yes no (no data) int
    open_fire = str
    terrace = str
    terrace_area = str
    garden = str
    garden_area = str
    surface_land = str
    surface_plot_land = str
    number_of_facades = str
    swimming_pool = str
    isnewly_built = str


ur = 'https://www.immoweb.be/en/classified/house/for-sale/merelbeke/9820/9768055?searchId=621c996e4790f'


def scrape_house1(url):
    options = FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    driver.get(url)


    soup = BeautifulSoup(driver.page_source, "html.parser")

    h_data = HouseData()

    _alldata = soup.find("div", attrs={"class": "container-main-content"}).find(
        "script", attrs={"type": "text/javascript"}).text.strip()

    d = _alldata.replace('window.classified =', '')
    e = d.replace(';', '')

    data = json.loads(e)  # python dictionary

    # TODO read data from data dict and put in in to class

    h_data.link = url
    h_data.price = data["price"]["mainValue"]
    h_data.adress = data["property"]["location"]["postalCode"] + \
        "/" + data["property"]["location"]["locality"]
    h_data.type_of_property = data["property"]["type"]
    h_data.subtype_of_property = data["property"]["subtype"]
    h_data.number_of_rooms = data["property"]["bedroomCount"]
    h_data.area = data["property"]["land"]["surface"]
    h_data.fully_equipped_kitchen = data["property"]["kitchen"]["type"]
    h_data.open_fire = data["property"]["fireplaceExists"]
    h_data.terrace = data["property"]["hasTerrace"]
    h_data.terrace_area = data["property"]["terraceSurface"]
    h_data.garden = data["property"]["hasGarden"]
    h_data.garden_area = data["property"]["gardenSurface"]
    h_data.surface_land = data["property"]["land"]["surface"]
    h_data.surface_plot_land = data["property"]["netHabitableSurface"]
    h_data.number_of_facades = data["property"]["building"]["facadeCount"]
    h_data.swimming_pool = data["property"]["hasSwimmingPool"]
    h_data.isnewly_built = data["flags"]["isNewlyBuilt"]

    print(h_data.__dict__)

    # js = json.dumps(h_data.__dict__)

    with open('json_data1.txt', 'w') as outfile:
        json.dump(data, outfile)

    driver.close()


# scrape_house1(ur)


# 1 :   from 1 to 350 we are going every page and getting links of the properties    X 350   times thread
#           try catch, 20 pages to each thread save the urls in to a file with append (a)
# 2:    we have 350 X 30 urls now
# 3:    scrape_house1(url)
#
#




class SyncThread(Thread):
    def __init__(self,k,l):
        Thread.__init__(self)
        self.k = k
        self.l = l
    def run(self):
        
        for i in range(self.k, self.l):
            links = []
            
            urlmain = 'https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page='
            #urlmain = 'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page='
            
            
            #urlmain = 'https://www.immoweb.be/en/search/house/for-sale?countries=BE&page='
            page_nr = str(i) + "&orderBy=cheapest"
            url = (
                urlmain + page_nr
            )
            time.sleep(
                2
            )

            options = FirefoxOptions()
            driver1 = webdriver.Firefox(options=options)

            # s=Service(ChromeDriverManager().install())
            # driver = webdriver.Chrome(service=s)
            # driver.maximize_window()
           
            # options = webdriver.ChromeOptions()
            # options.add_experimental_option('excludeSwitches', ['enable-logging'])
           
            
            # driver1 = webdriver.Chrome(service=s) # executable_path="c:\dev\chromedriver.exe", options=options, service=Service(ChromeDriverManager().install())
    
            driver1.get(url)
            soup = BeautifulSoup(driver1.page_source, "html.parser")

            for elem in soup.find_all("a", attrs={"class": "card__title-link"}):
                links.append(elem.get("href"))
                #print(elem.get("href"))

            # write in to a file maybe

            
            with open("apt" + str(self.k)+ "-" + str(self.l)+  "_url.txt", "a") as textfileurls:
                for element in links:
                    textfileurls.write(element + "\n")
                textfileurls.close()
        
            driver1.close()

            # with open('json_links.txt', 'w') as outfile:
            #     json.dump(links, outfile)

        # return links









def starteverything():
    # 1 to 20 call bringpages
    k = 1
    l = 32
    for i in range(1, 11):  # 11 last one
        # bringpages(k,l)
        threadx=SyncThread(k,l)
        threadx.start()
        print(k, "/", l)
        k = l+1
        l = l+32+1


starteverything()
