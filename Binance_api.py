from Top_functions import *
from Generate_token import *

CMC_NO_DATA = ['EUR', 'BEAMX']

parameters_dict = read_trading_parameters()

TRADING_VOLUME_LIMIT = parameters_dict.get('trading_volume_limit', 50_000_000)
INITIAL_FUND = parameters_dict.get('initial_fund_spot', 200_000)
CHECK_SIZE = parameters_dict.get('check_size', 20_000)
POSITIONS_LIMIT = parameters_dict.get('position_limit_spot', 10)
TARGET_PROFIT_PERCENTAGE = parameters_dict.get('target_profit_percentage', 0.13)
TARGET_PROFIT_USDT = parameters_dict.get('target_profit_usdt', 300)
FULLLY_DILUTED_MARKET_CAP_UP_LIMIT = parameters_dict.get('fully_diluted_market_cap_up_limit', 5_000_000_000)
MARKET_CAP_DOWN_LIMIT = parameters_dict.get('market_cap_down_limit', 30_000_000)
CIRCULATION_RATIO = parameters_dict.get('circulation_ratio', 0.3)
DAILY_TARGET_PROFIT = parameters_dict.get('daily_target_profit', 2000)
DAILY_NEW_POSITIONS_LIMIT = parameters_dict.get('daily_new_positions_limit', 2)
TRADING_BOT_STATUS = parameters_dict.get('trading_bot_status', 0)
INITIAL_FUNDING_FUND = parameters_dict.get('initial_funding_fund', 300_000)
BOT_STARTING_DATE = parameters_dict.get('bot_starting_date')
TARGET_PROFIT = TARGET_PROFIT_PERCENTAGE

SHORT_COINS_LIST = []

def set_new_target_profit(target_profit, chat_id=TG_BOT_OWNER_ID):
    target_profit = float(target_profit) if target_profit else 0.01
    if target_profit > 0 and target_profit < 1:
        if set_target_profit_default(target_profit): return send_msg(f"Set target profit: {target_profit*100}%", chat_id)
    else: return send_msg(f"Target profit: {target_profit*100}% is not valid, it should be between 0 and 1. For example: 0.05 means 5%.", chat_id)


def read_positions_limit(from_id=TG_BOT_OWNER_ID):
    global POSITIONS_LIMIT
    positions_limit = get_position_limit()
    if positions_limit != POSITIONS_LIMIT: POSITIONS_LIMIT = positions_limit
    if from_id: send_msg(f"Current positions limit: {POSITIONS_LIMIT}\n\nIf you want to change your positions limit, you could use command:\n\n/set_position_limit 10", from_id)
    return POSITIONS_LIMIT


