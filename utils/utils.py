from time import sleep
import platform
import os
import yaml
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# common tools
from utils import email_manager

def create_driver(existing_session=True):
    system = platform.system()

    if system == 'Darwin':
        path = '/Users/cognistx2019/Documents/GitHub/fifa21/chrome_mac/chromedriver'
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
        
        # New session
        executor_url = driver.command_executor._url
        print(executor_url)
        session_id = driver.session_id
        print(session_id)

        # Save Params of new session
        config_dict = read_yaml_configs()
        config_dict['executor_url'] = executor_url
        config_dict['session_id'] = session_id
        write_yaml_configs(config_dict)
    else:
        
        config_dict = read_yaml_configs()
        executor_url = config_dict['executor_url']
        session_id = config_dict['session_id']
        driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        driver.session_id = session_id

    return driver

def read_yaml_configs():
    with open('/Users/cognistx2019/Documents/GitHub/fifa21/utils/config.yaml') as f:
            yaml_config = yaml.safe_load(f)
    return yaml_config

def write_yaml_configs(dict_file):
    with open(r'/Users/cognistx2019/Documents/GitHub/fifa21/utils/config.yaml', 'w') as file:
        documents = yaml.dump(dict_file, file)
    return

def get_coins(driver):
    coins = int(driver.find_element(By.CLASS_NAME, 'view-navbar-currency-coins').text.replace(" ", "").replace(",", ""))
    return coins

def login(driver, user):
    go_to_login_page(driver)

    driver.find_element(By.ID, 'email').send_keys(user["email"])
    driver.find_element(By.ID, 'password').send_keys(user["password"])
    driver.find_element(By.ID, 'btnLogin').click()

    btn_send = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, 'btnSendCode')))
    driver.implicitly_wait(random.randint(5,10)/10)
    btn_send.click()

    access_code = email_manager.get_access_code()

    driver.find_element(By.ID, 'oneTimeCode').send_keys(access_code)
    driver.find_element(By.ID, 'btnSubmit').click()

    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'icon-transfer'))
    )
    sleep(random.randint(1,30)/10)

def login_manually(driver):
    sleep(3)
    go_to_login_page(driver)

    print("Enter your account credentials and click login button.")
    print("Waiting 5 minutes...")

    WebDriverWait(driver, 300).until(
        EC.element_to_be_clickable((By.ID, 'btnSendCode'))
    ).click()

    print("Provide EA access code and click submit button.")
    print("Waiting 5 minutes...")

    # WebDriverWait(driver, 300).until(
    #     EC.visibility_of_element_located((By.CLASS_NAME, 'icon-transfer'))
    # )
    # sleep(random.randint(1,30)/10)
    return

def go_to_login_page(driver):
    login_page = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@class="ut-login-content"]//button')))
    print("Logging in...")
    sleep(random.randint(1,30)/10)
    login_page.click()

    email_id = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'email')))
    driver.implicitly_wait(random.randint(5,20)/10)
    email_id.click()
    return

def go_to_transfers(driver):
    
    try:
        driver.implicitly_wait(random.randint(30,60)/10)
        transfers = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'icon-transfer')))
        driver.find_element(By.CLASS_NAME, 'icon-transfer')
        driver.implicitly_wait(random.randint(7,20)/10)
        transfers.click()
    except:
        print("Transfers not reachable at first")
        driver.implicitly_wait(8)
        transfers = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'icon-transfer')))
        driver.find_element(By.CLASS_NAME, 'icon-transfer')
        driver.implicitly_wait(random.randint(7,20)/10)
        transfers.click()

    return driver

#TODO make follwing 3 funcitons into one
def go_to_transfer_market(driver):
    """
        From Transfers
    """
    try:
        driver.implicitly_wait(random.randint(30,60)/10)
        transfer_market = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ut-tile-transfer-market')))
        driver.implicitly_wait(random.randint(5,20)/10)
        transfer_market.click()
    except:
        print("Transfer Market not reachable")
    return driver


def go_to_transfer_lists(driver):
    """
        From Transfers
    """

    try:
        driver.implicitly_wait(random.randint(30,60)/10)
        transfer_list = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ut-tile-transfer-list')))
        driver.implicitly_wait(random.randint(10,20)/10)
        transfer_list.click()
    except:
        print("Transfer List not Reacchable at first")
        driver.implicitly_wait(10)
        transfer_list = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ut-tile-transfer-list')))
        driver.implicitly_wait(random.randint(10,20)/10)
        transfer_list.click()
    return driver

def go_to_transfer_targets(driver):
    """
        From Transfers
    """

    try:
        driver.implicitly_wait(random.randint(30,60)/10)
        transfer_targets = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ut-tile-transfer-targets')))
        driver.implicitly_wait(random.randint(10,20)/10)
        transfer_targets.click()
    except:
        print("Transfer List not Reacchable at first")
        driver.implicitly_wait(10)
        transfer_targets = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ut-tile-transfer-targets')))
        driver.implicitly_wait(random.randint(10,20)/10)
        transfer_targets.click()
    return driver

def wait_for_shield_invisibility(driver, duration=0.25):
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, 'ut-click-shield showing interaction'))
    )
    sleep(duration)

def clean_characters(name):
    name = (
        name.lower().
        replace("á","a").
        replace("à","a").
        replace("ä","a").
        replace("ã","a").
        replace("å","a").
        replace("é","e").
        replace("ë","e").
        replace("è","e").
        replace("ě","e").
        replace("ē","e").
        replace("í","i").
        replace("ì","i").
        replace("ó","o").
        replace("ö","o").
        replace("ø","o").
        replace("ú","u").
        replace("ñ","n").
        replace("ü","u").
        replace("ę","e").
        replace("ć","c").
        replace("č","c").        
        replace("š","s").
        replace("ž","z").
        replace("ç","c").
        replace("ý","c").        
        replace("  "," ").
        strip() 
    )
    return name