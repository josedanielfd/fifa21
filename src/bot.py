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

from config import URL
from config import create_driver, INCREASE_COUNT
from email_manager import get_access_code
from helpers import wait_for_shield_invisibility
import time


class Bot:
    def __init__(self, existing_session):
        self.driver = create_driver(existing_session)
        
        executor_url = self.driver.command_executor._url
        print(executor_url)
        session_id = self.driver.session_id
        print(session_id)

        self.action = ActionChains(self.driver)
        self.driver.get(URL)
        print("Starting bot...")

    def go_to_login_page(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class="ut-login-content"]//button'))
        )
        print("Logging in...")
        sleep(random.randint(1,30)/10)
        self.driver.find_element(By.XPATH, '//*[@class="ut-login-content"]//button').click()

        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.ID, 'email'))
        )

    def login(self, user):
        self.go_to_login_page()

        self.driver.find_element(By.ID, 'email').send_keys(user["email"])
        self.driver.find_element(By.ID, 'password').send_keys(user["password"])
        self.driver.find_element(By.ID, 'btnLogin').click()

        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, 'btnSendCode'))
        ).click()

        access_code = get_access_code()

        self.driver.find_element(By.ID, 'oneTimeCode').send_keys(access_code)
        self.driver.find_element(By.ID, 'btnSubmit').click()

        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'icon-transfer'))
        )
        sleep(random.randint(1,30)/10)

    def login_manually(self):
        self.go_to_login_page()

        print("Enter your account credentials and click login button.")
        print("Waiting 5 minutes...")

        WebDriverWait(self.driver, 300).until(
            EC.element_to_be_clickable((By.ID, 'btnSendCode'))
        ).click()

        print("Provide EA access code and click submit button.")
        print("Waiting 5 minutes...")

        WebDriverWait(self.driver, 300).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'icon-transfer'))
        )
        sleep(random.randint(1,30)/10)

    def go_to_transfer_market(self):
        sleep(random.randint(5,20)/10)

        try:
            WebDriverWait(self.driver, 35).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'icon-transfer')))
            self.driver.find_element(By.CLASS_NAME, 'icon-transfer').click()
        except:
            sleep(random.randint(10,30)/10)
            WebDriverWait(self.driver, 35).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'icon-transfer')))
            self.driver.find_element(By.CLASS_NAME, 'icon-transfer').click()

        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ut-tile-transfer-market')))
        sleep(random.randint(1,20)/10)
        self.driver.find_element(By.CLASS_NAME, 'ut-tile-transfer-market').click()

    def relist_transfer_list(self):
        sleep(random.randint(1,20)/10)

        try:
            WebDriverWait(self.driver, 35).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'icon-transfer')))
            self.driver.find_element(By.CLASS_NAME, 'icon-transfer').click()
        except:
            sleep(random.randint(20,60)/10)
            WebDriverWait(self.driver, 35).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'icon-transfer')))
            self.driver.find_element(By.CLASS_NAME, 'icon-transfer').click()

        try:
            sleep(random.randint(5,10)/10)
            WebDriverWait(self.driver, 25).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'ut-tile-transfer-list')))
            self.driver.find_element(By.CLASS_NAME, 'ut-tile-transfer-list').click()
            sleep(random.randint(5,20)/10)
        except:
            sleep(random.randint(20,50)/10)
            WebDriverWait(self.driver, 25).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'ut-tile-transfer-list')))
            self.driver.find_element(By.CLASS_NAME, 'ut-tile-transfer-list').click()
            sleep(random.randint(1,20)/10)

        try:
            self.driver.find_element_by_xpath('//button[text()="Re-list All"]').click()
            sleep(random.randint(2,10)/10)
            self.driver.find_element_by_xpath('//span[text()="Yes"]').click()
        except:
            print("Re list Button Not Clikable")

        # Clear Sold Items and save them
        self.save_sold_items()

        return

    def save_sold_items(self):
        
        # Get current time to save items
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Find container of listings
        # TODO unselect first elment (otherwise is not considered)
        
        # Get players
        player_listings = self.driver.find_elements_by_xpath("//li[contains(@class, 'has-auction-data won')]")
        print("Number of players: ", len(player_listings))
        
        # Get items
        items_listings = self.driver.find_elements_by_xpath("//li[contains(@class, 'has-auction-data chemistryStyle won')]")
        print("Number of items: ", len(items_listings))
        
        #Combine players and items
        listings = player_listings+items_listings
        print("Number of listings: ", len(listings))

        list_winner_bids=[]
        for element in listings:
            auction_current_bid_int = self.get_current_bid(element)

            # Get name
            name = element.find_element_by_xpath('.//div[contains(@class, "name")]').text

            list_winner_bids.append(("winner_bid", name, auction_current_bid_int, current_time))
            print("Winner BID: ", auction_current_bid_int, " Name: ", name, "Time: ", current_time)

            #TODO get more info of sold elements

        if len(listings) > 0:
            # Save Items Sold
            print("Saving Data..")
            sold_data = pd.DataFrame(list_winner_bids, columns=['bids','name','winner_bid','time_stamp'])
            sold_data.to_csv("/Users/cognistx2019/Documents/GitHub/fifa21/Sold_Items/sold_items.csv", mode='a', header=False, index=False)

            # Clear Sold ITEMS
            self.driver.find_element_by_xpath('//button[text()="Clear Sold"]').click()
            print("Cleared Sold Items")
        else:
            print("No items Sold")
        return

    def get_current_bid(self, element):
        
        auction_value = element.find_element(By.XPATH, "(.//div[@class='auctionValue'])[1]")
        auction_current_bid = auction_value.find_element_by_xpath('.//span[contains(@class, "currency-coins value")]')
        auction_current_bid_int = int(auction_current_bid.text.replace(" ", "").replace(",", "").replace("---", "0"))
        
        return auction_current_bid_int


    def get_coins(self):
        coins = int(self.driver.find_element(By.CLASS_NAME, 'view-navbar-currency-coins').text.replace(" ", "").replace(",", ""))
        return coins

    def search_player(self, player, max_price):
        count = 1
        success_count = 0
        coins = self.get_coins()
        print("Number of coins: " + coins)

        while int(coins) >= max_price and success_count < 5:
            sleep(random.randint(50,100)/10)
            if count % INCREASE_COUNT == 0:
                min_price_input = self.driver.find_element(By.XPATH, '(//input[contains(@class, "numericInput")])[3]')
                min_price_input.click()
                sleep(0.05)
                min_price_input.send_keys(1000)

            self.driver.find_element(By.XPATH, '(//*[@class="button-container"]/button)[2]').click()
            result = WebDriverWait(self.driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, 'no-results-icon') or
                                                                    d.find_elements(By.CLASS_NAME, 'DetailView'))[0]

            if "DetailView" in result.get_attribute("class"):
                coins = self.get_coins()

                try:
                    self.driver.find_element(By.XPATH, '//button[contains(@class, "buyButton")]').click()
                except WebDriverException:
                    wait_for_shield_invisibility(self.driver, 0.1)
                    self.driver.find_element(By.XPATH, '//button[contains(@class, "buyButton")]').click()

                self.driver.find_element(By.XPATH, '//div[contains(@class,"view-modal-container")]//button').click()

                sleep(0.5)

                new_coins = self.get_coins()

                if coins == new_coins:
                    print("Found something, but it was too late.")
                else:
                    price = coins - new_coins
                    print("Success! You bought " + player + " for " + str(price) + " coins.")
                    coins = new_coins
                    success_count += 1

            try:
                self.driver.find_element(By.XPATH, '//button[contains(@class, "ut-navigation-button-control")]').click()
            except WebDriverException:
                wait_for_shield_invisibility(self.driver, 0.1)
                self.driver.find_element(By.XPATH, '//button[contains(@class, "ut-navigation-button-control")]').click()

            inc_max_price_button = self.driver.find_element(By.XPATH, '(//div[@class="price-filter"]//button)[6]')

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '(//div[@class="price-filter"]//button)[6]'))
            )

            wait_for_shield_invisibility(self.driver)

            inc_max_price_button.click()

            count += 1

        if success_count == 15:
            print("You bought 15 players. Assign them and rerun the bot.")
        else:
            print("You have no coins for more players.")

    def buy_player(self, player, max_price):
        try:
            self.go_to_transfer_market()

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'ut-player-search-control'))
            )
            wait_for_shield_invisibility(self.driver)

            self.driver.find_element(By.XPATH, '//div[contains(@class, "ut-player-search-control")]//input').click()
            sleep(0.1)
            self.driver.find_element(By.XPATH, '//div[contains(@class, "ut-player-search-control")]//input').send_keys(player)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//ul[contains(@class, "playerResultsList")]/button'))
            )
            sleep(1)

            self.driver.find_element(By.XPATH, '//ul[contains(@class, "playerResultsList")]/button').click()

            self.driver.find_element(By.XPATH, '(//input[@class="numericInput"])[4]').click()
            sleep(0.1)
            self.driver.find_element(By.XPATH, '(//input[@class="numericInput"])[4]').send_keys(max_price)

            print("Looking for " + player + " with max price " + str(max_price) + "...")

            self.search_player(player, max_price)

        except TimeoutException:
            print("Error, check the browser")


    def search_consumable(self, item, max_price):
        try:
            print("Buy Consumable")
            print("Going to Transfer Market..")
            self.go_to_transfer_market()

            print("Searching for ITEM")
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'ea-filter-bar-item-view'))
            )
            wait_for_shield_invisibility(self.driver)
    
            self.driver.find_element_by_xpath('//button[text()="Consumables"]').click()
            sleep(random.randint(1,20)/10)
            
            WebDriverWait(self.driver, 12).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Position Change"]')))
            self.driver.find_element_by_xpath('//span[text()="Position Change"]').click()
            #'flat ut-search-filter-control--row-button'
            sleep(random.randint(1,20)/10)

            self.driver.find_element_by_xpath('//li[text()="Chemistry Styles"]').click()
            sleep(random.randint(1,20)/10)

            # Click to select Chemistry Style
            self.driver.find_element_by_xpath('//span[text()="Chemistry Style"]').click()
            sleep(random.randint(1,20)/10)

            self.driver.find_element_by_xpath('//li[text()="'+item+'"]').click()
            sleep(random.randint(1,20)/10)

            self.driver.find_element(By.XPATH, '(//input[@class="numericInput"])[2]').click()
            sleep(random.randint(1,20)/10)

            self.driver.find_element(By.XPATH, '(//input[@class="numericInput"])[2]').send_keys(max_price)
            sleep(random.randint(1,20)/10)

            # Send the search request
            self.driver.find_element_by_xpath('//button[text()="Search"]').click()

            # Check results
            result = WebDriverWait(self.driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, 'no-results-icon') or
                                                                    d.find_elements(By.CLASS_NAME, 'DetailView'))[0]
            print(result)

            #Bid on consumable
            for i in range(10):
                self.bid_consumable(max_price)
                sleep(random.randint(1,10)/10)

        except TimeoutException:
            print("Error, check the browser")

    def bid_consumable(self, max_price):
        
        # Find container of listings
        resultSet = self.driver.find_element_by_xpath("//ul[@class='paginated']")
        # Get all the listings (Python list)
        listings = resultSet.find_elements_by_xpath("//li[contains(@class, 'has-auction-data')]")
        print("Number of listings: ", len(listings))
        list_bid_prices=[]

        for element in listings:
            auction_current_bid_int = self.get_current_bid(element)
            auction_time = element.find_element_by_xpath('.//span[contains(@class, "time")]')
            print("Current BID: ", auction_current_bid_int, "Time Left: ", auction_time.text)
            
            list_bid_prices.append(auction_current_bid_int)

            # If bid is less than max price, not expired and not the highest bidder, make a bid
            if auction_current_bid_int < int(max_price) and auction_time != "Expired" and not self.check_if_winning(element):
                element.click()
                sleep(random.randint(5,20)/10)

                #Click Make Bid
                self.driver.find_element_by_xpath('//button[text()="Make Bid"]').click()
                sleep(random.randint(15,35)/10)
                print("Bid Made: ", auction_current_bid_int+100)
        
        # If all prices greater or equal than max price, go to next page
        if all(bid >= max_price for bid in list_bid_prices):
            self.driver.find_element_by_xpath('//button[text()="Next"]').click()
            print("Went to Next Page")

        return

    def check_if_winning(self, element):
        return "highest-bid" in element.get_attribute("class")