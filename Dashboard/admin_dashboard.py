import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


# Données simulées pour le portefeuille
data = {
    'Date': ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01'],
    'BTC': [5000, 5200, 5100, 5300],
    'ETH': [2000, 2100, 2050, 2200],
    'AAPL': [150, 155, 160, 170],
    'Portfolio_Value': [7150, 7450, 7350, 7670]
}
df = pd.DataFrame(data)

# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Layout du tableau de bord
app.layout = html.Div([
    html.H1("Panneau d'Administration"),
    
    # Vue d'ensemble du portefeuille
    html.Div([
        html.H3("Valeur Totale du Portefeuille"),
        dcc.Graph(id='portfolio-value-graph'),
        dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0)  # Mise à jour toutes les 5 secondes
    ]),
    
    # Répartition des actifs
    html.Div([
        html.H3("Répartition Actuelle des Actifs"),
        dcc.Graph(id='asset-allocation-graph'),
    ]),
    
    # Gestion des bots
    html.Div([
        html.H3("Gestion des Bots"),
        html.Button("Démarrer Bot DCA", id="start-dca-bot", n_clicks=0),
        html.Button("Arrêter Bot DCA", id="stop-dca-bot", n_clicks=0),
        html.Div(id="bot-status", style={"margin-top": "10px"}),
    ]),
    
    # Logs
    html.Div([
        html.H3("Logs en Temps Réel"),
        dcc.Textarea(id="logs", value="Chargement des logs...", style={"width": "100%", "height": 200}),
        dcc.Interval(id='log-update-interval', interval=5*1000, n_intervals=0)  # Mise à jour toutes les 5 secondes
    ]),
])

# Callback pour mettre à jour le graphique du portefeuille
@app.callback(
    Output('portfolio-value-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_portfolio_graph(n):
    fig = px.line(df, x='Date', y='Portfolio_Value', title="Évolution de la Valeur du Portefeuille")
    return fig

# Callback pour afficher la répartition des actifs
@app.callback(
    Output('asset-allocation-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_asset_allocation(n):
    last_row = df.iloc[-1]
    allocation_data = {
        'Actif': ['BTC', 'ETH', 'AAPL'],
        'Valeur': [last_row['BTC'], last_row['ETH'], last_row['AAPL']]
    }
    allocation_df = pd.DataFrame(allocation_data)
    fig = px.pie(allocation_df, names='Actif', values='Valeur', title="Répartition Actuelle des Actifs")
    return fig

# Callback pour mettre à jour le statut des bots
@app.callback(
    Output('bot-status', 'children'),
    [Input('start-dca-bot', 'n_clicks'), Input('stop-dca-bot', 'n_clicks')]
)
def update_bot_status(start_clicks, stop_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "Statut du Bot : Inactif"
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == "start-dca-bot":
        return "Statut du Bot : Actif"
    elif button_id ==  "stop-dca-bot":
        return "Statut du Bot : Inactif"
    return "Statut du Bot : Inconnu"        
# Callback pour mettre à jour les logs
@app.callback(
    Output('logs', 'value'),
    [Input('log-update-interval', 'n_intervals')]
)
def update_logs(n):
    # Simuler des logs (remplacez cela par des logs réels)
    try:
        with open("logs/dca_log.txt", "r") as f:
            logs = f.read()
        return logs
    except FileNotFoundError:
        return "Aucun log disponible pour le moment."

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)

import subprocess

# Callback pour démarrer/arrêter le bot DCA
@app.callback(
    Output('bot-status', 'children'),
    [Input('start-dca-bot', 'n_clicks'), Input('stop-dca-bot', 'n_clicks')]
)
def update_bot_status(start_clicks, stop_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "Statut du Bot : Inactif"
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "start-dca-bot":
        # Démarrer le bot DCA en arrière-plan
        subprocess.Popen(["nohup", "python", "bots/dca_bot.py", "&"])
        return "Statut du Bot : Actif"
    elif button_id == "stop-dca-bot":
        # Arrêter le bot DCA
        subprocess.run(["pkill", "-f", "dca_bot.py"])
        return "Statut du Bot : Arrêté"