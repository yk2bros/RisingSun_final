import time
import access_token
import numpy as np
import pandas as pd
import talib
from datetime import datetime

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']

CURRENT_TIME = int(time.time())
MARKET_OPEN_TIME = 9.25  # in hours


def get_custom_epoch(days: int) -> int:
    """
    Returns the time in EPOCH format
    :param days: We pass the number of DAYS in integer
    :return:epoch_time
    """
    current_time = time.time()
    seconds_in_day = days * (24 * 60 * 60)
    required_time = current_time - seconds_in_day
    return int(required_time)


def get_custom_date(days: int):
    """
    Convert EPOCH time into human-readable format
    :param days: We pass the EPOCH value
    :return: date
    """
    epoch_time = get_custom_epoch(days)
    year = time.localtime(epoch_time)[0]
    month = time.localtime(epoch_time)[1]
    date = time.localtime(epoch_time)[2]
    months_in_name = MONTHS[month - 1]
    return f"{date} {months_in_name}, {year}"


def get_current_day_time_hour():
    '''
    Return the number of days since market open time.
    :return: days (float)
    '''
    now = datetime.now()
    current_hour, current_minute = int(now.strftime("%H")), int(now.strftime("%M"))
    current_time_in_hours = current_hour + (current_minute / 60)
    return (current_time_in_hours - MARKET_OPEN_TIME) / 24


def pass_stock_data(stock_name: str, resolution: str, from_days: int, to_days=CURRENT_TIME, cont_flag="1",
                    date_format="0", ):
    """
    Returns the dictionary(key-value pair)
    :param stock_name:
    :param resolution: Time frame of a chart i.e., 5min, 10min, 15min, etc.
    :param from_days: Data lene ke liye defined days pehle se
    :param to_days: Current Time is already defined
    :param cont_flag: Flag need for FYERS API
    :param date_format: As defined in the FYERS API
    :return:data
    """
    print("\nGenerating String of Stock Meta Data")
    data = {"symbol": f"NSE:{stock_name}-EQ", "resolution": f"{resolution}", "date_format": f"{date_format}",
            "range_from": get_custom_epoch(from_days),
            "range_to": CURRENT_TIME, "cont_flag": "1"}
    print("Generated String of Stock Meta Data is - \n", data, "\n")
    return data


def get_history_data(data2: dict):
    """
    Return the dictionary which contains Stock data
    :param data2:
    :return: data
    """

    data = access_token.get_fyers_entry_point().history(data2)
    return data


def get_supertrend(df, atr_period, multiplier):
    """
    Returns the values of Supertrend
    :param df: Excel jaisa table dikhta hain Dataframe  mein, else wo list rahegi
    :param atr_period: value defined by us
    :param multiplier: value defined by us
    :return: upperband and lowerband
    """
    high = df['HIGH']
    low = df['LOW']
    close = df['CLOSE']

    # calculate ATR
    price_diffs = [high - low,
                   high - close.shift(),
                   close.shift() - low]
    true_range = pd.concat(price_diffs, axis=1)
    true_range = true_range.abs().max(axis=1)

    # default ATR calculation in supertrend indicator
    atr = true_range.ewm(alpha=1 / atr_period, min_periods=atr_period).mean()

    # df['atr'] = df['tr'].rolling(atr_period).mean()

    # HL2 is simply the average of high and low prices
    hl2 = (high + low) / 2

    # upperband and lowerband calculation
    # notice that final bands are set to be equal to the respective bands
    final_upperband = upperband = hl2 + (multiplier * atr)
    final_lowerband = lowerband = hl2 - (multiplier * atr)

    # initialize Supertrend column to True
    supertrend = [True] * len(df)

    for i in range(1, len(df.index)):
        curr, prev = i, i - 1

        # if current close price crosses above upperband
        if close[curr] > final_upperband[prev]:
            supertrend[curr] = True
        # if current close price crosses below lowerband
        elif close[curr] < final_lowerband[prev]:
            supertrend[curr] = False
        # else, the trend continues
        else:
            supertrend[curr] = supertrend[prev]

            # adjustment to the final bands
            if supertrend[curr] == True and final_lowerband[curr] < final_lowerband[prev]:
                final_lowerband[curr] = final_lowerband[prev]
            if supertrend[curr] == False and final_upperband[curr] > final_upperband[prev]:
                final_upperband[curr] = final_upperband[prev]

        # to remove bands according to the trend direction
        if supertrend[curr] == True:
            final_upperband[curr] = np.nan
        else:
            final_lowerband[curr] = np.nan

    return pd.DataFrame({
        'Supertrend': supertrend,
        'Final Lowerband': final_lowerband,
        'Final Upperband': final_upperband
    }, index=df.index)


