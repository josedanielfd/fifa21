from time import sleep
from random import randint
import random
import pandas as pd
import re
import os
from datetime import datetime

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

print(os.getcwd())

import functions.transfer_list as transfer_list
import utils.utils as utils
from functions.bidder import bidder
from functions.bidder import snipper


class Bot:
    def __init__(self, existing_session):
        URL = utils.read_yaml_configs()['URL']

        self.driver = utils.create_driver(existing_session)

        self.action = ActionChains(self.driver)      
        self.driver.get(URL)
        
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("Starting bot...")
        return
    
    def relist_transfer_list(self):

        self.driver = utils.go_to_transfers(self.driver)
        items_transferlist = transfer_list.get_total_transfers(self.driver)
        self.driver = utils.go_to_transfer_lists(self.driver)
        self.driver, sold_items = transfer_list.save_sold_items(self.driver)
        self.driver = transfer_list.relist_expired_items(self.driver)
        if len(sold_items) > 0:
            transfer_list.clear_sold_items(self.driver)
        return items_transferlist, sold_items

    def mass_bid_on_autions(self, item_type, item, max_price, number_desired_items):

        if item_type == 'Consumable':
            print("Buy Consumable")
        
            self.driver = utils.go_to_transfers(self.driver)
            print("Going to Transfer Market..")
            self.driver = utils.go_to_transfer_market(self.driver)
            bidder.search_consumable(self.driver, item, max_price)
            
            # keep bidding until sucessfully make X bids
            successful_bids = 0
            while successful_bids < number_desired_items:
                successful_bids = bidder.bid_consumable(self.driver, max_price, number_desired_items)

        return

    
    def snipper_bid(self, min_price, max_price, ammount_to_invest):
        self.driver = utils.go_to_transfers(self.driver)
        self.driver = utils.go_to_transfer_market(self.driver)
        snipper.search_player(self.driver, min_price, max_price)
        sucessful_bids = 0
        while sucessful_bids < 2 :
            snipper.snipper_auction(self.driver, )
        return

    




