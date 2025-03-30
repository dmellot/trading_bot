import talib
import numpy as np
import ccxt

# Paramètres du bot
symbol = 'BTC/USD'
interval = '1h'  # Intervalle des données (1 heure)

# Configuration initiale
API_KEY = 'votre_api_key'  # Remplacez par votre clé API Binance réelle ou Testnet
API_SECRET = 'votre_api_secret'  # Remplacez par votre clé secrète Binance réelle ou Testnet

# Initialisation de l'API Binance
binance = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
})

def trading_bot():
    print("Bot de trading algorithmique démarré...")
    while True:
        try:
            # Récupérer les données historiques
            ohlcv = binance.fetch_ohlcv(symbol, timeframe=interval, limit=100)
            data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

            # Calculer les indicateurs techniques
            data['rsi'] = talib.RSI(data['close'], timeperiod=14)
            data['macd'], _, _ = talib.MACD(data['close'], fastperiod=12, slowperiod=26, signalperiod=9)

            # Conditions d'achat/vente
            last_row = data.iloc[-1]
            if last_row['rsi'] < 30 and last_row['macd'] > 0:
                print("Signal d'achat détecté !")
                binance.create_market_buy_order(symbol, 0.001)  # Acheter 0.001 BTC
            elif last_row['rsi'] > 70 and last_row['macd'] < 0:
                print("Signal de vente détecté !")
                binance.create_market_sell_order(symbol, 0.001)  # Vendre 0.001 BTC

            # Attendre avant la prochaine analyse
            time.sleep(60 * 60)  # 1 heure en secondes

        except Exception as e:
            print(f"Erreur lors de l'exécution du bot de trading : {e}")

# Lancer le bot
trading_bot()