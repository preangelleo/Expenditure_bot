from Top_functions import *
from Generate_token import *

TRADING_VOLUME_LIMIT = int(os.getenv('TRADING_VOLUME_LIMIT', 50_000_000))
INITIAL_FUND = int(os.getenv('INITIAL_FUND', 100_000))
CHECK_SIZE = int(os.getenv('CHECK_SIZE', 10_000))

positions_limit = get_position_limit()
POSITIONS_LIMIT = positions_limit if positions_limit else int(INITIAL_FUND / CHECK_SIZE)

# from "CREATE TABLE IF NOT EXISTS target_profit (ID INTEGER PRIMARY KEY AUTO_INCREMENT, Date DATE, TargetProfit FLOAT)" table read the target profit
def read_target_profit_default(from_id=None):
    df_target_profit = pd.DataFrame(engine.connect().execute(text("SELECT * FROM target_profit ORDER BY ID DESC LIMIT 1")).fetchall())
    target_profit = float(df_target_profit['TargetProfit'].values[0])
    if from_id: send_msg(f"Current target profit: {target_profit*100}%", from_id)
    return target_profit

target_profit = read_target_profit_default()
TARGET_PROFIT = target_profit if target_profit else float(os.getenv('TARGET_PROFIT', 0.05))

SHORT_COINS_LIST = []

def set_new_target_profit(target_profit, chat_id=TG_BOT_OWNER_ID):
    target_profit = float(target_profit) if target_profit else 0.001
    if target_profit > 0 and target_profit < 1:
        if set_target_profit_default(target_profit): 
            send_msg(f"Set target profit: {target_profit*100}%", chat_id)
            return read_target_profit_default(from_id=chat_id)
    else: return send_msg(f"Target profit: {target_profit*100}% is not valid, it should be between 0 and 1. For example: 0.05 means 5%.", chat_id)


def read_positions_limit(from_id=TG_BOT_OWNER_ID):
    global POSITIONS_LIMIT
    positions_limit = get_position_limit()
    if positions_limit != POSITIONS_LIMIT: POSITIONS_LIMIT = positions_limit
    if from_id: send_msg(f"Current positions limit: {POSITIONS_LIMIT}\n\nIf you want to change your positions limit, you could use command:\n\n/set_position_limit 10", from_id)
    return POSITIONS_LIMIT


