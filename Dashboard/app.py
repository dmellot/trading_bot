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
    html.H1("Tableau de Bord des Performances"),
    
    # Graphique interactif
    dcc.Graph(id='portfolio-graph'),
    
    # Répartition des actifs
    dcc.Graph(id='asset-allocation'),
])

# Callback pour mettre à jour le graphique du portefeuille
@app.callback(
    Output('portfolio-graph', 'figure'),
    [Input('portfolio-graph', 'id')]
)
def update_portfolio_graph(_):
    fig = px.line(df, x='Date', y='Portfolio_Value', title="Évolution de la Valeur du Portefeuille")
    return fig

# Callback pour afficher la répartition des actifs
@app.callback(
    Output('asset-allocation', 'figure'),
    [Input('asset-allocation', 'id')]
)
def update_asset_allocation(_):
    last_row = df.iloc[-1]
    allocation_data = {
        'Actif': ['BTC', 'ETH', 'AAPL'],
        'Valeur': [last_row['BTC'], last_row['ETH'], last_row['AAPL']]
    }
    allocation_df = pd.DataFrame(allocation_data)
    fig = px.pie(allocation_df, names='Actif', values='Valeur', title="Répartition Actuelle des Actifs")
    return fig

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from utils.api_utils import fetch_real_time_data

# Initialisation de l'application Dash
app = dash.Dash(
    __name__,
    assets_folder='dashboard/assets',
    external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css"]
)

# Récupérer des données réelles
df = fetch_real_time_data('BTC/USD', timeframe='1d', limit=100)

# Layout de l'application
app.layout = html.Div([
    html.Header([
        html.H1("Tableau de Bord d'Investissement Automatisé"),
        html.P("Gérez vos actifs et suivez vos performances en temps réel."),
        html.Div([
            html.I(className="fas fa-moon", id="dark-mode-toggle")
        ], className="theme-toggle")
    ], className="header"),

    html.Main([
        html.Section([
            html.H2("Valeur Totale du Portefeuille"),
            dcc.Graph(id='portfolio-value-graph', className="chart-container"),
        ], className="card"),

        html.Section([
            html.H2("Répartition Actuelle des Actifs"),
            dcc.Graph(id='asset-allocation-graph', className="chart-container"),
        ], className="card"),

        html.Section([
            html.H2("Gestion des Bots"),
            html.Div([
                html.Button("Démarrer Bot DCA", id="start-dca-bot", className="btn btn-primary"),
                html.Button("Arrêter Bot DCA", id="stop-dca-bot", className="btn btn-danger"),
            ], className="button-group"),
            html.Div(id="bot-status", className="status-message"),
        ], className="card"),

        html.Section([
            html.H2("Logs en Temps Réel"),
            dcc.Textarea(id="logs", value="Chargement des logs...", className="log-textarea", readOnly=True),
        ], className="card"),
    ],
        ], className="main-content"),

    html.Footer([
        html.P("© 2023 - Tableau de Bord d'Investissement Automatisé")
    ], className="footer"),
], className="app-container")

# Callbacks
@app.callback(
    Output('portfolio-value-graph', 'figure'),
    [Input('portfolio-value-graph', 'id')]
)
def update_portfolio_graph(_):
    fig = px.line(df, x='timestamp', y='close', title="Évolution de la Valeur du Portefeuille")
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font_color='white',
        title_font_size=20,
        xaxis_title="Date",
        yaxis_title="Valeur (USD)"
    )
    return fig

@app.callback(
    Output('asset-allocation-graph', 'figure'),
    [Input('asset-allocation-graph', 'id')]
)
def update_asset_allocation(_):
    allocation_data = {
        'Actif': ['BTC', 'ETH', 'AAPL'],
        'Valeur': [5000, 3000, 2000]
    }
    allocation_df = pd.DataFrame(allocation_data)
    fig = px.pie(allocation_df, names='Actif', values='Valeur', title="Répartition Actuelle des Actifs")
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font_color='white',
        title_font_size=20
    )
    return fig

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
    elif button_id == "stop-dca-bot":
        return "Statut du Bot : Arrêté"

@app.callback(
    Output('logs', 'value'),
    [Input('logs', 'id')]
)
def update_logs(_):
    try:
        with open("logs/dca_log.txt", "r") as f:
            logs = f.read()
        return logs
    except FileNotFoundError:
        return "Aucun log disponible pour le moment."

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)