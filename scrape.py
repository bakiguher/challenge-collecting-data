import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from dataclasses import dataclass


driver = webdriver.Chrome(executable_path="chromedriver.exe")


class HouseData:
    link: str
    price: str  # float
    adress = str  # post code and municipality
    type_of_property = str  # enum    from url 5th one when we split
    subtype_of_property = str  # enum   WE DONT HAVE THIS
    number_of_rooms = str  # int
    area = str  # float
    fully_equipped_kitchen = str  # yes no (no data) int
    furnished = str  # int yes no no data
    open_fire = str
    terrace = str
    terrace_area = str
    garden = str
    garden_area = str
    surface_land = str
    surface_plot_land = str
    number_of_facades = str
    swimmin_pool = str
    state_of_building = str


ur = 'https://www.immoweb.be/en/classified/house/for-sale/merelbeke/9820/9768055?searchId=621c996e4790f'


def scrape_house1(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    h_data = HouseData()
    h_data.link = url

    _a = url.split('/')

    # type of property

    # FIND THE PRICE

    _alldata = soup.find("div", attrs={"class": "container-main-content"}).find(
        "script", attrs={"type": "text/javascript"}).text.strip()

    d = _alldata.replace('window.classified =', '')
    e = d.replace(';', '')

    data = json.loads(e)  # python dictionary

    # price= e[0]['price']['mainValue']
    print(data["price"]["mainValue"])
    h_data.price = data["price"]["mainValue"]
    h_data.adress = data["property"]["location"]["postalCode"] + \
        "/" + data["property"]["location"]["locality"]
    h_data.type_of_property = data["property"]["type"]
    h_data.subtype_of_property = data["property"]["subtype"]
    h_data.number_of_rooms = data["property"]["bedroomCount"]
    h_data.area = data["property"]["land"]["surface"]
    h_data.fully_equipped_kitchen = data["property"]["kitchen"]["type"]





    print(h_data.__dict__)

    # js = json.dumps(data)

    # print(js)

    # TODO read data from data dict and put in in to class

    # with open('json_data.txt', 'w') as outfile:
    #     json.dump(data, outfile)

    driver.close()


scrape_house1(ur)


# 1 :   from 1 to 350 we are going every page and getting links of the properties    X 350   times thread
#           try catch, 20 pages to each thread save the urls in to a file with append (a)
# 2:    we have 350 X 30 urls now
# 3:    scrape_house1(url)
#
#


def bringpages(start, end):
    links = []
    for i in range(start, end):
        urlmain = 'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page='
        page_nr = str(i) + "&orderBy=relevance"
        url = (
            urlmain + page_nr
        )
        time.sleep(
            2
        )

        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        for elem in soup.find_all("a", attrs={"class": "card__title-link"}):
            links.append(elem.get("href"))
    # write in to a file maybe
    return links


def starteverything():
    # 1 to 20 call bringpages
    for i in range(1, 33):

        pass
