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
    



ur='https://www.immoweb.be/en/classified/house/for-sale/merelbeke/9820/9768055?searchId=621c996e4790f'


# for each house go bring data put this under a thread
def scrape_house(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    
    h_data = HouseData()
    h_data.link=url
    
    # FIND THE PRICE
    for elem in soup.find_all("p", attrs={"class": "classified__price"}):
        for x in elem.find_all("span", attrs={"aria-hidden": "true"}):
            h_data.price=x.text


    #  FIND THE ADRESS   -   classified__information--address-row
    for elem in soup.find_all("span", attrs={"class": "classified__information--address-row"}):
        h_data.adress= elem.text
    



    print(h_data.adress)

    driver.close()

scrape_house(ur)





for i in range(1, 1):

    urlmain='https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page='
    page_nr = str(i) + "&orderBy=relevance"
    url = (
        urlmain + page_nr
    )


    list_of_houses = []  # 30 houses

    # wait a little

    time.sleep(
        2
    )

    # chrome drv add
    

    # get the address-
    driver.get(url)

    # make soup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    links = []
    for elem in soup.find_all("a", attrs={"class": "card__title-link"}):
        links.append(elem.get("href"))
    # print(json.dumps(links))
        scrape_house(elem)
