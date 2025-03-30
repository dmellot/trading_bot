import time
import ccxt
import pandas as pd

# Configuration initiale
API_KEY = 'votre_api_key'  # Remplacez par votre clé API Binance réelle ou Testnet
API_SECRET = 'votre_api_secret'  # Remplacez par votre clé secrète Binance réelle ou Testnet

# Initialisation de l'API Binance
binance = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
})

# Allocation cible
allocation = {
    'BTC': 0.5,  # 50 % en Bitcoin
    'ETH': 0.3,  # 30 % en Ethereum
    'AAPL': 0.2  # 20 % en Apple (actions)
}

# Montant mensuel à investir
monthly_investment = 200  # Modifiez cette valeur si vous souhaitez investir un montant différent

def dca_bot():
    print("Bot DCA démarré...")
    while True:
        try:
            # Récupérer le solde disponible
            balance = binance.fetch_balance()
            available_balance = balance['free']['EUR']  # Solde en euros disponibles

            if available_balance >= monthly_investment:
                print(f"Investissement mensuel de {monthly_investment} € en cours...")

                # Calculer les montants à investir pour chaque actif
                btc_amount = monthly_investment * allocation['BTC']
                eth_amount = monthly_investment * allocation['ETH']
                aapl_amount = monthly_investment * allocation['AAPL']

                # Acheter les actifs
                binance.create_market_buy_order('BTC/EUR', btc_amount)
                binance.create_market_buy_order('ETH/EUR', eth_amount)
                # Note : Pour les actions comme AAPL, utilisez une API comme Alpaca.
                print("Investissement effectué avec succès.")
            
            else:
                print("Solde insuffisant pour effectuer l'investissement.")

            # Attendre un mois avant la prochaine exécution
            time.sleep(30 * 24 * 60 * 60)  # 30 jours en secondes

        except Exception as e:
            print(f"Erreur lors de l'exécution du bot DCA : {e}")

# Lancer le bot
dca_bot()