def remove_from_future_profit(coin: str, chat_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    if remove_from_future_profit_table(coin): send_msg(f"Removed {coin} from future profit table.", chat_id)
    else: send_msg(f"Failed to remove {coin} from future profit table.", chat_id)


def network_name_change(str_name: str):
    str_name = str_name.upper()
    str_name = 'ETH' if str_name.startswith("ERC") else 'TRX' if str_name.startswith("TRC") else 'BSC' if str_name.startswith("BEP") else str_name
    return str_name


def generate_bottom_msg(coin):
    return f"/as_{coin} | /cpa_{coin} | /buy_{coin}\n/tvb_{coin} | /tvs_{coin}\n/limit_buy_{coin} | /limit_sell_{coin}\n/funding_buy_{coin} | /funding_sell_{coin}\n/cpu | /gpu | /cmp | /ptt | /cpp | /cab | /ulb"


def get_trading_parameters(from_id=TG_BOT_OWNER_ID):
    parameters_dict = read_trading_parameters()
    # make a dict of parameters
    parameters_dict = {key: value for key, value in parameters_dict.items() if key not in ['ID']}
    reply_string = '\n'.join([f"{key}: {value}" for key, value in parameters_dict.items()])
    return send_msg(reply_string, from_id)


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

    if df_new.empty: 
        get_exchange_info()
        with open('binance_exchange_info.json') as f: data = json.load(f)
        df = pd.DataFrame(data['symbols'])
        df_new = df[df['symbol'].str.endswith(coin.upper()+'USDT')]
        if df_new.empty: return

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
    with engine.connect() as connection: df_response.to_sql('binance_exchange_info', connection, if_exists='append', index=False)

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
def get_token_price_table(coin_column=True):
    df_ticker = pd.read_json(BINANCE_TICKER_URL)
    df_ticker = df_ticker.loc[:, ['symbol', 'lastPrice']]
    df_ticker = df_ticker[df_ticker['symbol'].str.endswith('USDT')]
    df_ticker = df_ticker[~df_ticker['symbol'].str.contains('UP|DOWN')]
    df_ticker = df_ticker.reset_index(drop=True)
    if coin_column: df_ticker['coin'] = df_ticker['symbol'].str[:-4]
    return df_ticker

# use get_api_fuction() resutl convert to string send to chat_id
def get_api_functions_str(chat_id=TG_BOT_OWNER_ID):
    data = get_api_functions()
    if data: return send_msg('\n'.join([f'{key}: {value}' for key, value in data.items()]), chat_id)
    else: return send_msg(f"You don't have a binance API key and secrets in database yet.", chat_id)

# 账户API交易状态(USER_DATA), 获取 api 账户交易状态详情, 权重(IP): 1
# GET /sapi/v1/account/apiTradingStatus (HMAC SHA256)
# https://binance-docs.github.io/apidocs/spot/cn/#api-user_data 
def get_api_status(from_id=TG_BOT_OWNER_ID):
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
        if from_id: send_msg('\n'.join([f'{key}: {value}' for key, value in data['data'].items()]), from_id)
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

'''
查询每日资产快照 (USER_DATA)

    响应

{
   "code":200, // 200表示返回正确，否则即为错误码
   "msg":"", // 与错误码对应的报错信息
   "snapshotVos":[
      {
         "data":{
            "balances":[
               {
                  "asset":"BTC",
                  "free":"0.09905021",
                  "locked":"0.00000000"
               },
               {
                  "asset":"USDT",
                  "free":"1.89109409",
                  "locked":"0.00000000"
               }
            ],
            "totalAssetOfBtc":"0.09942700"
         },
         "type":"spot",
         "updateTime":1576281599000
      }
   ]
}

    或

{
   "code":200, // 200表示返回正确，否则即为错误码
   "msg":"", // 与错误码对应的报错信息
   "snapshotVos":[
      {
         "data":{
            "marginLevel":"2748.02909813",
            "totalAssetOfBtc":"0.00274803",
            "totalLiabilityOfBtc":"0.00000100",
            "totalNetAssetOfBtc":"0.00274750",
            "userAssets":[
               {
                  "asset":"XRP",
                  "borrowed":"0.00000000",
                  "free":"1.00000000",
                  "interest":"0.00000000",
                  "locked":"0.00000000",
                  "netAsset":"1.00000000"
               }
            ]
         },
         "type":"margin",
         "updateTime":1576281599000
      }
   ]
}

    或

{
   "code":200, // 200表示返回正确，否则即为错误码
   "msg":"", // 与错误码对应的报错信息
   "snapshotVos":[
      {
         "data":{
            "assets":[
               {
                  "asset":"USDT",
                  "marginBalance":"118.99782335", // 不会实时更新，可以忽略
                  "walletBalance":"120.23811389"
               }
            ],
            "position":[
               {
                  "entryPrice":"7130.41000000",
                  "markPrice":"7257.66239673",
                  "positionAmt":"0.01000000",
                  "symbol":"BTCUSDT",
                  "unRealizedProfit":"1.24029054" // 只显示开仓当时的未实现盈亏，不会实时更新，可以忽略
               }
            ]
         },
         "type":"futures",
         "updateTime":1576281599000
      }
   ]
}

GET /sapi/v1/accountSnapshot

权重(IP): 2400

参数:
名称 	类型 	是否必需 	描述
type 	STRING 	YES 	"SPOT", "MARGIN", "FUTURES"
startTime 	LONG 	NO 	
endTime 	LONG 	NO 	
limit 	INT 	NO 	min 7, max 30, default 7
recvWindow 	LONG 	NO 	
timestamp 	LONG 	YES 	

    查询时间范围最大不得超过30天
    仅支持查询最近 1 个月数据
    若startTime和endTime没传，则默认返回最近7天数据
'''

# Define a function to check todays binance asset value with 查询每日资产快照 rest api
def check_asset_snapshot():
    PATH = '/sapi/v1/accountSnapshot'
    timestamp = int(time.time() * 1000)
    params = {
        'type': 'SPOT',
        'limit': 1,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.get(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200: return
        data = r.json()
        return data
    except Exception as e:
        print(e)
        return 

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
    except: return send_msg(f'ERROR: Wrong amount: {amount}, please input a number.', chat_id)
    df = get_funding_asset()
    if not df.empty:
        df = df[df['asset'] == coin]
        if not df.empty:
            balance = float(df['free'].values[0])
            if balance >= amount: 
                tranId = funding_main_transfer(coin, amount)
                if tranId: 
                    time.sleep(1)
                    return tranId
            else: 
                send_msg(f"Failed to transfer {format_number(amount)} {coin} from funding account to spot account, because the balance of {coin} in funding account is: {format_number(balance)}", chat_id)
                return False
        else: 
            send_msg(f"Failed to transfer {format_number(amount)} {coin} from funding account to spot account, because the balance of {coin} in funding account is: 0", chat_id)
            return False
    send_msg(f"Failed to transfer {format_number(amount)} {coin} from funding account to spot account, network error.", chat_id)
    return False

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
    except: return send_msg(f'ERROR: Wrong amount: {amount}, please input a number.', from_id)

    df = get_user_asset()
    if not df.empty:
        df = df[df['asset'] == coin]
        if not df.empty:
            balance = float(df['free'].values[0])
            if balance >= amount: 
                tranId = main_funding_transfer(coin, amount)
                if tranId: 
                    time.sleep(1)
                    return 
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
    if not df.empty: 
        # convert free and locked to float
        df['free'] = df['free'].astype(float)
        df['locked'] = df['locked'].astype(float)
        return dict(zip(df['asset'].values, df['free'].values + df['locked'].values))
    else: return {}


def get_coin_wallet_balance_all_str(chat_id=TG_BOT_OWNER_ID):
    df = read_position_table(0, None)
    if not df.empty:
        # select only coin, amount, account columns
        df = df.loc[:, ['coin', 'amount', 'account']]
        df_balance_spot = df[df['account'] == 'spot']
        if not df_balance_spot.empty:
            coin_in_spot_position_dict = dict(zip(df_balance_spot['coin'].values, df_balance_spot['amount'].values))
            coin_in_spot_position_dict_str = '\n'.join([f"{key}: {format_number(value)}" for key, value in coin_in_spot_position_dict.items()])
            send_msg(f"Coins in spot position:\n\n{coin_in_spot_position_dict_str}", chat_id)
        df_balance_funding = df[df['account'] == 'funding']
        if not df_balance_funding.empty:
            df_balance_funding_position_dict = dict(zip(df_balance_funding['coin'].values, df_balance_funding['amount'].values))
            df_balance_funding_position_dict_str = '\n'.join([f"{key}: {format_number(value)}" for key, value in df_balance_funding_position_dict.items()])
            send_msg(f"Coins in funding position:\n\n{df_balance_funding_position_dict_str}", chat_id)
    coin_in_position_dict = {**coin_in_spot_position_dict, **df_balance_funding_position_dict}
    data_spot = get_coin_wallet_balance_with_locked()
    if data_spot: 
        '''{'AAVE': '091.627', 'BNB': '2.014138090', 'OGN': '0.58882430', 'ONG': '140000', 'RSR': '0.099999980', 'RUNE': '01515.4', 'SAND': '018230', 'USDT': '71305.788331640'}'''
        # Coins in balance except coins in position
        coin_in_balance_dict = {key: value for key, value in data_spot.items() if key not in coin_in_position_dict.keys()}
        coin_in_balance_str = '\n'.join([f"{key}: {format_number(value)}" for key, value in coin_in_balance_dict.items()])
        send_msg(f"Other coins in spot balance:\n\n{coin_in_balance_str}", chat_id)
    data_funding = get_coin_funding_balance_all()
    if data_funding:
        '''{'ENS': '1', 'GMT': '25468.3', 'KP3R': '85.13', 'LSK': '5681.1', 'ONG': '13182', 'RSR': '17872854.2', 'SXP': '23532.7', 'USDT': '118199.81977274'}'''
        # Coins in balance except coins in position
        coin_in_balance_dict = {key: value for key, value in data_funding.items() if key not in coin_in_position_dict.keys()}
        coin_in_balance_str = '\n'.join([f"{key}: {format_number(value)}" for key, value in coin_in_balance_dict.items()])
        send_msg(f"Other coins in funding balance:\n\n{coin_in_balance_str}", chat_id)


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
def get_deposit_history_by_hours(chat_id=TG_BOT_OWNER_ID, hours=24):
    try: hours = float(hours)
    except: return send_msg(f'Wrong hours: {hours}, please input a number.', chat_id)
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
        if df.empty: return send_msg(f'No deposit history in the past {hours} hours.', chat_id)
        for i in range(df.shape[0]):
            status_explanation = 'pending' if df['status'].values[i] == 0 else 'credited but cannot withdraw' if df['status'].values[i] == 6 else 'Wrong Deposit' if df['status'].values[i] == 7 else 'Waiting User confirm' if df['status'].values[i] == 8 else 'success' if df['status'].values[i] == 1 else 'unknown'
            df_dict = df.iloc[i].to_dict()
            df_dict['status'] = status_explanation
            df_dict['amount'] = format_number(df_dict['amount'])
            df_dict['insertTime'] = datetime.fromtimestamp(df_dict['insertTime']/1000).strftime('%Y-%m-%d %H:%M:%S')
            df_dict['txId'] = markdown_tokentnxs(df_dict['txId'])
            df_dict['address'] = markdown_token_address(df_dict['address'])
            reply_msg = '\n'.join([f"{key}: {value}" for key, value in df_dict.items() if value and value != ''])
            send_msg_markdown(reply_msg, chat_id)
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
    time.sleep(0.5)
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
    data_to_table(data, 'binance_withdraw_task')
    del data['withdraw_id_binance']
    del data['withdraw_id_self']
    del data['from_id']
    del data['created_at']

    string_dict = '\n'.join([f'{k}: {v}' for k, v in data.items()])
    if str(from_id) == str(TG_BOT_OWNER_ID): reply_string_from_dict = f"Please confirm the following withdraw task:\n\n{string_dict}\n\nYou can reply: \n/confirm {withdraw_id_self}\n\nOr click the following link to confirm"
    else: reply_string_from_dict = f"Please confirm the following withdraw task:\n\n{string_dict}\n\nClick the following link to confirm"
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
    try:
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(f"SELECT * FROM binance_withdraw_task WHERE withdraw_id_self = '{token}' AND withdraw_id_binance = 'waiting_for_update'")).fetchall())
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


def refill_stella_danli(usdt_amount, from_id=TG_BOT_OWNER_ID):
    return binance_pay_usdt(usdt_amount, os.getenv('STELLA_DANLI_ADDRESS'), from_id)


def refill_1000_danli(from_id=None):
    if from_id: return binance_pay_usdt(1000, os.getenv('STELLA_DANLI_ADDRESS'), from_id)


def refill_stella_leo(usdt_amount, from_id=TG_BOT_OWNER_ID):
    return binance_pay_usdt(usdt_amount, os.getenv('STELLA_LEO_ADDRESS'), from_id)


def check_transfer_and_sell_ong(usdt_amount: float, from_id=TG_BOT_OWNER_ID):
    ong_price = get_token_price('ONG')
    if ong_price == 0: return send_msg(f'Can not get ONG price.', from_id)
    ong_amount = usdt_amount / ong_price
    polish_parameters = polish_parameters_for_limit_order('ONG', ong_amount, ong_price, from_id)
    if not polish_parameters: return send_msg(f'Failed to polish parameters for ONG market sell', from_id)
    ong_amount = polish_parameters['amount']
    ong_balance = get_coin_wallet_balance('ONG')
    if ong_balance < ong_amount:
        amount_need_to_transfer = ong_amount - ong_balance
        if not funding_main_transfer_with_check_and_send('ONG', amount_need_to_transfer, from_id): return
    data = binance_market_sell('ONG', ong_amount)
    if not data: return send_msg(f'Failed to market sell ONG for USDT.', from_id)
    if 'fills' in data: del data['fills']
    data_to_table(data, 'binance_ong_sell_history')
    return True


# Define binance_pay_usdt, user input a usdt amount and a target address; then market sell coin ONG for this target usdt amount, and send the USDT to the target address with TRX network only, usdt input must less than 1000 usd.
def binance_pay_usdt(usdt_amount: float, target_address: str, from_id=TG_BOT_OWNER_ID):
    try: usdt_amount = float(usdt_amount)
    except: return send_msg(f'You need to input a number for amount, but you input: {usdt_amount}', from_id)

    if usdt_amount > 1000: return send_msg(f'You can only pay less than 1000 usdt, but you input: {usdt_amount}. \n\nIf you want to transfer more than 1000 usdt, please login to binance and transfer manually.', from_id)

    '''TRX_REGEX = r'T[1-9A-HJ-NP-Za-km-z]{33}'''
    # CHECK IF target_address IS A VALID TRX ADDRESS
    if not re.match(TRX_REGEX, target_address): return send_msg(f'Invalid TRX address: {target_address}', from_id)

    usdt_amount = round(usdt_amount, 2)

    if funding_main_transfer_with_check_and_send('USDT', usdt_amount, from_id): 
        data = {
            'coin': 'USDT',
            'amount': usdt_amount,
            'network': 'TRX',
            'to_address': target_address,
            'from_id': from_id,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        data_to_table(data, 'binance_pay_records')
        return binance_send_coin(usdt_amount, 'TRX', 'USDT', target_address, from_id)

    if check_transfer_and_sell_ong(usdt_amount, from_id):
        data = {
            'coin': 'USDT',
            'amount': usdt_amount,
            'network': 'TRX',
            'to_address': target_address,
            'from_id': from_id,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        data_to_table(data, 'binance_pay_records')
        return binance_send_coin(usdt_amount, 'TRX', 'USDT', target_address, from_id)

# df = get_df_from_given_tablename('binance_pay_records')
'''
   coin  amount network                          to_address     from_id        created_at
0  USDT  1000.0     TRX  TQKgU4QRWpfoUYBno6dG8USABkeYQRvQ72  2118900665  2024-01-13 08:56
'''

def binance_pay_record(from_id=TG_BOT_OWNER_ID):
    with engine.connect() as connection: 
        try: df = pd.DataFrame(connection.execute(text(f"SELECT * FROM binance_pay_records")).fetchall())
        except: df = pd.DataFrame()
    if df.empty: return send_msg(f'No binance_pay_records table.', from_id)
    # select amount sum of total records
    total_amount = df['amount'].sum()
    # select amount sum of this year
    this_year_amount = df[df['created_at'].str.startswith(datetime.now().strftime('%Y'))]['amount'].sum()
    # select amount sum of this month
    this_month_amount = df[df['created_at'].str.startswith(datetime.now().strftime('%Y-%m'))]['amount'].sum()
    reply_msg = f"Total payout: {format_number(total_amount)}\nThis year: {format_number(this_year_amount)}\nThis month: {format_number(this_month_amount)}"
    send_msg(reply_msg, from_id)
    return reply_msg


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
        time.sleep(0.5)
        return data
    else: 
        print(r.reason)
        return


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
        time.sleep(0.5)
        return data
    else: 
        print(r.json())
        return
'''binance_limit_sell('SAND', 18230, 0.55)
{'symbol': 'SANDUSDT', 'orderId': 2769384671, 'orderListId': -1, 'clientOrderId': 'GKVPOrFIkwz5IbsRhsx220', 'transactTime': 1702318694019, 'price': '0.55000000', 'origQty': '18230.00000000', 'executedQty': '0.00000000', 'cummulativeQuoteQty': '0.00000000', 'status': 'NEW', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'SELL', 'workingTime': 1702318694019, 'fills': [], 'selfTradePreventionMode': 'EXPIRE_MAKER'}
'''


def binance_limit_buy(coin, amount, price):
    coin = coin.upper()
    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': coin + 'USDT',
        'side': 'BUY',
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
        time.sleep(0.5)
        return data
    else: 
        print(r.json())
        return
    

def get_avg_price(coin):
    coin = coin.upper()
    PATH = '/api/v3/avgPrice'
    params = {'symbol': coin + 'USDT'}
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        return data
    else: return
'''{'mins': 5, 'price': '0.02581267', 'closeTime': 1705445177106}'''


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
        time.sleep(0.5)
        return data
    else: 
        print(r.json())
        return


def binance_cancel_order_by_orderId(coin: str, orderId):
    coin = coin.upper()
    symbol = coin if coin.endswith('USDT') else coin + 'USDT'
    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': symbol,
        'orderId': orderId,
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


def check_order_status_by_orderId(coin, orderId):
    coin = coin.upper()
    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': coin + 'USDT',
        'orderId': orderId,
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
def get_open_orders_list(from_id=None, side = 'NONE'):
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
        if df.empty: return pd.DataFrame()
        df.loc[:, 'coin'] = df['symbol'].apply(lambda x: x[:-4])  
        df_orderId = df.loc[:, ['coin', 'side', 'orderId']]
        if from_id: 
            df_orderId = df_orderId.sort_values(by=['side'])
            df_orderId_buy = df_orderId[df_orderId['side'] == 'BUY'].copy()
            if not df_orderId_buy.empty:
                df_orderId_buy.loc[:, 'cancel'] = df_orderId_buy.apply(lambda x: f"/as_{x['coin']} | /cancel_{x['coin']}_{x['orderId']}", axis=1)
                df_dict_string_buy = df_orderId_buy['cancel'].to_list()
                df_dict_string_buy = '\n'.join(df_dict_string_buy)
                send_msg(f"Open BUY orders ({df_orderId_buy.shape[0]}):\n\n{df_dict_string_buy}", from_id)
            df_orderId_sell = df_orderId[df_orderId['side'] == 'SELL'].copy()
            if not df_orderId_sell.empty:
                df_orderId_sell.loc[:, 'cancel'] = df_orderId_sell.apply(lambda x: f"/as_{x['coin']} | /cancel_{x['coin']}_{x['orderId']}", axis=1)
                df_dict_string_sell = df_orderId_sell['cancel'].to_list()
                df_dict_string_sell = '\n'.join(df_dict_string_sell)
                send_msg(f"Open SELL orders ({df_orderId_sell.shape[0]}):\n\n{df_dict_string_sell}", from_id)
        df_orderId = df_orderId[df_orderId['side']==side] if side == 'BUY' or side == 'SELL' else df_orderId
        return df_orderId
    else: print(r.json())
    return pd.DataFrame()


# Define cancel all of the open orders
def binance_cancel_all_orders(from_id=None, side = 'NONE'):
    df_orderId = get_open_orders_list(from_id, side)
    if df_orderId.empty: return send_msg(f'No open orders', from_id)
    for index, row in df_orderId.iterrows(): 
        data = binance_cancel_order_by_orderId(row['coin'], row['orderId'])
        if from_id: 
            if data: send_msg(f"/as_{row['coin']} limit order canceled successfully", from_id)
            else: send_msg(f"Failed to cancel /as_{row['coin']} limit order: \n/cancel_{row['coin']}_{row['orderId']}", from_id)
    return 


# cancel all BUY orders
def cancel_all_buy_orders(from_id=None):
    df_orderId = get_open_orders_list(from_id, 'BUY')
    if df_orderId.empty: return send_msg('No open buy orders.', from_id)
    for index, row in df_orderId.iterrows():
        coin = row['coin']
        orderId = row['orderId']
        data = binance_cancel_order_by_orderId(coin, orderId)
        if from_id: 
            if data: send_msg(f"/as_{coin} limit buy canceled.", from_id)
            else: send_msg(f"Failed to cancel /as_{coin} limit buy order: \n/cancel_{coin}_{orderId}", from_id)
    return


def cancel_all_sell_orders(from_id=None):
    df_orderId = get_open_orders_list(from_id, 'SELL')
    if df_orderId.empty: 
        if from_id: send_msg('No open sell orders.', from_id)
        return
    for index, row in df_orderId.iterrows():
        coin = row['coin']
        orderId = row['orderId']
        data = binance_cancel_order_by_orderId(coin, orderId)
        if from_id: 
            if data: send_msg(f"/as_{coin} limit sell canceled.", from_id)
            else: send_msg(f"Failed to cancel /as_{coin} limit sell order: \n/cancel_{coin}_{orderId}", from_id)
    return


# Define a function to check the last filled orders for a given coin, side = 'BUY' or 'SELL'
def get_last_filled_orders(coin, side = 'BUY', time_offset = 24):
    coin = coin.upper()
    PATH = '/api/v3/myTrades'
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': coin + 'USDT',
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        df = pd.DataFrame(data)
        if df.empty: return pd.DataFrame()
        df.loc[:, 'coin'] = df['symbol'].apply(lambda x: x[:-4])  
        # Keep only isBuyer
        df = df[df['isBuyer']] if side == 'BUY' else df[~df['isBuyer']] if side == 'SELL' else df
        # Keep only coin, orderId
        df_orderId = df.loc[:, ['coin', 'orderId', 'time']]
        # Keep only the orderId within last 24 hours
        df_orderId = df_orderId[df_orderId['time'] >= int(datetime.now().timestamp() * 1000) - time_offset * 60 * 60 * 1000]
        # Group by orderId, and time column keep only the latest one
        df_orderId = df_orderId.groupby('orderId').last()
        # Sort by time, Descending
        df_orderId = df_orderId.sort_values(by=['time'], ascending=False)
        return df_orderId
    else: 
        print(r.json())
        return pd.DataFrame()
    

def read_position_table_of_this_year(is_close = 1, coin = None, engine = engine):
    with engine.connect() as conn: 
        if not coin: 
            try: df_position = pd.DataFrame(conn.execute(text(f"SELECT coin, symbol, price_close FROM position_table WHERE is_closed = {is_close} AND year_create = {datetime.now().year}")).fetchall())
            except: df_position = pd.DataFrame()
        else:
            try: df_position = pd.DataFrame(conn.execute(text(f"SELECT coin, symbol, price_close FROM position_table WHERE is_closed = {is_close} AND coin = '{coin}' AND year_create = {datetime.now().year}")).fetchall())
            except: df_position = pd.DataFrame()
    return df_position


def read_position_table_account(is_close = 0, coin = None, account = 'spot', engine = engine):
    with engine.connect() as conn: 
        if not coin: 
            try: df_position = pd.DataFrame(conn.execute(text(f"SELECT * FROM position_table WHERE is_closed = {is_close} AND account = '{account}'")).fetchall())
            except: df_position = pd.DataFrame()
        else:
            try: df_position = pd.DataFrame(conn.execute(text(f"SELECT * FROM position_table WHERE is_closed = {is_close} AND coin = '{coin}' AND account = '{account}'")).fetchall())
            except: df_position = pd.DataFrame()
    return df_position


def read_position_table_by_orderId_close(orderId_close, engine = engine):
    with engine.connect() as conn: 
        try: df_position = pd.DataFrame(conn.execute(text(f"SELECT * FROM position_table WHERE orderId_close = {orderId_close}")).fetchall())
        except: df_position = pd.DataFrame()
    return df_position


def read_position_table_by_orderId_create(orderId_create, engine = engine):
    with engine.connect() as conn: 
        try: df_position = pd.DataFrame(conn.execute(text(f"SELECT * FROM position_table WHERE orderId_create = {orderId_create}")).fetchall())
        except: df_position = pd.DataFrame()
    return df_position


def update_limit_orderId_in_position_table(orderId_create, orderId_close, target_profit = 0.1, is_manual = 0, engine = engine):
    with engine.connect() as conn: 
        try:
            conn.execute(text(f"UPDATE position_table SET orderId_close = {orderId_close}, target_profit = {target_profit}, is_manual = {is_manual} WHERE orderId_create = {orderId_create}"))
            conn.commit()
        except: pass
    return


def get_webhook_signature(message: str, from_id=TG_BOT_OWNER_ID):
    token = hash_md5(message)
    data = {'token': token, 'is_used': 0, 'created_day': datetime.now().strftime("%Y-%m-%d"), 'created_time': datetime.now().strftime("%H:%M:%S"), 'message': message}
    data_to_table(data, 'webhook_signature')
    symbol = message.split(' ')[-1].upper()
    data_dict = get_resistant_price(symbol, interval = '4h', for_webhook = True)
    if not data_dict: return send_msg(token, from_id)
    data_dict['token'] = token
    data_dict['message'] = message
    reply_string = '\n'.join([f"{key}: {format_number(value)}" for key, value in data_dict.items()])
    webhook_json = f'''Webhook Triger Json:\n\n"condition": "ALERT", "message": "{symbol} approaching suport price {data_dict['support_price']}, suggesting market buy", "token": "{TRADINGVIEW_WEBHOOK_TOKEN}", "signature": "{token}"\n\n{reply_string}'''
    return send_msg(webhook_json, from_id)


def tradingview_fmb_webhook_command(coin, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    message = f"funding_market_buy {coin}"
    return get_webhook_signature(message, from_id)


def tradingview_fms_webhook_command(coin, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    message = f"funding_market_sell {coin}"
    return get_webhook_signature(message, from_id)


def get_webhook_signature_coin(coin, from_id=TG_BOT_OWNER_ID):
    message = f"fmb {coin}"
    token = hash_md5(message)
    data = {'token': token, 'is_used': 0, 'created_day': datetime.now().strftime("%Y-%m-%d"), 'created_time': datetime.now().strftime("%H:%M:%S"), 'message': message}
    data_to_table(data, 'webhook_signature')
    data_dict = get_resistant_price(coin, interval = '4h', for_webhook = True)
    if not data_dict: return
    support_price = data_dict['support_price']
    data_dict['token'] = token
    data_dict['message'] = message
    reply_string = '\n'.join([f"{key}: {format_number(value)}" for key, value in data_dict.items()])
    reply_msg = f'''Webhook FMB Triger Json:\n\n"condition": "ALERT", "message": "{coin} approaching support price {support_price}, suggesting market buy", "token": "{TRADINGVIEW_WEBHOOK_TOKEN}", "signature": "{token}"\n\n{reply_string}'''
    return send_msg(reply_msg, from_id)


def update_position_table(data: dict, from_id=TG_BOT_OWNER_ID, engine = engine):
    if not data or type(data) is not dict: return send_msg('No data to update.', from_id)
    usdt_close = float(data['cummulativeQuoteQty']) if 'cummulativeQuoteQty' in data else float(data['cumulativeQuoteQty']) if 'cumulativeQuoteQty' in data else 0
    if not usdt_close: return send_msg(f'No usdt_close value from data: {data}', from_id)
    profit = usdt_close - data['usdt_value'] - data['commission']
    target_profit = profit / data['usdt_value']
    target_profit = round(target_profit, 2)
    price_close = usdt_close / data['amount']
    time_close = int(datetime.now().timestamp() * 1000)
    year_close = datetime.now().year
    month_close = datetime.now().month
    day_close = datetime.now().day
    duration = time_close - data['time_create']
    with engine.connect() as conn: 
        conn.execute(text(f"UPDATE position_table SET is_closed = 1, time_close = {time_close}, price_close = {price_close}, orderId_close = {data['orderId']}, usdt_close = {usdt_close}, profit = {profit}, duration = {duration}, target_profit = {target_profit}, type_close = '{data['type']}', year_close = {year_close}, month_close = {month_close}, day_close = {day_close} WHERE orderId_create = {data['orderId_create']}"))
        conn.commit()
    reply_msg = f"{data['coin']} Position closed with profit: {format_number(profit)} usdt"
    send_msg(f"{reply_msg}\n/as_{data['coin']} | /tvb_{data['coin']} | /limit_buy_{data['coin']}", from_id)
    return profit


def update_position_table_for_limit_sell_order(coin: str, orderId: int, from_id=TG_BOT_OWNER_ID, engine = engine):
    coin = coin.upper()
    coin = coin if not coin.endswith('USDT') else coin[:-4]
    df_position = read_position_table_by_orderId_close(orderId, engine)
    if df_position.empty: return send_msg(f'No open position with limit orderId', from_id)
    row = df_position.iloc[0]
    data = check_order_status_by_orderId(coin, orderId)
    if not data: return send_msg(f'No data for coin: {coin}, orderId: {orderId}', from_id)
    if data['status'] == 'FILLED':
        data['coin'] = coin
        data['orderId_create'] = int(row['orderId_create'])
        data['time_create'] = int(row['time_create'])
        data['commission'] = float(row['commission'])
        data['usdt_value'] = float(row['usdt_value'])
        data['price_create'] = float(row['price_create'])
        data['amount'] = float(row['amount'])
        return update_position_table(data, from_id, engine)


def update_all_position_table_for_limit_sell_order(from_id=TG_BOT_OWNER_ID):
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    df_position = read_position_table_account(0, None, 'spot', engine)
    if df_position.empty: return
    for index, row in df_position.iterrows():
        coin = row['coin']
        orderId = int(row['orderId_close'])
        data = check_order_status_by_orderId(coin, orderId)
        if not data: continue
        if data['status'] == 'FILLED':
            data['coin'] = coin
            data['orderId_create'] = int(row['orderId_create'])
            data['time_create'] = int(row['time_create'])
            data['commission'] = float(row['commission'])
            data['usdt_value'] = float(row['usdt_value'])
            data['price_create'] = float(row['price_create'])
            data['amount'] = float(row['amount'])
            try: update_position_table(data, from_id, engine)
            except: pass
    

def check_all_limit_buy_order_filled(from_id = TG_BOT_OWNER_ID, engine = engine):
    # Check current spot balance coin in binance spot account
    df = get_user_asset()
    df_position = read_position_table_account(0, None, 'spot', engine)
    # Check coins in df asset but not in df_position['coin']
    coins = df['asset'].values
    coins = [coin for coin in coins if coin not in df_position['coin'].values]
    # Remove 'USDT', 'BNB' from coins
    coins = [coin for coin in coins if coin not in ['USDT', 'BNB']]
    if not coins: return
    holding_list = read_holding_list()
    for coin in coins:
        # Get the latest trade history for the coin from binance
        df_orderId = get_last_filled_orders(coin, side = 'BUY', time_offset = 48)
        # get orderId from data
        for orderId_create in df_orderId.index:
            orderId_create = int(orderId_create)
            df_spot_coins_history = read_position_table_by_orderId_create(orderId_create, engine)
            if not df_spot_coins_history.empty: continue
            data = check_order_status_by_orderId(coin, orderId_create)
            if not data: continue
            instert_position_table(data, 'spot', engine)
            price = float(data['cummulativeQuoteQty']) / float(data['executedQty'])
            send_msg(f"Limit order bought {coin} at {format_number(price)} usdt/{coin.lower()}\n{generate_bottom_msg(coin)}", from_id)
            try:
                if coin in holding_list: switch_position_from_main_to_funding(coin, from_id) 
                else: set_limit_sell_to_resistant_price(coin, from_id, engine)
            except: pass


def update_limit_buy_orders(from_id = TG_BOT_OWNER_ID):
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    return check_all_limit_buy_order_filled(from_id, engine)


# Create a function to check position_table, find out the duplicated orderId_create, and delete the one with bigger time_create
def check_position_table_for_duplicated_orderId_create(from_id = TG_BOT_OWNER_ID):
    with engine.connect() as conn: 
        try: df = pd.DataFrame(conn.execute(text(f"SELECT orderId_create, count(orderId_create) as count, max(time_create) as max_time_create FROM position_table GROUP BY orderId_create HAVING count > 1")).fetchall())
        except: df = pd.DataFrame()
    if df.empty: return send_msg('No duplicated orderId_create', from_id)
    for index, row in df.iterrows():
        orderId_create = int(row['orderId_create'])
        max_time_create = int(row['max_time_create'])
        try: 
            with engine.connect() as conn:
                conn.execute(text(f"DELETE FROM position_table WHERE orderId_create = {orderId_create} AND time_create = {max_time_create}"))
                conn.commit()
        except: pass
    return send_msg('Duplicated orderId_create deleted', from_id)


def update_position_table_with_orderId(coin, orderId_create, orderId_close, from_id=TG_BOT_OWNER_ID, row = pd.DataFrame(), data = {}, engine = engine):
    if row.empty: 
        if not orderId_create: return send_msg(f'row or orderId_create has to be provided at least one.', from_id)
        orderId_create = int(orderId_create)
        df = read_position_table_by_orderId_create(orderId_create, engine)
        if df.empty: return send_msg(f'No open position with orderId_create: {orderId_create}', from_id)
        row = df.iloc[0]
    if not data: 
        data = check_order_status_by_orderId(coin, orderId_close)
        if not data: return send_msg(f'No data for {coin}, orderId_close: {orderId_close}', from_id)
    if data.get('status', 'None') == 'FILLED':
        data['coin'] = coin
        data['orderId_create'] = int(row['orderId_create'])
        data['time_create'] = int(row['time_create'])
        data['commission'] = float(row['commission'])
        data['usdt_value'] = float(row['usdt_value'])
        data['price_create'] = float(row['price_create'])
        data['amount'] = float(row['amount'])
        return update_position_table(data, from_id, engine)


def do_market_sell_by_orderId_create(orderId_create = None, from_id = TG_BOT_OWNER_ID, coin_df = pd.DataFrame(), coin = None, engine = engine):
    if coin_df.empty: 
        if not orderId_create: return send_msg(f'coin_df or orderId_create has to be provided at least one.', from_id)
        orderId_create = int(orderId_create)
        coin_df = read_position_table_by_orderId_create(orderId_create, engine)
        if coin_df.empty: return send_msg(f'No open position with orderId_create: {orderId_create}', from_id)
        coin = coin_df['coin'].values[0]
    coin = coin.upper() if coin else coin_df['coin'].values[0]
    row = coin_df.iloc[0]
    amount = float(row['amount'])
    account = row['account']
    orderId_close = int(row['orderId_close'])
    if orderId_close:  binance_cancel_order_by_orderId(coin, orderId_close)
    if account == 'funding': funding_main_transfer_with_check_and_send(coin, amount, from_id)
    data = binance_market_sell(coin, amount)
    if not data: return send_msg(f'Failed to do market sell for {coin}', from_id)
    profit = update_position_table_with_orderId(coin, int(row['orderId_create']), int(data.get('orderId', 0)), from_id, row, data, engine)
    if account == 'funding': main_funding_transfer_with_check_and_send('USDT', float(data['cummulativeQuoteQty']), from_id)
    return profit
    

def do_market_sell(coin: str, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    coin = coin if not coin.endswith('USDT') else coin[:-4]
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    df_position = read_position_table_account(0, coin, 'spot', engine)
    if df_position.empty: return send_msg(f'No open position for coin: {coin}', from_id)
    df_position = df_position.sort_values(by=['price_create'], ascending=True)
    coin_df = df_position.head(1)
    orderId_create = int(coin_df['orderId_create'].values[0])
    return do_market_sell_by_orderId_create(orderId_create, from_id, coin_df, coin, engine)


def get_latest_sold_coin():
    try:
        with engine.connect() as connection: df_latest_sold_coin = pd.DataFrame(connection.execute(text("SELECT * FROM position_table ORDER BY time_close DESC LIMIT 1")).fetchall())
        if df_latest_sold_coin.empty: return
    except: return
    coin = df_latest_sold_coin['coin'].values[0]
    profit = df_latest_sold_coin['profit'].values[0]
    reply_msg = f"Latest sold {coin} with profit: {format_number(profit)} usdt"
    return reply_msg


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


def instert_position_table(data, account = 'spot', engine = engine):
    if data.get('status', 'None') != 'FILLED': return
    position_table = {
        'coin': data['symbol'].replace('USDT', ''),
        'symbol': data['symbol'],
        'account': account.lower(),
        'price_create': float(data['cummulativeQuoteQty']) / float(data['executedQty']),
        'amount': float(data['executedQty']),
        'usdt_value': float(data['cummulativeQuoteQty']),
        'orderId_create': int(data['orderId']),
        'time_create': datetime.now().timestamp() * 1000,
        'type_create': data['type'],
        'is_closed': 0,
        'is_manual': 0,
        'target_profit': 0,
        'price_close': 0,
        'orderId_close': 0,
        'time_close': 0,
        'type_close': '',
        'usdt_close': 0,
        'profit': 0,
        'duration': 0,
        'year_create': datetime.now().year,
        'month_create': datetime.now().month,
        'day_create': datetime.now().day,
        'year_close': 0,
        'month_close': 0,
        'day_close': 0,
        'commission': float(data['cummulativeQuoteQty']) * 0.0015,
        'exchange': 'binance',
    }
    return data_to_table(position_table, 'position_table', 'append', engine)


def do_market_buy(coin: str, value, engine = engine):
    print(f"Calling do_market_buy for {coin} with checksize: {value} usdt")
    coin = coin.upper()
    counts = check_positions_counts()
    if counts >= POSITIONS_LIMIT: return f'Current spot positions + limit buy orders counts ({counts}) is full.'
    data = binance_market_buy(coin, value)
    if not data: return f'Failed to do market buy for coin: {coin}'
    instert_position_table(data, 'spot', engine)
    price = float(data['cummulativeQuoteQty']) / float(data['executedQty'])
    return f'''Market bought {coin} at {format_number(price)} usdt/{coin.lower()}\n/as_{coin} | /close_{data['orderId']}'''


def bot_market_buy_one_unit(coin: str, from_id=TG_BOT_OWNER_ID, engine = engine):
    coin = coin.upper()
    reply_msg = do_market_buy(coin, CHECK_SIZE, engine)
    if reply_msg: send_msg(reply_msg, from_id)
    return reply_msg


def set_limit_sell_to_resistant_price(coin, from_id=TG_BOT_OWNER_ID, engine = engine):
    coin = coin.upper()
    resistant_price_dict = get_resistant_price(coin)
    if not resistant_price_dict: resistant_price_dict = {'target_profit': 0.1}
    return binance_position_set_limit_sell(round(resistant_price_dict.get('target_profit', 0.01), 2), from_id, coin, 0, engine)


def reset_target_profit_for_resistance(from_id = TG_BOT_OWNER_ID):
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    df_balance = read_position_table_account(0, None, 'spot', engine)
    if df_balance.empty: return print('No position found')
    try: df = get_token_price_table()
    except: df = pd.DataFrame()
    if df.empty: return print('Failed to fetch price info')
    df = df.drop(columns=['coin'])
    df_balance = pd.merge(df_balance, df, on='symbol', how='left')
    df_balance['profit'] = (df_balance['lastPrice'] - df_balance['price_create']) * df_balance['amount'] - df_balance['commission']
    df_balance = df_balance[df_balance['profit'] < 100]
    if df_balance.empty: return print('No position with profit < 100 found')
    for i in range(df_balance.shape[0]): 
        coin = df_balance.iloc[i]['coin']
        resistance_dict = get_resistant_price(coin)
        if not resistance_dict: continue
        resistant_price = resistance_dict.get('resistant_price', 0)
        ideal_target_profit = resistant_price / df_balance.iloc[i]['price_create'] - 1
        ideal_target_profit = round(ideal_target_profit, 2)
        target_profit = max(ideal_target_profit, 0.01)
        current_target_profit = df_balance.iloc[i]['target_profit']
        if current_target_profit == target_profit or df_balance.iloc[i]['is_manual']: continue
        binance_position_set_limit_sell(target_profit, from_id, df_balance.iloc[i]['coin'], 1, engine)
    return True


def manually_market_buy_one_unit(coin: str, from_id=TG_BOT_OWNER_ID, engine = engine):
    coin = coin.upper()
    reply_msg = do_market_buy(coin, CHECK_SIZE, engine)
    if reply_msg: send_msg(reply_msg, from_id)
    set_limit_sell_to_resistant_price(coin, from_id, engine)
    return reply_msg


def click_to_create(coin, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    if coin == 'BTC': return send_msg(f'Yes, now you know how to create a position by coin, just replace the BTC with a valid coin', from_id)
    return manually_market_buy_one_unit(coin, from_id)


def plot_net_profit_sum(chat_id=TG_BOT_OWNER_ID, engine = engine):
    filename = f"net_profit_daily_record/{datetime.now().strftime('%Y-%m-%d')}.png"
    # check if the file exists, if yes, return the file name
    if os.path.isfile(filename): return send_img(chat_id, filename)

    # print current time string format and the function is running
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} plot_net_profit_sum() is running ...')

    try:
        # Read data from the table into a DataFrame
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text("SELECT Date, NetProfit FROM net_profit_daily_record")).fetchall())
        # print(df)

        # if the df is empty, return a default image
        if df.empty: return f"net_profit_daily_record/Leowang.net.jpg"

        df.columns = ['Date', 'NetProfit']

        # Calculate percentage
        df['Percentage'] = (df['NetProfit'] / INITIAL_FUND) * 100

        # Convert 'Date' to datetime
        df['Date'] = pd.to_datetime(df['Date'])

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


def update_kline_data_from_binance_to_table(symbol: str, interval: str):
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    try: 
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(f"SELECT * FROM {symbol}_{interval}_kline_data ORDER BY `Close Time` DESC LIMIT 1")).fetchall())
    except: df = pd.DataFrame()
    if not df.empty: 
        last_close_time = df.iloc[-1]['Close Time']
        last_close_time = int(last_close_time.timestamp() * 1000)
        last_open_time_str = df.iloc[-1]['Open Time']
        last_open_time = int(last_open_time_str.timestamp() * 1000)
        current_utc_time = int(time.time() * 1000)
        if last_close_time >= current_utc_time: 
            # Only need to update the last 1 row
            url = f"https://api.binance.com/api/v3/klines"
            params = {
                'symbol': symbol,
                'interval': interval,
                'startTime': last_open_time,
            }
            response = requests.get(url, params=params)
            data = response.json()
            if not data: 
                with engine.connect() as connection: reply_df = pd.DataFrame(connection.execute(text(f"SELECT * FROM {symbol}_{interval}_kline_data ORDER BY `Close Time` DESC LIMIT 500")).fetchall())
                return reply_df
            df = pd.DataFrame(data, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])
            df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
            df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
            df['High'] = pd.to_numeric(df['High'], errors='coerce')
            df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
            df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
            df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
            df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')
            df['Quote Asset Volume'] = pd.to_numeric(df['Quote Asset Volume'], errors='coerce')
            df = df.drop(columns=['Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])
            # Before append the last row, delete the last row in the table with the same open time
            with engine.connect() as con:
                con.execute(text(f"DELETE FROM {symbol}_{interval}_kline_data WHERE `Open Time` = '{last_open_time_str}'"))
                con.commit()
            execution_if_exists = 'append'
            with engine.connect() as connection: df.to_sql(f"{symbol}_{interval}_kline_data", connection, if_exists=execution_if_exists, index=False)
            with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(f"SELECT * FROM {symbol}_{interval}_kline_data ORDER BY `Close Time` DESC LIMIT 500")).fetchall())
            return df
        else: open_time = last_close_time + 1
    else:
        if interval == '4h': open_time = int(time.time() * 1000) - 500 * 4 * 60 * 60 * 1000
        elif interval == '1h': open_time = int(time.time() * 1000) - 500 * 60 * 60 * 1000
        elif interval == '5m': open_time = int(time.time() * 1000) - 500 * 5 * 60 * 1000
        elif interval == '1d': open_time = int(time.time() * 1000) - 500 * 24 * 60 * 60 * 1000
        elif interval == '1w': open_time = int(time.time() * 1000) - 500 * 7 * 24 * 60 * 60 * 1000
        elif interval == '1M': open_time = int(time.time() * 1000) - 500 * 30 * 24 * 60 * 60 * 1000
        elif interval == '15m': open_time = int(time.time() * 1000) - 500 * 365 * 24 * 60 * 60 * 1000
        else: return print(f"Interval {interval} is not supported.")
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': open_time
    }
    response = requests.get(url, params=params)
    data = response.json()
    if not data: return pd.DataFrame()
    df = pd.DataFrame(data, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
    df['High'] = pd.to_numeric(df['High'], errors='coerce')
    df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')
    df['Quote Asset Volume'] = pd.to_numeric(df['Quote Asset Volume'], errors='coerce')
    df = df.drop(columns=['Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])
    execution_if_exists = 'replace'
    with engine.connect() as connection: df.to_sql(f"{symbol}_{interval}_kline_data", connection, if_exists=execution_if_exists, index=False)
    with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(f"SELECT * FROM {symbol}_{interval}_kline_data ORDER BY 'Close Time' DESC LIMIT 500")).fetchall())
    return df


def get_kline_data_from_binance(symbol: str, interval: str):
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': interval
    }
    response = requests.get(url, params=params)
    data = response.json()
    if not data: return pd.DataFrame()
    df = pd.DataFrame(data, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
    df['High'] = pd.to_numeric(df['High'], errors='coerce')
    df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')
    df['Quote Asset Volume'] = pd.to_numeric(df['Quote Asset Volume'], errors='coerce')
    df = df.drop(columns=['Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])
    return df


def get_kline_data(symbol, interval):
    symbol = symbol.upper()
    symbol = symbol + 'USDT' if not symbol.endswith('USDT') else symbol
    try: df = get_kline_data_from_binance(symbol, interval)
    except: df = pd.DataFrame()
    # if not df.empty: df = df.sort_values(by='Close Time', ascending=True)
    return df


def calculate_sma(data, period):
    return data.rolling(window=period).mean()

def calculate_rsi(data, period=13):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data, short_window=12, long_window=26, signal=9):
    short_ema = data.ewm(span=short_window, adjust=False).mean()
    long_ema = data.ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line


def analyze_rsi(coin, interval = '1d'):
    df = get_kline_data(coin, interval)
    if df.empty: return 50
    df['RSI'] = calculate_rsi(df['Close'], 13)
    last_rsi = df['RSI'].iloc[-1]
    return float(last_rsi)


def calculate_odds(df, period=13):
    df['up_percentage_change'] = ((df['Close'] - df['Open']) / df['Open']) * 100
    df['up_change_by_volume'] = df['up_percentage_change'] / df['Quote Asset Volume']
    positive_changes = df[df['up_percentage_change'] > 0]
    negative_changes = df[df['up_percentage_change'] < 0]
    df['avg_up_change_by_volume_positive'] = positive_changes['up_change_by_volume'].rolling(window=period).mean()
    df['avg_up_change_by_volume_negative'] = negative_changes['up_change_by_volume'].rolling(window=period).mean()
    df['conditions_boolean'] = 0
    df.loc[df['up_change_by_volume'] > df['avg_up_change_by_volume_positive'], 'conditions_boolean'] = 1
    df.loc[df['up_change_by_volume'] < df['avg_up_change_by_volume_negative'], 'conditions_boolean'] = -1
    df.loc[:, 'Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    last_condition = df['conditions_boolean'].iloc[-1]
    previous_condition = df['conditions_boolean'].iloc[-2]
    general_condition = max(last_condition, previous_condition) if last_condition >= 0 else last_condition
    return general_condition


def analyze_data(df, interval):
    general_condition = calculate_odds(df, period=13)
    df['RSI'] = calculate_rsi(df['Close'], 13)
    df['RSI_SMA'] = calculate_sma(df['RSI'], 13)
    df['Quote Asset Volume SMA'] = calculate_sma(df['Quote Asset Volume'], 34)
    df['SMA_13'] = calculate_sma(df['Close'], 13)
    df['SMA_21'] = calculate_sma(df['Close'], 21)
    df['SMA_34'] = calculate_sma(df['Close'], 34)
    df['SMA_55'] = calculate_sma(df['Close'], 55)
    df['SMA_89'] = calculate_sma(df['Close'], 89)
    current_price = df['Close'].iloc[-1]
    condition_1d = df['SMA_55'].iloc[-1] > df['SMA_89'].iloc[-1]
    condition_4h = df['SMA_34'].iloc[-1] > df['SMA_55'].iloc[-1]
    condition_1h = df['SMA_21'].iloc[-1] > df['SMA_34'].iloc[-1]
    condition_15m = df['SMA_13'].iloc[-1] > df['SMA_21'].iloc[-1]
    condition_5m = current_price > df['SMA_13'].iloc[-1]
    current_condition = condition_5m if interval == '5m' else condition_15m if interval == '15m' else condition_1h if interval == '1h' else condition_4h if interval == '4h' else condition_1d if interval == '1d' else False
    if general_condition == 1 and current_condition and df['RSI'].iloc[-1] > df['RSI'].iloc[-2] and df['RSI'].iloc[-1] < 89 and df['RSI'].iloc[-1] > df['RSI_SMA'].iloc[-1]: return {'interval': interval, 'long': True, 'short': False}
    else: return {'interval': interval, 'long': False, 'short': False}

    
def analyze_symbol(symbol: str, interval_list = ['5m', '15m', '1h', '4h']):
    symbol = symbol.upper() + 'USDT' if not symbol.endswith('USDT') else symbol.upper()
    good_to_buy, target_profit = 0, 0
    interval_list_length = len(interval_list)
    for interval in interval_list:
        time.sleep(0.5)
        df = get_kline_data(symbol, interval)
        if not df.empty: 
            result = analyze_data(df, interval)
            if not result: continue
            if not result['long']: break
            good_to_buy += 1
            if good_to_buy >= interval_list_length: 
                current_price = float(df['Close'].iloc[-1])
                if current_price > 0:
                    nearest_resistance_level, nearest_support_level = get_resistance_support_levels(df, current_price)
                    target_profit = (nearest_resistance_level - current_price) / current_price
                    if target_profit > 0.03: 
                        deviation_percentage = (current_price - nearest_support_level) / nearest_support_level
                        if deviation_percentage < 0.05: return {'long': True, 'short': False, 'target_profit': target_profit}
    return {'long': False, 'short': False, 'target_profit': 0.01}


def calculate_vwap(df):
    # Calculate the volume-weighted average price for each unique price level
    vwap = (df['High'] * df['Volume']).groupby(df['High']).sum() / df['Volume'].groupby(df['High']).sum()
    return vwap

def calculate_resistance_support(df, gap=0.2):
    # Calculate the volume-weighted average price
    vwap = calculate_vwap(df)
    # Sort the vwap series
    vwap_sorted = vwap.sort_values()
    # Initialize the list of resistance/support levels with the first price
    levels = [vwap_sorted.iloc[0]]
    # Iterate over the sorted prices
    for price in vwap_sorted:
        # If the current price is more than (1 + gap) times the last level, add it to the list
        if price > levels[-1] * (1 + gap):
            levels.append(price)
    return levels
'''[0.1412, 0.1695, 0.2048, 0.24600000000000002, 0.2953, 0.35690000000000005, 0.4353]'''


# Define a function to get resistance_support_levels and compare with current price, findout the nearest resistance and support level
def get_resistance_support_levels(df, current_price):
    try: resistance_support_levels = calculate_resistance_support(df)
    except: resistance_support_levels = []
    if not resistance_support_levels: resistance_support_levels = [current_price]
    # From resistance_support_levels list pick up all of the prices that are higher than current_price
    resistance_levels = [price for price in resistance_support_levels if price >= current_price]
    # From resistance_support_levels list pick up all of the prices that are lower than current_price
    support_levels = [price for price in resistance_support_levels if price <= current_price]
    # Find out the nearest resistance level
    nearest_resistance_level = min(resistance_levels) if resistance_levels else current_price
    # Find out the nearest support level
    nearest_support_level = max(support_levels) if support_levels else current_price
    return float(nearest_resistance_level), float(nearest_support_level)


def analyze_symbol_prudently(symbol: str):
    symbol = symbol.upper() + 'USDT' if not symbol.endswith('USDT') else symbol.upper()
    good_to_buy, good_to_short, target_profit = 0, 0, 0
    for interval in ['5m', '15m', '1h', '4h']:
        if interval in ['4h']: print(f"Symbol: {symbol}, Interval: {interval}")
        time.sleep(0.5)
        df = get_kline_data(symbol, interval)
        if not df.empty: 
            result = analyze_data(df, interval)
            if not result: continue
            if result['short']: good_to_short += 1
            elif result['long']: good_to_buy += 1
            if good_to_buy >= 3: 
                current_price = float(df['Close'].iloc[-1])
                if current_price > 0:
                    nearest_resistance_level, nearest_support_level = get_resistance_support_levels(df, current_price)
                    target_profit = (nearest_resistance_level - current_price) / current_price
                    if target_profit > 0.03: 
                        deviation_percentage = (current_price - nearest_support_level) / nearest_support_level
                        if deviation_percentage < 0.05: return {'long': True, 'short': False, 'target_profit': target_profit}
            if good_to_short >= 3: return {'long': False, 'short': True, 'target_profit': target_profit}
    return {'long': False, 'short': False, 'target_profit': 0.01}


def get_resistant_price(symbol: str, interval = '4h', for_webhook=False):
    symbol = symbol.upper() + 'USDT' if not symbol.endswith('USDT') else symbol.upper()
    df = get_kline_data(symbol, interval)
    if not df.empty: 
        current_price = float(df['Close'].iloc[-1])
        if current_price > 0:
            nearest_resistance_level, nearest_support_level = get_resistance_support_levels(df, current_price)
            nearest_resistance_level = nearest_resistance_level * 0.99
            nearest_support_level = nearest_support_level * 1.01
            target_profit = (nearest_resistance_level - current_price) / current_price
            deviation_percentage = (current_price - nearest_support_level) / nearest_support_level
            target_profit = max(target_profit, 0.01)
            nearest_resistance_level = max(nearest_resistance_level, current_price * 1.01)
            nearest_support_level = min(nearest_support_level, current_price * 0.97)
            result = analyze_data(df, interval)
            long = 1 if result.get('long', False) else 0
            if for_webhook: return {'target_profit': f"{format_number(target_profit * 100)}%", 'resistant_price': format_number(nearest_resistance_level), 'support_price': format_number(nearest_support_level), 'deviation_percentage': f"{format_number(deviation_percentage * 100)}%", 'long': long}
            return {'target_profit': target_profit, 'resistant_price': nearest_resistance_level, 'support_price': nearest_support_level, 'deviation_percentage': deviation_percentage, 'long': long}
    return {}


def weekly_rsi_over_high(symbol):
    symbol = symbol.upper() + 'USDT' if not symbol.endswith('USDT') else symbol.upper()
    interval = '1w'
    df = get_filtered_df('weekly_rsi_over_high', ['is_over_high'], {'date_of_today': datetime.now().strftime("%Y-%m-%d"), 'symbol': symbol})
    if not df.empty: return df['is_over_high'].values[0]
    df = get_kline_data(symbol, interval)
    if df.empty: return 0
    df['RSI'] = calculate_rsi(df['Close'], 13)
    latest = df.iloc[-1]
    weekly_rsi_over_high_coin = {
        'coin': symbol[:-4],
        'symbol': symbol,
        'RSI': latest['RSI'],
        'interval': interval,
        'is_over_high': 0,
        'date_of_today': datetime.now().strftime('%Y-%m-%d')
    }
    weekly_rsi_over_high_coin['is_over_high'] = 1 if latest['RSI'] > 89 else 0
    if data_to_table(weekly_rsi_over_high_coin, 'weekly_rsi_over_high'): return weekly_rsi_over_high_coin['is_over_high']
    

def binance_spot_position_check(coin=None, chat_id=None, crontab_profit_record=False):
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    df_balance = read_position_table_account(0, coin, 'spot', engine)
    df = get_token_price_table()
    if df.empty: return 'Failed to fetch price info'
    df = df.drop(columns=['coin'])
    df_balance = pd.merge(df_balance, df, on='symbol', how='left')
    df_balance['profit'] = (df_balance['lastPrice'] - df_balance['price_create']) * df_balance['amount']
    df_balance['up_ratio'] = df_balance['lastPrice']/ df_balance['price_create'] - 1
    df_balance = df_balance.sort_values(by='profit', ascending=False)
    book_value = 0
    for_reply = {}
    for i in range(df_balance.shape[0]):
        # ignore coin BNB, ONG
        if df_balance.iloc[i]['coin'] in ['BNB', 'ONG', 'USDT', 'USDC']: continue
        reply_dict = df_balance.iloc[i].to_dict()
        coin = reply_dict['coin']
        for_reply['Coin'] = reply_dict['coin']
        for_reply['Amount'] = format_number(reply_dict['amount'])
        for_reply['Profit'] = format_number(reply_dict['profit'])
        for_reply['Up_Ratio'] = f"{round(float(reply_dict['up_ratio'])*100, 2)}%"
        for_reply['Buy_Price'] = f"{reply_dict['price_create']:.2f}"
        for_reply['Current_Price'] = f"{reply_dict['lastPrice']:.2f}"
        for_reply['Position_Since'] = datetime.fromtimestamp(reply_dict['time_create'] / 1000).strftime('%Y-%m-%d %H:%M')
        for_reply['Order_ID'] = reply_dict['orderId_create']
        reply_msg = '\n'.join([f"{k}: {v}" for k, v in for_reply.items()])
        if chat_id: send_msg(f"{i+1}/{df_balance.shape[0]}\n{reply_msg}", chat_id)
        book_value += reply_dict['profit']
    try: check_profit_and_record(chat_id, crontab_profit_record, book_value, df_balance.shape[0], engine)
    except: pass
    return


def check_profit_and_record(chat_id=None, crontab_profit_record=False, book_value=0, current_positions=0, engine=engine):
    if chat_id or crontab_profit_record: 
        df_profit = read_position_table_account(1, None, 'spot', engine)
        if not df_profit.empty: 
            with engine.connect() as conn: df_earliest_transactTime = pd.DataFrame(conn.execute(text('SELECT time_create FROM position_table ORDER BY time_create ASC LIMIT 1')).fetchall())
            earliest_transactTime = int(df_earliest_transactTime['time_create'].values[0])
            duration = (int(time.time() * 1000) - earliest_transactTime) / 1000 / 60 / 60
            duration_day = f'{int(duration / 24)} Days {int(duration % 24)} Hours' if duration > 24 else f'{int(duration)} Hours'
            profit_sum = df_profit['profit'].astype(float).sum()
            net_profit_sum = profit_sum + book_value
            annualized_return = net_profit_sum / (duration / 24 / 365) / INITIAL_FUND
            annualized_return = f"{annualized_return * 100:.2f}%"
            chat_id = chat_id if chat_id else TG_BOT_OWNER_ID
            investment_return = net_profit_sum / INITIAL_FUND
            investment_return = f"{investment_return * 100:.2f}%"
            summary_msg = f"BOT RUNNING: {duration_day}\n\nInitial Fund: {format_number(INITIAL_FUND)} usdt\nUnrealized_Gain: {format_number(book_value)} usdt\nRealized_Gain: {format_number(profit_sum)} usdt\nNet_Profit: {format_number(net_profit_sum)} usdt\nCurrent_Positions: {current_positions}/{POSITIONS_LIMIT}\n\nInvestment_Return: {investment_return}\nAnnualized_Return: {annualized_return}"
            send_msg(summary_msg, chat_id)
            if crontab_profit_record:
                with engine.connect() as connection:
                    try:
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

                year_and_month_day = datetime.now().strftime('%Y-%m-%d')
                send_email(f'TRADING BOT OPERATION SUMMARY {year_and_month_day}', summary_msg, GMAIL_ADDRESS_MAIN)
                send_email(f'TRADING BOT OPERATION SUMMARY {year_and_month_day}', summary_msg, os.getenv('GMAIL_DANLI'))
                plot_net_profit_sum(chat_id, engine)
                send_msg_markdown('''[Online Dashboard](https://wh.leowang.net/dashboard)''', chat_id)
    return 

def today_profit_sum():
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    try:
        with engine.connect() as connection: df_profit = pd.DataFrame(connection.execute(text(f'SELECT coin, profit FROM position_table WHERE is_closed = 1 AND day_close = {datetime.now().day} AND month_close = {datetime.now().month} AND year_close = {datetime.now().year}')).fetchall())
    except: df_profit = pd.DataFrame()
    return df_profit


def monthly_profit_sum():
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    try:
        with engine.connect() as connection: df_profit = pd.DataFrame(connection.execute(text(f"SELECT profit FROM position_table WHERE is_closed = 1 AND month_close = {datetime.now().month} AND year_close = {datetime.now().year}")).fetchall())
    except: df_profit = pd.DataFrame()
    return df_profit


# Define a function to set positon limit to 5 if the monthly profit is over 30000
def reset_position_limit(monthly_profit_target = 30_000, upper_limit = 10, lower_limit = 5, from_id = TG_BOT_OWNER_ID):
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(f"SELECT SUM(profit) FROM position_table WHERE is_closed = 1 AND account = 'spot' AND month_close = {datetime.now().month} AND year_close = {datetime.now().year}")).fetchall())
    df = df.fillna(0)
    monthly_profit = df.iloc[0].astype(float).values[0]
    current_position_limit = get_position_limit()
    if monthly_profit_target > monthly_profit and current_position_limit != upper_limit: 
        if set_position_limit_default(upper_limit): send_msg(f"Monthly gained profit {format_number(monthly_profit)} is lower than {format_number(monthly_profit_target)}, POSITION_LIMIT has been set to {upper_limit}", from_id)
    elif monthly_profit_target < monthly_profit and current_position_limit != lower_limit: 
        if set_position_limit_default(lower_limit): send_msg(f"Monthly gained profit {format_number(monthly_profit)} is higher than {format_number(monthly_profit_target)}, POSITION_LIMIT has been set to {lower_limit}", from_id)
    return


def check_today_profit_sum():
    reply_dict = {
        'profit_sum': 0,
        'profit_coinlist': []
    }
    df_profit = today_profit_sum()
    if df_profit.empty: return reply_dict
    df_profit = df_profit.groupby('coin').sum().reset_index()
    # sort by profit
    df_profit = df_profit.sort_values(by='profit', ascending=False)
    profit_coinlist = []
    for index, row in df_profit.iterrows(): profit_coinlist.append(f"/as_{row['coin']}: {format_number(row['profit'])}")
    profit_sum = df_profit['profit'].sum()
    reply_dict = {
        'profit_sum': profit_sum,
        'profit_coinlist': profit_coinlist
    }
    return reply_dict


def profit_taken_today(chat_id=TG_BOT_OWNER_ID, report = False):
    try:
        reply_dict = check_today_profit_sum()
        profit_take = reply_dict['profit_sum']
        if profit_take <= 0: return send_msg('No profit has been taken today', chat_id)
        profit_coinlist = reply_dict['profit_coinlist']
        profit_coinlist_string = '\n'.join(profit_coinlist)
        reply_title = f"Profit Take {datetime.now().strftime('%Y-%m-%d')}: {format_number(profit_take)} usdt"
        reply_msg = f"{reply_title}\n\n{profit_coinlist_string}"
        send_msg(reply_msg, chat_id)
        if not report: return
        send_email(reply_title, profit_coinlist_string, GMAIL_ADDRESS_MAIN)
        send_email(reply_title, profit_coinlist_string, os.getenv('GMAIL_DANLI'))
    except Exception as e: return send_email(f"ERRO: profit_taken_today()", e, GMAIL_ADDRESS_MAIN)


def reset_target_profit_for_coins(limit_hour = 72, target_profit = 0.01, from_id = TG_BOT_OWNER_ID):
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    df_balance = read_position_table_account(0, None, 'spot', engine)
    if df_balance.empty: return print('No position found')
    try: df = get_token_price_table()
    except: df = pd.DataFrame()
    if df.empty: return print('Failed to fetch price info')
    df = df.drop(columns=['coin'])
    df_balance = pd.merge(df_balance, df, on='symbol', how='left')
    df_balance['profit'] = (df_balance['lastPrice'] - df_balance['price_create']) * df_balance['amount'] - df_balance['commission']
    df_balance = df_balance[df_balance['profit'] < 100]
    if df_balance.empty: return print('No position with profit < 100 found')
    df_balance['duration'] = (int(time.time() * 1000) - df_balance['time_create']) / 1000 / 60 / 60
    df_duration = df_balance[df_balance['duration'] >= limit_hour].copy()
    for i in range(df_duration.shape[0]): 
        current_target_profit = df_duration.iloc[i]['target_profit']
        if current_target_profit == target_profit or df_duration.iloc[i]['is_manual']: continue
        binance_position_set_limit_sell(target_profit, from_id, df_duration.iloc[i]['coin'], 1, engine)
    return True


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

    price = is_scientific_notation(price)

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


def is_scientific_notation(number):
    # Convert the number to a string
    number_str = str(number)
    # Check if 'e' or 'E' is in the string
    if 'e' in number_str or 'E' in number_str:
        formatted_number = "{:.20f}".format(number).rstrip('0').rstrip('.')
        return formatted_number
    else: return number


def update_position_table_amount(amount: float, orderId_create: int, engine=engine):
    with engine.connect() as connection:
        try:
            # Execute the query with the updated update_id
            connection.execute(text(f"UPDATE position_table SET amount = :amount WHERE orderId_create = :orderId_create"), {'amount': amount, 'orderId_create': orderId_create})
            connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()
    return


def cancel_orderId(coin, orderId_close, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    try: orderId_close = int(orderId_close)
    except: return send_msg(f'Input orderId_close: {orderId_close} is not an integer', from_id)
    data = binance_cancel_order_by_orderId(coin, orderId_close)
    if not data: return send_msg(f'Failed to cancel orderId_close: {orderId_close}', from_id)
    return send_msg(f"{coin} {data['type']} {data['side']} orderId {orderId_close} canceled successfully\n/limit_buy_{coin}", from_id)


def binance_position_set_limit_sell(target_profit=None, chat_id=TG_BOT_OWNER_ID, coin=None, is_manual = 0, engine=engine):
    df_balance = read_position_table_account(0, coin, 'spot', engine)
    if df_balance.empty: return
    target_profit = TARGET_PROFIT_PERCENTAGE if not target_profit else float(target_profit)
    for i in range(df_balance.shape[0]):
        coin = df_balance.iloc[i]['coin']
        amount = float(df_balance.iloc[i]['amount'])
        price_create = float(df_balance.iloc[i]['price_create'])
        orderId_create = int(df_balance.iloc[i]['orderId_create'])
        orderId_close = int(df_balance.iloc[i]['orderId_close'])
        current_target_profit = float(df_balance.iloc[i]['target_profit'])
        if_manual = int(df_balance.iloc[i]['is_manual'])
        if current_target_profit == target_profit: continue
        if orderId_close: 
            if not if_manual or is_manual: binance_cancel_order_by_orderId(coin, orderId_close)
            else: continue
            time.sleep(0.5)
        price = price_create * (1 + float(target_profit))
        try:
            polished_parameters = polish_parameters_for_limit_order(coin, amount, price, chat_id)
            price = polished_parameters['price']
        except Exception as e: print(f"An error occurred while calling polish_parameters_for_limit_order(): \nCoin: {coin}\nAmount: {amount}\nPrice: {price}\n\n{e}\n\n")
        need_to_adjust = False
        data = {}
        try: data = binance_limit_sell(coin, amount, price)
        except:
            df_coin_balance = get_user_asset()
            df_coin_balance = df_coin_balance[df_coin_balance['asset']==coin]
            if df_coin_balance.empty: 
                send_msg(f"No balance for {coin}", chat_id)
                continue
            new_amount = df_coin_balance['free'].values[0]
            amount = float(new_amount)
            need_to_adjust = True
            try: data = binance_limit_sell(coin, amount, price)
            except Exception as e: print(f"An error occurred while calling binance_limit_sell(): \nCoin: {coin}\nAmount: {amount}\nPrice: {price}\n\n{e}\n\n")
        if not data: continue
        if need_to_adjust: update_position_table_amount(amount, orderId_create, engine)
        orderId_close = int(data['orderId'])
        update_limit_orderId_in_position_table(orderId_create, orderId_close, target_profit, is_manual, engine)
        send_msg(f"Limit Sell Order Set:\nCoin: {coin}\nAmount: {format_number(amount)}\nPrice: {format_number(price)}\nTarget_profit: {target_profit*100:.2f}%\n/cancel_{coin}_{orderId_close}", chat_id)
    return


# difne a function to update net_profit_daily_record, alter NetProfit value to input value for a given date(string like 2023-12-10)
def update_net_profit_daily_record(date, net_profit, engine=engine):
    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE net_profit_daily_record SET NetProfit = :NetProfit WHERE Date = :Date"), {'Date': date, 'NetProfit': net_profit})
            connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()
    return


def bot_call_binance_position_check(from_id=TG_BOT_OWNER_ID):
    return binance_spot_position_check(coin = None, chat_id = from_id)


def bot_call_binance_position_check_coin(coin, from_id=TG_BOT_OWNER_ID):
    return binance_spot_position_check(coin = coin, chat_id = from_id)


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
    
    
# define a function to switch on the trading bot and send a message to the user
def webhook_switch_on_bot(msg = 'None', from_id=TG_BOT_OWNER_ID):
    if trading_bot_switch_on(): 
        send_msg(f"Succeed to switch on the bot! \n{msg}", from_id)
        return buy_back_most_profitable(0.03, from_id)
    return send_msg(f"Failed to switch on the bot! \n{msg}", from_id)


# define a function to switch off the trading bot and send a message to the user
def webhook_switch_off_bot(msg = 'None', from_id=TG_BOT_OWNER_ID):
    if trading_bot_switch_off(): 
        send_msg(f"Succeed to switch off the bot!\n{msg}", from_id)
        return close_postive_positions(from_id, 1, 'spot')
    return send_msg(f"Failed to switch off the bot!\n{msg}", from_id)


def calculate_missed_profit_yesterday(from_id=TG_BOT_OWNER_ID, buy_back_target_profit=0.03, is_yesterday = True):
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    try:
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text('SELECT coin, usdt_value, price_close, time_close FROM position_table WHERE is_closed = 1')).fetchall())
    except: df = pd.DataFrame()
    if df.empty: return 
    if is_yesterday: 
        timestamp_yesterday = int(time.time() * 1000) - 24 * 60 * 60 * 1000
        df = df[df['time_close'] > timestamp_yesterday]
    df = df.sort_values(by=['coin', 'time_close']).groupby('coin').last().reset_index()
    with engine.connect() as connection: df_position = pd.DataFrame(connection.execute(text('SELECT coin FROM position_table WHERE is_closed = 0 GROUP BY coin')).fetchall())
    df = df[~df['coin'].isin(df_position['coin'])]
    try:
        with engine.connect() as connection: df_white = pd.DataFrame(connection.execute(text('SELECT coin FROM token_supply_info WHERE is_white = 1')).fetchall())
    except: df_white = pd.DataFrame()
    df = df[df['coin'].isin(df_white['coin'])]
    latest_price_df = get_token_price_table()
    latest_price_df = latest_price_df.drop(columns=['symbol'])
    df = pd.merge(df, latest_price_df, how='left', on='coin')
    if df.empty: return
    df['price_diff'] = df['lastPrice'] - df['price_close']
    df['price_diff_percentage'] = df['price_diff'] / df['price_close']
    df['diff_profit'] = (df['price_diff_percentage']) * df['usdt_value']
    total_profit_missed = df['diff_profit'].sum()
    reply_msg = f"Sorry, you missed: {format_number(total_profit_missed)} usdt profit\n\n" if total_profit_missed > 0 else f"Great, you locked: {format_number(abs(total_profit_missed))} usdt profit.\n\n"
    if from_id: send_msg(reply_msg, from_id)
    df = df.sort_values(by='diff_profit').reset_index(drop=True)
    df_locked = df.iloc[:10]
    df_locked = df_locked[df_locked['diff_profit'] < 0]
    if df_locked.empty: return {}
    reply_list_locked = []
    coins_could_buy_back = {}
    for i in range(df_locked.shape[0]):
        coin = df_locked.iloc[i]['coin']
        diff_profit = df_locked.iloc[i]['diff_profit']
        previous_price = df_locked.iloc[i]['price_close']
        current_price = df_locked.iloc[i]['lastPrice']
        target_profit = df_locked.iloc[i]['price_diff_percentage']
        target_profit = abs(target_profit) - 0.1
        if target_profit > buy_back_target_profit and len(coins_could_buy_back) < 3: coins_could_buy_back[coin] = round(abs(target_profit), 2)
        msg = f"/as_{coin} {format_number(previous_price)} >> {format_number(current_price)} | locked {format_number(abs(diff_profit))}"
        reply_list_locked.append(msg)
    if from_id: send_msg('\n'.join(reply_list_locked), from_id)
    return coins_could_buy_back


