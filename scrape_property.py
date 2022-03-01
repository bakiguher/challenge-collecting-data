from selenium import webdriver
from selenium.webdriver import FirefoxOptions

from threading import Thread, RLock
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import csv


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

    def __str__(self):
        return iter([self.link, self.price, self.adress, self.type_of_property, self.subtype_of_property, self.number_of_rooms,
                    self.area, self.fully_equipped_kitchen, self.open_fire, self.terrace, self.terrace_area, self.garden, self.garden_area,
                    self.surface_land, self.surface_plot_land, self.number_of_facades, self.swimming_pool, self.isnewly_built])


ur = 'https://www.immoweb.be/en/classified/house/for-sale/merelbeke/9820/9768055?searchId=621c996e4790f'


class SyncThread(Thread):
    def __init__(self, k, l, urls):
        Thread.__init__(self)
        self.k = k
        self.l = l
        self.urls = urls

    def run(self):

        
        for url in self.urls:
            options = FirefoxOptions()
            options.add_argument("--headless")

            driver = webdriver.Firefox(options=options)
        
            #try:

            driver.get(url)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            _alldata = soup.find("div", attrs={"class": "container-main-content"}).find(
                "script", attrs={"type": "text/javascript"}).text.strip()

            d = _alldata.replace('window.classified =', '')
            e = d.replace(';', '')

            data = json.loads(e)  # python dictionary

            # TODO read data from data dict and put in in to list
            _h = []
            _h.append(url)
            _h.append(data["id"])
            _h.append(data["price"]["mainValue"])
            _h.append(data["property"]["location"]["postalCode"] +
                        "/" + data["property"]["location"]["locality"])
            _h.append(data["property"]["type"])
            _h.append(data["property"]["subtype"])
            _h.append(data["property"]["bedroomCount"])
            _h.append(data["property"]["land"]["surface"])
            _h.append(data["property"]["kitchen"]["type"])
            _h.append(data["property"]["fireplaceExists"])
            _h.append(data["property"]["hasTerrace"])
            _h.append(data["property"]["terraceSurface"])
            _h.append(data["property"]["hasGarden"])
            _h.append(data["property"]["gardenSurface"])
            _h.append(data["property"]["land"]["surface"])
            _h.append(data["property"]["netHabitableSurface"])
            _h.append(data["property"]["building"]["facadeCount"])
            _h.append(data["property"]["hasSwimmingPool"])
            _h.append(data["flags"]["isNewlyBuilt"])

            # print(_h)

            # append list to csv
            with open(str(self.k) + "_" + str(self.l) + '_prop.csv', 'a', newline='') as f:
                write = csv.writer(f)
                write.writerow(_h)

            driver.close()
            
            # except:
            #     pass


def get_urls():
    lines = []
    with open("unique_urls.txt") as file:
        for line in file:
            line = line.strip()
            lines.append(line)
    return lines


u_urls = get_urls()

# print(u_urls[0])
# print(u_urls[1])
# b = 12


# 18 threads each one has 1000 urls

def starteverything(a: list):
    # 18 threads each has 1000 pages 

    k = 1
    l = 32

    for i in range(1, 19):  # 18 threads last one
        # bringpages(k,l)
        t = 0

        threadx = SyncThread(k, l, a[t:t+100])
        try:

            threadx.start()
        except:
            
            pass
        print(k, "/", l)
        k = l+1
        l = l+32+1
        t = t+10


starteverything(u_urls)


# starteverything()
# starteverything2()


#taskkill /F /IM Firefox.exe /T

