import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains 
import time
from _datetime import datetime
from selenium.webdriver.common.keys import Keys 
import requests
import bs4 
import csv
import re 
import pandas as pd 
import urllib.request
import urllib.parse 
import io 


options = webdriver.ChromeOptions()
options.headless = False
prefs = {"profile.default_content_setting_values.notifications":2}
options.add_experimental_option("prefs",prefs)


driver = webdriver.Chrome('chromedriver.exe',options=options)
driver.maximize_window()
time.sleep(5)

driver.get("https://www.tripadvisor.com")
time.sleep(1)

# Clicking hotel button using Xpath
driver.find_element_by_xpath('//a[@class="_1yB-kafB"][@title="Hotels"]').click()

# Finding search bar on page
search_bar = driver.find_element_by_xpath('//form[@class="R1IsnpX3"]//input[@placeholder="Where to?"]')

# Tried Sending only "delhi" but didn't get desired results
"""
search_bar.send_keys("delhi",Keys.ENTER)
time.sleep(5)
search_bar.send_keys(Keys.ARROW_DOWN)
time.sleep(2)
search_bar.send_keys(Keys.ENTER)
"""

# Send input to search bar and selected suggestion from Auto Suggestion box
search_bar.send_keys("New Delhi National Capital Territory of Delhi")
time.sleep(5)
search_bar.send_keys(Keys.ARROW_DOWN)
time.sleep(2)
search_bar.send_keys(Keys.ENTER)

time.sleep(4)

# Selected hotels button present on page
delhi_hotels = driver.find_element_by_xpath('//a[@title="Hotels"]')
delhi_hotels.click()



time.sleep(2)

# ################  Scraping data  ####################

domain = 'https://www.tripadvisor.com'
data = bs4.BeautifulSoup(driver.page_source,'html.parser')

# XPath for Next page button and Script to move page down
next_page = '//*[@id="taplc_main_pagination_bar_dusty_hotels_resp_0"]//div//div//div//a[text()="Next"]'
page_down = "window.scrollTo(0, 1000);"

# To extract page number list
page_list = range(int(data.find("div", {"class": "pageNumbers"}).find_all("a")[-1].get("data-page-number")))
print("Total number of page: {}".format(len(page_list)))


# Stored data using both csv library and pandas 
with open('./data/url_req.csv', 'a',encoding='utf-8') as csvfile:
    fieldnames = ['hotel_id', 'hotel_name', 'price', 'n_star','no_of_reviews','amenities']

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    df = pd.DataFrame(columns=fieldnames)
    index = 0

    for p in page_list:
        print('the number of page = {0}/{1}'.format(p+1, len(page_list)))
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

        # Finding all the Hotels Card on Page
        hotel_blocks = soup.find_all('div', {"class": "prw_rup prw_meta_hsx_responsive_listing ui_section listItem"})

        # Parsing through every block to collect hotel info
        for element in hotel_blocks:
            index += 1
            # Hotel Name
            hotel_name = element.find('div', {"class": "listing_title"}).text
            hotel_name = hotel_name.lstrip()

            # URL for hotel
            #url = domain+element.find('div', {"class": "listing_title"}).find('a').get('href')

            # Hotel Price
            hotel_price = element.find('div',{"class":"priceBlock"})
            if(hotel_price != None):
                hotel_price = hotel_price.find('div',{"class":"price-wrap"}).find('div',{"class":"price __resizeWatch"}).text
                hotel_price = hotel_price[1:]
            else:
                hotel_price = ""
            
            # Hotel Stars
            n_star = element.find('a', {"data-clicksource":"BubbleRating"})
            if (n_star != None):
                n_star = n_star.attrs['alt']
            else:
                n_star = ""

            # Hotel No. of Reviews
            no_of_reviews = element.find('a',{"data-clicksource":"ReviewCount"})
            if (no_of_reviews != None):
                no_of_reviews = no_of_reviews.text
                no_of_reviews = no_of_reviews[:-8]
            else:
                no_of_reviews = ""
            
            # Hotel Amenities
            amenities = element.find('ul',{"class":"icons_list"})
            if (amenities != None):
                amenities = amenities.find_all('span',{"class":"text"})
            else:
                amenities = ""
            req_amen = []
            if (len(amenities) > 0):
                for i in amenities:
                    req_amen.append(i.text)
            final_amenities = ""
            if (len(req_amen) > 0):
                final_amenities = ", ".join(req_amen)
            
            """Tried to extract image but many came as None
            imgs = element.find('div',{"class":"photo-wrapper"}).find('div',{"data-clicksource":"Photo"}).find('div',{"class":"ZVAUHZqh"}).find('img')
            print(imgs)
            """
            
            writer.writerow(
                            {
                                'hotel_id':index,
                                'hotel_name':hotel_name,
                                'price':hotel_price,
                                'n_star':n_star,
                                'no_of_reviews':no_of_reviews,
                                'amenities':final_amenities
                            }
                            )
            
            df = df.append({
                                'hotel_id':index,
                                'hotel_name':hotel_name,
                                'price':hotel_price,
                                'n_star':n_star,
                                'no_of_reviews':no_of_reviews,
                                'amenities':final_amenities
                            },ignore_index=True)
        
        # Moves page down and detect the Next button to move to the next page
        try:
            driver.execute_script(page_down)
            time.sleep(5)
            driver.find_element_by_xpath(next_page).click()
            time.sleep(8)
        except:
            print('in the end')

    df.to_csv('output.csv') 
driver.quit()