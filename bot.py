# -*- coding: utf-8 -*-
# Written by Ibrahim Aderinto

'''
    This program is bot that scrapes data from capitolhills.com and updates status on twitter with the data.
'''

# import system modules
from datetime import datetime

# import third party modules
import requests
import tweepy
from bs4 import BeautifulSoup


def scrape_data():
    '''
        Function to scrape first row of "JUST IN" table (first table) from capitolhills.com

        :arguments: 
            None
        
        :returns:
            data : details of the latest(first) row of "JUST IN" table in the form {Politician name} 
                    purchased/sold {size} of {stock name} {stock symbol} on {transaction date}
    '''

    headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    response = requests.get('https://www.capitoltrades.com/', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    just_in_table = soup.find('ul', class_="q-data-list-root")
    first_row = just_in_table.li

    transaction_type = first_row.span.text
    if transaction_type == 'buy':
        transaction_type = 'purchased'
    else:
        transaction_type = 'sold'

    stock_name = first_row.select('a > div:nth-of-type(2) > div > h3')[0].text
    stock_symbol = first_row.select('a > div:nth-of-type(2) > div > span')[0].text
    if stock_symbol.lower()=='n/a':
        stock_symbol = ''
    else:
        stock_symbol = f'({stock_symbol}) '
    
    buyer = first_row.select('a > div:nth-of-type(3) > h3')[0].text
    size = first_row.select('a > div:nth-of-type(4) > span > div > span')[0].text
    
    data = f'{buyer} {transaction_type} {size} of {stock_name} {stock_symbol}on {datetime.now().date()}'
    return data


def update_status(status):
    '''
        A function to update status on twitter

        :arguments:
            status - the text with which status is to be updated
        
        :returns:
            None
    '''

    consumer_key = 'yOuaqdkBSQxChujXSQMECCv42'
    consumer_secret = 'tpFICXz4jFxTEvmoeg5wajbPMp1u0mvVE1TpfEi5lkgIfa29wI'
    bearer_token = r'AAAAAAAAAAAAAAAAAAAAANaZcQEAAAAAC7vXYH%2FMd2jVM6o9m2viiulxzJ4%3DGx8r\
                    39jkuL7iX4Cq6QQDzzj8Irg7F2LEx80H1mh4Ody9pFj8d7'
    access_token = '1504961633860390926-GJo2Akp2MXRWcTaAMWzTTnVZmUuy9d'
    access_token_secret = 'fuI4nqNGFYt5zCsS3oR4ugpBLIXi2pKRtPtjqVShUvBan'

    client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret, wait_on_rate_limit=True)
    client.create_tweet(text=status)


def main():
    '''
        The main function

        :arguments:
            None
        
        :returns:
            None
    '''

    with open('previous_status.txt') as file:
        previous_status = file.readline().strip()
    
    status = scrape_data()
    status_ = status[:-11]
    if status_ == previous_status:
        return None
    
    update_status(status)
    with open('previous_status.txt', 'w') as file:
        file.write(status_)


if __name__=="__main__":
    main()
