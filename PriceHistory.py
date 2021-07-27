# -*- coding: utf-8 -*-
"""
Jingtian Zou
Class: CS 521 - Fall 1
Date: 10/20/2020
Final Project - Part3 - PriceHistory Class
"""

import pandas as pd
import mplfinance as mpf
from datetime import datetime

PRICE_HISTORY_FILE = "BTC-USD.csv"

class PriceHistory():
    """Show data and chart for one_day price and a period of prices history."""
    
    def __init__(self, date="", start="", end=""):
        self.__one_day = date
        self.__period_start = start 
        self.__period_end = end
    
    def __repr__(self):
        return ("valid input one day: {} \n"
                "valid input a period: {} - {} \n"
                "one day price history: {} \n"
                "a period price history: {}"                
               .format(self.__one_day, self.__period_start, self.__period_end,\
                        self.get_historical_price("one date"),\
                        self.get_historical_price("time period")))
          
    def get_one_day(self):
        """Prompt for a valid date."""
        while True:
            # prompt user to input one date
            one_day = input("The avaiable historical price is from 2014-09-17"
                             " to 2020-10-20 except 2020-08-04.\n"
                             "Please enter the date as 'YYYY-MM-DD': ")
            
            # check if input is a valid datetime in required format
            try:
                # convert string to datetime object
                one_day = datetime.strptime(one_day.strip(), "%Y-%m-%d")
            except ValueError:
                print("Error: You must enter a reasonable date in the "
                      "required format.")
                continue
            
            # check if input equal 2020-08-04 of which data is unavailable
            if one_day == datetime.strptime("2020-08-04", "%Y-%m-%d"):
                print("Error: The price history on 2020-08-04 is unavailable.")
                continue      
            
            # check if input in the range of availble dates
            if not datetime.strptime("2014-09-17", "%Y-%m-%d") <= one_day\
                <= datetime.strptime("2020-10-20", "%Y-%m-%d"):
                print("Error: The date is out of available range.")
                continue                
            else:
                self.__one_day = one_day.date()  # get only date
                return self.__one_day
                break
            
    def get_a_period(self):
        """Prompt for a valid period of time."""       
        while True:
            # prompt user to input time period
            a_period = input("The avaiable historical price is from "
                                "2014-09-17 to 2020-10-20 except 2020-08-04.\n"
                                "Please enter a period of time as "
                                "'YYYY-MM-DD,YYYY-MM-DD': ")
            # start validate input
            try:
                start, end = a_period.strip().split(",")
            except ValueError:
                print("Error: you must enter twos dates split by comma.")
                continue            
            
            # check if input are valid datetimes in required format
            try:
                # convert string to datetime object
                start = datetime.strptime(start, "%Y-%m-%d")
                end = datetime.strptime(end, "%Y-%m-%d")
            except ValueError:
                print("Error: you must enter the reasonable dates in the "
                      "required format.")
                continue
            
            # check if input equal 2020-08-04 of which data is unavailable
            if start == datetime.strptime("2020-08-04", "%Y-%m-%d") or\
               end == datetime.strptime("2020-08-04", "%Y-%m-%d"):
                print("Error: The price history on 2020-08-04 is unavailable.")
                continue      
            
            # check if the start date is earlier than the end date
            if start >= end:
                print("Error: The start date of the period must be earlier "
                      "than the end date.")
                continue          
            
            # check if input in the range of availble dates
            if not datetime.strptime("2014-09-17", "%Y-%m-%d") <= start \
                <= datetime.strptime("2020-10-20", "%Y-%m-%d") or \
               not datetime.strptime("2014-09-17", "%Y-%m-%d") <= end \
                <= datetime.strptime("2020-10-20", "%Y-%m-%d"):
                print("Error: The dates are out of available range.") 
                continue
            else:
                self.__period_start = start.date() # get only date
                self.__period_end = end.date()
                return self.__period_start, self.__period_end
                break
        
    def get_historical_price(self, interval):
        """Return summary of the historical price."""
        self.interval = interval        
        # get a data frame of historial price from csv file
        df = pd.read_csv(PRICE_HISTORY_FILE)
        # convert strings in the Date column to datetime objects
        df["Date"] = pd.to_datetime(df.Date)        
        # set the Date column as the index
        df.set_index("Date", inplace=True)
        
        # get a data frame of one day history
        if self.interval == "one": 
            self.view_date = self.get_one_day()
            self.df_one = df[self.view_date : self.view_date]
            return self.df_one
        
        # get a data frame of a period history
        elif self.interval == "period":
            self.view_period = self.get_a_period()
            self.df_period = df[self.view_period[0] : self.view_period[1]]
            return self.df_period  

    def view_historical_price(self, interval):
        """Return text description of the historical price.""" 
        self.interval = interval
        # view history for one day
        if self.interval == "one":             
            self.df_one = self.get_historical_price("one")
            # get a summary info of one day data frame
            # round all data to two decimal places
            df_info = self.df_one.describe().round(2)                        
            return ("\nPrice History on {}: \n"
                  "Open Price:  ${} \n"
                  "High Price:  ${} \n"
                  "Low Price:   ${} \n"
                  "Close Price: ${} \n"
                  "Volumn:      {:,.2f}"\
                  .format(self.view_date, df_info.iat[1,0], df_info.iat[1,1], \
                         df_info.iat[1,2], df_info.iat[1,3], df_info.iat[1,5]))
        
        # view history for a period        
        elif self.interval == "period":
            # get a summary info of a period data frame
            self.df_period = self.get_historical_price("period")
            df_info = self.df_period.describe().round(2)            
            return ("\nPrice History Summary from {} to {}: \n"
                  "                Max                Min               Mean\n"
                  "Open Price:   ${:<16.2f}  ${:<16.2f}  ${:<16.2f} \n"
                  "High Price:   ${:<16.2f}  ${:<16.2f}  ${:<16.2f} \n"
                  "Low Price:    ${:<16.2f}  ${:<16.2f}  ${:<16.2f} \n"
                  "Close Price:  ${:<16.2f}  ${:<16.2f}  ${:<16.2f} \n"
                  "Volumn:       {:<16,.2f}  {:<16,.2f}  {:<16,.2f}"\
                  .format(self.view_period[0], self.view_period[1], \
                      df_info.iat[7,0], df_info.iat[3,0], df_info.iat[1,0],\
                      df_info.iat[7,1], df_info.iat[3,1], df_info.iat[1,1],\
                      df_info.iat[7,2], df_info.iat[3,2], df_info.iat[1,2],\
                      df_info.iat[7,3], df_info.iat[3,3], df_info.iat[1,3],\
                      df_info.iat[7,5], df_info.iat[3,5], df_info.iat[1,5]))
        
    def price_chart(self, interval):
        """Get candlestick chart of historical price."""
        self.interval = interval
        # get candlestick chart from one day dataframe
        if self.interval == "one":            
            view_history = self.view_historical_price("one")                                            
            mpf.plot(self.df_one, type="candle", style="yahoo",\
                     title="   Bitcoin Candlestick Chart", ylabel="Price ($)",\
                     ylabel_lower="Volume", volume=True)
            
            # print info of one day price history
            print(view_history)
            print("The Bitcoin candlestick chat shows in the Plots window.")
                                                                       
        # get candlestick chart from period dataframe
        elif self.interval == "period": 
            view_history = self.view_historical_price("period")
                    
            mpf.plot(self.df_period, type="candle", style="yahoo",mav=(3,6,9),\
                     title="   Bitcoin Candlestick Chart", ylabel="Price ($)",\
                     ylabel_lower="Volume", volume=True, show_nontrading=True)
            
            # print summary of period price history
            print(view_history)
            print("The candlesticks chat shows in the Plots window.")
                
    def price_history_main(self):
        """Prompt user to select actions in the submenu.""" 
        while True:
            # prompt user to select actions in the submenu
            select_str = input("Here is the Historical Price Menu: \n"
                               "1 - View Historical Price For A Day \n"
                               "2 - View Historical Price For A Period \n"
                               "3 - Exit View Historical Price \n"
                               "Please enter number 1-3 to select actions: ")
            # start validate input
            try:
                select_int = int(select_str)
            except ValueError:
                print("Error: You must enter an 1-digit integer.")
                continue
                        
            if not 1 <= select_int <= 3:
                print("Error: You must enter the number between 0 and "
                      "3(inclusive).")
                continue
            
            # 1 - View Historical Price For One Day
            if select_int == 1:
                print("\nYou select: 1 - View Historical Price For A Day")
                interval = "one"
                one_date_history = PriceHistory()
                one_date_history.price_chart(interval)
            # 2 - View Historical Price For A Period    
            elif select_int == 2:
                print("\nYou select:2 - View Historical Price For A Period")
                interval = "period"
                time_period_history = PriceHistory()
                time_period_history.price_chart(interval)
            # 3 - Exit   
            else:
                print("\nYou select: 3 - Exit View Historical Price")
                break        

    

