import pandas as pd
import numpy as np
import ccxt
import talib

# Paramètres du backtest
symbol = 'BTC/USD'
timeframe = '1d'  # Intervalle des données (1 jour)
start_date = '2022-01-01'
end_date = '2023-01-01'

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

def backtest_strategy(df):
    """
    Exécute une stratégie de backtest basée sur le RSI.
    """
    # Calculer le RSI
    df['rsi'] = talib.RSI(df['close'], timeperiod=14)

    # Initialiser les colonnes pour les signaux et positions
    df['signal'] = 0
    df['position'] = 0
    df['balance'] = 1000  # Solde initial (ex. : 1000 €)
    df['asset_balance'] = 0  # Solde en actif (ex. : BTC)

    for i in range(1, len(df)):
        # Générer des signaux d'achat/vente
        if df['rsi'][i - 1] < 30 and df['rsi'][i] >= 30:  # Signal d'achat
            df.at[df.index[i], 'signal'] = 1
        elif df['rsi'][i - 1] > 70 and df['rsi'][i] <= 70:  # Signal de vente
            df.at[df.index[i], 'signal'] = -1

        # Mettre à jour les positions
        if df['signal'][i] == 1:  # Achat
            df.at[df.index[i], 'asset_balance'] = df['balance'][i - 1] / df['close'][i]
            df.at[df.index[i], 'balance'] = 0
        elif df['signal'][i] == -1:  # Vente
            df.at[df.index[i], 'balance'] = df['asset_balance'][i - 1] * df['close'][i]
            df.at[df.index[i], 'asset_balance'] = 0
        else:  # Conserver la position précédente
            df.at[df.index[i], 'balance'] = df['balance'][i - 1]
            df.at[df.index[i], 'asset_balance'] = df['asset_balance'][i - 1]

    # Calculer la valeur totale du portefeuille
    df['portfolio_value'] = df['balance'] + df['asset_balance'] * df['close']
    return df

def analyze_results(df):
    """
    Analyse les résultats du backtest.
    """
    initial_value = df['portfolio_value'].iloc[0]
    final_value = df['portfolio_value'].iloc[-1]
    roi = (final_value - initial_value) / initial_value * 100
    print(f"ROI : {roi:.2f}%")
    print(f"Valeur initiale : {initial_value:.2f} €")
    print(f"Valeur finale : {final_value:.2f} €")

# Récupérer les données historiques
df = fetch_historical_data(symbol, timeframe, start_date, end_date)

# Exécuter le backtest
df = backtest_strategy(df)

# Analyser les résultats
analyze_results(df)

# Afficher les données pour inspection
print(df[['timestamp', 'close', 'rsi', 'signal', 'balance', 'asset_balance', 'portfolio_value']])