# define a function to check all of the coin sold today, if don't sell, how much profit missed or locked
def calculate_missed_profit(from_id=TG_BOT_OWNER_ID, buy_back_target_profit=0.03):
    return calculate_missed_profit_yesterday(from_id, buy_back_target_profit, is_yesterday = False)


def calculate_missed_profit_for_coin(coin, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    try:
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(f"SELECT coin, usdt_value, price_close, time_close FROM position_table WHERE is_closed = 1 AND coin = '{coin}' ORDER BY time_close DESC LIMIT 1")).fetchall())
    except: df = pd.DataFrame()
    if df.empty: return 
    current_price = get_avg_price(coin)
    if not current_price: return
    current_price = float(current_price['price'])
    usdt_value = df['usdt_value'].values[0]
    last_price_close = df['price_close'].values[0]
    price_diff = last_price_close - current_price
    price_diff_percentage = price_diff / last_price_close
    diff_profit = price_diff_percentage * usdt_value
    if diff_profit < 0: reply_msg = f"{coin} {format_number(last_price_close)} >> {format_number(current_price)} | missed {format_number(abs(diff_profit))}"
    if diff_profit > 0: reply_msg = f"/buy_{coin} {format_number(last_price_close)} >> {format_number(current_price)} | locked {format_number(abs(diff_profit))}"
    if diff_profit == 0: reply_msg = f"{coin} {format_number(current_price)} hasn't changed"
    with engine.connect() as connection: 
        df_history = pd.DataFrame(connection.execute(text(f"SELECT coin, account, profit, is_closed FROM position_table WHERE coin = '{coin}'")).fetchall())
        if not df_history.empty:
            df_current_position = df_history[df_history['is_closed'] == 0]
            if not df_current_position.empty:
                df_funding_position = df_current_position[df_current_position['account'] == 'funding']
                if not df_funding_position.empty: reply_msg += f"\n{coin} in funding position: {df_funding_position.shape[0]}"
                df_spot_position = df_current_position[df_current_position['account'] == 'spot']
                if not df_spot_position.empty: reply_msg += f"\n{coin} in spot position: {df_spot_position.shape[0]}"
            traded_times = df_history.shape[0]
            history_profit = df_history['profit'].sum()
            reply_msg += f"\nTraded {traded_times} times"
            reply_msg += f"\nGained {format_number(history_profit)} usdt"
    if from_id: send_msg(reply_msg, from_id)
    return 