def get_dema(close_values: list, time_period: int):
    """
    Returns the value of DEMA
    :param close_values:
    :param time_period:
    :return: DEMA
    """

    dema = talib.DEMA(np.array(close_values), timeperiod=time_period)
    return dema.tolist()


def get_dema_last_value(close_values: list, time_period: int):
    """
    Returns the last value of DEMA
    :param close_values: close values in list form
    :param time_period: 5 or 10 or 15 in integer value
    :return: DEMA
    """

    dema = talib.DEMA(np.array(close_values), timeperiod=time_period)
    return dema[-1]


def list_to_numpy_array(list: list):
    """
    Converts list into numpy array
    :param list: any LIST
    :return: nparray
    """
    return np.array(list)


def list_to_npdf(list: list):
    """
    Converts the list in to pandas dataframe
    :param list: any LIST
    :return: pandas dataframe
    """
    numpy_list = list_to_numpy_array(list)
    return pd.DataFrame(numpy_list)


def get_ema(close_values, period):
    """
    Gives the EMA value
    :param price: closing price of stocks
    :param period: Looks for the previous specific number of candles for calculation, user-defined integer
    :return: EMA Value
    """
    value = talib.EMA(np.array(close_values), period)

    return value


def ema_initializer(HIGH_VALUES,
                    CLOSE_VALUES,
                    LOW_VALUES,
                    EMA_VALUES,
                    rr_ratio_changer,
                    stock_length,
                    quantity,
                    symbol,
                    type,
                    BUY_SIDE,
                    SELL_SIDE,
                    product_type,
                    limit_price,
                    stop_price,
                    validity="DAY",
                    disclosed_quantity=0,
                    offline_order="False",
                    fix_rr=2):
    buy_value = 0
    sell_value = 0
    trade_counter = 0
    profit_loss_value = 0
    final_pnl = 0
    stop_loss = 0
    rr_ratio = 0
    target_value1 = 0
    target_value2 = 0
    rr_ratio_changer = rr_ratio_changer
    FLAG = 0
    stop_loss_counter = 0
    sell_counter = 0
    total_amount_invested = 0
    quantity2 = quantity / 2
    rr_method2_breaker_flag = 0

    for i in range(len(HIGH_VALUES)):
        if ((EMA_VALUES[i] > HIGH_VALUES[i]) and (i < (stock_length - 1))):
            if (CLOSE_VALUES[i + 1] > HIGH_VALUES[i] and FLAG == 0):
                FLAG = 1

                buy_value = CLOSE_VALUES[i + 1]
                total_amount_invested = buy_value * quantity

                print("Index at BUY candle is = ", i)
                print("Stop loss is = ", stop_loss)
                print("BUY\n")

                min = LOW_VALUES[i] if LOW_VALUES[i] < LOW_VALUES[i + 1] else LOW_VALUES[i + 1]
                stop_loss = min
                rr_ratio = buy_value - stop_loss
                target_value1 = buy_value + (rr_ratio * rr_ratio_changer)
                target_value2 = buy_value + (rr_ratio * fix_rr)

        # EMA method for SELL
        # elif ((EMA_VALUES[i] < LOW_VALUES[i])):
        #
        #     if (CLOSE_VALUES[i + 1] < LOW_VALUES[i] and FLAG == 1):
        #         sell_counter = sell_counter + 1
        #
        #         if(sell_counter > 4 ):
        #             FLAG = 0
        #             sell_value = CLOSE_VALUES[i + 1]
        #             profit_loss_value = sell_value - buy_value
        #             final_pnl += profit_loss_value
        #             trade_counter = trade_counter + 1
        #
        #             print(("1st"))
        #             print("Index at SELL candle is = ", i)
        #             print("PnL value is = ", profit_loss_value)
        #             print("SELL")

        # STOP LOSS method for Sell
        elif ((CLOSE_VALUES[i] < stop_loss) and FLAG == 1 and rr_method2_breaker_flag == 0):
            FLAG = 0
            sell_value = CLOSE_VALUES[i + 1]

            profit_loss_value = sell_value - buy_value
            final_pnl += profit_loss_value
            trade_counter = trade_counter + 1
            stop_loss_counter = stop_loss_counter + 1

            print(("2nd"))
            print("Index at SELL candle is = ", i)
            print("PnL value is = ", profit_loss_value)
            print("SELL")

        # STOP LOSS method-2 for Sell
        elif ((CLOSE_VALUES[i] < stop_loss) and FLAG == 1 and rr_method2_breaker_flag == 1):
            FLAG = 0
            rr_method2_breaker_flag = 0

            sell_value = CLOSE_VALUES[i + 1]
            print("sell /2 ==== 2")
            # sell_order(create_sell_data(symbol,type,quantity2,SELL_SIDE,product_type,sell_value,stop_price))

            print(("2nd"))
            print("Index at SELL candle is = ", i)
            print("PnL value is = ", profit_loss_value)
            print("SELL")

        # Target method for Sell
        elif ((CLOSE_VALUES[i] > target_value1) and FLAG == 1 and rr_method2_breaker_flag == 1):
            FLAG = 0
            rr_method2_breaker_flag = 0

            sell_value = CLOSE_VALUES[i + 1]
            print("sell /2 ====2 ")

            # sell_order(create_sell_data(symbol,type,quantity2,SELL_SIDE,product_type,sell_value,stop_price))

            print(("2nd"))
            print("Index at SELL candle is = ", i)
            print("PnL value is = ", profit_loss_value)
            print("SELL")

        # RR method for Sell
        elif ((CLOSE_VALUES[i] >= target_value1) and FLAG == 1):
            FLAG = 0

            sell_value = CLOSE_VALUES[i + 1]
            profit_loss_value = sell_value - buy_value
            final_pnl += profit_loss_value
            trade_counter = trade_counter + 1

            print(("3rd"))
            print("Index at SELL candle is = ", i)
            print("PnL value is = ", profit_loss_value)
            print("SELL")

        # # RR method-2 for Sell
        # elif((CLOSE_VALUES[i] >= target_value2) and (rr_method2_breaker_flag == 0 ) ):
        #     rr_method2_breaker_flag = 1
        #
        #     sell_value = CLOSE_VALUES[i]
        #     print("sell /2 ===1 ")
        #
        # # sell_order(create_sell_data(symbol,type,quantity2,SELL_SIDE,product_type,sell_value,stop_price))
        #     stop_loss = buy_value

        else:
            print("")

    print("Number of trades executed = ", trade_counter)
    print("Final PnL is = ", final_pnl)
    print("Number of stop loss hit = ", stop_loss_counter)


