
#Import Modules
import praw
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from praw.models import MoreComments 
from selenium import webdriver
import time
import copy

#Parse historical Daily Discussions (1/3)
#Load driver
parent_url = 'https://www.reddit.com/r/CryptoCurrency/search/?q=daily%20discussion&restrict_sr=1&sr_nsfw='
chrome_path = chrome_driver_path
driver = webdriver.Chrome(chome_path)
driver.get(parent_url)
time.sleep(60) #This sleep is to allow you to manually scroll down the page and obtain links
hist_soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()


#Parse historical Daily Discussions (2/3)
#Obtain Historical DD Links
hist_container = hist_soup.find('div', class_='QBfRw7Rj8UkxybFpX-USO')
hist_heads = hist_container.find_all('a', href=True)

#Add Links to List
url_list = []
for head in hist_heads:
    grab_href = head.get('href')
    if 'http' in grab_href:
        url_list.append(grab_href)


#Parse historical Daily Discussions (3/3)
#Make copy of original list
link_list = copy.deepcopy(url_list)

for url in link_list:
    if '/daily_discussion' not in url or 'megathread_december_15_2018/' in url:
        link_list.remove(url)

#Remove duplicates and sort
link_list = list(set(link_list))
link_list.sort()

#Check retrieved links
print(len(link_list))
for url in link_list:
    print(url)

#Parse Daily Discussion Links 
'''
This should be used to grab links of DDs not included in the historical grab. 
'''
parent_url = 'https://www.reddit.com/r/CryptoCurrency/search/?q=daily%20discussion&restrict_sr=1&sr_nsfw='
r = requests.get(parent_url)

#Parse Daily Discussion link
soup = BeautifulSoup(r.content, 'html.parser')
container = soup.find('div', class_='QBfRw7Rj8UkxybFpX-USO')
heads = container.find_all('a', href=True)

#Add Links to List
dd_list = []
for head in heads:
    grab_href = head.get('href')
    if 'http' in grab_href:
        dd_list.append(grab_href)


#Top Coins by Marketcap
class Coin:
    #Coin instance to track names and aliases
    def __init__(self, name, alias):
        self.name = name
        self.alias = alias

#Define Coins
coin0 = Coin('bitcoin', 'btc')
coin1 = Coin('ethereum', 'eth')
coin2 = Coin('solana', 'sol')
coin3 = Coin('cardano', 'ada')
coin4 = Coin('xrp', 'xrp')
coin5 = Coin('terra', 'luna')
coin6 = Coin('polkadot', 'dot')
coin7 = Coin('avalanche', 'avax')
coin8 = Coin('dogecoin', 'doge')
coin9 = Coin('shiba', 'shib')
coin_list = [coin0, coin1, coin2, coin3, coin4, coin5, coin6, coin7, coin8, coin9]

#Scrape CoinMarketCap for daily price and top 10 coins via webdriver grab the data
coin_url = 'https://coinmarketcap.com/'
driver = webdriver.Chrome(chrome_driver_path)
driver.get(coin_url)
time.sleep(15) #Scroll down the page during this sleep
coin_soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()
coin_tag = coin_soup.find('div', class_ = 'h7vnx2-1 bFzXgL').find('tbody').find_all('tr') #All coins are in a <tr> tag

#Create main dataframe
#Determine how many weeks were grabbed during hist_dd parse
day_dict = {}
count = 0

#Create Day Dict
for link in link_list:
    grab = (link.split('_discussion_')[1]).split('_gmt')[0].replace('_', ' ').title()
    day_dict[grab] = {} #Create dictionary within day_dict for {coin.name : count}
    for coin in coin_list:  #Loop through coin_list to assign coin.name as a key 
        day_dict[grab][(coin.name).title()] = count

#Connect PRAW Agent
reddit_read_only = praw.Reddit(client_id="7x_7QVnkR6nS4tvF7nC9_Q",
                    client_secret="YyzTlh9gNBliHn2QQG8iMBG5WBkCTw",
                    user_agent="Lando Scraping") #Hide sensitive information if you place this on github

#Scrape Comments from Daily Discussion Links
#Reddit utilizes JS to load more comments as you scroll down. Let's utilize PRAW to scrape comments

i = 0
for grab in day_dict:
    submission = reddit_read_only.submission(url = link_list[i])
    for coin in coin_list:
        count = 0
        for comment in submission.comments:
            if type(comment) == MoreComments:
                submission.comments.replace_more(limit = 0)
                for comment in submission.comments.list():
                    if coin.name in comment.body.lower() or coin.alias in comment.body.lower():
                        count+=1
            elif coin.name in comment.body.lower() or coin.alias in comment.body.lower():
                count+=1
        day_dict[grab][(coin.name).title()] = count                
    i+=1                


#Create 'Total' row in day_dict
for grab in day_dict:
    day_dict[grab]['Total'] = sum(day_dict[grab].values())

#Create save copy of day_dict
day_dict_save = copy.deepcopy(day_dict)

#Create averages in day_dict
for grab in day_dict:
    for coin in coin_list:
        day_dict[grab][str((coin.name).title()) + ' Avg'] = int(day_dict[grab][(coin.name).title()])/day_dict[grab]['Total']

#Create Dataframe
pd.options.display.float_format = "{:,.2f}".format 
df = pd.DataFrame(day_dict)
df.sort_index(axis=0,ascending=True, inplace = True) 

#Reindex df
df = df.reindex([df.index[0], df.index[1], df.index[2], df.index[3], df.index[4], df.index[5],
           df.index[6], df.index[7], df.index[8], df.index[9], df.index[10], df.index[11], 
           df.index[12],df.index[13], df.index[14], df.index[15], df.index[16], df.index[17],
           df.index[19], df.index[20], df.index[18]], axis = 0)

#Save dataframe to excel
df.to_excel(save_path, sheet_name = 'Daily Tracker')