def get_token_info_for_user(coin: str, from_id=TG_BOT_OWNER_ID):
    if get_token_info(coin, from_id): return calculate_missed_profit_for_coin(coin, from_id)


def calculate_hot_coin_price_change(from_id=None):
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    try: 
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text('SELECT * FROM hot_coin_history WHERE date LIKE :date'), {'date': f"{yesterday_date}%"}).fetchall())
    except: return
    if df.empty: return 'hot_coin_history table is empty'
    df_current_price = get_token_price_table()
    df = pd.merge(df, df_current_price, how='left', on='coin')
    df['price_up_percentage'] = (df['lastPrice'] - df['price']) / df['price'] * 100
    df = df[df['price_up_percentage'] > 0]
    if df.empty: return
    df = df.sort_values(by='price_up_percentage', ascending=False).reset_index(drop=True)
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
    return


def update_coin_info_to_token_cmc_info_table(token_cmc_info_dict):
    print(f"Updating coin info to token_cmc_info table for {token_cmc_info_dict['coin']}")
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    with engine.connect() as connection:
        try:
            # Execute the query with the updated update_id
            connection.execute(text("UPDATE token_cmc_info SET cmc_rank = :cmc_rank, is_fiat = :is_fiat, in_ignorelist = :in_ignorelist, in_whitelist = :in_whitelist, total_supply = :total_supply, date_added = :date_added, price_of_today = :price_of_today, volume_24h = :volume_24h, market_cap = :market_cap, fully_diluted_market_cap = :fully_diluted_market_cap, circulating_supply = :circulating_supply, circulating_ratio = :circulating_ratio, turnover_ratio = :turnover_ratio, updated_date = :updated_date, token_slug = :token_slug, token_tag = :token_tag WHERE coin = :coin"), token_cmc_info_dict)
            connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()
    return 


