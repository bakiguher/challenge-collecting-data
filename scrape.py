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
    surface_land = str
    surface_plot_land = str
    number_of_facades = str
    swimmin_pool = str
    state_of_building = str
    swimming_pool = str
    isnewly_built = str


ur = 'https://www.immoweb.be/en/classified/house/for-sale/merelbeke/9820/9768055?searchId=621c996e4790f'
def scrape_house1(url):
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


