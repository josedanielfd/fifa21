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

from utils import utils as utils

def check_if_winning(element):
    return "highest-bid" in element.get_attribute("class")
    
def search_consumable(driver, item, max_price):
    try:
        
        print("Searching for ITEM")
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'ea-filter-bar-item-view'))
        )
        utils.wait_for_shield_invisibility(driver)

        #TODO Handle this issue
        try:
            driver.find_element_by_xpath('//button[text()="Consumables"]').click()
            sleep(random.randint(1,20)/10)
        except:
            # When recent search is done xpath changes text to "seleccted"
            driver.find_element_by_xpath('//button[text()="Players"]').click()
            sleep(random.randint(1,20)/10)
            driver.find_element_by_xpath('//button[text()="Consumables"]').click()
            sleep(random.randint(1,20)/10)

        
        WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Position Change"]')))
        driver.find_element_by_xpath('//span[text()="Position Change"]').click()
        #'flat ut-search-filter-control--row-button'
        sleep(random.randint(1,20)/10)

        driver.find_element_by_xpath('//li[text()="Chemistry Styles"]').click()
        sleep(random.randint(1,20)/10)

        # Click to select Chemistry Style
        driver.find_element_by_xpath('//span[text()="Chemistry Style"]').click()
        sleep(random.randint(1,20)/10)

        driver.find_element_by_xpath('//li[text()="'+item+'"]').click()
        sleep(random.randint(1,20)/10)

        driver.find_element(By.XPATH, '(//input[@class="numericInput"])[2]').click()
        sleep(random.randint(1,20)/10)

        driver.find_element(By.XPATH, '(//input[@class="numericInput"])[2]').send_keys(max_price)
        sleep(random.randint(1,20)/10)

        # Send the search request
        try:
            driver.find_element_by_xpath('//button[text()="Search"]').click()
        except:
            print("Button click not reachable")

        # Check results
        result = WebDriverWait(driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, 'no-results-icon') or
                                                                d.find_elements(By.CLASS_NAME, 'DetailView'))[0]
        print(result)
        return driver

    except TimeoutException:
        print("Error, check the browser")

def bid_consumable(driver, max_price, number_desired_items):
    
    # Get all the listings (Python list)
    listings = get_listings_info(driver)
    print("Number of listings: ", len(listings))
    list_bid_prices=[]
    sucessfull_bids = 0

    for element in listings:
        
        auction_current_bid_int = get_current_bid(element)
        auction_time = element.find_element_by_xpath('.//span[contains(@class, "time")]')
        print("Current BID: ", auction_current_bid_int, "Time Left: ", auction_time.text)
        
        # List of current bid prices
        list_bid_prices.append(auction_current_bid_int)

        # Get coins pre bid
        prebid_coins = utils.get_coins(driver)

        # If bid is less than max price, not expired and not the highest bidder, make a bid
        if auction_current_bid_int < int(max_price) and auction_time != "Expired" and not check_if_winning(element) and (number_desired_items >= sucessfull_bids) and (prebid_coins > int(max_price)):
            
            # Lowest default bid
            make_bid(element, driver)

            sleep(random.randint(5,10)/100)
            postbid_coins = utils.get_coins(driver)
            #print("Post Bid Coins: ", postbid_coins)

            #TODO Does not work properly
            if postbid_coins < prebid_coins:
                print("Bid Made: ", prebid_coins - postbid_coins )
                sucessfull_bids += 1
                print("Succesfull BIDS ", sucessfull_bids)

            sleep(random.randint(15,35)/10)
            
    # TODO click Next page with other conditions (currently almost never changes)
    # If all prices greater or equal than max price, go to next page
    if all(bid >= max_price for bid in list_bid_prices) and (number_desired_items >= sucessfull_bids):
        driver.find_element_by_xpath('//button[text()="Next"]').click()
        print("Went to Next Page")

    return sucessfull_bids

def make_bid(element, driver):
    '''
    Makes the default bid
    '''
    element.click()
    sleep(random.randint(5,20)/10)

    #Click Make Bid
    #print("Pre Bid Coins: ", prebid_coins)
    driver.find_element_by_xpath('//button[text()="Make Bid"]').click()

    return

#TODO check that this works
def buy_now(element, driver):
    '''
    Makes the default bid
    '''
    element.click()
    sleep(random.randint(5,20)/10)

    #Click Make Bid
    #print("Pre Bid Coins: ", prebid_coins)
    driver.find_element_by_xpath('//button[text()="Buy Now"]').click()

    return

def get_listings_info(driver):
    '''
        Get the list of players listed
    '''
    
    resultSet = driver.find_element_by_xpath("//ul[@class='paginated']")
    # Get all the listings (Python list)
    listings = resultSet.find_elements_by_xpath("//li[contains(@class, 'has-auction-data')]")
    
    return listings

def was_bid_successfull(driver):

    return

def get_current_bid(element):
        
    auction_value = element.find_element(By.XPATH, "(.//div[@class='auctionValue'])[1]")
    auction_current_bid = auction_value.find_element_by_xpath('.//span[contains(@class, "currency-coins value")]')
    auction_current_bid_int = int(auction_current_bid.text.replace(" ", "").replace(",", "").replace("---", "0"))
    
    return auction_current_bid_int

def get_starting_price(element):
    auction_value = element.find_element(By.XPATH, "(.//div[@class='auctionStartPrice auctionValue'])")
    auction_starting = auction_value.find_element_by_xpath('.//span[contains(@class, "currency-coins value")]')
    auction_starting_int = int(auction_starting.text.replace(" ", "").replace(",", "").replace("---", "0"))

    return auction_starting_int

def get_rating(element):
    rating = element.find_element_by_xpath('.//div[@class="rating"]').text
    return rating