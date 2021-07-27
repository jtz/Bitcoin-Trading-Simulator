# -*- coding: utf-8 -*-
"""
Jingtian Zou
Class: CS 521 - Fall 1
Date: 10/20/2020
Final Project - Part2 - BitcoinPrice Class
"""

import requests
from datetime import datetime

# get the API URL for Bitcoin price data
API_URL = "https://min-api.cryptocompare.com/data/price"

class BitcoinPrice():
    """Get current datetime and bitcoin price."""
    
    def __init__(self, datetime="", price=0):
        self.current_date = datetime
        self.current_price = price
    
    def __repr__(self):
        return ("\ncurrent datetime: {}, current price: ${}."
                .format(self.current_date, self.current_price))
        
    def get_current_datetime(self):
        """Get a formatted current datetime through datetime module."""
        # .strftime(): format datetime object to string in specified format
        self.current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.current_date

    def get_current_price(self):
        """Request a current bitcoin price from API."""
        # set what kind of cryptocurrency and its unit to get
        parameters = {"fsym":"BTC", "tsyms":"USD"}
        self.current_price = requests.get(API_URL, parameters).json()["USD"]
        return self.current_price
    
              
# unit test
if __name__ == "__main__": 
    
    bp = BitcoinPrice()    
    # test if get_current_datetime() returns a datetime formatted string 
    # .strptime(): parse (convert) string to datetime object
    assert datetime.strptime(bp.get_current_datetime(),("%Y-%m-%d %H:%M:%S")),\
                                                  "Failed to get the datetime."   
    # test if get_current_price() returns a float
    assert float(bp.get_current_price()), "Failed to get the bitcoin price."
    
    # check the accuracy of the datetime and the price by eyes 
    print(bp.__repr__())

    print("\nBitcoinPrice Class Tests All Passed!")
    
