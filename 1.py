from mimetypes import init
from bs4 import BeautifulSoup
from selenium import webdriver
import time

for i in range(1, 2):
    page_nr = str(i) + "&orderBy=relevance"
    url = (
        "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=" +page_nr
    )
    
    list_of_houses = []  # 30 houses

    #wait a little
    
    time.sleep(
        10
    )  

    # chrome drv add
    driver = webdriver.Chrome(executable_path="chromedriver.exe")

    # get the address- 
    driver.get(url)

    # make soup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # listing help us to find all web pages
    listings = soup.find_all("a", class_="card__title-link")
    print(listings)


