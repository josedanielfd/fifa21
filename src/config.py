from selenium import webdriver
import platform
import os


def create_driver(existing_session=True, executor_url="http://127.0.0.1:53471", session_id="e10bcc396efebf58e92f2236c719fac8"):
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


