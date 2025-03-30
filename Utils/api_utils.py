import ccxt
import pandas as pd

def fetch_historical_data(symbol, timeframe, start_date, end_date):
    """
    Récupère les données historiques pour un actif donné.
    """
    exchange = ccxt.binance()
    since = exchange.parse8601(start_date + 'T00:00:00Z')
    until = exchange.parse8601(end_date + 'T00:00:00Z')
    ohlcv = []

    while since < until:
        data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=1000)
        if not data:
            break
        ohlcv.extend(data)
        since = data[-1][0] + 1  # Passer à la prochaine période

    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def fetch_real_time_data(symbol, timeframe='1d', limit=100):
    """
    Récupère des données en temps réel ou historiques pour un actif donné.
    """
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df