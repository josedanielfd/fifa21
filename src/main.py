from bot import Bot
from config import USER, PLAYER, LOGIN_MANUALLY

bot = Bot()
"""
if LOGIN_MANUALLY:
    bot.login_manually()
    print("Login Manually Finished")
else:
    bot.login(USER)
"""

#bot.buy_player(PLAYER["name"], PLAYER["cost"])
#bot.buy_consumable('shadow', 2100)
bot.relist_transfer_list()