# From the returned dictionary, get market_cap, fully_diluted_market_cap and calculate the circulating ratio
def get_token_market_cap_and_ratio(token_symbol, turnover_ratio_eth=0.05):
    token_symbol = token_symbol.upper()
    if not turnover_ratio_eth: turnover_ratio_eth = get_turnover_ratio_from_coinmarketcap(coin='ETH')
    try:
        token_info = get_token_info_from_coinmarketcap(token_symbol)
        if token_info:
            if token_info['is_fiat']: return
            fully_diluted_market_cap = token_info['quote']['USD']['fully_diluted_market_cap']
            if fully_diluted_market_cap > FULLLY_DILUTED_MARKET_CAP_UP_LIMIT: return
            market_cap = token_info['quote']['USD']['market_cap']
            if market_cap < MARKET_CAP_DOWN_LIMIT: return
            circulating_ratio = token_info['circulating_supply'] / token_info['total_supply']
            if circulating_ratio < CIRCULATION_RATIO : return
            turnover_ratio = token_info['quote']['USD']['volume_24h'] / market_cap
            turnover_ratio = round(turnover_ratio, 2)
            if turnover_ratio < turnover_ratio_eth: return
            current_price = token_info['quote']['USD']['price']
            coin_rank = token_info['cmc_rank']
            return {'market_cap': int(market_cap), 'fully_diluted_market_cap': int(fully_diluted_market_cap), 'circulation_ratio': circulating_ratio, 'turnover_ratio': turnover_ratio, 'token_slug': token_info['slug'], 'current_price': current_price, 'coin_rank': coin_rank}
    except: return 

# with engine.connect() as connection: df = pd.DataFrame(connection.execute(text('SELECT * FROM token_supply_info')).fetchall())
# Get the total supply of a given token and append the token info to the token_info dict
def get_token_total_supply(coin):
    coin = coin.upper()
    coin = coin[:-4] if coin.endswith('USDT') else coin
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    with engine.connect() as connection: df = pd.DataFrame(connection.execute(text('SELECT * FROM token_supply_info WHERE coin = :coin'), {'coin': coin}).fetchall())
    if not df.empty: return df.to_dict(orient='records')[0]
    try: token_info = get_token_info_from_coinmarketcap(coin)
    except: return 
    if not token_info: return
    data = {
        'coin': coin,
        'symbol': token_info['symbol']+ 'USDT',
        'total_supply': token_info['total_supply'],
        'max_supply': token_info['max_supply'],
        'circulating_supply': token_info['circulating_supply'],
        'is_ignore': 0,
        'is_white': 0,
        'is_stablecoin': 1 if token_info['is_fiat'] or 'USD' in coin else 0,
        'token_tags': ', '.join(token_info['tags']) if token_info['tags'] else 'None',
        'slug': token_info['slug'],
        'token_name': token_info['name'],
        'date_added': token_info['date_added'],
        'is_active': token_info['is_active'],
        }
    data_to_table(data, 'token_supply_info')
    return data


