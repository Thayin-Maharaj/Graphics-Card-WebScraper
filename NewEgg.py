from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 
from pprint import pprint
import numpy as np
import pandas as pd
import os
import time


def openpage(myurl):
    #Opening connection to NewEgg and grabbing page
    time.sleep(np.random.normal(2, 0.1))
    uClient = uReq(myurl)
    page_html = uClient.read()
    # uClient.close()
    return soup(page_html, "html.parser") #Parser for HTML


def getcontainers(page_soup):
    #grab all the products
    containers = page_soup.findAll("div", {"class":"item-container"})
    title_list = []
    brand_list = []
    is_out_list = []
    for container in containers:
        title_con = container.findAll("a", {"class":"item-title"})
        title = title_con[0].text
        title_list.append(title)

        brand_list.append(container.div.div.a.img["title"])

        try:
            promo_con = container.findAll("p", {"class":"item-promo"})
            if promo_con[0].text == "OUT OF STOCK":
                is_out_list.append(promo_con[0].text)
            else:
                is_out_list.append("IN STOCK")
        except:
            is_out_list.append("IN STOCK")
    
    details = [brand_list, title_list, is_out_list]
    return details  
    

def writedata(data):
    try:
        os.remove("data.csv")
    except:
        pass
    data = pd.DataFrame(data)
    data.to_csv("data.csv", header=None, index=None)


if __name__ == "__main__":
    myurl = "https://www.newegg.com/p/pl?N=100007709%20601357282%20601359511&page="
    # page_soup = openpage(myurl + "1")
    # page_con = page_soup.findAll("div", {"class":"list-tool-pagination"})
    # try:
    #     pagetext = page_con[0].span.strong.text[-1]
    # except:
    #     pagetext = '2'
    
    while True:
        page_soup = openpage(myurl + "1")
        graphics_cards = np.array(getcontainers(page_soup)).transpose()      

        # for i in range(2,int(pagetext)+1):
        #     try:
        #         page_soup = openpage(myurl + "{}".format(i))
        #         cur_page = np.array(getcontainers(page_soup)).transpose()
        #         graphics_cards = np.concatenate((graphics_cards, cur_page))
        #     except:
        #         continue

        writedata(graphics_cards)
        flag = False
        stock_check = []

        for i in range(len(graphics_cards)):
            if graphics_cards[i, 2] == "IN STOCK":
                flag = True
                print("Card:\t" + graphics_cards[i, 1] + "\n" + graphics_cards[i, 2])

        if flag:
            print("Parsed Successfully")
        elif len(graphics_cards) > 1:
            print("ALL OUT OF STOCK")
            time.sleep(1)
            print(len(graphics_cards))
        else:
            print("They found out")
                    


                    