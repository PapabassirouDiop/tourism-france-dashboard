# app.py
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from src.utils.load_cleaned_data import load_cleaned_data
from src.layouts import home_layout, regional_layout, international_layout, economic_layout

# Chargement des données
df_dict = load_cleaned_data()

# Initialisation de l'application Dash avec thème Bootstrap
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# Configuration du serveur
server = app.server

# Layout principal
app.layout = dbc.Container([
    # En-tête
    dbc.Row([
        dbc.Col([
            html.H1(" Tourisme International en France", 
                   className="text-center text-primary mb-4 mt-4"),
            html.Hr()
        ])
    ]),
    
    # Navigation par onglets
    dbc.Row([
        dbc.Col([
            dcc.Tabs(
                id='tabs',
                value='accueil',
                children=[
                    dcc.Tab(label='🏠 Accueil', value='accueil', className='custom-tab'),
                    dcc.Tab(label='🗺️ Régions', value='regions', className='custom-tab'),
                    dcc.Tab(label='🌍 International', value='international', className='custom-tab'),
                    dcc.Tab(label='💼 Économie', value='economie', className='custom-tab'),
                ],
                className='mb-4'
            )
        ])
    ]),
    
    # Contenu dynamique
    dbc.Row([
        dbc.Col([
            html.Div(id='page-content')
        ])
    ])
], fluid=True)

# Callback pour la navigation
@app.callback(
    Output('page-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    """Affiche le contenu selon l'onglet sélectionné"""
    if tab == 'accueil':
        return home_layout.create_layout(df_dict)
    elif tab == 'regions':
        return regional_layout.create_layout(df_dict)
    elif tab == 'international':
        return international_layout.create_layout(df_dict)
    elif tab == 'economie':
        return economic_layout.create_layout(df_dict)
    else:
        return html.Div("Page non trouvée")

# Callbacks pour les interactions (seront définis dans les layouts)
regional_layout.register_callbacks(app, df_dict)
international_layout.register_callbacks(app, df_dict)
economic_layout.register_callbacks(app, df_dict)

# Lancement de l'application
if __name__ == '__main__':
    print("🚀 Lancement du dashboard...")
    print("📊 Données chargées avec succès")
    print("🌐 Accédez au dashboard : http://localhost:8050")
    app.run(debug=True, host='0.0.0.0', port=8050)