def set_coin_ignore(coin, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    coin = coin[:-4] if coin.endswith('USDT') else coin
    if not get_token_total_supply(coin): return send_msg(f'Failed to get token total supply of {coin} from CMC', from_id)
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    with engine.connect() as connection:
        try:
            # Execute the query with the updated update_id
            connection.execute(text("UPDATE token_supply_info SET is_ignore = 1 WHERE coin = :coin"), {'coin': coin})
            connection.commit()
            if from_id: send_msg(f"Successfully added {coin} to ignore list\n/gil | /remove_ignore_{coin}", from_id)
        except Exception as e:
            if from_id: send_msg(f"Failed to add {coin} to ignore list", from_id)
            print(f"An error occurred: {e}")
            connection.rollback()
    return


def remove_coin_ignore(coin, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    coin = coin[:-4] if coin.endswith('USDT') else coin
    if not get_token_total_supply(coin): return send_msg(f'Failed to get token total supply of {coin} from CMC', from_id)
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    with engine.connect() as connection:
        try:
            # Execute the query with the updated update_id
            connection.execute(text("UPDATE token_supply_info SET is_ignore = 0 WHERE coin = :coin"), {'coin': coin})
            connection.commit()
            if from_id: send_msg(f"Successfully removed {coin} from ignore list\n/gil | /ignore_{coin}", from_id)
        except Exception as e:
            if from_id: send_msg(f"Failed to remove {coin} from ignore list", from_id)
            print(f"An error occurred: {e}")
            connection.rollback()
    return


def get_ignore_list(from_id=TG_BOT_OWNER_ID):
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    try:
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text('SELECT coin FROM token_supply_info WHERE is_ignore = 1')).fetchall())
        if not df.empty:
            ignore_coin_list = df['coin'].values.tolist()
            if from_id: send_msg(f"Current ignore list ({len(ignore_coin_list)}): \n\n{', '.join(ignore_coin_list)}", from_id)
            return ignore_coin_list
    except: df = pd.DataFrame()
    if df.empty: send_msg("Your ignore list is empty! Use below command to add any coin into ignore list.\n\n/add_ignore_coin BTC | /ignore_BTC", from_id)
    return []


def set_coin_white(coin, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    coin = coin[:-4] if coin.endswith('USDT') else coin
    if not get_token_total_supply(coin): return send_msg(f'Failed to get token total supply of {coin} from CMC', from_id)
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    with engine.connect() as connection:
        try:
            # Execute the query with the updated update_id
            connection.execute(text("UPDATE token_supply_info SET is_white = 1 WHERE coin = :coin"), {'coin': coin})
            connection.commit()
            if from_id: send_msg(f"Successfully added {coin} to white list\n/gwl | /remove_white_{coin}", from_id)
        except Exception as e:
            if from_id: send_msg(f"Failed to add {coin} to white list", from_id)
            print(f"An error occurred: {e}")
            connection.rollback()
    return


def remove_coin_white(coin, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    coin = coin[:-4] if coin.endswith('USDT') else coin
    if not get_token_total_supply(coin): return send_msg(f'Failed to get token total supply of {coin} from CMC', from_id)
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    with engine.connect() as connection:
        try:
            # Execute the query with the updated update_id
            connection.execute(text("UPDATE token_supply_info SET is_white = 0 WHERE coin = :coin"), {'coin': coin})
            connection.commit()
            if from_id: send_msg(f"Successfully removed {coin} from white list\n/gwl | /white_{coin}", from_id)
        except Exception as e:
            if from_id: send_msg(f"Failed to remove {coin} from white list", from_id)
            print(f"An error occurred: {e}")
            connection.rollback()
    return


def get_white_list(from_id=TG_BOT_OWNER_ID):
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    try:
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text('SELECT coin FROM token_supply_info WHERE is_white = 1')).fetchall())
        if not df.empty: 
            white_list = df['coin'].values.tolist()
            if from_id: send_msg(f"Current white list ({len(white_list)}): \n\n{', '.join(white_list)}", from_id)
            return white_list
    except: df = pd.DataFrame()
    if df.empty: send_msg("Your white list is empty! Use below command to add any coin into white list.\n\n/add_white_list RSR | /white_RSR", from_id)
    return []


def add_holding_coin(coin, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    r = insert_coin_into_holding_list(coin)
    if not r: return send_msg(f"Failed to add {coin} into holding list", from_id)
    if r == 2: return send_msg(f"{coin} is already in holding list", from_id)
    if r == 1: return send_msg(f"Successfully added {coin} into holding list.\n/remove_holding_{coin}", from_id)


def remove_holding_coin(coin, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    r = remove_coin_from_holding_list(coin)
    if not r: return send_msg(f"Failed to remove {coin} from holding list", from_id)
    if r == 2: return send_msg(f"{coin} is not in holding list", from_id)
    if r == 1: return send_msg(f"Successfully removed {coin} from holding list.\n/add_holding_{coin}", from_id)


def get_holding_list(from_id=TG_BOT_OWNER_ID):
    holding_list = read_holding_list()
    if not holding_list: return send_msg("Your holding list is empty! Use below command to add any coin into holding list.\n/hold_RSR", from_id)
    return send_msg(f"Current holding list ({len(holding_list)}): \n{', '.join(holding_list)}", from_id)


def update_get_token_total_supply():
    df_ticker = pd.read_json(BINANCE_TICKER_URL)
    df_ticker = df_ticker.loc[:, ['symbol', 'priceChangePercent', 'lastPrice', 'openPrice', 'highPrice', 'lowPrice', 'quoteVolume', 'openTime', 'closeTime']]
    df_ticker = df_ticker[df_ticker['symbol'].str.endswith('USDT')]
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    with engine.connect() as connection: df_token_info = pd.DataFrame(connection.execute(text('SELECT * FROM token_supply_info')).fetchall())
    # find out the coins in df_ticker but not in df_token_info
    df_ticker = df_ticker[~df_ticker['symbol'].isin(df_token_info['symbol'])]
    if df_ticker.empty: return
    print(f"Updating token supply info for {df_ticker.shape[0]} coins")
    for index, row in df_ticker.iterrows():
        coin = row['symbol'][:-4]
        print(f"Updating token supply info for {coin}")
        get_token_total_supply(coin)


def top_turnover(from_id = TG_BOT_OWNER_ID, head = 10):
    global CMC_NO_DATA
    df_ticker = pd.read_json(BINANCE_TICKER_URL)
    df_ticker = df_ticker.loc[:, ['symbol', 'priceChangePercent', 'lastPrice', 'openPrice', 'highPrice', 'lowPrice', 'quoteVolume', 'openTime', 'closeTime']]
    df_ticker = df_ticker[df_ticker['symbol'].str.endswith('USDT')]
    df_ticker = df_ticker[(df_ticker['lastPrice'] > 0.0001) & (df_ticker['lastPrice'] < 2000)]
    if df_ticker.empty: return {}
    df_ticker['coin'] = df_ticker['symbol'].str[:-4]
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    try:
        with engine.connect() as connection: df_token_info = pd.DataFrame(connection.execute(text('SELECT * FROM token_supply_info')).fetchall())
        df_ticker_missed = df_ticker[~df_ticker['coin'].isin(df_token_info['coin'])]
        for index, row in df_ticker_missed.iterrows():
            coin = row['coin']
            if coin in CMC_NO_DATA: continue
            data = get_token_total_supply(coin)
            if not data: 
                CMC_NO_DATA.append(coin)
                print(f"CMC_NO_DATA: {CMC_NO_DATA}")
                continue
            data = pd.DataFrame([data])  # Convert data to DataFrame
            if data.empty: CMC_NO_DATA.append(coin)
            else: df_token_info = pd.concat([df_token_info, data], ignore_index=True)
            time.sleep(0.5)
    except: 
        for index, row in df_ticker.iterrows():
            time.sleep(0.5)
            coin = row['coin']
            get_token_total_supply(coin)
        with engine.connect() as connection: df_token_info = pd.DataFrame(connection.execute(text('SELECT * FROM token_supply_info')).fetchall())
    df_merge = pd.merge(df_ticker, df_token_info, on='coin', how='left')
    df_merge = df_merge[df_merge['is_ignore'] != 1]
    if df_merge.empty: return {}
    df_merge = df_merge[df_merge['is_stablecoin'] != 1]
    if df_merge.empty: return {}
    df_merge['marketcap'] = df_merge['total_supply'] * df_merge['lastPrice']
    df_merge['turnover_ratio'] = df_merge['quoteVolume'] / df_merge['marketcap']
    df_merge['circulating_ratio'] = df_merge['circulating_supply'] / df_merge['total_supply']
    df_merge = df_merge[df_merge['circulating_ratio'] > CIRCULATION_RATIO]
    if df_merge.empty: return {}
    df_merge = df_merge[df_merge['marketcap'] < FULLLY_DILUTED_MARKET_CAP_UP_LIMIT]
    if df_merge.empty: return {}
    df_merge = df_merge.sort_values(by='turnover_ratio', ascending=False)
    df_merge = df_merge.head(int(head))
    if df_merge.empty: return {}
    turnover_ratio_dict = df_merge.set_index('coin')['turnover_ratio'].to_dict()
    reply_string = '\n'.join([f"/buy_{k}: {format_number(v)}" for k, v in turnover_ratio_dict.items()])
    send_msg(reply_string, from_id)
    return turnover_ratio_dict


def count_positions(from_id=TG_BOT_OWNER_ID):
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    with engine.connect() as connection: df = pd.DataFrame(connection.execute(text('SELECT coin, account FROM position_table WHERE is_closed = 0')).fetchall())
    if df.empty: return send_msg("No positions in spot account or funding account", from_id)
    df_spot = df[df['account'] == 'spot']
    spot_coinlist = df_spot['coin'].values.tolist() if not df_spot.empty else []
    df_funding = df[df['account'] == 'funding']
    funding_coinlist = df_funding['coin'].values.tolist() if not df_funding.empty else []
    reply_msg = f"Positions in spot: {df_spot.shape[0]}\n{', '.join(set(spot_coinlist))}\n\nPositions in funding: {df_funding.shape[0]}\n{', '.join(set(funding_coinlist))}"
    if from_id: send_msg(reply_msg, from_id)
    return


def positions_counts():
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    with engine.connect() as connection: 
        try: df = pd.DataFrame(connection.execute(text('SELECT count(*) FROM position_table WHERE is_closed = 0 AND account = "spot"')).fetchall())
        except: df = pd.DataFrame()
    counts = df.iloc[0].values[0] if not df.empty else 0
    return counts


def check_positions_counts():
    df_orderId = get_open_orders_list(None, 'BUY')
    counts = df_orderId.shape[0]
    counts += positions_counts()
    return counts


def count_positions_amounts(coin, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(f"SELECT coin, account, amount, usdt_value FROM position_table WHERE is_closed = 0 AND coin = '{coin}'")).fetchall())
    if df.empty: return send_msg(f"No {coin} positions in spot account or funding account", from_id)
    total_coin_in_position = df['amount'].sum()
    position_total_counts = df.shape[0]
    df_spot = df[df['account'] == 'spot']
    if not df_spot.empty: 
        total_coin_in_spot = df_spot['amount'].sum()
        total_cost_in_spot = df_spot['usdt_value'].sum()
        position_spot_counts = df_spot.shape[0]
    else: 
        total_coin_in_spot, position_spot_counts, total_cost_in_spot = 0, 0, 0
    df_funding = df[df['account'] == 'funding']
    if not df_funding.empty: 
        total_coin_in_funding = df_funding['amount'].sum()
        total_cost_in_funding = df_funding['usdt_value'].sum()
        position_funding_counts = df_funding.shape[0]
    else: total_coin_in_funding, position_funding_counts, total_cost_in_funding = 0, 0, 0
    reply_msg = f"{coin} positions:\n\nTotal ({position_total_counts}): {format_number(total_coin_in_position)}\nSpot ({position_spot_counts}): {format_number(total_coin_in_spot)}\nFunding ({position_funding_counts}): {format_number(total_coin_in_funding)}"
    total_cost_usdt = total_cost_in_spot + total_cost_in_funding
    position_avg_price = total_cost_usdt / total_coin_in_position if total_coin_in_position else 0
    if total_cost_usdt and position_avg_price: reply_msg += f"\n\nTotal Cost: {format_number(total_cost_usdt)}\nAvg Price: {format_number(position_avg_price)}"
    avg_price = get_avg_price(coin)
    if avg_price: 
        current_value = float(total_coin_in_position) * float(avg_price['price'])
        profit_or_lost = current_value - total_cost_usdt
        percentage_up_or_down = round(profit_or_lost / total_cost_usdt * 100, 2)
        reply_msg += f"\n\nCurrent Value: {format_number(current_value)}\nCurrent Price: {format_number(avg_price['price'])}\n\nProfit/Lost: {format_number(profit_or_lost)}\nUp/Down: {percentage_up_or_down}%"
    reply_msg += f"\n\n{generate_bottom_msg(coin)}"
    if from_id: send_msg(reply_msg, from_id)
    return


# from position_table table get a given coin's higest close price
def get_highest_close_price(coin):
    coin = coin.upper()
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    try:
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(f"SELECT coin, price_close FROM position_table WHERE is_closed = 1 AND coin = '{coin}'")).fetchall())
    except: df = pd.DataFrame()
    if df.empty: return 0
    highest_close_price = df['price_close'].max()
    return float(highest_close_price)


def is_spot_full(engine=engine):
    with engine.connect() as connection: 
        df_in_position = pd.DataFrame(connection.execute(text('''SELECT coin FROM position_table WHERE is_closed = 0 AND account = "spot"''')).fetchall())
        if df_in_position.shape[0] >= POSITIONS_LIMIT: return True
        df_orderId = get_open_orders_list(None, 'BUY')
        if df_orderId.shape[0] + df_in_position.shape[0] >= POSITIONS_LIMIT: return True
    return False


def check_coin_position_in_funding_account(coin = 'RSR', amount_target = 146652243, down_step = 0.1, from_id=TG_BOT_OWNER_ID):
    total_amount, total_cost, price_create = 0, 0, 0
    with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(f'SELECT coin, account, amount, price_create, usdt_value FROM position_table WHERE is_closed = 0 AND coin = "{coin}" AND account = "funding"')).fetchall())
    if not df.empty: 
        total_amount = df['amount'].sum()
        total_cost = df['usdt_value'].sum()
        price_create = df['price_create'].min()
    if total_amount >= amount_target: return send_msg(f"RSR amount in funding account: {format_number(total_amount)} >= amount_target: {format_number(amount_target)}, \ntotal_position: {df.shape[0]}\nprice_min: {format_number(price_create)}\ntotal_usdt_cost: {format_number(total_cost)}\n/ccv_{coin}_{int(total_amount)}", from_id)
    current_price = get_avg_price(coin)
    if not current_price: return
    current_price = float(current_price['price'])
    if current_price > price_create * (1 - down_step): return print(f"{coin} current price: {current_price} > price_create_min: {price_create} * (1 - down_step: {down_step})")
    return binance_funding_buy_and_hold(coin, from_id)


def coin_create_position(coin, current_price, step, from_id, is_holding = False, engine = engine):
    coin = coin.upper()
    if not current_price: current_price = float(get_avg_price(coin)['price'])
    if step == 0.03: today_hotcoin_check_save(coin, current_price, engine)
    with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(f'SELECT price_create, price_close, is_closed, time_close FROM position_table WHERE coin = "{coin}" AND is_closed = 0')).fetchall())
    if not df.empty and current_price > float(df['price_create'].min()) * (1 - step): return
    if is_holding: return binance_funding_buy_and_hold(coin, from_id, engine)
    if not is_spot_full(engine): 
        resistance_dict = get_resistant_price(coin)
        if not resistance_dict: return send_msg(f"Failed to get resistance price for {coin}", from_id)
        else: target_profit = resistance_dict.get('target_profit', 0.01)
        if target_profit < TARGET_PROFIT_PERCENTAGE and step != 0.03: return send_msg(f"Target profit for {coin} is too low: {round(target_profit*100)}%", from_id)
        bot_market_buy_one_unit(coin, from_id, engine)
        target_profit = max(target_profit, TARGET_PROFIT_PERCENTAGE)
        binance_position_set_limit_sell(target_profit, from_id, coin, engine)
        return