# unit test
if __name__ == "__main__":
    
    
    time_period = "2016-10-12,2016-10-18"
    date_start, date_end = time_period.split(",")
    
    one_date = "2014-09-17"
    date_list = [465.86401399999994, 468.174011, 452.421997, 
                 457.334015, 457.334015, 21056800.0]
    data_view = ("\nPrice History on 2014-09-17: \n"
                 "Open Price:  $465.86 \n"
                 "High Price:  $468.17 \n"
                 "Low Price:   $452.42 \n"
                 "Close Price: $457.33 \n"
                 "Volumn:      21,056,800.00")    
        
    ph = PriceHistory() 
    
    # test get_time_period() by using time_period "2016-10-12,2016-10-18"
    get_a_period = ph.get_a_period()
    assert datetime.strftime(get_a_period[0],"%Y-%m-%d") == date_start\
       and datetime.strftime(get_a_period[1],"%Y-%m-%d") == date_end,\
                                 "Failed to get valid input time period."

    # test get_one_day() by using one_date "2014-09-17"
    get_one_day = ph.get_one_day()
    assert datetime.strftime(get_one_day,"%Y-%m-%d") == one_date,\
                               "Failed to get valid input one date."
     
    # test get_historical_price() by using one_date "2014-09-17"
    # convert date frame to list of lists
    get_price = ph.get_historical_price("one").values.tolist()
    assert get_price[0] == date_list, "Failed to get historical price."
       
    # test view_historical_price() by using one_date "2014-09-17"
    assert ph.view_historical_price("one") == data_view, \
                             "Failed to view historical price."
    
    print("\nPriceHistory Class Tests All Passed!")
    