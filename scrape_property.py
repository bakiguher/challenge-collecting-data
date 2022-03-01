from selenium import webdriver
from selenium.webdriver import FirefoxOptions

from threading import Thread, RLock
import json
from bs4 import BeautifulSoup
from selenium import webdriver

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
    options.add_argument("--headless")

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

    with open('json_data1.txt', 'a') as outfile:
        json.dump(h_data.__dict__, outfile)

    driver.close()



scrape_house1(ur)

