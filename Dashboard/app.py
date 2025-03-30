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