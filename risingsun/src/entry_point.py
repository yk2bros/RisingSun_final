import access_token
import repository
import pandas as pd

STOCK_NAME = "HINDUNILVR"
RESOLUTION = "5"
FROM_DAYS = repository.get_current_day_time_hour()

dema_time_period = 3
supertrend_ATR = 12
supertrend_Multiplier = 3
per = 1.03 # sell percentage criteria

# Constants
BUY_SIDE = 1
SELL_SIDE = -1

# Variables
OPEN_VALUES = []
HIGH_VALUES = []
LOW_VALUES = []
CLOSE_VALUES = []
EPOCH_VALUES = []
EMA_VALUES = []
FLAG = 0

# orderId = ""
# quantity = 1
# type = 1
# product_type = "INTRADAY"
# validity = "DAY"
# symbol = "NSE:" + STOCK_NAME + "-EQ"
# limit_price = 0

#***********************************************************************************************************************
# Generating Stock Details
stock_meta_data = repository.pass_stock_data(STOCK_NAME, RESOLUTION, FROM_DAYS)

# Getting the entire data of the stock
entire_stock_data = access_token.get_fyers_entry_point().history(stock_meta_data)

# length of entire stock data
length_of_entire_stock_data = len(entire_stock_data['candles'])

for i in range(len((entire_stock_data)["candles"])):
    EPOCH_VALUES.append((entire_stock_data)["candles"][i][0])
    OPEN_VALUES.append((entire_stock_data)["candles"][i][1])
    HIGH_VALUES.append((entire_stock_data)["candles"][i][2])
    LOW_VALUES.append((entire_stock_data)["candles"][i][3])
    CLOSE_VALUES.append((entire_stock_data)["candles"][i][4])
#***********************************************************************************************************************


dataframe_data = pd.DataFrame(
    {"HIGH": repository.list_to_numpy_array(HIGH_VALUES), "LOW": repository.list_to_numpy_array(LOW_VALUES),
     "CLOSE": repository.list_to_numpy_array(CLOSE_VALUES)})

print(repository.get_supertrend(dataframe_data,supertrend_ATR,supertrend_Multiplier))





# print("The length of the entire stock data is = ", length_of_entire_stock_data, "\n")

# print("The entire stock detail is - \n ", entire_stock_data)

# print(repository.list_to_numpy_array(entire_stock_data))

# print(repository.list_to_npdf(entire_stock_data))

# print(CLOSE_VALUES)
# print(i)
# print("The placed orders is - ", (placed_order))
# print("Order modified is - ", modified_order)
# print("Cancelled Order - ",cancelled_order )
# print("Order Exited - ", exit_order)
# print("Sold order - ", sold_order)

print("\n====================APP CLOSED=====================")

# ********************************************************************************************************