def place_order(buy_data):
    """
    Order place karta hain FYERS app mein
    :param buy_data: contains all details as per FYERS API to place order
    :return: prints and returns placed order ID
    """
    orderId = ""
    placed_order = access_token.get_fyers_entry_point().place_order(buy_data)
    orderId = orderId + placed_order["id"]
    print("Placed Order is - ", placed_order)
    return orderId


def modify_order(modify_data):
    """
    Order Modify karta hain FYERS app mein
    :param modify_data: contains all details as per FYERS API to modify order
    :return: prints and returns modified order ID
    """
    modified_order = access_token.get_fyers_entry_point().modify_order(modify_data)
    print("Modified order is - ", modified_order)
    return modified_order


def cancel_order(cancel_order_id):
    """
    Order Cancel karta hain FYERS app mein
    :param cancel_data: contains all details as per FYERS API to cancel order
    :return: prints and returns cancelled order ID
    """
    cancelled_order = access_token.get_fyers_entry_point().cancel_order(cancel_order_id)
    print("Cancelled order - ", cancelled_order)
    return cancelled_order


def exit_order(exit_order_data):
    """
    Order Exit karta hain FYERS app mein
    :param exit_data: contains all details as per FYERS API to exit order
    :return: prints and returns exited order ID
    """
    exit_order = access_token.get_fyers_entry_point().exit_positions(exit_order_data)
    print("Exited order - ", exit_order)
    return exit_order


