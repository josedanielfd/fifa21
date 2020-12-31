from bot import Bot
import argparse
from time import sleep
import utils.utils as utils

def get_args():

    parser = argparse.ArgumentParser(description='Bot Parameters', conflict_handler='resolve')
    parser.add_argument('--login_manually', dest='login_manually', action='store_true', default=True)
    parser.add_argument('--existing_session', dest='existing_session', action='store_true', default=False)

    return parser.parse_args()

if __name__ == '__main__':
    print("-----------------------------------------")
    args = get_args()
    login_manually = args.login_manually
    print("Login Manually: ", login_manually)
    existing_session = args.existing_session
    print("Existing Session: ", existing_session)

    bot = Bot(existing_session)
    if not existing_session:
        if login_manually:
            utils.login_manually(bot.driver)
            print("Login Manually Finished")
        else:
            USER = "X"
            utils.login(bot.driver, USER)
    else:
        pass

    items_transferlist, sold_items = bot.relist_transfer_list()
    #available_listings = 100 - (int(items_transferlist) - sold_items)

    # If sold Items is greater than zero go to market and buy shadow
    '''
    if available_listings > 0:
        print("Sold Items: ", 100-available_listings)
        bot.buy_autions("Consumable", "SHADOW", 2300)
'''
    #bot.buy_player(PLAYER["name"], PLAYER["cost"])
    # bot.bid_on_autions(item_type="Consumable" 
    #                     ,item="SHADOW", 
    #                     max_price=2200, 
    #                     number_desired_items=available_listings)


