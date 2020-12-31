from time import sleep
from random import randint
import random
import pandas as pd
import re
from datetime import datetime

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import time
import numpy as np
from utils import utils as utils
from functions.bidder import bidder
from functions.bidder.bidder import get_current_bid, get_starting_price


def search_player(driver, min_price, max_price):

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'ut-player-search-control'))
    )
    utils.wait_for_shield_invisibility(driver)

    WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Quality"]')))
    driver.find_element_by_xpath('//span[text()="Quality"]').click()
    #'flat ut-search-filter-control--row-button'
    sleep(random.randint(1,20)/10)

    driver.find_element_by_xpath('//li[text()="Gold"]').click()
    sleep(random.randint(1,20)/10)

    # Click to select Rarity
    driver.find_element_by_xpath('//span[text()="Rarity"]').click()
    sleep(random.randint(1,20)/10)

    driver.find_element_by_xpath('//li[text()="Rare"]').click()
    sleep(random.randint(1,20)/10)


    # Min Price
    driver.find_element(By.XPATH, '(//input[@class="numericInput"])[1]').click()
    sleep(random.randint(1,20)/10)
    driver.find_element(By.XPATH, '(//input[@class="numericInput"])[1]').send_keys(min_price)
    sleep(random.randint(1,20)/10)

    # Max Price
    driver.find_element(By.XPATH, '(//input[@class="numericInput"])[2]').click()
    sleep(random.randint(1,20)/10)
    driver.find_element(By.XPATH, '(//input[@class="numericInput"])[2]').send_keys(max_price)
    sleep(random.randint(1,20)/10)

    # Send the search request
    driver.find_element_by_xpath('//button[text()="Search"]').click()

    return

# TODO add buy now options
def snipper_auction(driver, players_type):
    listings = bidder.get_listings_info(driver)
    print("Number of listings: ", len(listings))
    list_bid_prices=[]
    sucessfull_bids = 0

    for element in listings:
        
        auction_current_bid_int = get_current_bid(element)
        auction_initial_price = get_starting_price(element)
        name = utils.clean_characters(element.find_element_by_xpath('.//div[contains(@class, "name")]').text)
        auction_time = element.find_element_by_xpath('.//span[contains(@class, "time")]')
        print("Name: ", name, 
          #  "Starting Price: ",auction_initial_price, 
          #  "Current BID: ", auction_current_bid_int, 
            "Time Left: ", auction_time.text)
        prebid_coins = utils.get_coins(driver)
        
        # Compare with Futbin
        price_condition = compare_futbin(name, max([auction_current_bid_int, auction_initial_price]), players_type)

        # Bid if conditions (Price and Time)
        if price_condition: #and auction_time == '<15 segundos':
            # Lowest default bid
            print("\n***********************")
            print("Make Bid on player: ", name)
            #break
            bidder.make_bid(element, driver)
            
            
            #sleep(random.randint(5,10)/100)
            postbid_coins = utils.get_coins(driver)
            print("Pre Bid Coins: ", prebid_coins)
            print("Post Bid Coins: ", postbid_coins)
            print(postbid_coins-prebid_coins)
    
            if postbid_coins < prebid_coins:
                print("Bid Made: ", prebid_coins - postbid_coins )
                sucessfull_bids += 1
                print("Succesfull BIDS ", sucessfull_bids)
            
            print("*************************\n")
            #sleep(random.randint(15,35)/10)

    return sucessfull_bids

def snipper_accution_execute(driver, players_type='Rare'):
    error_count=0
    sucessfull_bids=0
    # Look in 25 pages
    for i in range(25):
        try:
            sucessfull_bids += snipper_auction(driver, players_type=players_type)
            driver.find_element_by_xpath('//button[text()="Next"]').click()
            sleep(1)
        except:
            print("Error")
            error_count += 1
        
        if error_count > 5:
            break
    return sucessfull_bids

#TODO Check players matching names
def compare_futbin(player, price, players_type):
    # Get futbin data
    futbin_data = load_merge_futbin_catalogue()
    futbin_price = futbin_data.loc[(futbin_data.version==players_type) & (futbin_data.name==player), "price"]
    if len(futbin_price) > 0:
        futbin_price = float(futbin_price.iloc[0])
        print("---------", player, " Price in Futbin :", futbin_price, " Price in FUT: ", price, ' Max Price to BId: ', futbin_price*0.95)
        return futbin_price*0.8 > price
    else:
        print("Not Matched\n")
        return False
    
def load_merge_futbin_catalogue():
    #TODO read files from yaml or generate todays date and load todays file
    futbin_data = pd.read_csv('/Users/cognistx2019/Documents/GitHub/fifa21/data/FutBinCards21_2020_11_23_all.csv')
    catalogue = pd.read_csv('/Users/cognistx2019/Documents/GitHub/fifa21/data/FutBin_catalogue_all.csv')
    futbin_data = futbin_data.merge(catalogue, on='full_name', how='inner')
    return futbin_data