import pandas
import access_token
import repository
import pandas as pd

STOCK_NAME = "SBIN"
RESOLUTION = "5"
FROM_DAYS = 1

dema_time_period = 3
supertrend_ATR = 12
supertrend_Multiplier = 3
per = 1.03 # sell percentage criteria


OPEN_VALUES = []
HIGH_VALUES = []
LOW_VALUES = []
CLOSE_VALUES = []
EPOCH_VALUES = []

# Generating Stock Details
stock_meta_data = repository.pass_stock_data(STOCK_NAME, RESOLUTION, FROM_DAYS)

# Getting the entire data of the stock
entire_stock_data = access_token.get_fyers_entry_point().history(stock_meta_data)

# length of entire stock data
print("The length of the entire stock data is = ", len(entire_stock_data['candles']), "\n")

# print
# print("The entire stock detail is - \n ", entire_stock_data)

for i in range(len((entire_stock_data)["candles"])):
    EPOCH_VALUES.append((entire_stock_data)["candles"][i][0])
    OPEN_VALUES.append((entire_stock_data)["candles"][i][1])
    HIGH_VALUES.append((entire_stock_data)["candles"][i][2])
    LOW_VALUES.append((entire_stock_data)["candles"][i][3])
    CLOSE_VALUES.append((entire_stock_data)["candles"][i][4])


dataframe_data = pd.DataFrame(
    {"HIGH": repository.list_to_numpy_array(HIGH_VALUES), "LOW": repository.list_to_numpy_array(LOW_VALUES),
     "CLOSE": repository.list_to_numpy_array(CLOSE_VALUES)})

sum_buy = 0
sum_sell = 0
a = 0
buy_value = 0
trade_counter = 0 # it will count sell orders
trade_diff_result = []
discrete_diff = 0

first_Epoch = (entire_stock_data)["candles"][0][0]
print(first_Epoch)
to_Epoch_range = first_Epoch + 3600
print(to_Epoch_range)

for i in range(len(CLOSE_VALUES)):
    if(first_Epoch <= (entire_stock_data)["candles"][0][i] <= to_Epoch_range ):



# for i in range(len(CLOSE_VALUES)):
#     if CLOSE_VALUES[i] > repository.get_dema(repository.list_to_numpy_array(CLOSE_VALUES),
#                                              dema_time_period)[i] and \
#             repository.get_supertrend(dataframe_data, supertrend_ATR, supertrend_Multiplier)["Supertrend"][i] and a != 1:
#         print("BUY @ UserIndex: ", (i+1), " SystemIndex: ", i)
#         sum_buy += CLOSE_VALUES[i]
#         buy_value = CLOSE_VALUES[i]
#         buy_index = i
#         a = 1
#     elif (repository.get_supertrend(dataframe_data, supertrend_ATR, supertrend_Multiplier)["Supertrend"][i] == False or (buy_value * (per) <
#                                                                                                                          CLOSE_VALUES[i])) and a == 1:
#         print("SELL @ UserIndex: ", (i+1), " SystemIndex: ", i)
#         sum_sell += CLOSE_VALUES[i]
#         trade_counter = trade_counter + 1
#         sell_value = CLOSE_VALUES[i]
#         a = 0
#
#
#         buy_dict = {
#             "index": buy_index,
#             "value": buy_value
#         }
#
#         sell_dict = {
#             "index": i,
#             "value": sell_value
#         }
#
#         trade_diff = sell_value - buy_value
#         serial_number = trade_counter
#
#         temp_list = []
#         discrete_diff = trade_diff + discrete_diff
#
#         temp_list.append(serial_number)
#         temp_list.append(buy_dict)
#         temp_list.append(sell_dict)
#         temp_list.append(trade_diff)
#         temp_list.append(discrete_diff)
#
#         trade_diff_result.append(temp_list)
#






# print(repository.get_dema(repository.list_to_numpy_array(CLOSE_VALUES),dema_time_period))
# print(pandas.DataFrame(trade_diff_result).to_string())

print("\n=================APP CLOSED=====================")
