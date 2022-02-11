# Coin_Tracker
Scrapes the amount of mentions on Reddit of the top 10 coins by market cap

## Description
Goal: 
    The goal of this program is to capture the name, alias, and price of the top 10 currencies via https://coinmarketcap.com/. It then searches the Daily Discussion threads within the r/CryptoCurrency subreddit to see how many times the name or alias has been mentioned. The intent is to uncover a correlation between the amount of times a coin was mentioned and how much its price changed in comparison to the other coins.
    
Method:
    • Selenium is used to perform the webscraping.
    • Reddit's PRAW API is utilized to scrape the comments within each Daily Discussion.

This program is broken down into two major sections: 
    • Coin Tracker Historical Grab
        - This program searches the furthest back that Reddit allows you to search its Daily Discussions within r/CryptoCurrency. It creates the original dataframe by taking the top 10 coins on the date that the program is ran and counting how many times the coins are mentioned in each day. 
    • Coin Tracker
        - This takes a previously created dataframe and appends to it. 