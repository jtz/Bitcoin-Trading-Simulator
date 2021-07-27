# -*- coding: utf-8 -*-

"""
Jingtian Zou
Class: CS 521 - Fall 1
Date: 10/20/2020
Final Project - Part1 - Main Program
"""

from BitcoinPrice import BitcoinPrice
from PriceHistory import PriceHistory
from SimulatedTrading import SimulatedTrading

print("\nWelcome to the Bitcoin Trading Simulator made by Jingtian Zou!")

back_to_main_menu = True

while back_to_main_menu:
    # prompt user to select actions in the main menu
    select_str = input("Here is the Main Menu: \n"
                       "1 - View Current Bitcoin Price \n"
                       "2 - View Historical Bitcoin Price \n"
                       "3 - Simulated Trading \n"
                       "4 - Exit \n"
                       "Please enter number 1-4 to select actions: ")
    # start validate input
    try:
        select_int = int(select_str)        
    except ValueError:
        print("Error: You must enter an 1-digit integer.")
        continue
    
    if not 1 <= select_int <= 4:
        print("Error: You must enter the number between 0 and 4(inclusive).") 
        continue
    
    else:
        # 1 - view current Bitcoin price
        if select_int == 1:
            print("\nYou select: 1 - View Current Bitcoin Price")
            btc_price = BitcoinPrice()            
            print("\nThe current Bitcoin price is ${} at {}."
                  .format(btc_price.get_current_price(), \
                          btc_price.get_current_datetime()))
        # 2 - view historical Bitcoin price
        elif select_int == 2:
            print("\nYou select: 2 - View Historical Bitcoin Price")
            price_history = PriceHistory()
            price_history.price_history_main()
        # 3 - simulated trading                                    
        elif select_int == 3:
            simulated_trading = SimulatedTrading()
            simulated_trading.simulated_trading_main()
        # exit program    
        elif select_int == 4:           
            back_to_main_menu = False        
            print("\nThank you for using the Bitcoin Trading Simulator made "
                  "by Jingtian Zou!")
            break
        
        while True:
            # prompt user to select action back to main menu or to exit 
            sub_select_str = input("Please enter number 0 to go back to "            
                                   "the Main Menu or number 4 to Exit: ")            
            # start validate input
            try:
                sub_select_int = int(sub_select_str)        
            except ValueError:
                print("Error: You must enter integer 0 or 4.")
                continue
            
            if sub_select_int != 0 and sub_select_int != 4:
                print("Error: You must enter number 0 or 4.") 
                continue
           
            else:
                # back to main menu
                if sub_select_int == 0:
                    back_to_main_menu = True
                    break
                elif sub_select_int == 4:
                    back_to_main_menu = False
                    print("\nThank you for using the Bitcoin Trading Simulator"
                          " made by Jingtian Zou!")
                    break
        