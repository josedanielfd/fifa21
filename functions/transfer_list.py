from time import sleep
from random import randint
import random
import pandas as pd
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils import utils as utils
from functions.bidder.bidder import get_current_bid, get_starting_price

def relist_expired_items(driver):
    try:
        driver.implicitly_wait(random.randint(30,60)/10)
        driver.find_element_by_xpath('//button[text()="Re-list All"]').click()
        sleep(random.randint(2,10)/10)
        driver.find_element_by_xpath('//span[text()="Yes"]').click()
    except:
        print("Re list Button Not Clikable")
    return driver

def save_sold_items(driver):
    driver.implicitly_wait(random.randint(30,60)/10)
    # Get current time to save items
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Find container of listings
    # Get players
    player_listings = driver.find_elements_by_xpath(
        "//li[contains(@class, 'has-auction-data won')] | //li[contains(@class, 'has-auction-data seleted won')] | //li[contains(@class, 'has-auction-data chemistryStyle selected won')]")
    print("Number of players: ", len(player_listings))
    
    # Get items
    items_listings = driver.find_elements_by_xpath(
        "//li[contains(@class, 'has-auction-data chemistryStyle won')] | //li[contains(@class, 'has-auction-data selected chemistryStyle won')]")
    print("Number of items: ", len(items_listings))
    
    #Combine players and items
    listings = player_listings+items_listings
    print("Number of listings: ", len(listings))

    list_winner_bids=[]
    for element in listings:
        auction_current_bid_int = get_current_bid(element)
        auction_starting_price = get_starting_price(element)

        # Get name
        name = element.find_element_by_xpath('.//div[contains(@class, "name")]').text

        list_winner_bids.append((name, auction_starting_price, auction_current_bid_int, current_time))
        print("Starting Price: ", auction_starting_price, 
            "Winner BID: ", auction_current_bid_int, 
            " Name: ", name, 
            "Time: ", current_time)

        #TODO get more info of sold elements

    if len(listings) > 0:
        #Load previous Data
        history_sold = pd.read_csv("/Users/cognistx2019/Documents/GitHub/fifa21/Sold_Items/sold_items.csv")

        # Save Items Sold
        print("Saving Data..")
        sold_data = pd.DataFrame(list_winner_bids, columns=['name','starting_price','winner_bid','timestamp'])
        final_data = pd.concat([history_sold,sold_data], axis=0)
        final_data.to_csv("/Users/cognistx2019/Documents/GitHub/fifa21/Sold_Items/sold_items.csv", header=True, index=False)

    else:
        print("No items Sold")
        sold_data = []
    return driver, sold_data

def clear_sold_items(driver):
    try:
        driver.find_element_by_xpath('//button[text()="Clear Sold"]').click()
        print("Cleared Sold Items")
    except:
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//button[text()="Clear Sold"]').click()
        print("Cleared Sold Items")


def get_total_transfers(driver):
    """
        From transfers view
    """
    total_transfers = driver.find_element_by_xpath('//div[contains(@class, "total-transfers")]')
    items = total_transfers.find_element_by_xpath('.//span[contains(@class, "value")]').text
    print("Items in transfer list: ", items)
    return items