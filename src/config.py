from selenium import webdriver
import platform
import os
import yaml
import random


def create_driver(existing_session=True):
    system = platform.system()

    if system == 'Darwin':
        path = 'chrome_mac/chromedriver'
    elif system == 'Linux':
        path = 'chrome_linux/chromedriver'
    elif system == 'Windows':
        path = os.getcwd() + '\chrome_windows\chromedriver.exe'
    else:
        raise OSError(f'Operating system {system} is not supported')
    
    if existing_session == False:
        driver = webdriver.Chrome(
            executable_path=path
        )
        driver.maximize_window()
    else:
        
        with open('/Users/cognistx2019/Documents/GitHub/fifa21/config.yaml') as f:
            config_dict = yaml.safe_load(f)
        executor_url = config_dict['executor_url']
        session_id = config_dict['session_id']
        driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        driver.session_id = session_id

    return driver


URL = "https://www.ea.com/en-gb/fifa/ultimate-team/web-app/"

EA_EMAIL = "EA@e.ea.com"

PLAYER = {
    "name": "Kante",
    "cost": 350000,
}

INCREASE_COUNT = 5

LOGIN_MANUALLY = True

# Credentials - fill in if LOGIN_MANUALLY is False

USER = {
    "email": "",
    "password": "",
}

EMAIL_CREDENTIALS = {
    "email": "your_email@example.com",
    "password": "your_password",
}