# from "CREATE TABLE IF NOT EXISTS ignore_coin_list (id INT NOT NULL AUTO_INCREMENT, symbol VARCHAR(20) DEFAULT NULL, PRIMARY KEY (id))" table remove the given coin
def remove_from_ignore_coin_list(coin: str, chat_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    if remove_from_ignore_coin_table(coin): send_msg(f"Removed {coin} from ignore coin list.", chat_id)
    else: send_msg(f"Failed to remove {coin} from ignore coin list.", chat_id)


def remove_from_future_profit(coin: str, chat_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    if remove_from_future_profit_table(coin): send_msg(f"Removed {coin} from future profit table.", chat_id)
    else: send_msg(f"Failed to remove {coin} from future profit table.", chat_id)


# remove coin from white_list table
def remove_from_white_list(coin: str, chat_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    if remove_from_white_list_table(coin): send_msg(f"Removed {coin} from white list.", chat_id)
    else: send_msg(f"Failed to remove {coin} from white list.", chat_id)
    

def network_name_change(str_name: str):
    str_name = str_name.upper()
    str_name = 'ETH' if str_name.startswith("ERC") else 'TRX' if str_name.startswith("TRC") else 'BSC' if str_name.startswith("BEP") else str_name
    return str_name


def server_time_diff():
    PATH = '/api/v1/time'
    params = None
    timestamp = int(time.time() * 1000)
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.get(url, params=params)
        data = r.json()
        diff = {timestamp - data['serverTime']}
        return diff
    except Exception as e:
        print(e)
        time.sleep(0.1)
        return


def get_listed_assets_info():
    PATH = '/sapi/v1/asset/assetDetail'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.get(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200:
            return
        data = r.json()
        return data
        # df = pd.DataFrame(data)
        # return df.T
    except Exception as e:
        print(e)
        return
'''r = get_listed_assets_info()
df = pd.DataFrame(r)
df = df.T
print(df)'''


# 查询用户API Key权限 (USER_DATA), 权重(IP): 1
# GET /sapi/v1/account/apiRestrictions (HMAC SHA256)
def get_api_functions():
    PATH = '/sapi/v1/account/apiRestrictions'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.get(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200:
            return
        data = r.json()
        return data
    except Exception as e:
        print(e)
        return
'''{'ipRestrict': True, 'createTime': 1665449424000, 'enableInternalTransfer': True, 'permitsUniversalTransfer': True, 'enablePortfolioMarginTrading': False, 'enableVanillaOptions': False, 'enableReading': True, 'enableSpotAndMarginTrading': True, 'enableWithdrawals': True, 'enableMargin': True, 'enableFutures': True}'''

# User curl -X GET "https://api.binance.com/api/v3/exchangeInfo" get all symbols exchange info, change to dataframe and save to a json file 'binance_exchange_info.json'
def get_exchange_info():
    PATH = '/api/v3/exchangeInfo'
    params = None
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.get(url, params=params)
        if r.status_code != 200:
            return
        data = r.json()
        # save to json file
        with open('binance_exchange_info.json', 'w') as f:
            json.dump(data, f, indent=2)
        return data
    except Exception as e:
        print(e)
        time.sleep(0.1)
        return


''' SAND EXCHANGE INFO
      "symbol": "SANDUSDT",
      "status": "TRADING",
      "baseAsset": "SAND",
      "baseAssetPrecision": 8,
      "quoteAsset": "USDT",
      "quotePrecision": 8,
      "quoteAssetPrecision": 8,
      "baseCommissionPrecision": 8,
      "quoteCommissionPrecision": 8,
      "orderTypes": [
        "LIMIT",
        "LIMIT_MAKER",
        "MARKET",
        "STOP_LOSS_LIMIT",
        "TAKE_PROFIT_LIMIT"
      ],
      "icebergAllowed": true,
      "ocoAllowed": true,
      "quoteOrderQtyMarketAllowed": true,
      "allowTrailingStop": true,
      "cancelReplaceAllowed": true,
      "isSpotTradingAllowed": true,
      "isMarginTradingAllowed": true,
      "filters": [
        {
          "filterType": "PRICE_FILTER",
          "minPrice": "0.00010000",
          "maxPrice": "1000.00000000",
          "tickSize": "0.00010000"
        },
        {
          "filterType": "LOT_SIZE",
          "minQty": "1.00000000",
          "maxQty": "9000000.00000000",
          "stepSize": "1.00000000"
        },
        {
          "filterType": "ICEBERG_PARTS",
          "limit": 10
        },
        {
          "filterType": "MARKET_LOT_SIZE",
          "minQty": "0.00000000",
          "maxQty": "533669.64166666",
          "stepSize": "0.00000000"
        },
        {
          "filterType": "TRAILING_DELTA",
          "minTrailingAboveDelta": 10,
          "maxTrailingAboveDelta": 2000,
          "minTrailingBelowDelta": 10,
          "maxTrailingBelowDelta": 2000
        },
        {
          "filterType": "PERCENT_PRICE_BY_SIDE",
          "bidMultiplierUp": "5",
          "bidMultiplierDown": "0.2",
          "askMultiplierUp": "5",
          "askMultiplierDown": "0.2",
          "avgPriceMins": 5
        },
        {
          "filterType": "NOTIONAL",
          "minNotional": "5.00000000",
          "applyMinToMarket": true,
          "maxNotional": "9000000.00000000",
          "applyMaxToMarket": false,
          "avgPriceMins": 5
        },
        {
          "filterType": "MAX_NUM_ORDERS",
          "maxNumOrders": 200
        },
        {
          "filterType": "MAX_NUM_ALGO_ORDERS",
          "maxNumAlgoOrders": 5
        }
      ],
      '''

def get_exchange_info_symbols(coin: str):
    # try to get response dict from table binance_exchange_info
    try:
        response = pd.read_sql(f"SELECT * FROM binance_exchange_info WHERE coin = '{coin.upper()}'", engine)
        if not response.empty: return response.to_dict(orient='records')[0]
    except: pass

    # if binance_exchange_info.json not exist, get it from binance
    if not os.path.exists('binance_exchange_info.json'): get_exchange_info()

    with open('binance_exchange_info.json') as f: data = json.load(f)
    
    # get the symbols info of coin.upper()+'USDT
    df = pd.DataFrame(data['symbols'])
    df_new = df[df['symbol'].str.endswith(coin.upper()+'USDT')]

    # convert df back into dict 
    result_list = df_new.to_dict(orient='records')
    response = {
        'symbol': result_list[0]['symbol'],
        'status': result_list[0]['status'],
        'baseAsset': result_list[0]['baseAsset'],
        'coin': result_list[0]['baseAsset'],
        'baseAssetPrecision': result_list[0]['baseAssetPrecision'],
        'quoteAsset': result_list[0]['quoteAsset'],
        'quotePrecision': result_list[0]['quotePrecision'],
        'quoteAssetPrecision': result_list[0]['quoteAssetPrecision'],
        'baseCommissionPrecision': result_list[0]['baseCommissionPrecision'],
        'quoteCommissionPrecision': result_list[0]['quoteCommissionPrecision'],
        'minPrice': result_list[0]['filters'][0]['minPrice'],
        'maxPrice': result_list[0]['filters'][0]['maxPrice'],
        'tickSize': result_list[0]['filters'][0]['tickSize'],
        'minQty': result_list[0]['filters'][1]['minQty'],
        'maxQty': result_list[0]['filters'][1]['maxQty'],
        'stepSize': result_list[0]['filters'][1]['stepSize'],
    }

    # make response to a dataframe and append to binance_exchange_info table
    df_response = pd.DataFrame(response, index=[0])
    df_response.to_sql('binance_exchange_info', engine, if_exists='append', index=False)

    return response

'''r = get_exchange_info_symbols('FTT')
Got response from binance_exchange_info table.
{
  "symbol": "FTTUSDT",
  "status": "TRADING",
  "baseAsset": "FTT",
  "coin": "FTT",
  "baseAssetPrecision": 8,
  "quoteAsset": "USDT",
  "quotePrecision": 8,
  "quoteAssetPrecision": 8,
  "baseCommissionPrecision": 8,
  "quoteCommissionPrecision": 8,
  "minPrice": "0.00010000",
  "maxPrice": "100000.00000000",
  "tickSize": "0.00010000",
  "minQty": "0.01000000",
  "maxQty": "922327.00000000",
  "stepSize": "0.01000000"
}
'''

# 获取币安全部交易对最新价格
def get_token_price_table():
    # Get ticker data
    df_ticker = pd.read_json(BINANCE_TICKER_URL)
    df_ticker = df_ticker.loc[:, ['symbol', 'lastPrice']]
    # pick up the symbol endswith 'USDT'
    df_ticker = df_ticker[df_ticker['symbol'].str.endswith('USDT')]
    df_ticker = df_ticker.reset_index(drop=True)
    # 增加一列, coin, coin = symbol[:-4]
    df_ticker['coin'] = df_ticker['symbol'].str[:-4]
    return df_ticker
'''
        symbol    lastPrice   coin
0      BTCUSDT  43405.08000    BTC
1      ETHUSDT   2375.71000    ETH
2      BNBUSDT    235.80000    BNB
3      BCCUSDT      0.00000    BCC
4      NEOUSDT     12.13000    NEO
..         ...          ...    ...
467    VICUSDT      1.00200    VIC
468   BLURUSDT      0.49800   BLUR
469  VANRYUSDT      0.06315  VANRY
470   AEURUSDT      2.88920   AEUR
471    JTOUSDT      3.00780    JTO'''

# use get_api_fuction() resutl convert to string send to chat_id
def get_api_functions_str(chat_id=TG_BOT_OWNER_ID):
    data = get_api_functions()
    if data: return send_msg('\n'.join([f'{key}: {value}' for key, value in data.items()]), chat_id)
    else: return send_msg(f"You don't have a binance API key and secrets in database yet.", chat_id)


# 账户API交易状态(USER_DATA), 获取 api 账户交易状态详情, 权重(IP): 1
# GET /sapi/v1/account/apiTradingStatus (HMAC SHA256)
# https://binance-docs.github.io/apidocs/spot/cn/#api-user_data 
def get_api_status():
    PATH = '/sapi/v1/account/apiTradingStatus'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.get(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200:
            return
        data = r.json()
        return data
    except Exception as e:
        print(e)
        return
'''{'data': {'isLocked': False, 'plannedRecoverTime': 0, 'triggerCondition': {'UFR': 300, 'IFER': 150, 'GCR': 150}, 'updateTime': 0}}'''


# 获取所有币信息 (USER_DATA), 获取针对用户的所有(Binance支持充提操作的)币种信息。权重(IP): 10
# GET /sapi/v1/capital/config/getall (HMAC SHA256)
# https://binance-docs.github.io/apidocs/spot/cn/#system
def get_account_all():
    PATH = '/sapi/v1/capital/config/getall'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.get(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200:
            return
        data = r.json()
        return data
    except Exception as e:
        time.sleep(0.1)
        return 
'''r = get_account_all()
df = pd.DataFrame(r)
df = df.T
print(df)    
           coin  depositAllEnable  withdrawAllEnable                            name free locked freeze withdrawing ipoing ipoable storage  isLegalMoney  trading                                        networkList
0          AGLD              True               True                  Adventure Gold    0      0      0           0      0       0       0         False     True  [{'network': 'ETH', 'coin': 'AGLD', 'entityTag...
1          STPT              True               True  Standard Tokenization Protocol    0      0      0           0      0       0       0         False     True  [{'network': 'ETH', 'coin': 'STPT', 'entityTag...
2           MXN              True               True                    Mexican Peso    0      0      0           0      0       0       0          True    False  [{'network': 'FIAT_MONEY', 'coin': 'MXN', 'ent...
3    MATICUSDCE              True               True                    Bridged USDC    0      0      0           0      0       0       0         False    False  [{'network': 'MATIC', 'coin': 'MATICUSDCE', 'e...
4           UGX              True               True                 Uganda Shilling    0      0      0           0      0       0       0          True    False  [{'network': 'FIAT_MONEY', 'coin': 'UGX', 'ent...
..          ...               ...                ...                             ...  ...    ...    ...         ...    ...     ...     ...           ...      ...                                                ...
486        AKRO              True               True                       Akropolis    0      0      0           0      0       0       0         False     True  [{'network': 'ETH', 'coin': 'AKRO', 'entityTag...
487         NZD              True               True              New Zealand Dollar    0      0      0           0      0       0       0          True    False  [{'network': 'FIAT_MONEY', 'coin': 'NZD', 'ent...
488        MOVR              True               True                       Moonriver    0      0      0           0      0       0       0         False     True  [{'network': 'MOVR', 'coin': 'MOVR', 'entityTa...
489         XMR              True               True                          Monero    0      0      0           0      0       0       0         False     True  [{'network': 'XMR', 'coin': 'XMR', 'entityTag'...
490        COTI              True               True                            COTI    0      0      0           0      0       0       0         False     True  [{'network': 'BSC', 'coin': 'COTI', 'entityTag...

[491 rows x 14 columns]
'''


# from result of get_account_all(), check if a given coin is in the list, and the given network is in the list of the coin's networkList and withdrawEnable is True and check the withdrawFee, withdrawMin, withdrawMax, withdrawIntegerMultiple, and check the address is valid with addressRegex, return networkList
def check_coin_network(coin, network):
    coin = coin.upper()
    network = network.upper()
    data = get_account_all()
    if data:
        df = pd.DataFrame(data)
        df = df[df['coin'] == coin]
        if not df.empty:
            df_networkList = pd.DataFrame(df['networkList'].values[0])
            # MAKE a list of network
            networkList = df_networkList['network'].values.tolist()

            df_networkList = df_networkList[df_networkList['network'] == network]
            if not df_networkList.empty:
                df_networkList = df_networkList[df_networkList['withdrawEnable'] == True]
                if not df_networkList.empty: return {'status': True, 'network_list': networkList}
    return {'status': False, 'network_list': networkList}
'''
  network coin entityTag withdrawIntegerMultiple  isDefault  depositEnable  withdrawEnable depositDesc withdrawDesc specialTips              name  resetAddressStatus           addressRegex addressRule memoRegex withdrawFee withdrawMin  withdrawMax  minConfirm  unLockConfirm  sameAddress  estimatedArrivalTime   busy                                            country           contractAddressUrl                             contractAddress
0     ETH  RSR      main              0.00000001       True           True            True                                       Ethereum (ERC20)               False  ^(0x)[0-9A-Fa-f]{40}$                              3531        7062  10000000000           6             64        False                     4  False  AE,BINANCE_BAHRAIN_BSC,KZ,FR,ES,PL,IT,SE,JP,NL...  https://etherscan.io/token/  0x320623b8e4ff03373931769a31fc52a4e78b5d70
'''


# 资金账户 (USER_DATA), 权重(IP): 1
# POST /sapi/v1/asset/get-funding-asset (HMAC SHA256)
# 目前仅支持查询以下业务资产：Binance Pay, Binance Card, Binance Gift Card, Stock Token
def get_funding_asset():
    PATH = '/sapi/v1/asset/get-funding-asset'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.post(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200:
            return
        data = r.json()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(e)
        return
'''
  asset            free locked freeze withdrawing btcValuation
0   ENS               1      0      0           0            0
1   NFT  8077335.411327      0      0           0            0
'''


# 定义 FUNDING_MAIN 资金钱包转向现货钱包功能
def funding_main_transfer(coin:str, amount):
    PATH = '/sapi/v1/asset/transfer'
    timestamp = int(time.time() * 1000)
    params = {
        'type': 'FUNDING_MAIN',
        'asset': coin.upper(),
        'amount': amount,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.post(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200: return
        data = r.json()
        tranId = data['tranId']
        return tranId
    except Exception as e:
        print(e)
        return
    

# 通过用户input 的 coin 和 amount，调用 get_funding_asset() 获取 coin 的余额，如果余额大于 amount，则调用 funding_main_transfer(coin, amount) 转账
def funding_main_transfer_with_check_and_send(coin, amount, chat_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    try: amount = float(amount)
    except: return send_msg(f'转账失败，您输入的转账数量: {amount} 不是数字。', chat_id)

    df = get_funding_asset()
    if not df.empty:
        df = df[df['asset'] == coin]
        if not df.empty:
            balance = float(df['free'].values[0])
            if balance >= amount: 
                tranId = funding_main_transfer(coin, amount)
                if tranId: return send_msg(f'已经成功将 {format_number(amount)} {coin} 从资金账户转入到现货账户, tranId: \n{tranId}', chat_id)
            else: return send_msg(f'资金账户 {coin} 余额: {format_number(balance)} 小于转账数量: {format_number(amount)}', chat_id)
        else: return send_msg(f'资金账户没有 {coin} 资产。', chat_id)
    return send_msg(f'转账失败，可能是网络问题，请稍后再试。', chat_id)

'''目前支持的type划转类型:
MAIN_UMFUTURE 现货钱包转向U本位合约钱包
MAIN_CMFUTURE 现货钱包转向币本位合约钱包
MAIN_MARGIN 现货钱包转向杠杆全仓钱包
UMFUTURE_MAIN U本位合约钱包转向现货钱包
UMFUTURE_MARGIN U本位合约钱包转向杠杆全仓钱包
CMFUTURE_MAIN 币本位合约钱包转向现货钱包
MARGIN_MAIN 杠杆全仓钱包转向现货钱包
MARGIN_UMFUTURE 杠杆全仓钱包转向U本位合约钱包
MARGIN_CMFUTURE 杠杆全仓钱包转向币本位合约钱包
CMFUTURE_MARGIN 币本位合约钱包转向杠杆全仓钱包
ISOLATEDMARGIN_MARGIN 杠杆逐仓钱包转向杠杆全仓钱包
MARGIN_ISOLATEDMARGIN 杠杆全仓钱包转向杠杆逐仓钱包
ISOLATEDMARGIN_ISOLATEDMARGIN 杠杆逐仓钱包转向杠杆逐仓钱包
MAIN_FUNDING 现货钱包转向资金钱包
FUNDING_MAIN 资金钱包转向现货钱包
FUNDING_UMFUTURE 资金钱包转向U本位合约钱包
UMFUTURE_FUNDING U本位合约钱包转向资金钱包
MARGIN_FUNDING 杠杆全仓钱包转向资金钱包
FUNDING_MARGIN 资金钱包转向杠杆全仓钱包
FUNDING_CMFUTURE 资金钱包转向币本位合约钱包
CMFUTURE_FUNDING 币本位合约钱包转向资金钱包
MAIN_OPTION 现货钱包转向期权钱包
OPTION_MAIN 期权钱包转向现货钱包
UMFUTURE_OPTION U本位合约钱包转向期权钱包
OPTION_UMFUTURE 期权钱包转向U本位合约钱包
MARGIN_OPTION 杠杆全仓钱包转向期权钱包
OPTION_MARGIN 期权全仓钱包转向杠杆钱包
FUNDING_OPTION 资金钱包转向期权钱包
OPTION_FUNDING 期权钱包转向资金钱包
MAIN_PORTFOLIO_MARGIN 现货钱包转向统一账户钱包
PORTFOLIO_MARGIN_MAIN 统一账户钱包转向现货钱包
MAIN_ISOLATED_MARGIN 现货钱包转向逐仓账户钱包
ISOLATED_MARGIN_MAIN 逐仓钱包转向现货账户钱包'''


# DEFINE a function to transfer coin from uer input accout type to another account type
def transfer_between_accounts(coin, amount, transfer_type, chat_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    try: amount = float(amount)
    except: return send_msg(f'Wrong amount: {amount}, please input a number.', chat_id)

    if transfer_type not in TRANSFER_TYPE:
        # make a string from TRANSFER_TYPE_DICT and sent to user
        reply_string = '\n'.join([f'{key}: {value}' for key, value in TRANSFER_TYPE_DICT.items()])
        return send_msg(f'Wrong transfer type: {transfer_type}, please choose from below:\n\n{reply_string}', chat_id)

    PATH = '/sapi/v1/asset/transfer'
    timestamp = int(time.time() * 1000)
    params = {
        'type': transfer_type,
        'asset': coin,
        'amount': amount,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.post(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200: return
        data = r.json()
        tranId = data['tranId']
        transfer_direction = TRANSFER_TYPE_DICT[transfer_type]
        return send_msg(f'{transfer_direction} Success, tranId: \n{tranId}', chat_id)
    except Exception as e:
        print(e)
        return
    

# 定义 MAIN_FUNDING 现货钱包转向资金钱包功能
def main_funding_transfer(coin, amount):
    PATH = '/sapi/v1/asset/transfer'
    timestamp = int(time.time() * 1000)
    params = {
        'type': 'MAIN_FUNDING',
        'asset': coin.upper(),
        'amount': amount,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.post(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200: return
        data = r.json()
        tranId = data['tranId']
        return tranId
    except Exception as e:
        print(e)
        return


# 通过用户input 的 coin 和 amount，调用 get_user_asset() 获取 asset / coin 的余额，如果余额大于 amount，则调用 main_funding_transfer(coin, amount) 转账
def main_funding_transfer_with_check_and_send(coin:str, amount, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    try: amount = float(amount)
    except: return send_msg(f'转账失败，您输入的转账数量: {amount} 不是数字。', from_id)

    df = get_user_asset()
    if not df.empty:
        df = df[df['asset'] == coin]
        if not df.empty:
            balance = float(df['free'].values[0])
            if balance >= amount: 
                tranId = main_funding_transfer(coin, amount)
                if tranId: return send_msg(f'已经成功将 {format_number(amount)} {coin} 从现货账户转入到资金账户, tranId: \n{tranId}', from_id)
            else: return send_msg(f'现货账户 {coin} 余额: {format_number(balance)} 小于转账数量: {format_number(amount)}', from_id)
        else: return send_msg(f'现货账户没有 {coin} 资产。', from_id)
    return send_msg(f'转账失败，可能是网络问题，请稍后再试。', from_id)


# 通过 get_funding_asset 检查资金账户中的 USDT 余额，如果存在 USDT 余额，则调用 funding_main_transfer_with_check_and_send(coin, amount) 将所有 USDT 余额转入到现货账户
def funding_main_transfer_all_usdt(from_id=TG_BOT_OWNER_ID):
    df = get_funding_asset()
    if not df.empty:
        df = df[df['asset'] == 'USDT']
        if not df.empty:
            amount = float(df['free'].values[0])
            if amount > 0: return funding_main_transfer_with_check_and_send('USDT', amount, from_id)
    return send_msg(f'No USDT asset in funding account.', from_id)


# 通过 get_funding_asset() 获取所有 coin 的余额并返回一个 dict key is asset, value is free
def get_coin_funding_balance_all():
    df = get_funding_asset()
    if not df.empty: 
        df = df[df['asset'] != 'NFT']
        return dict(zip(df['asset'].values, df['free'].values))
    else: return {}


# 通过 get_funding_asset() 获取某个 coin 的余额
def get_coin_funding_balance(coin):
    df = get_funding_asset()
    df = df[df['asset'] == coin.upper()]
    if not df.empty: return df['free'].values[0]
    else: return 0


# 币安统一账户查询, 用户持仓 (USER_DATA), 获取用户持仓, 仅返回>0的数据。权重(IP): 5
# POST /sapi/v3/asset/getUserAsset 
def get_user_asset():
    PATH = '/sapi/v3/asset/getUserAsset'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.post(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200:
            print(r)
            return
        data = pd.DataFrame(r.json())
        return data
    except Exception as e:
        print(e)
        return
'''
   asset            free locked freeze withdrawing ipoable btcValuation
0   AKRO          124370      0      0           0       0            0
1   API3           585.1      0      0           0       0            0
2   ASTR         13229.6      0      0           0       0            0
3    BNB       3.1130512      0      0           0       0            0
4   CELO            1560      0      0           0       0            0
5   FLOW         1210.65      0      0           0       0            0
6   MANA            2107      0      0           0       0            0
7    OMG          1331.5      0      0           0       0            0
8    SXP          2402.3      0      0           0       0            0
9   USDT  35404.13927066      0      0           0       0            0
10   XEC        28953771      0      0           0       0            0
'''


# 通过 get_user_asset() 获取所有 coin 的余额并返回一个 dict key is asset, value is free
def get_coin_wallet_balance_all():
    df = get_user_asset()
    if not df.empty: return dict(zip(df['asset'].values, df['free'].values))
    else: return {}
'''{'AKRO': '124370', 'API3': '585.1', 'ASTR': '13229.6', 'BNB': '3.1130512', 'CELO': '1560', 'FLOW': '1210.65', 'MANA': '2107', 'OMG': '1331.5', 'SXP': '2402.3', 'USDT': '35404.13927066', 'XEC': '28953771'}'''


def get_coin_wallet_balance_with_locked():
    df = get_user_asset()
    if not df.empty: return dict(zip(df['asset'].values, df['free'].values + df['locked'].values))
    else: return {}


def get_coin_wallet_balance_all_str(chat_id=TG_BOT_OWNER_ID):
    df_balance_all = pd.DataFrame(engine.connect().execute(text('SELECT coin, executedQty FROM binance_position_buy WHERE is_closed = 0')).fetchall())
    ''' df_balance_all
        symbol     orderId  orderListId           clientOrderId   transactTime       price         origQty     executedQty cummulativeQuoteQty  status timeInForce    type side    workingTime selfTradePreventionMode  coin  buy_cost_bnb  buy_bnb_price  update_id  is_closed
    0  SANDUSDT  2766936618           -1  k4H1XOehj8sOh3Z9FJpXCS  1702238418107    0.548528  18230.00000000  18230.00000000       9999.66300000  FILLED         GTC  MARKET  BUY  1702238418107            EXPIRE_MAKER  SAND      0.031214          240.1          5          0
    1  RUNEUSDT  1250812918           -1  UzouLOzpJKumY2DB2C5kOz  1702238420773    6.598612   1515.40000000   1515.40000000       9999.53610000  FILLED         GTC  MARKET  BUY  1702238420773            EXPIRE_MAKER  RUNE      0.031195          240.0          6          0
    2  AAVEUSDT  1508986082           -1  jUZBtFcfMtPYX73iAb5MqI  1702658512922  109.138053     91.62700000     91.62700000       9999.99235000  FILLED         GTC  MARKET  BUY  1702658512922            EXPIRE_MAKER  AAVE      0.030264          246.6         11          0
    '''
    if not df_balance_all.empty:
        # Coins in position, make a dict from df_balance_all with key is coin, value is executedQty
        coin_in_position_dict = dict(zip(df_balance_all['coin'].values, df_balance_all['executedQty'].values))
        coin_in_position_str = '\n'.join([f"{key}: {format_number(value)}" for key, value in coin_in_position_dict.items()])
        send_msg(f"Coins in position:\n\n{coin_in_position_str}", chat_id)
    else: 
        coin_in_position_dict = {}
        send_msg("No coins in position.", chat_id)
        try: binance_adjust_profit(chat_id)
        except: pass

    data = get_coin_wallet_balance_with_locked()
    if data: 
        '''{'AAVE': '091.627', 'BNB': '2.014138090', 'OGN': '0.58882430', 'ONG': '140000', 'RSR': '0.099999980', 'RUNE': '01515.4', 'SAND': '018230', 'USDT': '71305.788331640'}'''
        # Coins in balance except coins in position
        coin_in_balance_dict = {key: value for key, value in data.items() if key not in coin_in_position_dict.keys()}
        coin_in_balance_str = '\n'.join([f"{key}: {format_number(value)}" for key, value in coin_in_balance_dict.items()])
        send_msg(f"Other coins in balance:\n\n{coin_in_balance_str}", chat_id)
        return
    
    else: return send_msg("No balance in your binance spot wallet.", chat_id)


# 通过 get_user_asset() 获取某个 coin 的余额
def get_coin_wallet_balance(coin):
    df = get_user_asset()
    df = df[df['asset'] == coin.upper()]
    if not df.empty: return float(df['free'].values[0])
    else: return 0


# 通过 get_token_price_table() 获取某个 coin 的价格
def get_token_price(coin: str, from_id=None):
    df = get_token_price_table()
    df = df[df['coin'] == coin.upper()]
    if not df.empty: 
        if from_id: send_msg(f"Current price of {coin.upper()}: {format_number(df['lastPrice'].values[0])} usdt\n\nCurrent time: {datetime.now().strftime('%Y-%m-%d %H:%M')}", from_id)
        return float(df['lastPrice'].values[0])
    else: return 0
'''235.8'''


# 获取给定 hours 小时内的充值记录并发送给 chat_id
def get_deposit_history_by_hours(chat_id=TG_BOT_OWNER_ID, hours=1):
    hours = float(hours)
    PATH = '/sapi/v1/capital/deposit/hisrec'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp,
        'startTime': int(timestamp - 60*60*1000*hours),
        'endTime': timestamp,
        'limit': 1000
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)

    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        df = pd.DataFrame(data)
        if not df.empty:
            df = df.loc[:, ['coin', 'amount', 'address', 'txId', 'insertTime', 'status']]
            df = df.rename(columns={'coin': 'Coin_Name', 'amount': 'Coin_Amount', 'address': 'From_Address', 'txId': 'Hash_ID', 'insertTime': ' UTC_Time', 'status': 'Status'})
            for i in range(df.shape[0]):
                '''status (0:pending,6: credited but cannot withdraw,7=Wrong Deposit,8=Waiting User confirm,1:success)'''
                df.loc[i, 'Status'] = 'pending' if df.loc[i, 'Status'] == 0 else 'success' if df.loc[i, 'Status'] == 1 else 'credited but cannot withdraw' if df.loc[i, 'Status'] == 6 else 'Wrong Deposit' if df.loc[i, 'Status'] == 7 else 'Waiting User confirm' if df.loc[i, 'Status'] == 8 else 'unknown'
                df.loc[i, ' UTC_Time'] = datetime.fromtimestamp(df.loc[i, ' UTC_Time']/1000).strftime('%Y-%m-%d %H:%M:%S')

                # convert df.loc[i] to dict
                df_dict = df.loc[i].to_dict()

                # Convert dict to str
                df_str = '\n'.join([f"{k}: {v}" for k, v in df_dict.items()])
                
                send_msg(df_str, chat_id)

            return True

    return 


def get_deposit_history():
    PATH = '/sapi/v1/capital/deposit/hisrec'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        df = pd.DataFrame(data)
        if not df.empty: 
            df_status_is_1 = df.loc[df['status']==1]
            if not df_status_is_1.empty: return df_status_is_1
    return
''' return from get_deposit_history():
                    id       amount  coin network  status                                     address addressTag                                               txId     insertTime  transferType confirmTimes  unlockConfirm  walletType
0  3384656949630549249        20950  USDT     ETH       1  0x34b940120aeb9cadbcc4131fb034ad3b83b0367d             0xb8a5941af952614b162323ee45c8b5a9471acb080443...  1679699675000             0        12/12             64           0
1  3367562419265538306  34.18681232   BTC     BTC       1          18a9tpwtVZsMUaU5cT2vYffo2vCFhwsop5             dd90460ca3d7d2817a1577180ab9ca0b707e9f0c4f72ef...  1678680762000             0          1/1              2           0
2  3364526220028378113        70000  USDT     ETH       1  0x34b940120aeb9cadbcc4131fb034ad3b83b0367d             0xc8270959e315ca2e8c45dc90624854e971735fc24d88...  1678499790000             0        12/12             64           0
3  3364522261393931265        90000  USDT     ETH       1  0x34b940120aeb9cadbcc4131fb034ad3b83b0367d             0x0fb0d5ec3cb4b7e71c52981d11b03b9c22e0ef228b67...  1678499554000             0        12/12             64           0
4  3364516246678109184        50000  USDT     ETH       1  0x34b940120aeb9cadbcc4131fb034ad3b83b0367d             0x1a3981c917d413117ac7a5bfe5f71d6f24abe7028fa7...  1678499196000             0        12/12             64           0
5  3364514171839806464       150000  USDT     ETH       1  0x34b940120aeb9cadbcc4131fb034ad3b83b0367d             0xa805da4d6c0dbe5ae4dbcedd522fd476e436d5f68abb...  1678499072000             0        12/12             64           0
6  3364506118323141633       130000  USDT     ETH       1  0x34b940120aeb9cadbcc4131fb034ad3b83b0367d             0xe06e748630f036e600a31db6756cb2c7769b62eaf542...  1678498592000             0        12/12             64           0
7  3364494037502884864       110000  USDT     ETH       1  0x34b940120aeb9cadbcc4131fb034ad3b83b0367d             0x057559b3f99af4f8b8fdaa3a2da93a85f05845e6c629...  1678497872000             0        12/12             64           0
8  3364481977083722753       100000  USDT     ETH       1  0x34b940120aeb9cadbcc4131fb034ad3b83b0367d             0x79f101b1b102be0bd071a86b6fe06a1bc77e0011ae7a...  1678497153000             0        12/12             64           0
'''


'''获取提币历史 (支持多网络) (USER_DATA) 权重(IP): 1
GET /sapi/v1/capital/withdraw/history (HMAC SHA256)
status = (0:已发送确认Email,1:已被用户取消 2:等待确认 3:被拒绝 4:处理中 5:提现交易失败 6 提现完成)
https://binance-docs.github.io/apidocs/spot/cn/#user_data-6
GET /sapi/v1/capital/withdraw/history (HMAC SHA256)
参数:
名称	类型	是否必需	描述
coin	STRING	NO	
withdrawOrderId	STRING	NO	
status	INT	NO	0(0:已发送确认Email,1:已被用户取消 2:等待确认 3:被拒绝 4:处理中 5:提现交易失败 6 提现完成)
offset	INT	NO	
limit	INT	NO	默认: 1000, 最大, 1000
startTime	LONG	NO	默认当前时间90天前的时间戳
endTime	LONG	NO	默认当前时间戳
recvWindow	LONG	NO	
timestamp	LONG	YES
'''


# 获取给定 hours 小时内的提币记录并发送给 chat_id
def get_withdraw_history_by_hours(chat_id=TG_BOT_OWNER_ID, hours=1):
    hours = float(hours)
    PATH = '/sapi/v1/capital/withdraw/history'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp,
        'startTime': int(timestamp - 60*60*1000*hours),
        'endTime': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        df = pd.DataFrame(data)
        if not df.empty: 
            df = df.loc[:, ['coin', 'amount', 'address', 'txId', 'applyTime', 'status']]
            df = df.rename(columns={'coin': '提币名称', 'amount': '提币数量', 'address': '目标地址', 'txId': '链上哈希', 'applyTime': ' UTC时间', 'status': '提币状态'})
            for i in range(df.shape[0]):
                '''status = (0:已发送确认Email,1:已被用户取消 2:等待确认 3:被拒绝 4:处理中 5:提现交易失败 6 提现完成), 将 status 转换成中文'''
                df.loc[i, '提币状态'] = '已发送确认Email' if df.loc[i, '提币状态'] == 0 else '已被用户取消' if df.loc[i, '提币状态'] == 1 else '等待确认' if df.loc[i, '提币状态'] == 2 else '被拒绝' if df.loc[i, '提币状态'] == 3 else '处理中' if df.loc[i, '提币状态'] == 4 else '提现交易失败' if df.loc[i, '提币状态'] == 5 else '提现完成'
                # 将 df.loc[i] 转换成 dict
                df_dict = df.loc[i].to_dict()
                # 将 dict 转换成 str
                df_str = '\n'.join([f"{k}: {v}" for k, v in df_dict.items()])
                # 发送给 chat_id
                send_msg(df_str, chat_id)
            return True
        # else: send_msg(f'No withdraw history in the past {hours} hours.', chat_id)
    return
'''
                                 id amount transactionFee  coin  status                                     address                                               txId            applyTime network  transferType                                        info  confirmNo  walletType txKey         completeTime
0  47601e0a25c847e1ac4f3d55a0e42c9b     10              1  USDT       6          TGgqTRjJxTVCVq7QsxfjvKVhdUKM4yTmtP  6308c7dcd2f755a5784f39fa1de8b6b31c02fba39fb63a...  2023-06-04 17:25:40     TRX             0          TAzsQ9Gx8eqFNFSKbeXrbi45CuVPHzA8wr         50           0        2023-06-04 17:27:42
1  bd7e16c6d2a240e1b2f86b970f45a623     10           0.29  USDT       6  0xb411B974c0ac75C88E5039ea0bf63a84aa7B5377  0xe19ad98e9f6ec2964a5de27eff46d0434282966b6929...  2023-06-03 22:10:54     BSC             0  0xa180fe01b906a1be37be6c534a3300785b20d947         20           0        2023-06-03 22:12:40'''


# 获取最近三个月的提币记录（默认）
def get_withdraw_history():
    PATH = '/sapi/v1/capital/withdraw/history'
    timestamp = int(time.time() * 1000)
    params = {'timestamp': timestamp}
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        df = pd.DataFrame(data)
        if not df.empty:
            df_status_is_6 = df.loc[df['status']==6]
            if not df_status_is_6.empty: return df_status_is_6
    return
'''
                                 id  amount transactionFee  coin  ...  confirmNo walletType txKey         completeTime
0  91e7db66a9474cbd9853dbf29f47a716    1000              1  USDT  ...         50          0        2023-12-03 16:50:43
1  fc328dd25399442cad86765c6a4abf9a    1000              1  USDT  ...         50          0        2023-12-03 16:46:41
2  c732a1766d1f4a23b1d81cfe3130d762      10              1  USDT  ...         50          0        2023-12-03 16:42:42
3  0c12df3c0f124cdc9af0ba607c5b291c  200000              5  USDT  ...        128          0        2023-11-27 02:44:41
'''


'''提币 (USER_DATA)
Parameters:

Name	Type	Mandatory	Description
coin	STRING	YES	
withdrawOrderId	STRING	NO	client id for withdraw
network	STRING	NO	
address	STRING	YES	
addressTag	STRING	NO	Secondary address identifier for coins like XRP,XMR etc.
amount	DECIMAL	YES	
transactionFeeFlag	BOOLEAN	NO	When making internal transfer, true for returning the fee to the destination account; false for returning the fee back to the departure account. Default false.
name	STRING	NO	Description of the address. Space in name should be encoded into %20.
walletType	INTEGER	NO	The wallet type for withdraw, 0-spot wallet, 1-funding wallet. Default walletType is the current "selected wallet" under wallet->Fiat and Spot/Funding->Deposit
recvWindow	LONG	NO	
timestamp	LONG	YES
'''
# Withdraw from binance to other address
def binance_withdraw(amount, network, coin, address):
    PATH = '/sapi/v1/capital/withdraw/apply'
    timestamp = int(time.time() * 1000)
    params = {
        'coin': coin,
        'address': address,
        'amount': amount,
        'network': network,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.post(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        return data
    else: return r.reason
''' return from binance_withdraw('eth', 0.1, '0xb411B974c0ac75C88E5039ea0bf63a84aa7B5377'):
{
    "id":"7213fea8e94b4a5593d507237e5a555b"
}
'''

# difine a binance_send_coin function for bot to call
def binance_send_coin(amount: float, network: str, coin: str, address: str, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    try: amount = float(amount)
    except: return send_msg(f'You need to input a number for amount, but you input: {amount}', from_id)

    df_usdt_balance = get_user_asset()
    df_usdt_balance = df_usdt_balance[df_usdt_balance['asset']==coin]
    if df_usdt_balance.empty: return send_msg(f'No {coin} in your binance wallet. \n\n/get_wallet_balance', from_id)
    
    balance = float(df_usdt_balance['free'].values[0])
    if balance < amount: return send_msg(f'{coin} balance is {balance}, which is not sufficient for {format_number(amount)}.', from_id)

    # change network name 
    network = network_name_change(network)

    # Check if the network is supported
    r = check_coin_network(coin, network)
    '''{'status': False, 'network_list': networkList}'''
    if not r.get('status'): return send_msg(f"Input network: {network} is not supported for {coin}. \n\nSupported networks are:\n{', '.join(r.get('network_list'))}", from_id)
    
    checksum_address = address
    
    # Polish address to checksum address
    if network in USDT_ETH_COMPATIBLE_NETWORK_LIST:
        try: checksum_address = web3.to_checksum_address(address)
        except Exception as e: return send_msg(f'Invalid address: {e}', from_id)

    withdraw_id_self = generate_token()
    withdraw_token = f"withdraw-{withdraw_id_self}"
    # Prepare data = {} to a dataframe and append to table binance_withdraw_task
    data = {
        'coin': coin,
        'amount': amount,
        'network': network,
        'to_address': checksum_address,
        'from_id': from_id,
        'withdraw_id_self': withdraw_id_self,
        'created_at': datetime.now(),
        'withdraw_id_binance': 'waiting_for_update'
    }

    df = pd.DataFrame(data, index=[0])
    df.to_sql('binance_withdraw_task', engine, if_exists='append', index=False)

    # del status, withdraw_id_binance, withdraw_id_self,from_id, created_at, updated_at from data
    del data['withdraw_id_binance']
    del data['withdraw_id_self']
    del data['from_id']
    del data['created_at']

    string_dict = '\n'.join([f'{k}: {v}' for k, v in data.items()])
    reply_string_from_dict = f"Please confirm the following withdraw task:\n\n{string_dict}\n\nYou can reply: \n/confirm {withdraw_id_self}\n\nOr click the following link to confirm"
    send_msg(reply_string_from_dict, from_id)

    confirm_link_markdown = f"[CONFIRM_WITHDRAW](https://wh.leowang.net/confirmation/{withdraw_token})"
    send_msg_markdown(confirm_link_markdown, from_id)

    return


def update_binance_withdraw_task(withdraw_id_self, withdraw_id_binance):
    connection = engine.connect()
    transaction = connection.begin()
    try:
        connection.execute(text(f"UPDATE binance_withdraw_task SET withdraw_id_binance = '{withdraw_id_binance}' WHERE withdraw_id_self = '{withdraw_id_self}'"))
        transaction.commit()
    except Exception as e: print(f'Failed to update binance_withdraw_task\n\n{e}')
    return 

# define a function to read binance_withdraw_task where status = 'pending' and withdraw_id_binance = 'waiting_for_update' and withdraw_id_self = given token, if exist, call bianance_withdraw() and update withdraw_id_binance, status, updated_at
def binance_withdraw_task_update(token, from_id=TG_BOT_OWNER_ID):
    # df = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_withdraw_task')).fetchall())

    try:
        df = pd.DataFrame(engine.connect().execute(text(f"SELECT * FROM binance_withdraw_task WHERE withdraw_id_self = '{token}' AND withdraw_id_binance = 'waiting_for_update'")).fetchall())
        if df.empty: 
            reply_msg = f'No withdraw task with token: {token}'
            send_msg(reply_msg, from_id)
            return reply_msg
    except: 
        reply_msg = f'binance_withdraw_task table not exist.'
        send_msg(reply_msg, from_id)
        return reply_msg

    # print(f"binance_withdraw_task_update():\n\n{df}\n\n")
    '''   coin  amount network                          to_address     from_id        withdraw_id_self          created_at withdraw_id_binance
        0  USDT   100.0     TRX  TQKgU4QRWpfoUYBno6dG8USABkeYQRvQ72  2118900665  u7s6TSq7EzLsWYNFzwFAQw 2023-12-21 19:05:21  waiting_for_update'''

    amount = float(df['amount'].values[0])
    network = df['network'].values[0]
    coin = df['coin'].values[0]
    address = df['to_address'].values[0]

    try:
        data = binance_withdraw(amount, network, coin, address)
        if data.get('id'):
            update_binance_withdraw_task(token, data.get('id'))
            # update_binance_withdraw_task('u7s6TSq7EzLsWYNFzwFAQw', 'a97b825669b94c0c9b2658c34ac5d6dc')
            reply_msg = f"Withdraw task with token: {token} is confirmed and updated.\n\nWithdraw ID from Binance: {data.get('id')}"
            send_msg(reply_msg, from_id)
            return reply_msg
        else: return 'Failed to withdraw.'
    except Exception as e: 
        send_msg(f'Error for calling binance_withdraw(): \n\n{e}', from_id)
        print(e)
        return f"Error:\n\n{e}"


# handle webhook task tokens, recieve task token from webhook and split with the first '-', first half is the identification fo a function, second half is the token for the validation of the task
def handle_webhook_confirmation(token: str, from_id=TG_BOT_OWNER_ID):

    token_list = token.split('-', 1)
    target_function = token_list[0].lower()
    task_token = token_list[1]

    if target_function == 'withdraw': return binance_withdraw_task_update(task_token, from_id)

    return


# Define binance_pay_usdt, user input a usdt amount and a target address; then market sell coin ONG for this target usdt amount, and send the USDT to the target address with TRX network only, usdt input must less than 1000 usd.
def binance_pay_usdt(usdt_amount: float, target_address: str, from_id=TG_BOT_OWNER_ID):
    try: usdt_amount = float(usdt_amount)
    except: return send_msg(f'You need to input a number for amount, but you input: {usdt_amount}', from_id)

    if usdt_amount > 1000: return send_msg(f'You can only pay less than 1000 usdt, but you input: {usdt_amount}', from_id)

    '''TRX_REGEX = r'T[1-9A-HJ-NP-Za-km-z]{33}'''
    # CHECK IF target_address IS A VALID TRX ADDRESS
    if not re.match(TRX_REGEX, target_address): return send_msg(f'Invalid TRX address: {target_address}', from_id)

    # Get ONG price
    ong_price = get_token_price('ONG')
    if ong_price == 0: return send_msg(f'Can not get ONG price.', from_id)

    # Calculate ONG amount
    ong_amount = usdt_amount / ong_price

    # Get ONG balance
    ong_balance = get_coin_wallet_balance('ONG')
    if ong_balance == 0: return send_msg(f'No ONG in your binance wallet. \n\n/get_wallet_balance', from_id)

    polish_parameters = polish_parameters_for_limit_order('ONG', ong_amount, ong_price, from_id)
    if not polish_parameters: return send_msg(f'Failed to polish parameters for ONG market sell', from_id)

    ong_amount = polish_parameters['amount']

    # Check if ONGUSDT balance is sufficient
    if ong_balance < ong_amount: return send_msg(f'ONG balance is {ong_balance}, which is not sufficient for {ong_amount}.', from_id)

    # Market sell ONG for USDT
    data = binance_market_sell('ONG', ong_amount)
    if not data: return send_msg(f'Failed to market sell ONG for USDT.', from_id)

    del data['fills']

    df = pd.DataFrame(data, index=[0])
    df.to_sql('binance_ong_sell_history', engine, if_exists='append', index=False)
    print(f"Market sell ONG for USDT:\n\n{df}\n\n")

    # withdraw USDT to target address
    return binance_send_coin(usdt_amount, 'TRX', 'USDT', target_address, from_id)


'''获取充值地址 (支持多网络) (USER_DATA)
GET /sapi/v1/capital/deposit/address (HMAC SHA256)
参数:
名称	类型	是否必需	描述
coin	STRING	YES	
network	STRING	NO	
recvWindow	LONG	NO	
timestamp	LONG	YES
'''
# 定义一个功能，获取给定 coin 给定 network 的充值地址
def binance_get_coin_deposit_address(coin, network):
    PATH = '/sapi/v1/capital/deposit/address'
    timestamp = int(time.time() * 1000)
    params = {
        'coin': coin,
        'network': network,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        return data
    else: return r.reason
'''{'coin': 'USDT', 'address': '0x34b940120aeb9cadbcc4131fb034ad3b83b0367d', 'tag': '', 'url': 'https://etherscan.io/address/0x34b940120aeb9cadbcc4131fb034ad3b83b0367d'}'''


def get_coin_deposit_address(coin: str, network: str, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    network = network.upper()

    data = binance_get_coin_deposit_address(coin.upper(), network)
    '''data : {'coin': 'USDT', 'address': 'TTiayzuQ6hA8spUtWTsmfFD7nMDxcw33hV', 'tag': '', 'url': 'https://tronscan.org/#/address/TTiayzuQ6hA8spUtWTsmfFD7nMDxcw33hV'}'''

    address = data['address']
    url = data['url']

    if data: return send_msg(f"Binance Deposit Address for {coin} at {network}\n\n{address}\n\n{url}", from_id)
    else: return send_msg(f"Can't get {coin.upper()} deposit address.", from_id)


'''
权重(UID): 1 权重(IP): 1

参数:

名称	类型	是否必需	描述
symbol	STRING	YES	
side	ENUM	YES	详见枚举定义：订单方向
type	ENUM	YES	详见枚举定义：订单类型
timeInForce	ENUM	NO	详见枚举定义：有效方式
quantity	DECIMAL	NO	
quoteOrderQty	DECIMAL	NO	
price	DECIMAL	NO	
newClientOrderId	STRING	NO	客户自定义的唯一订单ID。 如果未发送，则自动生成。
stopPrice	DECIMAL	NO	仅 STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT 和 TAKE_PROFIT_LIMIT 需要此参数。
trailingDelta	LONG	NO	用于 STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT 和 TAKE_PROFIT_LIMIT 类型的订单。更多追踪止盈止损订单细节, 请参考 追踪止盈止损(Trailing Stop)订单常见问题。
icebergQty	DECIMAL	NO	仅使用 LIMIT, STOP_LOSS_LIMIT, 和 TAKE_PROFIT_LIMIT 创建新的 iceberg 订单时需要此参数。
newOrderRespType	ENUM	NO	设置响应JSON。ACK，RESULT 或 FULL；MARKET 和 LIMIT 订单类型默认为 FULL，所有其他订单默认为 ACK。
selfTradePreventionMode	ENUM	NO	允许的 ENUM 取决于交易对的配置。支持的值有 EXPIRE_TAKER，EXPIRE_MAKER，EXPIRE_BOTH，NONE。
strategyId	INT	NO	
strategyType	INT	NO	不能低于 1000000
recvWindow	LONG	NO	赋值不能大于 60000
timestamp	LONG	YES'''


# 定义一个Market sell 交易功能 Input: coin, amount
def binance_market_sell(coin: str, amount):
    coin = coin.upper()
    symbol = coin + 'USDT' if not coin.endswith('USDT') else coin

    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    
    params = {
        'symbol': symbol,
        'side': 'SELL',
        'type': 'MARKET',
        'quantity': amount,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.post(url, headers=BINANCE_HEADERS, params=params)
    print(r)

    if r.status_code == 200:
        data = r.json()
        time.sleep(1)
        return data
    else: 
        print(r.reason)
        return
'''
{
  "symbol": "CAKEUSDT",
  "orderId": 513572490,
  "orderListId": -1,
  "clientOrderId": "zCg1E3eUBhiLWtMI17xtjn",
  "transactTime": 1685855174465,
  "price": "0.00000000",
  "origQty": "571.00000000",
  "executedQty": "571.00000000",
  "cummulativeQuoteQty": "999.24718000",
  "status": "FILLED",
  "timeInForce": "GTC",
  "type": "MARKET",
  "side": "SELL",
  "workingTime": 1685855174465,
  "fills": [
    {
      "price": "1.75000000",
      "qty": "46.92000000",
      "commission": "0.00020124",
      "commissionAsset": "BNB",
      "tradeId": 73422414
    },
    ...
  ],
  "selfTradePreventionMode": "NONE"
}
'''    


# 定义一个 Limit sell 交易功能 Input: coin, amount, price
def binance_limit_sell(coin, amount, price):
    coin = coin.upper()
    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': coin + 'USDT',
        'side': 'SELL',
        'type': 'LIMIT',
        'quantity': amount,
        'price': price,
        'timeInForce': 'GTC',
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.post(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        time.sleep(1)
        return data
    else: 
        print(r.json())
        return
'''binance_limit_sell('SAND', 18230, 0.55)
{'symbol': 'SANDUSDT', 'orderId': 2769384671, 'orderListId': -1, 'clientOrderId': 'GKVPOrFIkwz5IbsRhsx220', 'transactTime': 1702318694019, 'price': '0.55000000', 'origQty': '18230.00000000', 'executedQty': '0.00000000', 'cummulativeQuoteQty': '0.00000000', 'status': 'NEW', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'SELL', 'workingTime': 1702318694019, 'fills': [], 'selfTradePreventionMode': 'EXPIRE_MAKER'}
'''


'''撤销订单 (TRADE)
响应

{
  "symbol": "LTCBTC",
  "origClientOrderId": "myOrder1",
  "orderId": 4,
  "orderListId": -1, // OCO订单ID，否则为 -1
  "clientOrderId": "cancelMyOrder1",
  "transactTime": 1684804350068,
  "price": "2.00000000",
  "origQty": "1.00000000",
  "executedQty": "0.00000000",
  "cummulativeQuoteQty": "0.00000000",
  "status": "CANCELED",
  "timeInForce": "GTC",
  "type": "LIMIT",
  "side": "BUY",
  "selfTradePreventionMode": "NONE"
}
DELETE /api/v3/order

取消有效订单。

权重(IP): 1

参数:

名称	类型	是否必需	描述
symbol	STRING	YES	
orderId	LONG	NO	
origClientOrderId	STRING	NO	
newClientOrderId	STRING	NO	用户自定义的本次撤销操作的ID(注意不是被撤销的订单的自定义ID)。如无指定会自动赋值。
cancelRestrictions	ENUM	NO	支持的值:
ONLY_NEW - 如果订单状态为 NEW，订单取消将成功。
ONLY_PARTIALLY_FILLED - 如果订单状态为 PARTIALLY_FILLED，订单取消将成功。
recvWindow	LONG	NO	赋值不得大于 60000
timestamp	LONG	YES	
orderId 或 origClientOrderId 必须至少发送一个
'''

# Define a function to cancel an order
def binance_cancel_order(coin: str, clientOrderId):
    coin = coin.upper()
    symbol = coin if coin.endswith('USDT') else coin + 'USDT'

    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': symbol,
        'origClientOrderId': clientOrderId,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.delete(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        time.sleep(1)
        return data
    else: 
        print(r.json())
        return


'''查询订单 (USER_DATA)
响应

{
  "symbol": "LTCBTC", // 交易对
  "orderId": 1, // 系统的订单ID
  "orderListId": -1, // OCO订单的ID，不然就是-1
  "clientOrderId": "myOrder1", // 客户自己设置的ID
  "price": "0.1", // 订单价格
  "origQty": "1.0", // 用户设置的原始订单数量
  "executedQty": "0.0", // 交易的订单数量
  "cummulativeQuoteQty": "0.0", // 累计交易的金额
  "status": "NEW", // 订单状态
  "timeInForce": "GTC", // 订单的时效方式
  "type": "LIMIT", // 订单类型， 比如市价单，现价单等
  "side": "BUY", // 订单方向，买还是卖
  "stopPrice": "0.0", // 止损价格
  "icebergQty": "0.0", // 冰山数量
  "time": 1499827319559, // 订单时间
  "updateTime": 1499827319559, // 最后更新时间
  "isWorking": true, // 订单是否出现在orderbook中
  "workingTime":1499827319559,
  "origQuoteOrderQty": "0.000000", // 原始的交易金额
  "selfTradePreventionMode": "NONE"
}
GET /api/v3/order

查询订单状态。

权重(IP): 4

参数:

名称	类型	是否必需	描述
symbol	STRING	YES	
orderId	LONG	NO	
origClientOrderId	STRING	NO	
recvWindow	LONG	NO	赋值不得大于 60000
timestamp	LONG	YES	
注意:

至少需要发送 orderId 与 origClientOrderId中的一个
某些订单中cummulativeQuoteQty<0，是由于这些订单是cummulativeQuoteQty功能上线之前的订单。
响应示例没有显示所有可以出现的字段，更多请看 "订单响应中的特定条件时才会出现的字段" 部分。
数据源: 数据库
'''
def check_order_status(coin, clientOrderId):
    coin = coin.upper()
    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': coin + 'USDT',
        'origClientOrderId': clientOrderId,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        return data
    else: 
        print(r.json())
        return

'''{
  "symbol": "LTCBTC", // 交易对
  "orderId": 1, // 系统的订单ID
  "orderListId": -1, // OCO订单的ID，不然就是-1
  "clientOrderId": "myOrder1", // 客户自己设置的ID
  "price": "0.1", // 订单价格
  "origQty": "1.0", // 用户设置的原始订单数量
  "executedQty": "0.0", // 交易的订单数量
  "cummulativeQuoteQty": "0.0", // 累计交易的金额
  "status": "NEW", // 订单状态
  "timeInForce": "GTC", // 订单的时效方式
  "type": "LIMIT", // 订单类型， 比如市价单，现价单等
  "side": "BUY", // 订单方向，买还是卖
  "stopPrice": "0.0", // 止损价格
  "icebergQty": "0.0", // 冰山数量
  "time": 1499827319559, // 订单时间
  "updateTime": 1499827319559, // 最后更新时间
  "isWorking": true, // 订单是否出现在orderbook中
  "workingTime":1499827319559,
  "origQuoteOrderQty": "0.000000", // 原始的交易金额
  "selfTradePreventionMode": "NONE"
}'''


'''当前挂单 (USER_DATA)
响应

[
  {
    "symbol": "LTCBTC",
    "orderId": 1,
    "orderListId": -1, // OCO订单ID，否则为 -1
    "clientOrderId": "myOrder1",
    "price": "0.1",
    "origQty": "1.0",
    "executedQty": "0.0",
    "cummulativeQuoteQty": "0.0",
    "status": "NEW",
    "timeInForce": "GTC",
    "type": "LIMIT",
    "side": "BUY",
    "stopPrice": "0.0",
    "icebergQty": "0.0",
    "time": 1499827319559,
    "updateTime": 1499827319559,
    "isWorking": true,
    "workingTime": 1499827319559,
    "origQuoteOrderQty": "0.000000",
    "selfTradePreventionMode": "NONE"
  }
]
GET /api/v3/openOrders

获取交易对的所有当前挂单， 请小心使用不带交易对参数的调用。

权重(IP): 6 单一交易对;
80 交易对参数缺失;

参数:

名称	类型	是否必需	描述
symbol	STRING	NO	
recvWindow	LONG	NO	赋值不得大于 60000
timestamp	LONG	YES	
不带symbol参数，会返回所有交易对的挂单
数据源: 数据库

注意: 响应示例没有显示所有可以出现的字段，更多请看 "订单响应中的特定条件时才会出现的字段" 部分。
'''

# Define a function to get open orders list for all coin and make it a dataframe
def get_open_orders_list(from_id=None):
    PATH = '/api/v3/openOrders'
    timestamp = int(time.time() * 1000)
    params = {'timestamp': timestamp}
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        df = pd.DataFrame(data)
        if df.empty: return {}

        # select only the coin and clientOrderId, make a dict {symbol: clientOrderId}
        df = df.loc[:, ['symbol', 'clientOrderId']]
        df_dict = df.set_index('symbol').to_dict()['clientOrderId']

        if from_id:
            df_dict_string = '\n'.join([f"{k}: {v}" for k, v in df_dict.items()])
            send_msg(df_dict_string, from_id)

        return df_dict
    else: 
        print(r.json())
        return {}
''' Output dict:
{
  "FTTUSDT": "7w4KnO7kH4A4kupqItZT5x"
}
'''


# Define a function to sell all of the profit position
def close_postive_positions(from_id=TG_BOT_OWNER_ID):
    return send_msg('Just use /set_target_profit to set the target profit to 0: "/set_target_profit 00.1" or "stp 0.01". This is equal to close all positive positions, calling market sell to close positions that are with 0.01 profit. Or use /limit_sell_order to set limit orders for all positions: "/set_limit_sell 0.01" or "sls 0", waiting for the price to reach the buy in price to sell.\n\nRemember to use /cancel_all_orders first then others.', from_id)
    

# 定义一个 do_limit_sell 功能，输入 coin, 从数据库中读取 binance_position_buy 中 coin == coin, is_closed == 0 的记录, 按照 price 从小到大排序, 取第一条记录, 用这条记录的 amount, update_id, buy_cost_value, buy_cost_bnb, buy_bnb_price, open_position_time, 调用 binance_limit_sell(coin, amount, price)
def do_limit_sell(coin: str, target_profit_ratio=0.05):
    coin = coin.upper()
    reply_msg = ''
    # 读取 binance_position_buy 中 coin == coin, is_closed == 0 的记录, 按照 price 从小到大排序, 取第一条记录

    try:
        df_balance = pd.DataFrame(engine.connect().execute(text("SELECT * FROM binance_position_buy WHERE coin = :coin AND is_closed = 0 ORDER BY price ASC LIMIT 1"), {'coin': coin}).fetchall())
        if df_balance.empty: reply_msg = f'No open position for coin: {coin}'
    except: reply_msg = f'No open position for coin: {coin}'

    if reply_msg: return reply_msg

    amount = float(df_balance['executedQty'].values[0])
    buy_cost_value = float(df_balance['cummulativeQuoteQty'].values[0])

    # check coin balance see if it is enough
    df_coin_balance = get_user_asset()
    df_coin_balance = df_coin_balance[df_coin_balance['asset']==coin]
    if df_coin_balance.empty: 
        reply_msg = f'No balance for coin: {coin}'
        return reply_msg
    
    balance = float(df_coin_balance['free'].values[0])
    if balance < amount: 
        reply_msg = f'Balance {balance} is not enough for amount: {amount}'
        return reply_msg

    target_price = buy_cost_value * (1 + target_profit_ratio) / amount
    target_price = round(target_price, 4)

    try:
        data = binance_limit_sell(coin, amount, target_price)
        if not data: 
            reply_msg = f'Failed to do limit sell for coin: {coin}'
            return reply_msg
        
        print(json.dumps(data, indent=2))
        return data
    except Exception as e:
        print(f"An error occurred while doing limit sell order setup for {coin}: \n\n{e}")
        return


def do_market_sell(coin: str, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()

    # 读取 binance_position_buy 中 coin == coin, is_closed == 0 的记录, 按照 price 从小到大排序, 取第一条记录
    try:
        df_balance = pd.DataFrame(engine.connect().execute(text("SELECT * FROM binance_position_buy WHERE coin = :coin AND is_closed = 0 ORDER BY price ASC LIMIT 1"), {'coin': coin}).fetchall())
        if df_balance.empty: return send_msg(f'No open position for coin: {coin}', from_id)
    except: return send_msg(f"Reading binance_position_buy table failed.", from_id)

    amount = float(df_balance['executedQty'].values[0])
    update_id = int(df_balance['update_id'].values[0])
    buy_cost_value = float(df_balance['cummulativeQuoteQty'].values[0])
    buy_cost_bnb = float(df_balance['buy_cost_bnb'].values[0])
    buy_bnb_price = float(df_balance['buy_bnb_price'].values[0])
    open_position_time = int(df_balance['transactTime'].values[0])
    position_order_id = int(df_balance['orderId'].values[0])

    # check coin balance see if it is enough
    df_coin_balance = get_user_asset()
    df_coin_balance = df_coin_balance[df_coin_balance['asset']==coin]
    if df_coin_balance.empty: return send_msg(f'No balance for coin: {coin}', from_id)

    balance = float(df_coin_balance['free'].values[0])
    if balance < amount: return send_msg(f'Balance {balance} is not sufficient for amount: {amount}', from_id)

    data = binance_market_sell(coin, amount)
    if not data: return send_msg(f'Failed to do market sell for coin: {coin}', from_id)

    # convert data['fills] to dataframe
    df_fills = pd.DataFrame(data['fills'])

    # calculate sum of commission
    sell_cost_bnb = df_fills['commission'].astype(float).sum()

    # check price of bnb
    df_bnb_price = get_token_price('BNB')
    sell_bnb_price = df_bnb_price if df_bnb_price else 0

    total_bnb_cost_value = buy_cost_bnb * buy_bnb_price + sell_cost_bnb * sell_bnb_price

    profit = float(data['cummulativeQuoteQty']) - buy_cost_value - total_bnb_cost_value

    if profit < 0: add_coin_to_ignore_list(coin, from_id)

    # delete fills from data
    del data['fills']

    data['update_id'] = update_id
    data['sell_cost_bnb'] = sell_cost_bnb
    data['sell_bnb_price'] = sell_bnb_price
    data['total_bnb_cost_value'] = total_bnb_cost_value
    data['price'] = float(data['cummulativeQuoteQty']) / float(data['executedQty'])
    data['profit'] = profit

    # convert data to dataframe
    df_sellout_result = pd.DataFrame(data, index=[0])

    # 如果没有 binance_position_sell table, 就创建一个，如果 table 存在，就 append df_buyin_result
    df_sellout_result.to_sql('binance_position_sell', engine, if_exists='append', index=False)

    # 读取 binance_position_sell table 中的 profit 列，计算 sum(profit)
    df_profit = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_position_sell')).fetchall())
    if not df_profit.empty: profit_sum = df_profit['profit'].astype(float).sum()

    with engine.connect() as connection:
        try:
            # Execute the query with the updated update_id
            connection.execute(text("UPDATE binance_position_buy SET is_closed = 1 WHERE orderId = :position_order_id"), {'position_order_id': position_order_id})
            connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()

    order_id = data['orderId']

    duration = (data['transactTime'] - open_position_time) / 1000 / 60 / 60
    # 讲 duration 变为 xx 天 xx 小时
    duration = f'{int(duration / 24)} Days {int(duration % 24)} Hours' if duration > 24 else f'{int(duration)} Hours'

    reply_msg = f'''
Sold_Coin: {coin}
Sold_Price: {format_number(data['price'])}
Sold_Amount: {format_number(amount)}
Commition_Fee: {format_number(total_bnb_cost_value)} usdt
Trading_Profit: {format_number(profit)} usdt
Holding_Duration: {duration}
Order_ID: {order_id}
Update_ID: {update_id}
Profit_Sum: {format_number(profit_sum)} usdt
'''
    send_msg(reply_msg, from_id)
    return profit
'''
      symbol    orderId  orderListId           clientOrderId   transactTime     price       origQty   executedQty cummulativeQuoteQty  status timeInForce    type  side    workingTime selfTradePreventionMode  update_id  sell_cost_bnb  sell_bnb_price  total_bnb_cost_value   profit
0  CAKEUSDT  513576898           -1  ixTpmGNbj5w3J2vW1NPAel  1685860174026  1.746501  572.40000000  572.40000000        999.69736000  FILLED         GTC  MARKET  SELL  1685860174026                    NONE          1        0.00245      306.124284               1.50045 -1.78589
'''

''' df = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_position_sell')).fetchall())
      symbol     orderId  orderListId           clientOrderId   transactTime      price  ... selfTradePreventionMode update_id sell_cost_bnb sell_bnb_price total_bnb_cost_value      profit
0    FTTUSDT   688100726           -1  d8JXSWSmsEmVQoDqv3dIbC  1702224291468   5.562989  ...            EXPIRE_MAKER         1      0.033751          240.3            15.548180  789.421552
1   EGLDUSDT  1235576864           -1  HbstvGzUiiQBoTFxQGibwW  1702267644918  65.401010  ...            EXPIRE_MAKER         4      0.032888          233.8            15.186327  237.486573
2    IMXUSDT   533697410           -1  13Dj1FJeITi5795gIWyN00  1702267667019   1.928267  ...            EXPIRE_MAKER         2      0.032310          233.8            15.032396   57.087613
3    SNXUSDT  1057101036           -1  DlChdJwJRmwW7Lf9oNBtwu  1702267684943   4.439063  ...            EXPIRE_MAKER         9      0.032307          233.9            15.011603   56.354097
4    INJUSDT   809743269           -1  JY5FbpXFxPnePCNvO5BgT8  1702308983629  22.561297  ...            EXPIRE_MAKER        10      0.030714          243.9            15.039906  -22.595406
5   ORDIUSDT   238514100           -1  hWGYLLB2hBZNqWnhQ1AuMg  1702361706283  51.710000  ...            EXPIRE_MAKER         7      0.031247          250.2            15.314370  -15.249150
6    FTTUSDT   694080600           -1  RTIfMBTiRUilKbGM6QWnr9  1702464665994   5.500400  ...            EXPIRE_MAKER         3      0.031305          251.3            15.380309  -15.390928
7    FETUSDT   956488383           -1  RCLyLqsTG2os2Zq5nDHtJO  1702940167510   0.687657  ...            EXPIRE_MAKER        12      0.031685          240.4            15.098148  141.077352
8    STXUSDT   658898595           -1  FnIGPOiB6Hfp95EQA6NjrC  1702942206075   1.225800  ...            EXPIRE_MAKER        13      0.030880          240.9            14.856532   85.498898
9   NEARUSDT  2110473867           -1  b1vSFIYMRLWZrz4ecPsPaZ  1703034724092   2.550000  ...            EXPIRE_MAKER         8      0.031232          254.2            15.428633   84.505367
10  SANDUSDT  2782080420           -1  C9lGCy1BllCj9kATi9iaGz  1703211765923   0.554000  ...            EXPIRE_MAKER         5      0.031214          272.0            15.984787   83.772213
11  BAKEUSDT   657386867           -1  nEZ0RcxsNDo5G7pO7Lp9EE  1703227338598   0.421900  ...            EXPIRE_MAKER        15      0.027083          273.4            14.873934  484.989486
12  BAKEUSDT   657615307           -1  Ah0I3w2XaYjd9qywfk03VK  1703227686811   0.431500  ...            EXPIRE_MAKER        16      0.027978          272.9            15.261983  484.980807
'''

# get the latest sold coin from binance_position_sell
def get_latest_sold_coin():
    try:
        df_latest_sold_coin = pd.DataFrame(engine.connect().execute(text("SELECT * FROM binance_position_sell ORDER BY transactTime DESC LIMIT 1")).fetchall())
        if df_latest_sold_coin.empty: return
    except: return
    coin = df_latest_sold_coin['symbol'].values[0]
    coin = coin.replace('USDT', '') if coin.endswith('USDT') else coin
    return coin


def force_do_market_sell(coin: str, from_id=TG_BOT_OWNER_ID):
    current_orders = get_open_orders_list()
    symbol = coin + 'USDT'
    if symbol in current_orders:
        clientOrderId = current_orders[symbol]
        binance_cancel_order(coin, clientOrderId)
    do_market_sell(coin, from_id)
    return 


def close_all_positions(confirm: str, from_id=TG_BOT_OWNER_ID):

    if not confirm or confirm.upper() not in ['ALL', 'CONFIRM', 'YES']: return send_msg(f'You need to type ALL or CONFIRM or YES to confirm close all positions.', from_id)

    # 读取 binance_position_buy 中 coin == coin, is_closed == 0 的记录, 按照 price 从小到大排序, 取第一条记录
    try:
        df_balance = pd.DataFrame(engine.connect().execute(text("SELECT * FROM binance_position_buy WHERE is_closed = 0")).fetchall())
        if df_balance.empty: return send_msg(f'No open position for close', from_id)
    except: return send_msg(f"Reading binance_position_buy table failed.", from_id)

    # get coin list for all open positions
    coin_list = df_balance['coin'].unique().tolist()

    binance_cancel_all_orders(from_id)

    for coin in coin_list: do_market_sell(coin, from_id)

    return 


# 定义一个Market buy 交易功能 Input: coin, value
def binance_market_buy(coin, value):
    coin = coin.upper()
    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': coin + 'USDT',
        'side': 'BUY',
        'type': 'MARKET',
        'quoteOrderQty': value,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.post(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        time.sleep(1)
        return data
    else: 
        print(r.reason)
        return 
'''
{
  "symbol": "CAKEUSDT",
  "orderId": 513570977,
  "orderListId": -1,
  "clientOrderId": "1uDKFPwUZ3KciXE0UTY1XR",
  "transactTime": 1685853893276,
  "price": "0.00000000",
  "origQty": "571.10000000",
  "executedQty": "571.10000000",
  "cummulativeQuoteQty": "999.99610000",
  "status": "FILLED",
  "timeInForce": "GTC",
  "type": "MARKET",
  "side": "BUY",
  "workingTime": 1685853893276,
  "fills": [
    {
      "price": "1.75100000",
      "qty": "199.50000000",
      "commission": "0.00085585",
      "commissionAsset": "BNB",
      "tradeId": 73422265
    },
    ......
  ],
  "selfTradePreventionMode": "NONE"
}'''


def do_market_buy(coin: str, value):
    print(f"Calling do_market_buy for {coin} with checksize: {value} usdt")
    
    coin = coin.upper()
    reply_msg = ''
    # check USDT balance see if it is bigger than value
    df_usdt_balance = get_user_asset()
    df_usdt_balance = df_usdt_balance[df_usdt_balance['asset']=='USDT']
    if df_usdt_balance.empty: 
        reply_msg = 'No balance for coin: USDT'
        return reply_msg
    
    balance = float(df_usdt_balance['free'].values[0])
    if balance < value: 
        reply_msg = f'USDT Balance {balance} is not sufficient for value: {value}'
        return reply_msg

    data = binance_market_buy(coin, value)
    if not data: 
        reply_msg = f'Failed to do market buy for coin: {coin}'
        return reply_msg
    
    data['coin'] = data['symbol'].replace('USDT', '')
    data['price'] = float(data['cummulativeQuoteQty']) / float(data['executedQty'])

    # convert data['fills] to dataframe
    df_fills = pd.DataFrame(data['fills'])

    # calculate sum of commission, commision is string, convert to float first then sum
    commission = df_fills['commission'].astype(float).sum()
    data['buy_cost_bnb'] = commission

    # get bnb price
    df_bnb_price = get_token_price('BNB')
    bnb_price = df_bnb_price if df_bnb_price else 300

    data['buy_bnb_price'] = bnb_price

    # delete fills from data
    del data['fills']

    update_id = 0

    # Read out the max update_id from binance_position_buy table
    try:
        df_max_update_id = pd.DataFrame(engine.connect().execute(text('SELECT MAX(update_id) FROM binance_position_buy')).fetchall())
        if not df_max_update_id.empty: update_id = df_max_update_id['MAX(update_id)'].values[0]
    except: pass

    data['update_id'] = update_id + 1
    data['is_closed'] = 0

    # convert data to dataframe
    df_buyin_result = pd.DataFrame(data, index=[0])

    # If table binance_position_buy does not exist, create one, else append df_buyin_result to binance_position_buy
    df_buyin_result.to_sql('binance_position_buy', engine, if_exists='append', index=False)

    return f'''Bought {coin} at {format_number(data['price'])} usdt/{coin.lower()}'''


def do_market_buy_one_unit(coin: str, from_id=TG_BOT_OWNER_ID):
    reply_msg = do_market_buy(coin, CHECK_SIZE)
    if reply_msg: send_msg(reply_msg, from_id)
    return reply_msg


def plot_net_profit_sum(chat_id=TG_BOT_OWNER_ID):
    filename = f"net_profit_daily_record/{datetime.now().strftime('%Y-%m-%d')}.png"
    # check if the file exists, if yes, return the file name
    if os.path.isfile(filename): return send_img(chat_id, filename)

    # print current time string format and the function is running
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} plot_net_profit_sum() is running ...')

    try:
        # Read data from the table into a DataFrame
        df = pd.DataFrame(engine.connect().execute(text("SELECT Date, NetProfit FROM net_profit_daily_record")).fetchall())
        # print(df)

        # if the df is empty, return a default image
        if df.empty: return f"net_profit_daily_record/Leowang.net.jpg"

        df.columns = ['Date', 'NetProfit']

        # Calculate percentage
        df['Percentage'] = (df['NetProfit'] / INITIAL_FUND) * 100

        # Convert 'Date' to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        print(df)

    except: return send_img(chat_id, f"net_profit_daily_record/Leowang.net.jpg")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Percentage'], marker='o')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Net Profit as % of Initial Fund')
    plt.title('Daily Book Value Percentage')
    plt.grid(True)
    # plt.show()

    # Save the plot to a file
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    return send_img(chat_id, filename)


def get_kline_data(symbol, interval):
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': interval
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])
    df['Close'] = pd.to_numeric(df['Close'])
    df['Quote Asset Volume'] = pd.to_numeric(df['Quote Asset Volume'])
    # print(df)
    return df


def calculate_sma(data, period):
    return data.rolling(window=period).mean()


def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def analyze_data(df, sma_period, rsi_period, interval, tradingbot_status = False):

    df['SMA'] = calculate_sma(df['Close'], sma_period)
    df['RSI'] = calculate_rsi(df['Close'], rsi_period)
    df['RSI_SMA'] = calculate_sma(df['RSI'], rsi_period)

    df['Quote Asset Volume'] = pd.to_numeric(df['Quote Asset Volume'])
    df['Quote Asset Volume SMA'] = calculate_sma(df['Quote Asset Volume'], sma_period)

    df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

    latest = df.iloc[-1]
    previous = df.iloc[-2]

    good_to_short = 0
    good_to_buy = 1

    if interval == '4h' and latest['RSI'] > 89 and not tradingbot_status:
        good_to_short += 1
        good_to_buy = 0

    if latest['RSI'] < latest['RSI_SMA']: 
        good_to_short += 1
        good_to_buy = 0

    # Check if latest sma is lower than previous sma
    if latest['SMA'] < previous['SMA']: 
        good_to_short += 1
        good_to_buy = 0

    # check if latest rsi is lower than previous rsi
    if latest['RSI'] < previous['RSI']:
        good_to_short += 1
        good_to_buy = 0

    if interval == '5m':
        if previous['Quote Asset Volume'] < 100_000 and latest['Quote Asset Volume'] < 100_000:
            good_to_short += 1
            good_to_buy = 0

        if latest['Quote Asset Volume'] < latest['Quote Asset Volume SMA'] and previous['Quote Asset Volume'] < previous['Quote Asset Volume SMA']:
            good_to_short += 1
            good_to_buy = 0            

        if latest['Close'] < previous['Close']: 
            good_to_short += 1
            good_to_buy = 0

    return {'good_to_buy': good_to_buy, 'good_to_short': good_to_short}
    
    
def analyze_symbol(symbol: str, tradingbot_status = False):
    symbol = symbol.upper() + 'USDT' if not symbol.endswith('USDT') else symbol.upper()
    coin = symbol[:-4]
    global SHORT_COINS_LIST

    good_to_buy = 0
    good_to_short = 0

    for interval in ['4h', '1h', '15m', '5m']:
        df = get_kline_data(symbol, interval)
        result = analyze_data(df, 34, 14, interval, tradingbot_status)
        good_to_buy += result['good_to_buy']
        good_to_short += result['good_to_short']

    if good_to_buy == 4: 
        if coin in SHORT_COINS_LIST: SHORT_COINS_LIST.remove(coin)
        return {'long': True, 'short': False}

    if good_to_short > 13: 
        if coin not in SHORT_COINS_LIST: SHORT_COINS_LIST.append(coin)
        return {'long': False, 'short': True}
    
    return {'long': False, 'short': False}


# Define a function to check if the weekly interval rsi is over 90, if yes, remove from white_list
def weekly_rsi_over_high(symbol):
    symbol = symbol.upper() + 'USDT' if not symbol.endswith('USDT') else symbol.upper()
    interval = '1w'

    df = get_kline_data(symbol, interval)
    df['RSI'] = calculate_rsi(df['Close'], 14)
    latest = df.iloc[-1]
    if latest['RSI'] > 89: 
        # send_msg(f"{symbol[:-4]} weekly RSI {format_number(latest['RSI'])} is higher than 89", from_id)
        return True
    
    return False


# check binance_position_buy and calculate profit based on current price for all coins
def binance_position_buy_check_all(target_profit=0.01, coin=None, chat_id=None, crontab_profit_record=False, tradingbot_status=False):

    try: df_balance = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_position_buy WHERE is_closed = 0')).fetchall())
    except: 
        if chat_id: send_msg('Table binance_position_buy does not exist', chat_id)
        return 'Table binance_position_buy does not exist'

    if df_balance.empty: 
        if chat_id: send_msg('No open position currently.', chat_id)

        try: binance_adjust_profit(chat_id)
        except: pass

        try: check_profit_and_record(chat_id, crontab_profit_record)
        except: pass

        return 'No open position for all coins'

    if coin: 
        df_balance = df_balance[df_balance['coin']==coin.upper()]
        if df_balance.empty: 
            if chat_id: send_msg(f'No open position for coin: {coin}', chat_id)
            return f'No open position for coin: {coin}'

    # get current price for all coins
    df = get_token_price_table()
    if df.empty: 
        if chat_id: send_msg('Failed to fetch price info', chat_id)
        return 'Failed to fetch price info'

    # merge df_balance and df based on coin since df and df_balance all have coin column
    df_balance = pd.merge(df_balance, df, on='coin', how='left')

    '''convert df_balance first row to dict
    {
      "symbol_x": "CAKEUSDT",
      "orderId": 513582692,
      "orderListId": -1,
      "clientOrderId": "VUxnvBkLBvuNSVzmLKV2NM",
      "transactTime": 1685863960460,
      "price": 1.7495544727679897,
      "origQty": "571.57000000",
      "executedQty": "571.57000000",
      "cummulativeQuoteQty": "999.99285000",
      "status": "FILLED",
      "timeInForce": "GTC",
      "type": "MARKET",
      "side": "BUY",
      "workingTime": 1685863960460,
      "selfTradePreventionMode": "NONE",
      "coin": "CAKE",
      "buy_cost_bnb": 0.0024476899999999998,
      "buy_bnb_price": 306.7,
      "update_id": 3,
      "is_closed": 0,
      "symbol_y": "CAKEUSDT",
      "lastPrice": 1.749
    }'''

    # convert df_balance['executedQty'] to float and calculate profit
    df_balance['executedQty'] = df_balance['executedQty'].astype(float)
    df_balance['profit'] = (df_balance['lastPrice'] - df_balance['price']) * df_balance['executedQty']

    # calculate up_ratio in % format
    df_balance['up_ratio'] = df_balance['lastPrice']/ df_balance['price'] - 1

    # calculate bnb_cost_value
    df_balance['bnb_cost_value'] = df_balance['buy_cost_bnb'] * df_balance['buy_bnb_price']
    
    # sort by profit
    df_balance = df_balance.sort_values(by='profit', ascending=False)

    current_orders = get_open_orders_list()
    WHITE_LIST = get_white_list()
    book_value = 0
    for_reply = {}

    for i in range(df_balance.shape[0]):
        # ignore coin BNB, ONG
        if df_balance.iloc[i]['coin'] in ['BNB', 'ONG', 'USDT', 'USDC']: continue

        reply_dict = df_balance.iloc[i].to_dict()

        coin = reply_dict['coin']
        symbol = coin + 'USDT'

        for_reply['Coin'] = reply_dict['coin']
        for_reply['Amount'] = format_number(reply_dict['executedQty'])
        for_reply['Profit'] = format_number(reply_dict['profit'])
        for_reply['Up_Ratio'] = f"{round(float(reply_dict['up_ratio'])*100, 2)}%"
        for_reply['Buy_Price'] = f"{reply_dict['price']:.2f}"
        for_reply['Current_Price'] = f"{reply_dict['lastPrice']:.2f}"
        for_reply['BNB_Cost_Value'] = format_number(reply_dict['bnb_cost_value'])
        for_reply['Position_Since'] = datetime.fromtimestamp(reply_dict['transactTime'] / 1000).strftime('%Y-%m-%d %H:%M')
        for_reply['Order_ID'] = reply_dict['orderId']
        for_reply['Update_ID'] = reply_dict['update_id']

        reply_msg = '\n'.join([f"{k}: {v}" for k, v in for_reply.items()])
        if chat_id: send_msg(f"{i+1}/{df_balance.shape[0]}\n{reply_msg}", chat_id)

        long_or_short = analyze_symbol(coin, tradingbot_status)
        '''{'long': True, 'short': False}'''
        long = long_or_short['long']
        short = long_or_short['short']

        # Condition analysis: if the coin has profit but in the same time, the analysis_symbol() returns False (which means the coin is not good to buy), Or the weekly_rsi_over_high() returns True (which means the weekly rsi is over 89), then do market sell for this coin (cancel order first if there is an open order)
        if not long: 

            if (not tradingbot_status and reply_dict['up_ratio'] > 0.003) or reply_dict['up_ratio'] >= target_profit:
                if short: send_msg(f"{coin} is good to short now, close all positions.", TG_BOT_OWNER_ID)
                if reply_dict['up_ratio'] >= target_profit: send_msg(f"{coin} is not in good condition, and profit is positive, close position.", TG_BOT_OWNER_ID)
                
                if symbol in current_orders: binance_cancel_order(coin, current_orders[symbol])
                do_market_sell(coin, chat_id)
                continue
            if short: send_msg(f"SHORT {coin} on UMFUTURES to hedge the risk.", TG_BOT_OWNER_ID)

            binance_position_set_limit_sell(target_profit, chat_id, coin)

        book_value += reply_dict['profit']

    try: check_profit_and_record(chat_id, crontab_profit_record, book_value, current_positions=df_balance.shape[0])
    except: pass

    return

# check_profit_and_record(chat_id=TG_BOT_OWNER_ID, crontab_profit_record=False, book_value=0)

def check_profit_and_record(chat_id=None, crontab_profit_record=False, book_value=0, current_positions=0):
    if chat_id or crontab_profit_record: 
        # 读取 binance_position_sell table 中的 profit 列，计算 sum(profit)
        df_profit = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_position_sell')).fetchall())
        if not df_profit.empty: 
            # From binance_position_buy read out the earliest transactTime
            df_earliest_transactTime = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_position_buy ORDER BY transactTime ASC LIMIT 1')).fetchall())
            earliest_transactTime = df_earliest_transactTime['transactTime'].astype(int).min()
            # print('earliest_transactTime: ', earliest_transactTime)
            duration = (int(time.time() * 1000) - earliest_transactTime) / 1000 / 60 / 60
            duration_day = f'{int(duration / 24)} Days {int(duration % 24)} Hours' if duration > 24 else f'{int(duration)} Hours'
            profit_sum = df_profit['profit'].astype(float).sum()
            net_profit_sum = profit_sum + book_value
            annualized_return = net_profit_sum / (duration / 24 / 365) / INITIAL_FUND
            # annualized_return with percentage format
            annualized_return = f"{annualized_return * 100:.2f}%"
            if crontab_profit_record:
                # Record net_profit_sum to table net_profit_daily_record
                with engine.connect() as connection:
                    try:
                        # Check if today's record exists
                        query = "SELECT * FROM net_profit_daily_record WHERE Date = :Date"
                        params = {'Date': datetime.now().strftime('%Y-%m-%d')}
                        result = connection.execute(text(query), params)
                        df = pd.DataFrame(result.fetchall(), columns=result.keys())
                        if df.empty:
                            # Execute the query with the updated update_id
                            connection.execute(text("INSERT INTO net_profit_daily_record (Date, NetProfit) VALUES (:Date, :NetProfit)"), {'Date': datetime.now().strftime('%Y-%m-%d'), 'NetProfit': net_profit_sum})
                            connection.commit()
                    except Exception as e:
                        print(f"An error occurred for reading net_profit_daily_record and insert data: {e}")
                        connection.rollback()
            # Send profit_sum to chat_id
            chat_id = chat_id if chat_id else TG_BOT_OWNER_ID
            investment_return = net_profit_sum / INITIAL_FUND
            # investment_return with percentage format
            investment_return = f"{investment_return * 100:.2f}%"
            summary_msg = f"BOT RUNNING: {duration_day}\n\nInitial Fund: {format_number(INITIAL_FUND)} usdt\nUnrealized_Gain: {format_number(book_value)} usdt\nRealized_Gain: {format_number(profit_sum)} usdt\nNet_Profit: {format_number(net_profit_sum)} usdt\nCurrent_Positions: {current_positions}/{POSITIONS_LIMIT}\n\nInvestment_Return: {investment_return}\nAnnualized_Return: {annualized_return}"
            send_msg(summary_msg, chat_id)
            year_and_month_day = datetime.now().strftime('%Y-%m-%d')
            send_email(f'TRADING BOT OPERATION SUMMARY {year_and_month_day}', summary_msg, GMAIL_ADDRESS_MAIN)
            plot_net_profit_sum(chat_id)
            send_msg_markdown('''[Online Dashboard](https://wh.leowang.net/dashboard)''', chat_id)
    return 



# Define a function to check orderid and update status
def binance_check_order_status(symbol, clientOrderId=None):
    symbol = symbol.upper()
    coin = symbol.replace('USDT', '')

    if not clientOrderId:
        try:
            df_balance = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_limit_sell_order WHERE symbol = :symbol AND status = "NEW"'), {'symbol': symbol}).fetchall())
            if df_balance.empty: return
        except: return

        clientOrderId = df_balance['clientOrderId'].values[0]
        
    try: 
        df_balance = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_position_buy WHERE is_closed = 0 AND coin = :coin'), {'coin': coin}).fetchall())
        if df_balance.empty: return
    except: return 'Table binance_position_buy not found'

    
    limit_order_data = check_order_status(coin, clientOrderId)

    if limit_order_data:
        # print(json.dumps(limit_order_data, indent=2))

        # Check if the order is filled, if yes, do market sell
        if limit_order_data['status'] == 'FILLED':

            # create a dict akin to market sell data structure
            data = {}
            data['symbol'] = limit_order_data['symbol']
            data['orderId'] = limit_order_data['orderId']
            data['orderListId'] = limit_order_data['orderListId']
            data['clientOrderId'] = limit_order_data['clientOrderId']
            data['transactTime'] = limit_order_data.get('transactTime', int(time.time() * 1000))
            data['price'] = limit_order_data['price']
            data['origQty'] = limit_order_data['origQty']
            data['executedQty'] = limit_order_data['executedQty']
            data['cummulativeQuoteQty'] = limit_order_data['cummulativeQuoteQty']
            data['status'] = limit_order_data['status']
            data['timeInForce'] = limit_order_data['timeInForce']
            data['type'] = limit_order_data['type']
            data['side'] = limit_order_data['side']
            data['workingTime'] = limit_order_data['workingTime']
            data['selfTradePreventionMode'] = limit_order_data['selfTradePreventionMode']

            update_id = int(df_balance['update_id'].values[0])
            buy_cost_value = float(df_balance['cummulativeQuoteQty'].values[0])
            buy_cost_bnb = float(df_balance['buy_cost_bnb'].values[0])
            buy_bnb_price = float(df_balance['buy_bnb_price'].values[0])
            open_position_time = int(df_balance['transactTime'].values[0])
            position_order_id = int(df_balance['orderId'].values[0])

            sell_cost_bnb = buy_cost_bnb

            # check price of bnb
            df_bnb_price = get_token_price('BNB')
            sell_bnb_price = df_bnb_price if df_bnb_price else 250

            total_bnb_cost_value = buy_cost_bnb * buy_bnb_price + sell_cost_bnb * sell_bnb_price

            profit = float(limit_order_data['cummulativeQuoteQty']) - buy_cost_value - total_bnb_cost_value

            data['update_id'] = update_id
            data['sell_cost_bnb'] = sell_cost_bnb
            data['sell_bnb_price'] = sell_bnb_price
            data['total_bnb_cost_value'] = total_bnb_cost_value
            data['profit'] = profit

            # convert data to dataframe
            df_sellout_result = pd.DataFrame(data, index=[0])

            df_sellout_result.to_sql('binance_position_sell', engine, if_exists='append', index=False)

            df_profit = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_position_sell')).fetchall())
            if not df_profit.empty: profit_sum = df_profit['profit'].astype(float).sum()

            # Mark the position as closed in binance_position_buy table
            with engine.connect() as connection:
                try:
                    # Execute the query with the updated update_id
                    connection.execute(text("UPDATE binance_position_buy SET is_closed = 1 WHERE orderId = :position_order_id"), {'position_order_id': position_order_id})
                    connection.commit()
                except Exception as e:
                    print(f"An error occurred: {e}")
                    connection.rollback()

            duration = (data['transactTime'] - open_position_time) / 1000 / 60 / 60
            duration = f'{int(duration / 24)} Days {int(duration % 24)} Hours' if duration > 24 else f'{int(duration)} Hours'

            # Mark the limit order as filled in binance_limit_sell_order table
            with engine.connect() as connection:
                try:
                    # Execute the query with the updated update_id
                    connection.execute(text("UPDATE binance_limit_sell_order SET status = 'FILLED' WHERE clientOrderId = :clientOrderId"), {'clientOrderId': clientOrderId})
                    connection.commit()
                except Exception as e:
                    print(f"An error occurred: {e}")
                    connection.rollback()

            reply_msg = f'''{coin} Limit Order Filled\n\nSold_Price: {format_number(data['price'])}\nTrading_Profit: {format_number(profit)} usdt\nHolding_Duration: {duration}\n\nProfit_Sum: {format_number(profit_sum)} usdt\n'''
            send_msg(reply_msg, TG_BOT_OWNER_ID)


        if limit_order_data['status'] in ['CANCELED', 'CANCELLED', 'EXPIRED']:
            if mark_limit_order_as_canceled(clientOrderId, limit_order_data['status']): send_msg(f'''{coin} Order {limit_order_data['status']}\n\nOrder_ID: {limit_order_data['orderId']}\n''', TG_BOT_OWNER_ID)

    return 


# Mark a limit order as canceled in binance_limit_sell_order table
def mark_limit_order_as_canceled(clientOrderId, status='CANCELED'):
    
    with engine.connect() as connection:
        try:
            # Execute the query with the updated update_id
            connection.execute(text("UPDATE binance_limit_sell_order SET status = :status WHERE clientOrderId = :clientOrderId"), {'clientOrderId': clientOrderId, 'status': status})
            connection.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()
            return False


# select * from binance_balance_history
df = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_balance_history')).fetchall())


# define a function to UPDATE binance_limit_sell_order SET all status to 'CANCELLED' if status is not 'FILLED'
def binance_set_all_orders_to_cancelled(chat_id=TG_BOT_OWNER_ID):
    with engine.connect() as connection:
        try:
            # Execute the query with the updated update_id
            connection.execute(text("UPDATE binance_limit_sell_order SET status = 'CANCELLED' WHERE status != 'FILLED'"))
            connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()
    return send_msg(f"All Non-Filled Orders have been set to Cancelled.", chat_id)


# Define a function 'polish_parameters_for_limit_order' to polish parameters for limit order, take input coint, amount, price, get_exchange_info_symbols(coin) and compare the price, amount with minPrice, maxPrice, minQty, maxQty, tickSize, stepSize, quoteAssetPrecision, baseAssetPrecision, round the price and amount to the right precision if needed, return polished coin, amount, price
def polish_parameters_for_limit_order(coin, amount, price, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    print('Calling polish_parameters_for_limit_order()...')

    # Assuming get_exchange_info_symbols is a function that fetches the exchange information
    parameters_standard = get_exchange_info_symbols(coin)
    if not parameters_standard: return send_msg(f'Failed to get parameters_standard for coin: {coin}', from_id)

    # Check if the price is within the range
    min_price = float(parameters_standard['minPrice'])
    max_price = float(parameters_standard['maxPrice'])
    price = float(price)
    if price < min_price: return send_msg(f'Price: {price} is lower than minPrice: {min_price} for coin: {coin}', from_id)
    if price > max_price: return send_msg(f'Price: {price} is higher than maxPrice: {max_price} for coin: {coin}', from_id)

    # Check if the amount is within the range
    min_qty = float(parameters_standard['minQty'])
    max_qty = float(parameters_standard['maxQty'])
    amount = float(amount)
    if amount < min_qty: return send_msg(f'Amount: {amount} is lower than minQty: {min_qty} for coin: {coin}', from_id)
    if amount > max_qty: return send_msg(f'Amount: {amount} is higher than maxQty: {max_qty} for coin: {coin}', from_id)

    # Polish the price to the right tick size and precision
    tick_size = float(parameters_standard['tickSize'])
    quote_precision = int(parameters_standard['quoteAssetPrecision'])
    price = round((round(price / tick_size) * tick_size), quote_precision)

    # Polish the amount to the right step size and precision
    step_size = float(parameters_standard['stepSize'])
    base_precision = int(parameters_standard['baseAssetPrecision'])
    amount = round((round(amount / step_size) * step_size), base_precision)

    polished_parameters = {
        'coin': coin,
        'amount': amount,
        'price': price
    }

    return polished_parameters


# Define a function to call binance_limit_sell(coin, amount, price) to set limit sell order for all positions at target_profit, if target_profit is not given, use buy in price from binance_position_buy table.
def binance_position_set_limit_sell(target_profit=None, chat_id=TG_BOT_OWNER_ID, coin=None):

    target_profit = read_target_profit_default() if not target_profit else float(target_profit)

    try: df_balance = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_position_buy WHERE is_closed = 0')).fetchall())
    except: return 'binance_position_buy table does not exist'

    # if coin is given, filter df_balance with coin
    if coin: df_balance = df_balance[df_balance['coin']==coin.upper()]

    if df_balance.empty: 
        if chat_id: 
            if coin: send_msg(f'No open position for {coin}', chat_id)
            else: send_msg(f'No open position for all coins', chat_id)
        return 

    # get open orders from table binance_limit_sell_order
    try: df_current_openorders = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_limit_sell_order WHERE status = :status'), {'status': 'NEW'}).fetchall())
    except: return 'binance_limit_sell_order table does not exist'

    ''' df_current_openorders = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_limit_sell_order WHERE status = :status'), {'status': 'NEW'}).fetchall())
        symbol     orderId  orderListId           clientOrderId   transactTime         price         origQty executedQty cummulativeQuoteQty status timeInForce   type  side    workingTime selfTradePreventionMode
    0   FTTUSDT   694080600           -1  RTIfMBTiRUilKbGM6QWnr9  1702353638922    5.50040000   1818.04000000  0.00000000          0.00000000    NEW         GTC  LIMIT  SELL  1702353638922            EXPIRE_MAKER
    1  SANDUSDT  2770085235           -1  9zS4bRnuK5j9QAjBpoiTcp  1702353640162    0.54850000  18230.00000000  0.00000000          0.00000000    NEW         GTC  LIMIT  SELL  1702353640162            EXPIRE_MAKER
    2  RUNEUSDT  1254597462           -1  QgEIqdbxJkFL1ht8tgsEB6  1702353641278    6.59900000   1515.40000000  0.00000000          0.00000000    NEW         GTC  LIMIT  SELL  1702353641278            EXPIRE_MAKER
    3  ORDIUSDT   238514100           -1  hWGYLLB2hBZNqWnhQ1AuMg  1702353642364   51.71000000    193.38000000  0.00000000          0.00000000    NEW         GTC  LIMIT  SELL  1702353642364            EXPIRE_MAKER
    4  NEARUSDT  2096374086           -1  8fp85ObC2akoeUDfu6Rsu8  1702353643510    2.52500000   3960.70000000  0.00000000          0.00000000    NEW         GTC  LIMIT  SELL  1702353643510            EXPIRE_MAKER
    5  AAVEUSDT  1508986514           -1  kOC2n1SN3Yrb0txdhLL0EQ  1702658527940  114.59000000     91.62700000  0.00000000          0.00000000    NEW         GTC  LIMIT  SELL  1702658527940            EXPIRE_MAKER
    '''

    current_orders = get_open_orders_list()

    for i in range(df_balance.shape[0]):
        coin = df_balance.iloc[i]['coin']
        amount = df_balance.iloc[i]['executedQty']
        buy_price = df_balance.iloc[i]['price']
        price = buy_price * (1 + float(target_profit))
        symbol = coin + 'USDT'

        # Check if there is an open order for the coin, if yes, cancel it first
        if symbol in current_orders:
            # Check if there is an existing order for this coin
            existing_order = df_current_openorders[df_current_openorders['symbol'] == symbol]
            if not existing_order.empty:
                # Check the price of the existing order
                existing_order_price = float(existing_order.iloc[0]['price'])
                current_order_target_profit = (existing_order_price - buy_price) / buy_price
                if round(current_order_target_profit, 2) == round(target_profit, 2): continue
                else:
                    clientOrderId = current_orders[symbol]
                    cancel_confirm = binance_cancel_order(coin, clientOrderId)

                    '''cancel_confirm
                    {
                    "symbol": "FTTUSDT",
                    "origClientOrderId": "7w4KnO7kH4A4kupqItZT5x",
                    "orderId": 693520320,
                    "orderListId": -1,
                    "clientOrderId": "ugNFO2rYpp0aJJe5f3USeX",
                    "transactTime": 1702341486234,
                    "price": "5.50040000",
                    "origQty": "1818.04000000",
                    "executedQty": "0.00000000",
                    "cummulativeQuoteQty": "0.00000000",
                    "status": "CANCELED",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "SELL",
                    "selfTradePreventionMode": "EXPIRE_MAKER"
                    }
                    '''

                    # UPDATE binance_limit_sell_order SET status = 'CANCELED' WHERE clientOrderId = clientOrderId
                    with engine.connect() as connection:
                        try:
                            # Execute the query with the updated update_id
                            connection.execute(text("UPDATE binance_limit_sell_order SET status = :status WHERE clientOrderId = :clientOrderId"), {'clientOrderId': clientOrderId, 'status': cancel_confirm['status']})
                            connection.commit()
                        except Exception as e:
                            print(f"An error occurred: {e}")
                            connection.rollback()

        polished_parameters = polish_parameters_for_limit_order(coin, amount, price, chat_id)
        amount = polished_parameters['amount']
        price = polished_parameters['price']

        data = binance_limit_sell(coin, amount, price)
        if not data: continue

        ''' DATA format:
        {
        "symbol": "FTTUSDT",
        "orderId": 693489563,
        "orderListId": -1,
        "clientOrderId": "Af88C5Qb0P1bmzs3vjZh9u",
        "transactTime": 1702335015511,
        "price": "5.50040000",
        "origQty": "1818.04000000",
        "executedQty": "0.00000000",
        "cummulativeQuoteQty": "0.00000000",
        "status": "NEW",
        "timeInForce": "GTC",
        "type": "LIMIT",
        "side": "SELL",
        "workingTime": 1702335015511,
        "fills": [],
        "selfTradePreventionMode": "EXPIRE_MAKER"
        }
        '''

        if chat_id: send_msg(f"{coin} Limit Order >> {price} >> {target_profit*100:.2f}%", chat_id)

        # del data.fills and make data a dataframe df, make sure df not empty and instert or update to 'binance_limit_sell_order' table by checking if clientOrderId exists
        del data['fills']

        df = pd.DataFrame(data, index=[0])
        if df.empty: continue

        try: df.to_sql('binance_limit_sell_order', engine, if_exists='append', index=False)
        except Exception as e: print(f"An error occurred: {e}")

    return

''' READ TABLE binance_limit_sell_order
df = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_limit_sell_order')).fetchall())
'''


# check binance_position_buy, find out open positions that's been more than 7 days, cancel the current limit sell order for them and reset limit sell order at target_profit = 0.01
def binance_position_reset_limit_sell(target_profit = 0.01, transactTime = 3, from_id = TG_BOT_OWNER_ID):
    try: transactTime = int(transactTime)
    except: transactTime = 3

    days_ago_millis = int(time.time() * 1000) - (transactTime * 24 * 60 * 60 * 1000)
    query = "SELECT * FROM binance_position_buy WHERE is_closed = 0 AND transactTime < :three_days_ago"
    
    try: df_balance = pd.DataFrame(engine.connect().execute(text(query), {'three_days_ago': days_ago_millis}).fetchall())
    except: return 'binance_position_buy table does not exist'

    if df_balance.empty: return f'No open position in binance_position_buy table that has been holden for more than {transactTime} days'

    # for the coins in df_balance, if there's already an open order, check the price, if the price is higher than new target_profit, cancel the order and reset the order at target_profit
    for index, row in df_balance.iterrows():
        coin = row['coin']
        print(f"{index}. COIN: {coin} has been holden for {transactTime} days, trying to reset limit order to {target_profit*100:.2f}%")
        try: binance_position_set_limit_sell(target_profit, from_id, coin)
        except: pass

    return


# Define cancel all of the open orders
def binance_cancel_all_orders(chat_id=None):
    current_orders = get_open_orders_list()
    if not current_orders: return send_msg(f'No open orders', chat_id)

    for symbol, clientOrderId in current_orders.items():
        coin = symbol.replace('USDT', '')
        cancel_confirm = binance_cancel_order(coin, clientOrderId)

        # UPDATE binance_limit_sell_order SET status = 'CANCELED' WHERE clientOrderId = clientOrderId
        with engine.connect() as connection:
            try:
                # Execute the query with the updated update_id
                connection.execute(text("UPDATE binance_limit_sell_order SET status = :status WHERE clientOrderId = :clientOrderId"), {'clientOrderId': clientOrderId, 'status': cancel_confirm['status']})
                connection.commit()
            except Exception as e:
                print(f"An error occurred: {e}")
                connection.rollback()

        if chat_id: send_msg(f"Canceled order for: {coin} with clientOrderId: {clientOrderId}", chat_id)

    # df = pd.DataFrame(engine.connect().execute(text("SELECT * FROM binance_limit_sell_order WHERE status != 'CANCELED'")).fetchall())
    # print(df)        

    return 


# difne a function to update net_profit_daily_record, alter NetProfit value to input value for a given date(string like 2023-12-10)
def update_net_profit_daily_record(date, net_profit):
    with engine.connect() as connection:
        try:
            # Execute the query with the updated update_id
            connection.execute(text("UPDATE net_profit_daily_record SET NetProfit = :NetProfit WHERE Date = :Date"), {'Date': date, 'NetProfit': net_profit})
            connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()
    return


def bot_call_binance_position_check(from_id=TG_BOT_OWNER_ID):
    return binance_position_buy_check_all(target_profit = 0.01, coin = None, chat_id = from_id, crontab_profit_record = False, tradingbot_status = trading_bot_switch_status())


def bot_call_binance_position_check_coin(coin, from_id=TG_BOT_OWNER_ID):
    return binance_position_buy_check_all(target_profit = 0.01, coin = coin, chat_id = from_id, crontab_profit_record = False, tradingbot_status = trading_bot_switch_status())


'''小额资产转换 (USER_DATA)
POST /sapi/v1/asset/dust (HMAC SHA256)
把小额资产转换成 BNB. 权重(UID): 10
参数:
名称	类型	是否必需	描述
asset	ARRAY	YES	正在转换的资产。 例如: asset=BTC,USDT
recvWindow	LONG	NO	
timestamp	LONG	YES
'''


# 查看给定币种的上架资产详情
def binance_asset_details(coin, chat_id):
    coin = coin.upper()
    PATH = '/sapi/v1/asset/assetDetail'
    timestamp = int(time.time() * 1000)
    params = {
        'asset': coin,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        # print(json.dumps(data, indent=2))
        '''
        {
        "RSR": {
            "withdrawFee": "2167",
            "minWithdrawAmount": "4334",
            "withdrawStatus": true,
            "depositStatus": true
        }
        }'''
        real_data = data[coin]
        real_data_str = '\n'.join([f"{k}: {v}" for k, v in real_data.items()])
        send_msg(real_data_str, chat_id)
        return 


'''查询每日资产快照 (USER_DATA) 权重(IP): 2400
参数:
名称	类型	是否必需	描述
type	STRING	YES	"SPOT", "MARGIN", "FUTURES"
startTime	LONG	NO	
endTime	LONG	NO	
limit	INT	NO	min 7, max 30, default 7
recvWindow	LONG	NO	
timestamp	LONG	YES	

查询时间范围最大不得超过30天
仅支持查询最近 1 个月数据
若startTime和endTime没传，则默认返回最近7天数据
'''


# 查询每日资产快照
def binance_daily_account_snapshot(type='SPOT', startTime=None, endTime=None, limit=1):
    PATH = '/sapi/v1/accountSnapshot'
    timestamp = int(time.time() * 1000)
    params = {
        'type': type,
        'limit': limit,
        'timestamp': timestamp
        }
    if startTime: params['startTime'] = startTime
    if endTime: params['endTime'] = endTime
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        print(json.dumps(data, indent=2))
        '''
        {
        "snapshotVos": [
            {
                "type": "SPOT",
                "updateTime": 1576281599000,
                "data": {
                    "balances": [
                        {
                            "asset": "BTC",
                            "free": "4723846.89208129",
                            "locked": "0.00000000"
                        },
                        {
                            "asset": "USDT",
                            "free": "4763366.68006011",
                            "locked": "1000.00000000"
                        }
                    ],
                    "totalAssetOfBtc": "0.00000000"
                }
            }
        ],
        "success": true
        }'''
        return data
    else: 
        print(r.reason)
        return
    

def binance_market_buy_quantity(coin, quantity):
    coin = coin.upper()
    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': coin + 'USDT',
        'side': 'BUY',
        'type': 'MARKET',
        'quantity': quantity,  # Changed from 'quoteOrderQty' to 'quantity'
        'timestamp': timestamp
    }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.post(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        return data
    else: 
        print(r.reason)
        return None
    

# Check if bnb balance is less than 1, if yes, buy 1 bnb
def check_and_buy_bnb(coin = 'BNB', check_limit = 1, chat_id=TG_BOT_OWNER_ID):
    coin = coin.upper()

    try: check_limit = float(check_limit)
    except: return send_msg(f'check_limit: {check_limit} is not a number', chat_id)

    # print(f'bnb_balance: {bnb_balance} is less than check_limit: {check_limit}, trying to buy {check_limit} {coin}')
    data = binance_market_buy_quantity(coin, check_limit)
    if not data: return send_msg(f'Failed to market buy: {check_limit} {coin}', chat_id)
    
    # delete fills from data
    del data['fills']

    # convert data to dataframe
    df_buyin = pd.DataFrame(data, index=[0])

    # If table binance_position_buy does not exist, create one, else append df_buyin_result to binance_position_buy
    df_buyin.to_sql(f'check_and_buy_{coin}', engine, if_exists='append', index=False)

    send_msg(f'DONE: Market buy {check_limit} {coin}', chat_id)

    return

    
# define a function to switch on the trading bot and send a message to the user
def webhook_switch_on_bot(msg = 'None', from_id=TG_BOT_OWNER_ID):
    current_status = trading_bot_switch_status()
    if current_status: return True

    if trading_bot_switch_on(): 
        target_profit = float(os.getenv('TARGET_PROFIT', 0.05))
        set_target_profit_default(target_profit)
        return send_msg(f"Reset target profit to {target_profit*100:.2f}%\n\n{msg}", from_id)
    return send_msg(f"Failed to switch on the bot! \n\n{msg}", from_id)


# define a function to switch off the trading bot and send a message to the user
def webhook_switch_off_bot(msg = 'None', from_id=TG_BOT_OWNER_ID):
    current_status = trading_bot_switch_status()
    if not current_status: return True

    if trading_bot_switch_off(): 
        binance_position_reset_limit_sell(target_profit = 0.01, transactTime = 1, from_id = TG_BOT_OWNER_ID)
        return send_msg(f"Reset all limit sell orders target profit to 1% for positions older than 1 day.\n\n{msg}", from_id)
    return send_msg(f"Failed to switch off the bot!\n\n{msg}", from_id)

'''binance_position_sell
     symbol     orderId  orderListId           clientOrderId   transactTime      price         origQty     executedQty cummulativeQuoteQty  status timeInForce    type  side    workingTime selfTradePreventionMode  update_id  sell_cost_bnb  sell_bnb_price  total_bnb_cost_value      profit
0   FTTUSDT   688100726           -1  d8JXSWSmsEmVQoDqv3dIbC  1702224291468   5.562989   1942.29000000   1942.29000000      10804.93829100  FILLED         GTC  MARKET  SELL  1702224291468            EXPIRE_MAKER          1       0.033751           240.3             15.548180  789.421552
1  EGLDUSDT  1235576864           -1  HbstvGzUiiQBoTFxQGibwW  1702267644918  65.401010    156.76000000    156.76000000      10252.26230000  FILLED         GTC  MARKET  SELL  1702267644918            EXPIRE_MAKER          4       0.032888           233.8             15.186327  237.486573
2   IMXUSDT   533697410           -1  13Dj1FJeITi5795gIWyN00  1702267667019   1.928267   5223.40000000   5223.40000000      10072.10982900  FILLED         GTC  MARKET  SELL  1702267667019            EXPIRE_MAKER          2       0.032310           233.8             15.032396   57.087613
3   SNXUSDT  1057101036           -1  DlChdJwJRmwW7Lf9oNBtwu  1702267684943   4.439063   2268.80000000   2268.80000000      10071.34600000  FILLED         GTC  MARKET  SELL  1702267684943            EXPIRE_MAKER          9       0.032307           233.9             15.011603   56.354097
4   INJUSDT   809743269           -1  JY5FbpXFxPnePCNvO5BgT8  1702308983629  22.561297    442.90000000    442.90000000       9992.39860000  FILLED         GTC  MARKET  SELL  1702308983629            EXPIRE_MAKER         10       0.030714           243.9             15.039906  -22.595406
5  ORDIUSDT   238514100           -1  hWGYLLB2hBZNqWnhQ1AuMg  1702361706283  51.710000    193.38000000    193.38000000       9999.67980000  FILLED         GTC   LIMIT  SELL  1702353642364            EXPIRE_MAKER          7       0.031247           250.2             15.314370  -15.249150
6   FTTUSDT   694080600           -1  RTIfMBTiRUilKbGM6QWnr9  1702464665994   5.500400   1818.04000000   1818.04000000       9999.94721600  FILLED         GTC   LIMIT  SELL  1702353638922            EXPIRE_MAKER          3       0.031305           251.3             15.380309  -15.390928
7   FETUSDT   956488383           -1  RCLyLqsTG2os2Zq5nDHtJO  1702940167510   0.687657  14769.00000000  14769.00000000      10156.01120000  FILLED         GTC  MARKET  SELL  1702940167510            EXPIRE_MAKER         12       0.031685           240.4             15.098148  141.077352
8   STXUSDT   658898595           -1  FnIGPOiB6Hfp95EQA6NjrC  1702942206075   1.225800   8239.80000000   8239.80000000      10100.34684000  FILLED         GTC   LIMIT  SELL  1702941873518            EXPIRE_MAKER         13       0.030880           240.9             14.856532   85.498898
'''


# define a function to read the latest transactTime sell price for a given coin
def read_latest_sell_price(coin, from_id):
    
    ''' binance_position_sell
         symbol     orderId  orderListId           clientOrderId   transactTime      price         origQty     executedQty cummulativeQuoteQty  status timeInForce    type  side    workingTime selfTradePreventionMode  update_id  sell_cost_bnb  sell_bnb_price  total_bnb_cost_value      profit
    0   FTTUSDT   688100726           -1  d8JXSWSmsEmVQoDqv3dIbC  1702224291468   5.562989   1942.29000000   1942.29000000      10804.93829100  FILLED         GTC  MARKET  SELL  1702224291468            EXPIRE_MAKER          1       0.033751           240.3             15.548180  789.421552
    1  EGLDUSDT  1235576864           -1  HbstvGzUiiQBoTFxQGibwW  1702267644918  65.401010    156.76000000    156.76000000      10252.26230000  FILLED         GTC  MARKET  SELL  1702267644918            EXPIRE_MAKER          4       0.032888           233.8             15.186327  237.486573
    2   IMXUSDT   533697410           -1  13Dj1FJeITi5795gIWyN00  1702267667019   1.928267   5223.40000000   5223.40000000      10072.10982900  FILLED         GTC  MARKET  SELL  1702267667019            EXPIRE_MAKER          2       0.032310           233.8             15.032396   57.087613
    3   SNXUSDT  1057101036           -1  DlChdJwJRmwW7Lf9oNBtwu  1702267684943   4.439063   2268.80000000   2268.80000000      10071.34600000  FILLED         GTC  MARKET  SELL  1702267684943            EXPIRE_MAKER          9       0.032307           233.9             15.011603   56.354097
    4   INJUSDT   809743269           -1  JY5FbpXFxPnePCNvO5BgT8  1702308983629  22.561297    442.90000000    442.90000000       9992.39860000  FILLED         GTC  MARKET  SELL  1702308983629            EXPIRE_MAKER         10       0.030714           243.9             15.039906  -22.595406
    5  ORDIUSDT   238514100           -1  hWGYLLB2hBZNqWnhQ1AuMg  1702361706283  51.710000    193.38000000    193.38000000       9999.67980000  FILLED         GTC   LIMIT  SELL  1702353642364            EXPIRE_MAKER          7       0.031247           250.2             15.314370  -15.249150
    6   FTTUSDT   694080600           -1  RTIfMBTiRUilKbGM6QWnr9  1702464665994   5.500400   1818.04000000   1818.04000000       9999.94721600  FILLED         GTC   LIMIT  SELL  1702353638922            EXPIRE_MAKER          3       0.031305           251.3             15.380309  -15.390928
    7   FETUSDT   956488383           -1  RCLyLqsTG2os2Zq5nDHtJO  1702940167510   0.687657  14769.00000000  14769.00000000      10156.01120000  FILLED         GTC  MARKET  SELL  1702940167510            EXPIRE_MAKER         12       0.031685           240.4             15.098148  141.077352
    8   STXUSDT   658898595           -1  FnIGPOiB6Hfp95EQA6NjrC  1702942206075   1.225800   8239.80000000   8239.80000000      10100.34684000  FILLED         GTC   LIMIT  SELL  1702941873518            EXPIRE_MAKER         13       0.030880           240.9             14.856532   85.498898
    '''
    symbol = coin + 'USDT' if not coin.endswith('USDT') else coin

    try: df = pd.DataFrame(engine.connect().execute(text(f'SELECT * FROM binance_position_sell WHERE symbol = :symbol ORDER BY transactTime DESC LIMIT 1'), {'symbol': symbol}).fetchall())
    except: return send_msg(f'binance_position_sell table does not exist', from_id)

    if df.empty: return send_msg(f'No sell record for {coin}', from_id)

    price = df['price'].values[0]
    # price = float(price)

    # get current price of coin
    current_price = get_token_price(coin)

    send_msg(f"{coin}\n\nLast Sell Price: {format_number(price)}\nCurrent Price: {format_number(current_price)}\nPrice % Diff: {(current_price - price) / price * 100:.2f}%", from_id)
    return price


# define a function to read hot_coin_history table and use get_token_price_table() get current price datafram as df, merge the table, create a new column with value of the price up percentage, then make a string and broadcast to TG
def calculate_hot_coin_price_change(from_id=None):

    # from hot_coin_history select the latest date, then select all rows with that date
    latest_date = pd.DataFrame(engine.connect().execute(text('SELECT MAX(date) FROM hot_coin_history')).fetchall())
    latest_date = latest_date.values[0][0]
    try: df = pd.DataFrame(engine.connect().execute(text('SELECT * FROM hot_coin_history WHERE date = :date'), {'date': latest_date}).fetchall())
    except: return 'hot_coin_history table does not exist'

    if df.empty: return 'hot_coin_history table is empty'

    '''hot_coin_history table format
            coin  priceChangePercent       price  turnover_ratio  turnover_by_priceChangePercent         token_slug              date
    0        QI               2.116    0.025580            0.82                        0.387524              benqi  2023-12-14 22:05
    1      RNDR               0.802    4.525000            0.15                        0.187032             render  2023-12-14 22:05
    2       FET               5.907    0.701000            0.34                        0.057559              fetch  2023-12-14 22:05
    3   AUCTION              19.603   29.530000            0.73                        0.037239       bounce-token  2023-12-14 22:05
    4       FUN              27.756    0.010591            0.81                        0.029183           funtoken  2023-12-14 22:05
    5       WOO              17.930    0.365700            0.23                        0.012828           wootrade  2023-12-14 22:05
    6   AUCTION              15.892   27.930000            0.94                        0.059149       bounce-token  2023-12-15 05:15
    7       FET               9.522    0.723500            0.36                        0.037807              fetch  2023-12-15 05:15
    8      AAVE              21.936  117.010000            0.22                        0.010029               aave  2023-12-15 05:15
    9   AUCTION               0.108   27.900000            0.65                        6.018519       bounce-token  2023-12-16 05:15
    10      WOO              16.499    0.416600            0.20                        0.012122           wootrade  2023-12-16 05:15
    11      ICP              34.965    9.152000            0.10                        0.002860  internet-computer  2023-12-16 05:15
    '''

    # get current price of coin
    df_current_price = get_token_price_table()
    '''df_current_price
            symbol     lastPrice      coin
    0         BTCUSDT  43085.180000       BTC
    1         ETHUSDT   2235.790000       ETH
    2         BNBUSDT    245.100000       BNB
    3         BCCUSDT      0.000000       BCC
    4         NEOUSDT     12.730000       NEO
    ..            ...           ...       ...
    470      AEURUSDT      1.092000      AEUR
    471       JTOUSDT      2.605500       JTO
    472  1000SATSUSDT      0.000740  1000SATS
    473      BONKUSDT      0.000022      BONK
    474       ACEUSDT     14.176700       ACE
    [475 rows x 3 columns]
    '''
    
    # merge df and df_current_price
    df = pd.merge(df, df_current_price, how='left', on='coin')

    # calculate the price up percentage, make sure the data type is float
    df['price_up_percentage'] = (df['lastPrice'] - df['price']) / df['price'] * 100

    for index, row in df.iterrows():
        coin = row['coin']
        price = row['price']
        lastPrice = row['lastPrice']
        price_up_percentage = row['price_up_percentage']
        token_slug = row['token_slug']
        URL = f'https://coinmarketcap.com/currencies/{token_slug}/'
        date = row['date']
        time_delta = datetime.now() - datetime.strptime(date, '%Y-%m-%d %H:%M')
        time_delta = str(time_delta).split('.')[0]
        reply_string = f"{index+1}. [{coin}]({URL}) \nReport Price: {format_number(price)}\nCurrent Price: {format_number(lastPrice)}\nPrice % Change: {price_up_percentage:.2f}%\nTime Delta: {time_delta}"
        if not from_id: broadcast_markdown(reply_string)
        else: send_msg_markdown(reply_string, from_id)
        # send_msg_markdown(reply_string, TG_BOT_OWNER_ID)

    return


def binance_today_short_coin(from_id = TG_BOT_OWNER_ID, tradingbot_status = False):

    df_ticker = pd.read_json(BINANCE_TICKER_URL)

    # Keep symbol, priceChangePercent, lastPrice, openPrice, highPrice, lowPrice, volume, quoteVolume, openTime, closeTime
    df_ticker = df_ticker.loc[:, ['symbol', 'priceChangePercent', 'lastPrice', 'openPrice', 'highPrice', 'lowPrice', 'quoteVolume', 'openTime', 'closeTime']]

    # pick up the symbol endswith 'USDT'
    df_ticker = df_ticker[df_ticker['symbol'].str.endswith('USDT')]

    df_ticker = df_ticker[(df_ticker['priceChangePercent'] < -1) & (df_ticker['priceChangePercent'] > -20) & (df_ticker['lastPrice'] > 0.0001) & (df_ticker['lastPrice'] < 1000)]

    if df_ticker.empty: return []

    # df_ticker = df_ticker.sort_values(by='quoteVolume', ascending=False)
    df_ticker['coin'] = df_ticker['symbol'].str[:-4]

    # sort by 'turnover_by_priceChangePercent' in descending order
    df_ticker = df_ticker.sort_values(by='quoteVolume', ascending=False)

    # Keep the top 30 coins
    df_ticker = df_ticker.head(10)

    # make a coin list
    today_short_coin_list = df_ticker['coin'].values.tolist()
    
    global SHORT_COINS_LIST

    if today_short_coin_list: 
        for index, row in df_ticker.iterrows():
            time.sleep(1)
            coin = row['coin']

            long_or_short = analyze_symbol(coin, tradingbot_status)
            short = long_or_short['short']

            if not short: 
                if coin in SHORT_COINS_LIST: SHORT_COINS_LIST.remove(coin)
                continue

            if not weekly_rsi_over_high(coin): 
                if coin in SHORT_COINS_LIST: SHORT_COINS_LIST.remove(coin)
                continue

            SHORT_COINS_LIST.append(coin)

    if SHORT_COINS_LIST: send_msg(f"Coins ready to short:\n\n{', '.join(SHORT_COINS_LIST)}", from_id)
    
    return SHORT_COINS_LIST


# From the returned dictionary, get market_cap, fully_diluted_market_cap and calculate the circulating ratio
def get_token_market_cap_and_ratio(token_symbol, turnover_ratio_eth=None):
    if not turnover_ratio_eth: turnover_ratio_eth = get_turnover_ratio_from_coinmarketcap(coin='ETH')
    try:
        token_info = get_token_info_from_coinmarketcap(token_symbol)
        if token_info:
            market_cap = token_info['quote']['USD']['market_cap']
            fully_diluted_market_cap = token_info['quote']['USD']['fully_diluted_market_cap']
            if fully_diluted_market_cap > FULLLY_DILUTED_MARKET_CAP_UP_LIMIT: 
                add_coin_to_ignore_list(token_symbol, from_id = TG_BOT_OWNER_ID)
                return
            if market_cap < MARKET_CAP_DOWN_LIMIT: return
            circulating_ratio = market_cap / fully_diluted_market_cap
            circulating_ratio = round(circulating_ratio, 2)
            if circulating_ratio < CIRCULATION_RATIO: return 
            # Calculate turnover ratio
            turnover_ratio = token_info['quote']['USD']['volume_24h'] / market_cap
            turnover_ratio = round(turnover_ratio, 2)
            if turnover_ratio < turnover_ratio_eth: return

            current_price = token_info['quote']['USD']['price']
            coin_rank = token_info['cmc_rank']
                
            return {'market_cap': int(market_cap), 'fully_diluted_market_cap': int(fully_diluted_market_cap), 'circulation_ratio': circulating_ratio, 'turnover_ratio': turnover_ratio, 'token_slug': token_info['slug'], 'current_price': current_price, 'coin_rank': coin_rank}
    except: return 


def binance_today_hot_coin(trading_volume_limit = TRADING_VOLUME_LIMIT, only_check = False, from_id = None, tradingbot_status = False):

    df_ticker = pd.read_json(BINANCE_TICKER_URL)

    # Keep symbol, priceChangePercent, lastPrice, openPrice, highPrice, lowPrice, volume, quoteVolume, openTime, closeTime
    df_ticker = df_ticker.loc[:, ['symbol', 'priceChangePercent', 'lastPrice', 'openPrice', 'highPrice', 'lowPrice', 'quoteVolume', 'openTime', 'closeTime']]

    # pick up the symbol endswith 'USDT'
    df_ticker = df_ticker[df_ticker['symbol'].str.endswith('USDT')]

    df_ticker = df_ticker[(df_ticker['priceChangePercent'] > 1) & (df_ticker['quoteVolume'] > trading_volume_limit) & (df_ticker['priceChangePercent'] < 20) & (df_ticker['lastPrice'] > 0.0001) & (df_ticker['lastPrice'] < 1000)]

    if df_ticker.empty:
        print(f"1) No hot coin today after filtering the coins with priceChangePercent > 1 and quoteVolume > {trading_volume_limit} and priceChangePercent < 20 and lastPrice between 0.0001 and 1000")
        if only_check: broadcast_text(f"No hot coin today after filtering the coins with 20% > priceChangePercent > 1% and quoteVolume > {format_number(trading_volume_limit)} and lastPrice between 0.0001 and 1000")
        return []

    # df_ticker = df_ticker.sort_values(by='quoteVolume', ascending=False)
    df_ticker['coin'] = df_ticker['symbol'].str[:-4]

    # Eliminate the coins with 'USD' in coin name
    df_ticker = df_ticker[~df_ticker['coin'].str.contains('USD')]

    # Read the ignore_list from database
    IGNORE_LIST = get_ignore_list()
    df_ticker = df_ticker[~df_ticker['coin'].isin(IGNORE_LIST)]
    if df_ticker.empty:
        print(f"2) No hot coin today after eliminate the coins in IGNORE_LIST: {IGNORE_LIST}")
        if only_check: broadcast_text(f"No hot coin today after narrowing down to the coins in WHITE_LIST:\n\n{', '.join(WHITE_LIST)}")
        return []

    if not tradingbot_status:
        print(f"Trading bot is off, only check white_list coins")
        # Read white_list from database
        WHITE_LIST = get_white_list()
        df_ticker = df_ticker[df_ticker['coin'].isin(WHITE_LIST)]
        if df_ticker.empty:
            print(f"2-1) No hot coin today after narrowing down to the coins in WHITE_LIST: {WHITE_LIST}")
            if only_check: broadcast_text(f"No hot coin today after narrowing down to the coins in WHITE_LIST:\n\n{', '.join(WHITE_LIST)}")
            return []

    turnover_ratio_eth = get_turnover_ratio_from_coinmarketcap(coin='ETH')

    # Update ticker with market cap and fully diluted market cap
    df_ticker['market_cap'] = 0
    df_ticker['fully_diluted_market_cap'] = 0
    df_ticker['ratio'] = 0.01
    for index, row in df_ticker.iterrows():
        coin = row['coin']
        token_info = get_token_market_cap_and_ratio(coin, turnover_ratio_eth)
        if token_info:
            '''{'market_cap': 153456101, 'fully_diluted_market_cap': 303272927, 'circulation_ratio': 0.51, 'turnover_ratio': 0.07}'''
            df_ticker.loc[index, 'market_cap'] = int(token_info['market_cap'])
            df_ticker.loc[index, 'fully_diluted_market_cap'] = int(token_info['fully_diluted_market_cap'])
            df_ticker.loc[index, 'circulation_ratio'] = float(token_info['circulation_ratio'])
            df_ticker.loc[index, 'turnover_ratio'] = float(token_info['turnover_ratio'])
            df_ticker.loc[index, 'token_slug'] = token_info['token_slug']
        else: df_ticker.drop(index, inplace=True)

    if df_ticker.empty:
        print(f"3) No hot coin today after filtering the coins with market_cap between 100M and 5B and turnover_ratio > ETH's {turnover_ratio_eth} and circulation_ratio > {CIRCULATION_RATIO}")
        if only_check: broadcast_text(f"No hot coin today after filtering the coins with market_cap between 100M and 5B and turnover_ratio > ETH's {turnover_ratio_eth} and circulation_ratio > {CIRCULATION_RATIO}")
        return []

    # add a new column 'turnover_by_priceChangePercent' = turnover_ratio / priceChangePercent
    df_ticker['turnover_by_priceChangePercent'] = df_ticker['turnover_ratio'] / df_ticker['priceChangePercent']

    # sort by 'turnover_by_priceChangePercent' in descending order
    df_ticker = df_ticker.sort_values(by='turnover_by_priceChangePercent', ascending=False)

    # Keep the top 30 coins
    df_ticker = df_ticker.head(10)

    # make a coin list
    today_hot_coin_list = df_ticker['coin'].values.tolist()
    
    final_hotcoin_list = []

    if today_hot_coin_list: 

        i = 0
        
        for index, row in df_ticker.iterrows():
            if i > 10: break

            time.sleep(1)
            coin = row['coin']

            long_or_short = analyze_symbol(coin, tradingbot_status)
            '''{'long': True, 'short': False}'''
            long = long_or_short['long']
            # short = long_or_short['short']

            if not long: continue
            if weekly_rsi_over_high(coin): continue

            i += 1

            price = row['lastPrice']
            priceChangePercent = row['priceChangePercent']
            turnover_ratio = row['turnover_ratio']
            turnover_by_priceChangePercent = row['turnover_by_priceChangePercent']
            token_slug = row['token_slug']
            URL = f'https://coinmarketcap.com/currencies/{token_slug}/'
            reply_string = f"{i} [{coin}]({URL}) | +{priceChangePercent}% | {format_number(price)} | {round(turnover_ratio, 2)} | {round(turnover_by_priceChangePercent*100, 3)}"

            # make a dictionary of this coin and append to "hot_coin_history"
            hot_coin_history = {
                'coin': coin, 
                'priceChangePercent': priceChangePercent, 
                'price': price, 
                'turnover_ratio': turnover_ratio, 
                'turnover_by_priceChangePercent': turnover_by_priceChangePercent,
                'token_slug': token_slug,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                }

            # make dictionary to dataframe
            df_hot_coin_history = pd.DataFrame(hot_coin_history, index=[0])
            
            # append df_hot_coin_history to hot_coin_history table
            df_hot_coin_history.to_sql('hot_coin_history', engine, if_exists='append', index=False)

            # send_msg_markdown(reply_string, from_id)
            if only_check: broadcast_markdown(reply_string)

            final_hotcoin_list.append(coin)
            
        if only_check and not i: broadcast_text(f"No hot coin for today after filtering with our strategy, which assesses a cryptocurrency's performance across 4h, 1h, 15m, and 5m intervals. It checks if the price is above the 34-period SMA and if the 14-period RSI is higher than its SMA. All conditions must be met in each interval for a positive signal, which none have achieved today.")

    if SHORT_COINS_LIST: send_msg(f"Coins turning down: \n\n{', '.join(SHORT_COINS_LIST)}", from_id)

    return final_hotcoin_list

'''df_profit = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_position_sell')).fetchall())
      symbol     orderId  orderListId           clientOrderId   transactTime       price         origQty     executedQty cummulativeQuoteQty  status timeInForce    type  side    workingTime selfTradePreventionMode  update_id  sell_cost_bnb  sell_bnb_price  total_bnb_cost_value       profit
0    FTTUSDT   688100726           -1  d8JXSWSmsEmVQoDqv3dIbC  1702224291468    5.562989   1942.29000000   1942.29000000      10804.93829100  FILLED         GTC  MARKET  SELL  1702224291468            EXPIRE_MAKER          1       0.033751           240.3             15.548180   789.421552
1   EGLDUSDT  1235576864           -1  HbstvGzUiiQBoTFxQGibwW  1702267644918   65.401010    156.76000000    156.76000000      10252.26230000  FILLED         GTC  MARKET  SELL  1702267644918            EXPIRE_MAKER          4       0.032888           233.8             15.186327   237.486573
2    IMXUSDT   533697410           -1  13Dj1FJeITi5795gIWyN00  1702267667019    1.928267   5223.40000000   5223.40000000      10072.10982900  FILLED         GTC  MARKET  SELL  1702267667019            EXPIRE_MAKER          2       0.032310           233.8             15.032396    57.087613
3    SNXUSDT  1057101036           -1  DlChdJwJRmwW7Lf9oNBtwu  1702267684943    4.439063   2268.80000000   2268.80000000      10071.34600000  FILLED         GTC  MARKET  SELL  1702267684943            EXPIRE_MAKER          9       0.032307           233.9             15.011603    56.354097
4    INJUSDT   809743269           -1  JY5FbpXFxPnePCNvO5BgT8  1702308983629   22.561297    442.90000000    442.90000000       9992.39860000  FILLED         GTC  MARKET  SELL  1702308983629            EXPIRE_MAKER         10       0.030714           243.9             15.039906   -22.595406
5   ORDIUSDT   238514100           -1  hWGYLLB2hBZNqWnhQ1AuMg  1702361706283   51.710000    193.38000000    193.38000000       9999.67980000  FILLED         GTC   LIMIT  SELL  1702353642364            EXPIRE_MAKER          7       0.031247           250.2             15.314370   -15.249150
6    FTTUSDT   694080600           -1  RTIfMBTiRUilKbGM6QWnr9  1702464665994    5.500400   1818.04000000   1818.04000000       9999.94721600  FILLED         GTC   LIMIT  SELL  1702353638922            EXPIRE_MAKER          3       0.031305           251.3             15.380309   -15.390928
7    FETUSDT   956488383           -1  RCLyLqsTG2os2Zq5nDHtJO  1702940167510    0.687657  14769.00000000  14769.00000000      10156.01120000  FILLED         GTC  MARKET  SELL  1702940167510            EXPIRE_MAKER         12       0.031685           240.4             15.098148   141.077352
8    STXUSDT   658898595           -1  FnIGPOiB6Hfp95EQA6NjrC  1702942206075    1.225800   8239.80000000   8239.80000000      10100.34684000  FILLED         GTC   LIMIT  SELL  1702941873518            EXPIRE_MAKER         13       0.030880           240.9             14.856532    85.498898
9   NEARUSDT  2110473867           -1  b1vSFIYMRLWZrz4ecPsPaZ  1703034724092    2.550000   3960.70000000   3960.70000000      10099.78500000  FILLED         GTC   LIMIT  SELL  1703019732394            EXPIRE_MAKER          8       0.031232           254.2             15.428633    84.505367
10  SANDUSDT  2782080420           -1  C9lGCy1BllCj9kATi9iaGz  1703211765923    0.554000  18230.00000000  18230.00000000      10099.42000000  FILLED         GTC   LIMIT  SELL  1703019727319            EXPIRE_MAKER          5       0.031214           272.0             15.984787    83.772213
11  BAKEUSDT   657386867           -1  nEZ0RcxsNDo5G7pO7Lp9EE  1703227338598    0.421900  24887.00000000  24887.00000000      10499.82530000  FILLED         GTC   LIMIT  SELL  1703225114459            EXPIRE_MAKER         15       0.027083           273.4             14.873934   484.989486
12  BAKEUSDT   657615307           -1  Ah0I3w2XaYjd9qywfk03VK  1703227686811    0.431500  24334.20000000  24334.20000000      10500.20730000  FILLED         GTC   LIMIT  SELL  1703227513810            EXPIRE_MAKER         16       0.027978           272.9             15.261983   484.980807
13  BAKEUSDT   657707687           -1  74l6EIBov0YnUQzE7gk7mg  1703228412194    0.454900  23082.70000000  23082.70000000      10500.32023000  FILLED         GTC   LIMIT  SELL  1703227813069            EXPIRE_MAKER         17       0.027117           271.3             14.743589   485.601201
14   TRBUSDT   920027678           -1  XAYNWwD1K3HyahklWGskgz  1703275730432  174.980000     57.72000000     57.72000000      10099.84560000  FILLED         GTC   LIMIT  SELL  1703266208873            EXPIRE_MAKER         19       0.027617           270.8             14.971105    85.165795
15  AAVEUSDT  1522571378           -1  nuPlSOkci275D8OuMM7sBc  1703301012848   97.582201     91.62700000     91.62700000       8941.16429000  FILLED         GTC  MARKET  SELL  1703301012848            EXPIRE_MAKER         11       0.025097           267.0             14.163937 -1072.991997
16  RUNEUSDT  1274638830           -1  J0htytqcx0J3XYNFpbIFSd  1703301018111    5.205126   1515.40000000   1515.40000000       7887.84790000  FILLED         GTC  MARKET  SELL  1703301018111            EXPIRE_MAKER          6       0.022157           267.0             13.402615 -2125.090815
17  RNDRUSDT   560303558           -1  8V51QCjt4eJs5nt4munpXV  1703317812922    4.293253   2211.48000000   2211.48000000       9494.44291000  FILLED         GTC  MARKET  SELL  1703317812922            EXPIRE_MAKER         18       0.026700           266.5             14.606195  -520.130695
18  ALGOUSDT  1618310425           -1  8hOfRMyuVpceE9NHwoXLvm  1703325459228    0.242900  41583.00000000  41583.00000000      10100.51070000  FILLED         GTC   LIMIT  SELL  1703290509559            EXPIRE_MAKER         21       0.027694           268.1             14.935455    85.722145
19  ORDIUSDT   374002265           -1  rnQoSqo4haAR3ZCuA2Jv7R  1703364103075   53.527000    188.69000000    188.69000000      10100.00963000  FILLED         GTC   LIMIT  SELL  1703350509711            EXPIRE_MAKER         22       0.027713           270.6             14.984311    85.027879
20  ORDIUSDT   374865940           -1  IX9u6c7hHB6Yuq15kN9NPa  1703367036730   53.907000    187.36000000    187.36000000      10100.01552000  FILLED         GTC   LIMIT  SELL  1703364608675            EXPIRE_MAKER         24       0.027736           270.8             15.010696    85.071864
21  CAKEUSDT   596213818           -1  wEPZaI4U1oIzz40FP2BInA  1703368656462    2.939000   3436.61000000   3436.61000000      10100.19679000  FILLED         GTC   LIMIT  SELL  1703363409736            EXPIRE_MAKER         23       0.027705           271.0             15.002252    85.219678
22  ATOMUSDT  2582908475           -1  8ClVCLA10FkWiwpvssTUUx  1703407646491   11.620000    869.17000000    869.17000000      10099.75540000  FILLED         GTC   LIMIT  SELL  1703266206495            EXPIRE_MAKER         14       0.027261           268.7             14.841084    85.021496
23  CAKEUSDT   596437527           -1  L0UsaZhryFgw35dwIdzpvo  1703428973754    2.994000   3373.90000000   3373.90000000      10101.45660000  FILLED         GTC   LIMIT  SELL  1703371509130            EXPIRE_MAKER         25       0.027619           270.8             14.978011    86.505009
24  CAKEUSDT   597800248           -1  srwR5rF9tSfqU51NSBsajv  1703430904522    3.074000   3285.53000000   3285.53000000      10099.71922000  FILLED         GTC   LIMIT  SELL  1703429409548            EXPIRE_MAKER         27       0.027593           270.6             14.947366    84.795314
25   GRTUSDT  1380284656           -1  lVlMTloc0HjnRwnMi8bVP5  1703438762459    0.195800  51585.00000000  51585.00000000      10100.34300000  FILLED         GTC   LIMIT  SELL  1703281507217            EXPIRE_MAKER         20       0.027448           268.2             14.841296    85.614604
26  EGLDUSDT  1257719586           -1  8WzAF3o6SMGuOTgxmB6syD  1703461664725   74.220000    136.08000000    136.08000000      10099.85760000  FILLED         GTC   LIMIT  SELL  1703457309089            EXPIRE_MAKER         28       0.028138           265.0             14.910151    85.638949
27  EGLDUSDT  1257871388           -1  8Ji10eP1eZ7ofhGwCYmqQX  1703463345710   74.410000    135.74000000    135.74000000      10100.41340000  FILLED         GTC   LIMIT  SELL  1703463310828            EXPIRE_MAKER         29       0.028312           264.3             14.976958    85.672042
28  ORDIUSDT   380939246           -1  7eaEqGmblpQCUygjD7Uexf  1703476274498   55.996000    180.37000000    180.37000000      10099.99852000  FILLED         GTC   LIMIT  SELL  1703426409251            EXPIRE_MAKER         26       0.027691           264.9             14.806586    85.220994
'''

# Define a function to check the sum of the profit of all coins in binance_position_sell table and compare with USDT balance of get_coin_wallet_balance_with_locked(), if the INITIAL_FUND + profit - USDT Balance = amount_to_be_adjusted, then creat a new row for the table to put the - amount_to_be_adjusted number to the table, make the new sum of profit = INITIAL_FUND + profit - amount_to_be_adjusted.
def binance_adjust_profit(from_id = None):
    df_balance_all = pd.DataFrame(engine.connect().execute(text('SELECT coin, executedQty FROM binance_position_buy WHERE is_closed = 0')).fetchall())
    if not df_balance_all.empty: 
        if from_id: send_msg(f"Only can adjust profit when all positions are closed", from_id)
        return 0
    # Get the sum of profit of all coins in binance_position_sell table
    df_profit = pd.DataFrame(engine.connect().execute(text('SELECT sum(profit) FROM binance_position_sell')).fetchall())
    df_profit.columns = ['profit']
    profit = df_profit['profit'][0]
    spot_balance = get_coin_wallet_balance_with_locked()
    '''{'BNB': '2.043559780', 'ONG': '131820', 'USDT': '100161.787261640'}'''
    USDT_balance = float(spot_balance['USDT'])
    amount_to_be_adjusted = USDT_balance - (INITIAL_FUND + profit)
    if int(amount_to_be_adjusted) != 0:
        adjust_dict = {
            "symbol": "ADJUSTUSDT",
            "orderId": 1234567890,
            "orderListId": -1,
            "clientOrderId": "AAAAAAAAAAAAAAAAAAAAAA",
            "transactTime": datetime.now().timestamp() * 1000,
            "price": amount_to_be_adjusted,
            "origQty": "1",
            "executedQty": "1",
            "cummulativeQuoteQty": "1",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "LIMIT",
            "side": "NONE",
            "workingTime": datetime.now().timestamp() * 1000,
            "selfTradePreventionMode": "EXPIRE_MAKER",
            "update_id": 0,
            "sell_cost_bnb": 0,
            "sell_bnb_price": 0,
            "total_bnb_cost_value": 0,
            "profit": amount_to_be_adjusted,
            }
        # make dictionary to dataframe
        df_adjust = pd.DataFrame(adjust_dict, index=[0])
        df_adjust.to_sql('binance_position_sell', engine, if_exists='append', index=False)
        reply_string = f"Profit: {format_number(profit)}\nUSDT Balance: {format_number(USDT_balance)}\nAmount to be adjusted: {format_number(amount_to_be_adjusted)}\nNew Profit: {format_number(profit + amount_to_be_adjusted)}\n\nALL SET!"
        send_msg(reply_string, TG_BOT_OWNER_ID)
    return amount_to_be_adjusted


if __name__ == '__main__':
    print('Binance_api.py is running')

    binance_today_short_coin(from_id = TG_BOT_OWNER_ID, tradingbot_status = trading_bot_switch_status())