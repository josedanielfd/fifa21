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

from email_manager import get_access_code
import time

from utils import utils

def search_player(driver, player, max_price, INCREASE_COUNT):
    count = 1
    success_count = 0
    coins = utils.get_coins(driver)
    print("Number of coins: " + coins)

    while int(coins) >= max_price and success_count < 5:
        sleep(random.randint(50,100)/10)
        if count % INCREASE_COUNT == 0:
            min_price_input = driver.find_element(By.XPATH, '(//input[contains(@class, "numericInput")])[3]')
            min_price_input.click()
            sleep(0.05)
            min_price_input.send_keys(1000)

        driver.find_element(By.XPATH, '(//*[@class="button-container"]/button)[2]').click()
        result = WebDriverWait(driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, 'no-results-icon') or
                                                                d.find_elements(By.CLASS_NAME, 'DetailView'))[0]

        if "DetailView" in result.get_attribute("class"):
            coins = utils.get_coins(driver)

            try:
                driver.find_element(By.XPATH, '//button[contains(@class, "buyButton")]').click()
            except WebDriverException:
                utils.wait_for_shield_invisibility(driver, 0.1)
                driver.find_element(By.XPATH, '//button[contains(@class, "buyButton")]').click()

            driver.find_element(By.XPATH, '//div[contains(@class,"view-modal-container")]//button').click()

            sleep(0.5)

            new_coins = utils.get_coins(driver)

            if coins == new_coins:
                print("Found something, but it was too late.")
            else:
                price = coins - new_coins
                print("Success! You bought " + player + " for " + str(price) + " coins.")
                coins = new_coins
                success_count += 1

        try:
            driver.find_element(By.XPATH, '//button[contains(@class, "ut-navigation-button-control")]').click()
        except WebDriverException:
            utils.wait_for_shield_invisibility(driver, 0.1)
            driver.find_element(By.XPATH, '//button[contains(@class, "ut-navigation-button-control")]').click()

        inc_max_price_button = driver.find_element(By.XPATH, '(//div[@class="price-filter"]//button)[6]')

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '(//div[@class="price-filter"]//button)[6]'))
        )

        utils.wait_for_shield_invisibility(driver)

        inc_max_price_button.click()

        count += 1

    if success_count == 15:
        print("You bought 15 players. Assign them and rerun the bot.")
    else:
        print("You have no coins for more players.")

def buy_player(driver, player, max_price, INCREASE_COUNT):
    try:
        utils.go_to_transfer_market(driver)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'ut-player-search-control'))
        )
        utils.wait_for_shield_invisibility(driver)

        driver.find_element(By.XPATH, '//div[contains(@class, "ut-player-search-control")]//input').click()
        sleep(0.1)
        driver.find_element(By.XPATH, '//div[contains(@class, "ut-player-search-control")]//input').send_keys(player)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//ul[contains(@class, "playerResultsList")]/button'))
        )
        sleep(1)

        driver.find_element(By.XPATH, '//ul[contains(@class, "playerResultsList")]/button').click()

        driver.find_element(By.XPATH, '(//input[@class="numericInput"])[4]').click()
        sleep(0.1)
        driver.find_element(By.XPATH, '(//input[@class="numericInput"])[4]').send_keys(max_price)

        print("Looking for " + player + " with max price " + str(max_price) + "...")

        search_player(driver, player, max_price, INCREASE_COUNT)

    except TimeoutException:
        print("Error, check the browser")