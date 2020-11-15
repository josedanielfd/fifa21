from time import sleep
from random import randint
import random

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
        print("Starting sniping bot...")

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

        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'icon-transfer')))
        self.driver.find_element(By.CLASS_NAME, 'icon-transfer').click()

        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ut-tile-transfer-market')))
        sleep(random.randint(1,20)/10)
        self.driver.find_element(By.CLASS_NAME, 'ut-tile-transfer-market').click()

    def relist_transfer_list(self):
        WebDriverWait(self.driver, 12).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'icon-transfer')))
        self.driver.find_element(By.CLASS_NAME, 'icon-transfer').click()
        sleep(random.randint(1,20)/10)

        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ut-tile-transfer-list')))
        self.driver.find_element(By.CLASS_NAME, 'ut-tile-transfer-list').click()
        sleep(random.randint(1,20)/10)

        self.driver.find_element_by_xpath('//button[text()="Re-list All"]').click()
        sleep(random.randint(1,20)/10)

        self.driver.find_element_by_xpath('//span[text()="Yes"]').click()
        #self.driver.find_element(By.XPATH, '//div[contains(@class,"view-modal-container")]//button').click()

        return

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
            self.bid_consumable()

        except TimeoutException:
            print("Error, check the browser")

    def bid_consumable(self):
        resultSet = self.driver.find_element_by_xpath("//ul[@class='paginated']")
        listings = resultSet.find_elements_by_xpath("//li[contains(@class, 'has-auction-data')]")
        print("Number of listings: ", len(listings))
        print(listings[0].get_attribute("class"))

        for element in listings:
            'auctionValue'
            start_price = element.find_element_by_xpath("//div[contains(@class, 'auctionValue')][2] and .//div[contains(@class,'currency-coins value')]")
            print(start_price.text)

        return