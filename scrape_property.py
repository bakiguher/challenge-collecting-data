from selenium import webdriver
from selenium.webdriver import FirefoxOptions

from threading import Thread
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import csv



'''
    Scraped data structure: 
    url: str
    id: int
    price: float  
    adress : str  # post code and municipality
    type_of_property : str   
    subtype_of_property : str     
    bedroomCount : int  
    land_surface : float
    kitchen_type : string 
    fireplaceExists : bool
    hasTerrace : bool
    terraceSurface : float
    hasGarden : bool
    gardenSurface : float
    surface_land_area : float
    netHabitableSurface : float
    facadeCount : int
    hasSwimmingPool : bool
    isnewly_built : bool
'''


class SyncThread(Thread):
    '''
    Class for threads to scrape properties from immoweb.be
    k : starting file name number
    l: ending file name number
    urls: list containing property urls.
    Firefox webdriver will be used with --headless option so it will not create a browser window request did not work for us
    data is scraped from a javascript object from the web site then converted to a python dictionary.
    Data read from dictionary and put in to a list. But the dictionary did not have some of the values we were looking for. 
    First we tried to check if data is there, but "try except" was a much faster solution.
    Initialasing the driver is also in "try-except" if there is an error it goes to next url.  
   
    '''
    def __init__(self, k:int, l:int, urls:list):
        Thread.__init__(self)
        self.k = k
        self.l = l
        self.urls = urls

    def run(self):

        for url in self.urls:
            options = FirefoxOptions()
            options.add_argument("--headless")

            driver = webdriver.Firefox(options=options)

            # try:
            try:
                driver.get(url)

                soup = BeautifulSoup(driver.page_source, "html.parser")
                
               
                _alldata = soup.find("div", attrs={"class": "container-main-content"}).find(
                    "script", attrs={"type": "text/javascript"}).text.strip()

                _d = _alldata.replace('window.classified =', '')
                _e = _d.replace(';', '')

                data = json.loads(_e)  # python dictionary
                

                _h = []
                _h.append(url)
                _h.append(data["id"])
                _h.append(data["price"]["mainValue"])
                _h.append(data["property"]["location"]["postalCode"] +
                          "/" + data["property"]["location"]["locality"])
                _h.append(data["property"]["type"])
                _h.append(data["property"]["subtype"])
                _h.append(data["property"]["bedroomCount"])

                try:
                    _h.append(data["property"]["land"]["surface"])
                except:
                    _h.append("")

                try:
                    _h.append(data["property"]["kitchen"]["type"])
                except:
                    _h.append("")

                try:
                    _h.append(data["property"]["fireplaceExists"])
                except:
                    _h.append("")

                try:
                    _h.append(data["property"]["hasTerrace"])
                except:
                    _h.append("")
                try:
                    _h.append(data["property"]["terraceSurface"])
                except:
                    _h.append("")
                try:
                    _h.append(data["property"]["hasGarden"])
                except:
                    _h.append("")
                try:
                    _h.append(data["property"]["gardenSurface"])
                except:
                    _h.append("")
                try:
                    _h.append(data["property"]["land"]["surface"])
                except:
                    _h.append("")
                try:
                    _h.append(data["property"]["netHabitableSurface"])
                except:
                    _h.append("")

                try:
                    _h.append(data["property"]["building"]["facadeCount"])
                except:
                    _h.append("")
                try:
                    _h.append(data["property"]["hasSwimmingPool"])
                except:
                    _h.append("")
                try:
                    _h.append(data["flags"]["isNewlyBuilt"])
                except:
                    _h.append("")
                
                
                with open("4-" + str(self.k) + "_" + str(self.l) + '_prop.csv', 'a', newline='') as f:
                    write = csv.writer(f)
                    write.writerow(_h)

                driver.close()
            except:
                pass
            


def get_urls() -> list:
    '''
    Function to get url adresses of each property in to a list
    '''
    lines = []
    with open("./urls/unique_unscraped_urls.txt") as file:
        for line in file:
            line = line.strip()
            lines.append(line)
    return lines


def start_property_scraping(a: list):
    '''
    Function to start the threads;
    20 threads each will take 100 property urls from the list 
    This function will many times we choosed to run with 20 threads and 100 urls each 
    for file naming we used 2 variables:
        start_file_name_k 
        end_file_name_l
    url_count: numbers of url given to thread

    In theory it is expected to scrape 2000 preperties on each run
    After each run "taskkill /F /IM Firefox.exe /T"    command used on terminal to kill Firefox web driver

    '''

    start_file_name_k = 1
    end_file_name_l = 100
    url_count = 0
    for i in range(1, 21):  # 20 threads last one
        # bringpages(k,l)

        threadx = SyncThread(
            start_file_name_k, end_file_name_l, a[url_count:url_count+100])
        threadx.start()

        # print(k, "/", l)
        start_file_name_k = end_file_name_l+1
        end_file_name_l = end_file_name_l + 100 + 1
        url_count = url_count + 100+1


u_urls = get_urls()
start_property_scraping(u_urls)