def sell_order(sell_data):
    """
    Order Sell karta hain FYERS app mein
    :param modify_data: contains all details as per FYERS API to sell order
    :return: prints and returns sold order ID
    """
    sold_order = access_token.get_fyers_entry_point().place_order(sell_data)
    print("Sold order - ", sold_order)
    return sold_order


def create_buy_data(symbol,
                    type,
                    quantity,
                    BUY_SIDE,
                    product_type,
                    limit_price,
                    stop_price,
                    validity="DAY",
                    disclosed_quantity=0,
                    offline_order="False"):
    """
    Create a structure of data to be passed while placing orders.
    :param symbol:
    :param type: Limit Order, Market Order as per FYERS
    :param quantity:
    :param BUY_SIDE:
    :param product_type: CNC, MIS
    :param limit_price: MAX value jispe kharidna hain
    :param stop_price: MIN value jispe kharidna hain
    :param validity: Day, AMO
    :param disclosed_quantity:
    :param offline_order: False jab chalu hain market, True jab bnd hain market
    :return:
    """
    buy_data = {
        "symbol": symbol,
        "qty": quantity,
        "type": type,
        "side": BUY_SIDE,
        "productType": product_type,
        "limitPrice": limit_price,
        "stopPrice": stop_price,
        "validity": validity,
        "disclosedQty": disclosed_quantity,
        "offlineOrder": offline_order,
        # "stopLoss":500,
        # "takeProfit":600
    }

    return buy_data


def create_sell_data(symbol,
                     type,
                     quantity2,
                     SELL_SIDE,
                     product_type,
                     limit_price,
                     stop_price,
                     validity="DAY",
                     disclosed_quantity=0,
                     offline_order="False", ):
    """
    Create a structure of data to be passed while placing orders.
    :param symbol:
    :param type: Limit Order, Market Order as per FYERS
    :param quantity:
    :param SELL_SIDE:
    :param product_type: CNC, MIS
    :param limit_price: MAX value jispe bechna hain
    :param stop_price: MIN value jispe bechna hain
    :param validity: Day, AMO
    :param disclosed_quantity:
    :param offline_order: False jab chalu hain market, True jab bnd hain market
    :return:
    """
    sell_data = {
        "symbol": symbol,
        "qty": quantity2,
        "type": type,
        "side": SELL_SIDE,
        "productType": product_type,
        "limitPrice": limit_price,
        "stopPrice": stop_price,
        "validity": validity,
        "disclosedQty": disclosed_quantity,
        "offlineOrder": offline_order,
        # "stopLoss":500,
        # "takeProfit":600
    }

    return sell_data

def quantity(funds,stop_loss):

    funds = 50000
    risk_per_trade = 500
    stoploss =
