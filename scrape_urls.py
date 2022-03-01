from bs4 import BeautifulSoup
from selenium import webdriver
import time
from threading import Thread
from selenium import webdriver
from selenium.webdriver import FirefoxOptions


class SyncThread(Thread):
    def __init__(self, k, l):
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

            driver1.get(url)
            soup = BeautifulSoup(driver1.page_source, "html.parser")

            for elem in soup.find_all("a", attrs={"class": "card__title-link"}):
                links.append(elem.get("href"))

            with open("apt" + str(self.k) + "-" + str(self.l) + "_url.txt", "a") as textfileurls:
                for element in links:
                    textfileurls.write(element + "\n")
                textfileurls.close()

            driver1.close()


def starteverything():
    # 10 threads each has 32 pages to pick up urls of properties
    k = 1
    l = 32
    for i in range(1, 11):  # 11 last one
        # bringpages(k,l)
        threadx = SyncThread(k, l)
        threadx.start()
        print(k, "/", l)
        k = l+1
        l = l+32+1


starteverything()
