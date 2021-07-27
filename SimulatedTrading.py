# -*- coding: utf-8 -*-
"""
Jingtian Zou
Class: CS 521 - Fall 1
Date: 10/20/2020
Final Project - Part4 - SimulatedTrading Class
"""

from datetime import datetime
from BitcoinPrice import BitcoinPrice

TRADE_HISTORY_FILE = "my_trading_history.txt"

class SimulatedTrading():
    """Perform simulated Bitcoin trading."""

    def __init__(self, cash=0, amount=0):
        self.__current_cash = cash
        self.__current_amount = amount
        self.__current_price = BitcoinPrice()

    def __repr__(self):
        return ("current cash: {}, current amount: {}, current price: {}"
                .format(self.__current_cash, self.__current_amount,\
                        self.__current_price))
    
    def check_file_exist(self):
        """Return True if 'my_trading_history.txt' file exists."""
        try:
            with open(TRADE_HISTORY_FILE, "r") as temp:
                return True
        except FileNotFoundError:
            return False

    def setup_account(self):
        """Setup the trading account and record into file."""
        while True:
            # prompt user to input initial cash and bitcoin amounts
            setup_str = input("Trading account doesn't setup. \n"
                              "Please enter your Cash and Bitcoin amounts, "
                              "both must be numbers and split by comma: ")
            # start validate input
            try:
                setup_segment_str = setup_str.split(",")
            except ValueError:
                print("Error: You must enter 2 numbers and split by comma.")
                continue

            if len(setup_segment_str) != 2:
                print("Error: You must split 2 values by comma.")
                continue

            try:
                self.__current_cash = float(setup_segment_str[0])
                self.__current_amount = float(setup_segment_str[1])
            except ValueError:
                print("Error: You must enter 2 numbers.")
                continue

            if self.__current_cash < 0 or self.__current_amount < 0:
                print("Error: Cash or Bitcoin amount can't be lower than 0.")
                continue
            
            # get current bitcoin price
            btc_price = float(self.__current_price.get_current_price())
            # record initial info of trading account into file
            self.record_into_file(btc_price)
            break
    
    def record_into_file(self, btc_price):
        """Record account status into file."""
        # total bitcoin value according to current price
        btc_value = btc_price * self.__current_amount
        # total asset value according to current price
        total_value = btc_value + self.__current_cash
        # set items to record
        record = [datetime.now().strftime("%Y-%m-%d,%H:%M:%S"),\
                 str(total_value), str(self.__current_cash), str(btc_value),\
                 str(self.__current_amount)]
        
        # open file and write record
        with open(TRADE_HISTORY_FILE, "a") as trade_histoty:
            trade_histoty.write(" ".join(record) + "\n")

        print("\nSuccessfully record Total Assert Value ${:,.2f}, "
              "Available Cash ${:,.2f}, BitCoin Value ${:,.2f} "
              "and Bitcoin Amount {:,.2f}."
              .format(total_value, self.__current_cash, \
                      btc_value, self.__current_amount))

    def view_historical_trading(self):
        """Print historical trading information."""
        # open file to read by lines and then print records
        with open(TRADE_HISTORY_FILE, "r") as trade_histoty:
            for history in trade_histoty:
                history_info = history.split()
                if len(history_info) == 5:
                    for i in range(1, len(history_info)):
                        history_info[i] = float(history_info[i])                        
                print("{}\n"
                      "Total Asset Value:  ${:,.2f} \n"
                      "Available Cash:     ${:,.2f} \n"
                      "BitCoin Value:      ${:,.2f} \n"
                      "BitCoin Amount:     {:,.2f} \n"                      
                      .format(history_info[0], history_info[1],\
                              history_info[2], history_info[3],\
                              history_info[4]))
    
    def get_last_trading(self):
        """Get last trading history about cash and bitcoin amount."""
        with open(TRADE_HISTORY_FILE, "r") as trade_histoty:
            histories = trade_histoty.readlines()
            last_trading = histories[-1].split()  # get last record
            self.__current_cash = float(last_trading[2])
            self.__current_amount = float(last_trading[4])
            return self.__current_cash, self.__current_amount
    

    def simulated_trading(self):
        """Simulated trading."""
        # get last record to initialize this trading
        last_trading = self.get_last_trading()
        btc_price = float(self.__current_price.get_current_price())
        btc_value = btc_price * last_trading[1]
        total_value = btc_value + last_trading[0]
        print("Here is your current account status: \n"
              "Total Asset Value: ${:,.2f} \n"
              "Available Cash:    ${:,.2f} \n"
              "BitCoin Value:     ${:,.2f} \n"
              "BitCoin Amount:    {:,.2f} \n"                      
              "Current Price:     ${:,.2f}"
              .format(total_value, last_trading[0], btc_value,\
                      last_trading[1], btc_price))

        while True:
            # prompt user to input trading direction and amount split by comma
            trade_str = input("Sell: enter 0 and sell amount split by comma.\n"
                              "Buy: enter 1 and buy amount split by comma.\n"
                              "Please enter in the required format: ")
            # start validate input
            try:
                trade_segment_str = trade_str.split(",")
            except ValueError:
                print("Error: You must enter 2 numbers and split by comma.")
                continue

            if len(trade_segment_str) != 2:
                print("Error: You must split 2 values by comma.")
                continue

            try:
                sell_or_buy = int(trade_segment_str[0])
                trade_amount = float(trade_segment_str[1])
            except ValueError:
                print("Error: You must enter 2 numbers.")
                continue

            if sell_or_buy < 0 or sell_or_buy > 1:
                print("Error: You must enter 0 for sell or 1 for buy.")
                continue
                
            if trade_amount < 0:
                print("Error: Bitcoin amount can't be lower than 0.")
                continue
                
            if sell_or_buy == 0 and trade_amount > self.__current_amount:
                print("Error: You currently have {:,.2f} Bitcoin. "
                      "You can't sell more than this amount."
                      .format(self.__current_amount))
                continue
                
            if sell_or_buy==1 and trade_amount*btc_price > self.__current_cash:
                print("Error: You currently have ${:,.2f} Cash. "
                      "You can't buy more than this value."
                      .format(self.__current_cash))
                continue           
            break            
                        
        # all input values are valid, start trading
        # print trading info
        trade = "sell"
        if sell_or_buy == 1:
            trade = "buy"
        print("Start {} {:,.2f} Bitcoins with price {:,.2f}."
              .format(trade, trade_amount, btc_price))

        # sell: add Bitcoin amount and value, subtract cash amount
        if sell_or_buy == 0:
            self.__current_cash = self.__current_cash + trade_amount*btc_price
            self.__current_amount = self.__current_amount - trade_amount
        # buy: add cash amount, subtract Bitcoin amount and value
        else:
            self.__current_cash = self.__current_cash - trade_amount*btc_price
            self.__current_amount = self.__current_amount + trade_amount
        
        # record trading history
        self.record_into_file(btc_price)
        print("Finished trading!")
    

    def simulated_trading_main(self):
        """Prompt user to select actions in the submenu.""" 
        simulated_trading = SimulatedTrading()
        # check if need to initialize the trading account
        file_exist = simulated_trading.check_file_exist()
        if not file_exist:
            simulated_trading.setup_account()

        while True:
            # prompt user to select actions in the submenu
            select_str = input("Here is the Simulated Trading Menu: \n"
                               "1 - Start Simulated Trading \n"
                               "2 - View Trading History\n"
                               "3 - Exit Simulate Trading \n"
                               "Please enter number 1-3 to select actions: ")
            # start validate input
            try:
                select_int = int(select_str)
            except ValueError:
                print("Error: You must enter an 1-digit integer.")
                continue

            if not 1 <= select_int <= 3:
                print("Error: You must enter the number between 0 and 3(inclusive).")
                continue
            
            # 1 - Start Simulate Trading
            if select_int == 1:
                print("\nYou select: 1 - Start Simulated Trading \n")
                simulated_trading.simulated_trading()
            # 2 - View Trading History   
            elif select_int == 2:
                print("\nYou select: 2 - View Trading History \n")
                simulated_trading.view_historical_trading()
            # 3 - Exit   
            else:
                print("\nYou select: 3 - Exit Simulated Trading")
                break


# unit test
if __name__ == "__main__":
    """Since there are barely methods with return value in this class,
       it's hard to do unit test without any unit test framework.
       Just use assert to test only one method to show I understand the concept.
    """
    cash = 1000
    amount = 5    
    st = SimulatedTrading()
    st.setup_account()
    assert st.get_last_trading() == (float(cash), float(amount)), \
                        "Failed to get the last trading record." 
                        
    print("\nSimulatedTrading Class Tests All Passed!")