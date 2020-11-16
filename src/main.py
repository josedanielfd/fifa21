from bot import Bot
from config import USER, PLAYER, LOGIN_MANUALLY
import argparse

def get_args():

    parser = argparse.ArgumentParser(description='Bot Parameters', conflict_handler='resolve')
    parser.add_argument('--login_manually', dest='login_manually', action='store_true', default=True)
    parser.add_argument('--existing_session', dest='existing_session', action='store_true', default=False)

    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    login_manually = args.login_manually
    print("Login Manually: ", login_manually)
    existing_session = args.existing_session
    print("Existing Session: ", existing_session)

    bot = Bot(existing_session)
    if not existing_session:
        if login_manually:
            bot.login_manually()
            print("Login Manually Finished")
        else:
            bot.login(USER)
    else:
        pass

    #To DO: Execute every hour

    #bot.buy_player(PLAYER["name"], PLAYER["cost"])
    bot.search_consumable("SHADOW", 2700)
    #bot.relist_transfer_list()