def buy_back_most_profitable(buy_back_target_profit=0.03, from_id=TG_BOT_OWNER_ID):
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    coins_could_buy_back = calculate_missed_profit(from_id, buy_back_target_profit)
    if not coins_could_buy_back: return
    for coin in coins_could_buy_back:
        if is_spot_full(engine): return
        resistance_dict = get_resistant_price(coin)
        if not resistance_dict: return send_msg(f"Failed to get resistance price for {coin}", from_id)
        else: target_profit = resistance_dict.get('target_profit', 0.01)
        if target_profit < TARGET_PROFIT_PERCENTAGE: return send_msg(f"Target profit for {coin} is too low: {round(target_profit*100)}%", from_id)
        bot_market_buy_one_unit(coin, from_id, engine)
        target_profit = max(target_profit, TARGET_PROFIT_PERCENTAGE)
        binance_position_set_limit_sell(target_profit, from_id, coin, 0, engine)
    return


def coin_close_position(coin, current_price, profit, from_id, is_holding = False, engine = engine):
    profit = profit * 2 if is_holding else profit
    coin = coin.upper()
    with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(f'SELECT * FROM position_table WHERE is_closed = 0 AND coin = "{coin}"')).fetchall())
    if df.empty: return
    if not current_price: current_price = float(get_avg_price(coin)['price'])
    df['profit'] = (current_price - df['price_create']) * df['amount'] - df['commission']
    if df['profit'].sum() < profit:
        df = df[df['profit'] >= profit]
        if df.empty: return
    for i in range(df.shape[0]):
        coin_df = df[i:i+1]
        coin_with_highest_profit = coin_df['coin'].values[0]
        orderId_create = int(coin_df['orderId_create'].values[0])
        do_market_sell_by_orderId_create(orderId_create, from_id, coin_df, coin_with_highest_profit, engine)
    latest_price = get_hotcoin_latest(coin, engine)
    if latest_price:
        price_diff = current_price - latest_price
        if price_diff > 0:
            price_diff_percentage = round(price_diff / latest_price * 100, 2)
            broadcast_text(f"{coin} ({format_number(current_price)}) position is good to close. Price went up {format_number(price_diff_percentage)}% since reported last time at {format_number(latest_price)} usdt/{coin.lower()}")
    return


# Define a function to read hot_coin_history table and get today's hot coin list
def get_hot_coin_list_of_today(engine = engine):
    hotcoin_list = []
    today_date = datetime.now().strftime('%Y-%m-%d')
    try: 
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text('SELECT coin FROM hot_coins_history WHERE date LIKE :date'), {'date': f"{today_date}%"}).fetchall())
    except: return hotcoin_list
    hotcoin_list = df['coin'].values.tolist() if not df.empty else hotcoin_list
    return hotcoin_list


def today_hotcoin_check_save(coin, price, engine = engine):
    hotcoin_list = get_hot_coin_list_of_today(engine)
    if coin in hotcoin_list: return
    hot_coin_history = {
        'coin': coin, 
        'price': price, 
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    data_to_table(hot_coin_history, 'hot_coins_history', 'append', engine)
    return broadcast_text(f"{coin} ({format_number(price)}) is good to long.")


# Define a function to read hot_coin_history table and get today's hot coin list
def get_hotcoin_latest(coin, engine = engine):
    coin = coin.upper()
    try: 
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(f'''SELECT coin, price, date FROM hot_coins_history WHERE coin = "{coin}" ORDER BY date DESC LIMIT 1''')).fetchall())
    except: df = pd.DataFrame()
    if df.empty: return 0
    latest_price_reported = df['price'].values[0]
    return float(latest_price_reported)


