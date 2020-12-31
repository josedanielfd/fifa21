from time import sleep
from random import randint
import numpy as np
import time
import utils.utils as utils
import re
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def get_futbin_data(price_range='20000-50000', max_pages=600):

    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M")

    id = 0
    if price_range != 'all':
        tag_price_range = '&ps_price='+price_range
    else:
        tag_price_range = ''

    FutBin = requests.get('https://www.futbin.com/players?page=1'+tag_price_range, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
    bs = BeautifulSoup(FutBin.text, 'html.parser')
    try:
        TotalPages = str(bs.findAll('li', {'class': 'page-item '})[-1].text).strip()
    except IndexError:
        TotalPages = str(bs.findAll('li', {'class': 'page-item'})[-2].text).strip()
    print('Number of pages to be parsed for FIFA  21 is ' + TotalPages + ' Pages')
    table_players_df = []
    for page in range(1, np.min([int(TotalPages)+1, max_pages])):
        sleep(1.5)
        print("Page: ", page)
        url = 'https://www.futbin.com/players?page=' + str(page) + tag_price_range
        FutBin = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
        print(url)
        bs = BeautifulSoup(FutBin.text, 'html.parser')
        table = (bs.find('table', {'id': 'repTb'}))
        tbody = table.find('tbody')
        extracted = tbody.findAll('tr', {'class': re.compile('player_tr_\d+')})
        
        for cardDetails in extracted:
            
            name = str(cardDetails.text).strip().replace('\n', ' ').split('           ')[0]
            cardDetails = str(cardDetails.text).strip().replace('\n', ' ').replace(' \\ ', '\\').replace(' | ', '|').split('       ')[1]
            cardDetails = re.sub("\w\\\\\w", "", cardDetails)
            cardDetails = re.sub("\w+\|\d\'\d+\"", "", cardDetails)
            revision = re.findall("\s(\D*\s\D+)", cardDetails, re.IGNORECASE)[1].split()[1:]
            cardDetails = re.sub("\s\D*\s\D+", " ", cardDetails)
            cardDetails = cardDetails.split()
            cardDetails.insert(0, name)
            cardDetails.insert(0, id)
            cardDetails.extend([' '.join(revision)])
            table_players_df.append((cardDetails[1], cardDetails[2], cardDetails[3], cardDetails[-1]))
            
        
    df = pd.DataFrame(table_players_df, columns=['full_name','rating','price','version'])
    df['date'] = current_time

    # Cclean names
    df['full_name'] = df.full_name.apply(utils.clean_characters)

    # Clean prices 
    df = to_numeric(df)

    # Remove duplicate players (obsolete)
    df = drop_duplicates(df)

    df.head()
    output_path = '../data/FutBinCards21_'+now.strftime("%Y_%m_%d_%H%M")+"_"+price_range+'.csv'
    df.to_csv(output_path, header=True, sep=',', encoding='utf-8', index=False)
    print("Futbin Saved at: ", output_path)
    return

def to_numeric(data):
    data.price = (
        data.price.apply(lambda v : float(v.replace("K",""))*1000 if "K" in v else float(v.replace("M",""))*1000000 if "M" in v else float(v))
    )
    return data

def drop_duplicates(data):
    data = data.sort_values('price', ascending=True).groupby(['full_name','rating','version']).head(1)
    return data