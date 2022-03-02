from bs4 import BeautifulSoup
from selenium import webdriver
import time
from threading import Thread
from selenium import webdriver
from selenium.webdriver import FirefoxOptions




class SyncThread(Thread):
    '''
    Class for threads to scrape urls from immoweb.be
    k : starting url page number
    l: ending page number
    urlmain: 1st one is for houses in the second run it will be changed to appartments
    ---Because of immoweb returning same properties most of the time we choosed to sort the pages according to price, also many 
        duplicates have been found, probably those were paid advertisements 
    '''
    def __init__(self, k, l):
        Thread.__init__(self)
        self.k = k
        self.l = l

    def run(self):

        for i in range(self.k, self.l):
            links = []

            #   urls for house and apartments  in second run dont forget to change 
            urlmain = 'https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page='
            #urlmain = 'https://www.immoweb.be/en/search/house/for-sale?countries=BE&page='
            
            page_nr = str(i) + "&orderBy=cheapest"
            url = (
                urlmain + page_nr
            )

            #In between connection to web site deliberately 10 second wait time to awaid getting kicked out 
            time.sleep(
                10
            )

            options = FirefoxOptions()
            # did not use any options scrapind did not take too much time for urls neither too much memory or cpu power
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


def start_url_scraping():
    '''
    Function to start the threads;
    10 threads each will take 32 page numbers from immoweb web site in total 320 pages will be scraped for urls of properties
    This function will run 2 times
    1 - for sales houses
    2 - for sale apartments
    In theory it is expected to scrape 18600 preperty urls
    '''
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


start_url_scraping()