def binance_today_hot_coin(trading_volume_limit = TRADING_VOLUME_LIMIT, tradingbot_status = False):
    global CMC_NO_DATA
    with engine.connect() as connection:
        try: previous_ticker = pd.DataFrame(connection.execute(text('SELECT * FROM previous_ticker')).fetchall())
        except: previous_ticker = pd.DataFrame()
    df_ticker = pd.read_json(BINANCE_TICKER_URL)
    df_ticker = df_ticker.loc[:, ['symbol', 'priceChangePercent', 'lastPrice', 'openPrice', 'highPrice', 'lowPrice', 'quoteVolume', 'openTime', 'closeTime']]
    df_ticker = df_ticker[df_ticker['symbol'].str.endswith('USDT')]
    df_ticker = df_ticker[~df_ticker['symbol'].str.contains('UP|DOWN')]
    with engine.connect() as connection: df_ticker.to_sql('previous_ticker', connection, if_exists='replace', index=False)
    if not previous_ticker.empty:
        df_merge = pd.merge(df_ticker, previous_ticker, on='symbol', how='left')
        df_merge_symbols = df_merge[df_merge['lastPrice_x'] > df_merge['lastPrice_y']]
        df_ticker = df_ticker[df_ticker['symbol'].isin(df_merge_symbols['symbol'])]
    # UTC 0 is 16 of Los Angeles time, so when it's 17:00 in Los Angeles, it's 1:00 in UTC time, then the quoteVolume is only for the last hour
    hours_passed_since_utc_0 = datetime.utcnow().hour
    simulated_quoteVolume_per_hour = trading_volume_limit / 24
    trading_hours = hours_passed_since_utc_0 + 1
    trading_volume_limit = simulated_quoteVolume_per_hour * trading_hours
    df_ticker = df_ticker[(df_ticker['quoteVolume'] > trading_volume_limit) & (df_ticker['lastPrice'] > 0.0001) & (df_ticker['lastPrice'] < 2000)]
    if df_ticker.empty: return {}
    df_ticker['coin'] = df_ticker['symbol'].str[:-4]
    try:
        with engine.connect() as connection: df_token_info = pd.DataFrame(connection.execute(text('SELECT * FROM token_supply_info')).fetchall())
        df_ticker_missed = df_ticker[~df_ticker['coin'].isin(df_token_info['coin'])]
        for index, row in df_ticker_missed.iterrows():
            coin = row['coin']
            if coin in CMC_NO_DATA: continue
            data = get_token_total_supply(coin)
            if not data: 
                CMC_NO_DATA.append(coin)
                print(f"CMC_NO_DATA: {CMC_NO_DATA}")
                continue
            data = pd.DataFrame([data])  # Convert data to DataFrame
            if data.empty: CMC_NO_DATA.append(coin)
            else: df_token_info = pd.concat([df_token_info, data], ignore_index=True)
            time.sleep(0.5)
    except: 
        for index, row in df_ticker.iterrows():
            coin = row['coin']
            get_token_total_supply(coin)
            time.sleep(0.5)
        with engine.connect() as connection: df_token_info = pd.DataFrame(connection.execute(text('SELECT * FROM token_supply_info')).fetchall())
    df_merge = pd.merge(df_ticker, df_token_info, on='coin', how='left')
    df_merge = df_merge.query('is_ignore == 0 and is_stablecoin == 0 and is_white == 1')
    if df_merge.empty: return {}
    if not tradingbot_status:
        try: coinbase_coin_list = read_coinbase_coin_list()
        except: coinbase_coin_list = COINBASE_COIN_LIST
        df_merge = df_merge[df_merge['coin'].isin(coinbase_coin_list)]
        if df_merge.empty: return {}
    df_merge = df_merge.copy()
    df_merge['marketcap'] = df_merge['total_supply'] * df_merge['lastPrice']
    df_merge['turnover_ratio'] = df_merge['quoteVolume'] / df_merge['marketcap']
    df_merge['circulating_ratio'] = df_merge['circulating_supply'] / df_merge['total_supply']
    df_merge = df_merge.query('circulating_ratio > @CIRCULATION_RATIO and marketcap < @FULLLY_DILUTED_MARKET_CAP_UP_LIMIT')
    if df_merge.empty: return {}
    df_merge = df_merge.sort_values(by='turnover_ratio', ascending=False)
    df_merge = df_merge.head(30)
    df_ticker = df_merge.loc[:, ['coin', 'lastPrice']]
    today_hot_coin_list = df_ticker['coin'].values.tolist()
    print(f"TOP 30 coins sorted by turnover_ratio: {' '.join(today_hot_coin_list)}")
    final_hotcoins_dict = {}
    remainning_positions = 10
    for index, row in df_ticker.iterrows():
        if remainning_positions <= 0: break
        coin = row['coin']
        try: long_or_short = analyze_symbol(coin)
        except: continue
        long = long_or_short.get('long')
        if not long: continue
        target_profit = long_or_short.get('target_profit')
        if not target_profit: continue
        final_hotcoins_dict[coin] = target_profit
        remainning_positions -= 1
        price = row['lastPrice']
        hot_coin_history = {
            'coin': coin, 
            'price': price, 
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
        data_to_table(hot_coin_history, 'hot_coins_history')
        reply_string = f"{coin} | {format_number(price)}"
        broadcast_text(reply_string)
    return final_hotcoins_dict


def binance_adjust_profit():
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    df_spot_position = read_position_table_account(0, None, 'spot', engine)
    if df_spot_position.empty: fund_in_spot_position = 0
    else: fund_in_spot_position = df_spot_position['usdt_value'].sum()
    df_profit = read_position_table_account(1, None, 'spot', engine)
    profit = df_profit['profit'].sum()
    spot_balance = get_coin_wallet_balance_with_locked()
    USDT_balance = int(spot_balance['USDT'])
    amount_to_be_adjusted = USDT_balance - (INITIAL_FUND - fund_in_spot_position + profit)
    amount_to_be_adjusted = int(amount_to_be_adjusted)
    if amount_to_be_adjusted > 300:
        alert = f'amount_to_be_adjusted: {format_number(amount_to_be_adjusted)}'
        data = binance_market_buy_quantity('BNB', 1)
        if not data: return send_msg(f'{alert}\nfailed to market buy 1 BNB', TG_BOT_OWNER_ID)
        if 'fills' in data: del data['fills']
        if data_to_table(data, 'check_and_buy_BNB', 'append', engine): send_msg(f'{alert}\nDONE: Market buy 1 BNB', TG_BOT_OWNER_ID)
    return amount_to_be_adjusted


def mark_limit_order_as_canceled_by_orderId(orderId, engine = engine):
    with engine.connect() as connection:
        try:
            connection.execute(text(f"UPDATE position_table SET orderId_close = 0, target_profit = 0, is_manual = 0 WHERE orderId_close = :orderId"), {'orderId': orderId})
            connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()
    return

def switch_spot_to_funding(orderId_create, engine = engine):
    with engine.connect() as connection:
        try:
            connection.execute(text(f"UPDATE position_table SET account = 'funding', orderId_close = 0, is_manual =0, target_profit = 0 WHERE orderId_create = :orderId_create"), {'orderId_create': orderId_create})
            connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()
    return

def switch_funding_to_spot(orderId_create, engine = engine):
    with engine.connect() as connection:
        try:
            connection.execute(text(f"UPDATE position_table SET account = 'spot' WHERE orderId_create = :orderId_create"), {'orderId_create': orderId_create})
            connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()
    return


def user_limit_buy_at_support_price(coin, from_id=TG_BOT_OWNER_ID):
    chat_id = from_id
    if not coin: return send_msg(f'Coin is not given', chat_id)
    if check_positions_counts() >= POSITIONS_LIMIT: return
    coin = coin.upper()
    coin = coin if not coin.endswith('USDT') else coin[:-4]
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    df = read_position_table_account(0, coin, 'spot', engine)
    if not df.empty: return send_msg(f'Coin {coin} is in auto position, do not double buy', chat_id)
    target_price_dict = get_resistant_price(coin)
    if not target_price_dict: return send_msg(f'Failed to get target price for {coin}', chat_id)
    target_price = float(target_price_dict.get('support_price', 0))
    if not target_price: return send_msg(f'Failed to get target price for {coin}', chat_id)
    amount = CHECK_SIZE / target_price
    polished_parameters = polish_parameters_for_limit_order(coin, amount, target_price)
    if not polished_parameters: return send_msg(f'Failed to polish parameters for limit buy order', chat_id)
    amount = polished_parameters['amount']
    price = polished_parameters['price']
    data = binance_limit_buy(coin, amount, price)
    if not data: return send_msg(f'Failed to set limit buy order for {coin}', chat_id)
    orderId = data['orderId']
    if chat_id: send_msg(f"{coin} Limit Buy Order at {price} \n/cancel_{coin}_{orderId}\n{generate_bottom_msg(coin)}", chat_id)
    return


def bot_limit_buy(coin, target_price, from_id=TG_BOT_OWNER_ID):
    amount = CHECK_SIZE / target_price
    polished_parameters = polish_parameters_for_limit_order(coin, amount, target_price)
    if not polished_parameters: return
    amount = polished_parameters['amount']
    price = polished_parameters['price']
    data = binance_limit_buy(coin, amount, price)
    if not data: return
    orderId = data['orderId']
    return send_msg(f"Bot_Limit_Buy {coin} ordered at {format_number(price)}\n/ignore_{coin}\n/cancel_{coin}_{orderId}\n{generate_bottom_msg(coin)}", from_id)


def limit_buy_order_filled(symbol: str, orderId_create = 0, chat_id = TG_BOT_OWNER_ID, engine = engine):
    if not orderId_create: return send_msg(f'orderId_create is not given', chat_id)
    symbol = symbol.upper() if symbol.upper().endswith('USDT') else symbol.upper() + 'USDT'
    coin = symbol.replace('USDT', '')
    try: orderId_create = int(orderId_create)
    except: return send_msg(f'orderId_create: {orderId_create} is not a number', chat_id)
    data = check_order_status_by_orderId(coin, orderId_create)
    if not data: return send_msg(f'Failed to get order status by orderId: {orderId_create}', chat_id)
    instert_position_table(data, 'spot', engine)
    price = float(data['cummulativeQuoteQty']) / float(data['executedQty'])
    send_msg(f"Limit order bought {coin} at {format_number(price)} usdt/{coin.lower()}\n{generate_bottom_msg(coin)}", chat_id)
    return set_limit_sell_to_resistant_price(coin, chat_id, engine)


# check orderId get data and insert to position_table
def check_orderId_get_data_insert_position_table(coin, orderId, account = 'funding', engine = engine):
    data = check_order_status_by_orderId(coin, orderId)
    try: instert_position_table(data, account, engine)
    except Exception as e: print(f"Failed to insert position table: {e}")
    return


# Define a function to transfer 10000 usdt from funding to main, then market buy the given coin and then transfer all of the coin bought to funding account
def binance_funding_buy_and_hold(coin, from_id=TG_BOT_OWNER_ID, engine = engine):
    coin = coin.upper()
    coin = coin if not coin.endswith('USDT') else coin[:-4]
    tranId = funding_main_transfer_with_check_and_send('USDT', CHECK_SIZE, from_id)
    if not tranId: return
    data = binance_market_buy(coin, CHECK_SIZE)
    if not data: return send_msg(f'Failed to do market buy for coin: {coin}', from_id)
    executedQty = float(data['executedQty'])
    main_funding_transfer_with_check_and_send(coin, executedQty, from_id)
    cummulativeQuoteQty = float(data['cummulativeQuoteQty'])
    price = cummulativeQuoteQty / executedQty
    instert_position_table(data, 'funding', engine)
    return send_msg(f'''Funding account bought {coin} at {format_number(price)} usdt/{coin.lower()}\n\n{generate_bottom_msg(coin)}''', from_id)


def switch_position_from_main_to_funding(coin, from_id=TG_BOT_OWNER_ID, engine = engine):
    coin = coin.upper()
    coin = coin if not coin.endswith('USDT') else coin[:-4]
    df = read_position_table_account(0, coin, 'spot', engine)
    if df.empty: return send_msg(f'No {coin} position in main account', from_id)
    for index, row in df.iterrows():
        amount = float(row['amount'])
        usdt_value = float(row['usdt_value'])
        orderId_create = int(row['orderId_create'])
        orderId_close = int(row['orderId_close'])
        if orderId_close: binance_cancel_order_by_orderId(coin, orderId_close)
        if not funding_main_transfer_with_check_and_send('USDT', usdt_value, from_id): return send_msg(f'USDT in funding account is not sufficient', from_id)
        switch_spot_to_funding(orderId_create, engine)
        main_funding_transfer_with_check_and_send(coin, amount, from_id)
        send_msg(f'''{coin} has been switched to funding account!\norderId_create | {orderId_create}\n\n{generate_bottom_msg(coin)}''', from_id)
    return 


def switch_position_from_funding_to_main(coin, from_id=TG_BOT_OWNER_ID, engine = engine):
    coin = coin.upper()
    coin = coin if not coin.endswith('USDT') else coin[:-4]
    df = read_position_table_account(0, coin, 'funding', engine)
    if df.empty: return send_msg(f'No {coin} position in funding account', from_id)
    for index, row in df.iterrows():
        amount = float(row['amount'])
        usdt_value = float(row['usdt_value'])
        orderId_create = int(row['orderId_create'])
        if not funding_main_transfer_with_check_and_send(coin, amount, from_id): return send_msg(f'{coin} in funding account is not sufficient', from_id)
        switch_funding_to_spot(orderId_create, engine)
        main_funding_transfer_with_check_and_send('USDT', usdt_value, from_id)
        send_msg(f'''{coin} has been switched to main account!\norderId_create | {orderId_create}\n\n{generate_bottom_msg(coin)}''', from_id)
        set_limit_sell_to_resistant_price(coin, from_id, engine)
    return


def funding_position_price(coin, from_id=TG_BOT_OWNER_ID):
    coin = coin.upper()
    coin = coin if not coin.endswith('USDT') else coin[:-4]
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    df = read_position_table_account(0, coin, 'funding', engine)
    if df.empty: return send_msg(f'No {coin} position in funding account', from_id)
    # sort df by price, ascending
    df = df.sort_values(by='price_create', ascending=True)
    # Make a dict of price and orderId
    price_orderId_dict = df.set_index('price_create')['orderId_create'].to_dict()
    reply_string = '\n'.join([f"{v}: {format_number(k)} usdt/{coin.lower()}" for k, v in price_orderId_dict.items()])
    send_msg(f"{reply_string}\n\n{generate_bottom_msg(coin)}", from_id)
    return price_orderId_dict


# Define a function to reverse the process of binance_funding_buy_and_hold
def binance_funding_sell(coin, from_id=TG_BOT_OWNER_ID, is_repair = False):
    coin = coin.upper()
    coin = coin if not coin.endswith('USDT') else coin[:-4]
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    df = read_position_table_account(0, coin, 'funding', engine)
    if df.empty: return send_msg(f'No {coin} position in funding account', from_id)
    df = df.sort_values(by='price_create', ascending=True)
    row = df.iloc[0]
    orderId_create = int(row['orderId_create'])
    amount = float(row['amount'])
    if not is_repair: 
        transId = funding_main_transfer_with_check_and_send(coin, amount, from_id)
        if not transId: return send_msg(f'Failed to transfer {coin} from funding to main', from_id)
    data = binance_market_sell(coin, amount)
    if not data: return send_msg(f'Failed to do market sell for {coin}\n/repair_funding_sell_{coin}', from_id)
    profit = update_position_table_with_orderId(coin, orderId_create, int(data.get('orderId', 0)), from_id, row, data, engine)
    main_funding_transfer_with_check_and_send('USDT', float(data['cummulativeQuoteQty']), from_id)
    return profit


def monthly_summary():
    last_month = datetime.now().month - 1 if datetime.now().month != 1 else 12
    last_month_year = datetime.now().year - 1 if datetime.now().month == 1 else datetime.now().year
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    with engine.connect() as connection: df_profit = pd.DataFrame(connection.execute(text('SELECT coin, symbol, time_close, profit FROM position_table WHERE is_closed = 1 AND month_close = :month AND year_close = :year'), {'month': last_month, 'year': last_month_year}).fetchall())
    # Add string format column of transactTime
    df_profit['time_string_month'] = df_profit['time_close'].apply(lambda x: datetime.fromtimestamp(x / 1000).strftime('%Y-%m'))
    trading_counts = df_profit.shape[0]
    total_profit = df_profit['profit'].astype(float).sum()
    total_profit_by_initialfund = total_profit / INITIAL_FUND * 100
    df_profit = df_profit.groupby('coin').sum(numeric_only=True).reset_index()
    df_profit = df_profit.sort_values(by='profit', ascending=False).reset_index(drop=True)
    best_coin = df_profit['coin'][0]
    best_coin_profit = df_profit['profit'][0]
    worst_coin = df_profit['coin'][df_profit.shape[0] - 1]
    worst_coin_profit = df_profit['profit'][df_profit.shape[0] - 1]
    reply_sumary = f"Trading Counts: {trading_counts}\nTotal Profit: {format_number(total_profit)}\nROI: {total_profit_by_initialfund:.2f}%\n\nBest Coin: {best_coin} >> {format_number(best_coin_profit)}\nWorst Coin: {worst_coin} >> {format_number(worst_coin_profit)}"
    send_msg(f"Trading Bot Performance Summary of {last_month_year}-{last_month}:\n\n{reply_sumary}", TG_BOT_OWNER_ID)
    send_email(f'Trading Bot Performance Summary of {last_month_year}-{last_month}', reply_sumary, GMAIL_ADDRESS_MAIN)
    send_email(f'Trading Bot Performance Summary of {last_month_year}-{last_month}', reply_sumary, os.getenv('GMAIL_DANLI'))
    return reply_sumary


def rsi_bottom_coins():
    df_ticker = pd.read_json(BINANCE_TICKER_URL)
    df_ticker = df_ticker.loc[:, ['symbol', 'priceChangePercent', 'lastPrice', 'openPrice', 'highPrice', 'lowPrice', 'quoteVolume', 'openTime', 'closeTime']]
    df_ticker = df_ticker[df_ticker['symbol'].str.endswith('USDT')]
    df_ticker = df_ticker[(df_ticker['priceChangePercent'] < 0) & (df_ticker['lastPrice'] > 0.0001) & (df_ticker['lastPrice'] < 2000)]
    if df_ticker.empty: return []
    df_ticker['coin'] = df_ticker['symbol'].str[:-4]
    IGNORE_LIST = get_ignore_list()
    df_ticker = df_ticker[~df_ticker['coin'].isin(IGNORE_LIST)]
    if df_ticker.empty: return []
    today_date = datetime.now().strftime('%Y-%m-%d')
    today_hour_minute = datetime.now().strftime("%H:%M")
    final_bottom_list = []
    reply_msg_list = []
    for index, row in df_ticker.iterrows():
        coin = row['coin']
        coin_rsi_1d = analyze_rsi(coin, interval = '1d')
        if np.isnan(coin_rsi_1d) or coin_rsi_1d > 20: continue
        token_info = get_token_market_cap_and_ratio(coin, turnover_ratio_eth=0.05)
        if not token_info: continue
        market_cap = token_info['market_cap']
        fully_diluted_market_cap = token_info['fully_diluted_market_cap']
        circulating_ratio = token_info['circulation_ratio']
        turnover_ratio = token_info['turnover_ratio']
        final_bottom_list.append(coin)
        price = row['lastPrice']
        bottom_rsi_coins = {
            'coin': coin, 
            'price': price, 
            'coin_rsi_1d': coin_rsi_1d,
            'date': today_date,
            'hour_minute': today_hour_minute,
            }
        data_to_table(bottom_rsi_coins, 'bottom_rsi_coins')
        reply_msg_list.append(f"{coin} | PRICE: {format_number(price)} | RSI_1d: {coin_rsi_1d:.2f} | M/V: {turnover_ratio:.2f} | {format_number(market_cap)} / {format_number(fully_diluted_market_cap)} = {circulating_ratio:.2f}")
    if final_bottom_list: 
        send_msg(f"RSI Bottom Coins {today_date}: \n\n{', '.join(final_bottom_list)}", TG_BOT_OWNER_ID)
        send_email(f'RSI Bottom Coins {today_date}', '\n'.join(reply_msg_list), GMAIL_ADDRESS_MAIN)
    return final_bottom_list


def get_current_positions_from_all_tables(from_id = TG_BOT_OWNER_ID):
    df = read_position_table(0, None)
    if df.empty: 
        if from_id: send_msg(f"No positions", from_id)
        return []
    coin_in_positions = list(set(df['coin'].values.tolist()))
    if from_id: send_msg(f"Current Positions: \n{', '.join(coin_in_positions)}", from_id)
    return coin_in_positions


def grid_profit_check(grid_profit_target=10):
    df_balance = read_position_table()
    if df_balance.empty: return pd.DataFrame()
    try: df = get_token_price_table(coin_column=False)
    except: return pd.DataFrame()
    df_balance = pd.merge(df_balance, df, on='symbol', how='left')
    df_balance['profit'] = (df_balance['lastPrice'] - df_balance['price_create']) * df_balance['amount'] - df_balance['commission']
    df_balance['asset_value'] = df_balance['lastPrice'] * df_balance['amount']
    df_balance = df_balance.sort_values(by='profit', ascending=False)
    if grid_profit_target: df_balance = df_balance[df_balance['profit'] > grid_profit_target]
    df_balance = df_balance.loc[:, ['coin', 'profit', 'asset_value', 'account', 'orderId_create', 'orderId_close']]
    return df_balance


def check_usdt_balance(from_id=None):
    spot_balance = get_coin_wallet_balance_with_locked()
    spot_USDT_balance = int(spot_balance['USDT'])
    funding_balance = get_funding_asset()
    funding_USDT_balance = float(funding_balance[funding_balance['asset'] == 'USDT']['free'].values[0])
    total_usdt = spot_USDT_balance + int(funding_USDT_balance)
    reply_string = f"USDT Balance: \nSpot: {format_number(spot_USDT_balance)}\nFunding: {format_number(funding_USDT_balance)}\nTotal: {format_number(total_usdt)}"
    if from_id: send_msg(reply_string, from_id)
    return {'spot': spot_USDT_balance, 'funding': funding_USDT_balance, 'total': total_usdt}


def grid_profit_check_for_user(from_id=TG_BOT_OWNER_ID, grid_profit_target=1):
    df_balance = grid_profit_check(grid_profit_target)
    if df_balance.empty: return send_msg(f"No open positions with profit.", from_id)
    df_funding = df_balance[df_balance['account'] == 'funding']
    if not df_funding.empty:
        # Seperate 'RSR' with other coins
        df_rsr = df_funding[df_funding['coin'] == 'RSR']
        if not df_rsr.empty:
            total_profit_rsr = df_rsr['profit'].sum()
            reply_list = [f'RSR positions ({df_rsr.shape[0]}):'] if df_rsr.shape[0] <= 5 else [f'RSR Top 5 positions of {df_rsr.shape[0]}:']
            df_rsr_head = df_rsr.head(5)
            for index, row in df_rsr_head.iterrows(): reply_list.append(f"/ftm_{row['coin']} >> {format_number(row['profit'])} /close_{row['orderId_create']}")
            reply_string = '\n'.join(reply_list)
            send_msg(f"{reply_string}\nTotal profit: {format_number(total_profit_rsr)} usdt", from_id)
            df_funding = df_funding[df_funding['coin'] != 'RSR']
        reply_list = [f'FUNDING account ({df_funding.shape[0]}):']
        for index, row in df_funding.iterrows(): reply_list.append(f"/ftm_{row['coin']} >> {format_number(row['profit'])} /close_{row['orderId_create']}")
        reply_string = '\n'.join(reply_list)
        send_msg(f"{reply_string}\nTotal profit: {format_number(df_funding['profit'].sum())} usdt", from_id)
    df_spot = df_balance[df_balance['account'] == 'spot']
    if not df_spot.empty:
        reply_list = [f'SPOT account ({df_spot.shape[0]}):']
        for index, row in df_spot.iterrows(): reply_list.append(f"/mtf_{row['coin']} >> {format_number(row['profit'])} /close_{row['orderId_create']}")
        reply_string = '\n'.join(reply_list)
        send_msg(f"{reply_string}\nTotal profit: {format_number(df_spot['profit'].sum())} usdt", from_id)
    if grid_profit_target: return
    asset_value = df_balance['asset_value'].sum()
    data = check_usdt_balance()
    spot_usdt = data.get('spot', 0)
    funding_usdt = data.get('funding', 0)
    total_usdt = data.get('total', 0)
    total_value = asset_value + total_usdt
    df_balance = df_balance.groupby('coin').sum(numeric_only=True).reset_index()
    df_balance = df_balance.sort_values(by='profit', ascending=True).reset_index(drop=True)
    coin_with_highest_lost = df_balance['coin'][0]
    coin_with_highest_lost_profit = format_number(df_balance['profit'][0])
    send_msg(f"Asset: {format_number(asset_value)} usdt\nUSDT Spot: {format_number(spot_usdt)}\nUSDT Funding: {format_number(funding_usdt)}\nUSDT Total: {format_number(total_usdt)}\n\nValue Total: {format_number(total_value)} usdt\nHighest Loss: /cpa_{coin_with_highest_lost} | {coin_with_highest_lost_profit}\n\n/close_postive_positions\n/close_all_positions\n/open_orders_list\n/calculate_missed_profit", from_id)
    return 


def position_check_for_user(from_id=TG_BOT_OWNER_ID):
    return grid_profit_check_for_user(from_id, grid_profit_target=0)


def click_to_close(orderId_create, from_id=TG_BOT_OWNER_ID):
    try: orderId_create = int(orderId_create)
    except: return send_msg(f'orderId_create: {orderId_create} is not a number', from_id)
    if orderId_create == 123456789: return send_msg(f'Yes, now you know how to close a position by orderId_create, just replace the 123456789 with a valid orderId', from_id)
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    return do_market_sell_by_orderId_create(orderId_create, from_id, pd.DataFrame(), None, engine)


def close_all_positions(confirm: str, from_id=TG_BOT_OWNER_ID):
    if not confirm or confirm.upper() not in ['ALL', 'CONFIRM', 'YES']: return send_msg(f'You need to type ALL or CONFIRM or YES to confirm close all positions.', from_id)
    df_balance = read_position_table()
    coin_position_counts = df_balance['coin'].value_counts().to_dict()
    ignore_list = [k for k, v in coin_position_counts.items() if v > 1]
    df_balance = df_balance[~df_balance['coin'].isin(ignore_list)] if ignore_list else df_balance
    if df_balance.empty: return send_msg(f'No open position for close', from_id)
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    for i in range(df_balance.shape[0]): do_market_sell_by_orderId_create(int(df_balance.iloc[i]['orderId_create']), from_id, df_balance.iloc[i:i+1], df_balance.iloc[i]['coin'], engine)


def close_postive_positions(from_id, grid_profit_target=1, account = 'spot'):
    df_balance = grid_profit_check(grid_profit_target)
    if df_balance.empty: return send_msg(f"No open positions with profit.", from_id)
    engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)
    if account == 'spot': 
        df_spot = df_balance[df_balance['account'] == 'spot']
        if not df_spot.empty:
            for i in range(df_spot.shape[0]):
                coin_df = df_spot[i:i+1]
                coin_with_highest_profit = coin_df['coin'].values[0]
                orderId_create = int(coin_df['orderId_create'].values[0])
                do_market_sell_by_orderId_create(orderId_create, from_id, coin_df, coin_with_highest_profit, engine)
    if account == 'funding':
        df_funding = df_balance[df_balance['account'] == 'funding']
        if not df_funding.empty:
            for i in range(df_funding.shape[0]):
                coin_df = df_funding[i:i+1]
                coin_with_highest_profit = coin_df['coin'].values[0]
                orderId_create = int(coin_df['orderId_create'].values[0])
                do_market_sell_by_orderId_create(orderId_create, from_id, coin_df, coin_with_highest_profit, engine)
    return 


def auto_limit_buy_at_support_price(coin, from_id=TG_BOT_OWNER_ID):
    target_price_dict = get_resistant_price(coin)
    if not target_price_dict: return 
    target_price = float(target_price_dict.get('support_price', 0))
    if not target_price: return 
    amount = CHECK_SIZE / target_price
    polished_parameters = polish_parameters_for_limit_order(coin, amount, target_price)
    if not polished_parameters: return
    amount = polished_parameters['amount']
    price = polished_parameters['price']
    data = binance_limit_buy(coin, amount, price)
    if not data: return
    orderId = data['orderId']
    if from_id: send_msg(f"{coin} Limit Buy Order at {price} \n/cancel_{coin}_{orderId}\n{generate_bottom_msg(coin)}", from_id)
    return True


# Check open orders for BUY and place a new order for the coins in holding_list but not in open orders
def check_open_orders_and_place_new_order(from_id=TG_BOT_OWNER_ID, engine = engine):
    df = read_position_table_account(0, None, 'spot', engine)
    position_coins = df['coin'].values.tolist()
    limit_buy_df = get_open_orders_list(None, side = 'BUY')
    ''' limit_buy
       coin side      orderId
    0   ETH  BUY  16013178663
    2  IOTX  BUY    911140331
    3   OGN  BUY    812101781
    6   RSR  BUY    781465890
    8   GMT  BUY   1983013771
    9   APE  BUY   1607665465
    '''
    current_limit_buy = limit_buy_df['coin'].values.tolist()
    holding_list = read_holding_list()
    '''['RSR', 'OGN', 'IOTX', 'CTK', 'CHZ', 'WLD']'''
    # check if the length of position_coins + current_limit_buy is less than POSITIONS_LIMIT
    if len(position_coins) + len(current_limit_buy) >= POSITIONS_LIMIT: return send_msg(f'Positions and open orders are already at the limit: {POSITIONS_LIMIT}', from_id)
    coins_to_buy = set(holding_list) - set(current_limit_buy) - set(position_coins)
    for coin in coins_to_buy: 
        if auto_limit_buy_at_support_price(coin, from_id): return
    return


if __name__ == '__main__':
    print('Binance_api.py is running')
    parameters_dict = read_trading_parameters()
    print(f"Parameters: {parameters_dict}")
    print(TARGET_PROFIT)
    target_profit = read_target_profit_default()
    print(f"Target Profit: {target_profit}")