# src/layouts/regional_layout.py
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

iso3_mapping = {
    'Canada': 'CAN', 'États-Unis': 'USA', 'États-Unis (y compris Hawaii)': 'USA',
    'Mexique': 'MEX', 'Brésil': 'BRA', 'Argentine': 'ARG', 'Chili': 'CHL',
    'Colombie': 'COL', 'Pérou': 'PER', 'Venezuela': 'VEN', 'Uruguay': 'URY',
    'Royaume-Uni': 'GBR', 'Allemagne': 'DEU', 'Italie': 'ITA', 'Espagne': 'ESP',
    'France': 'FRA', 'Belgique': 'BEL', 'Pays-Bas': 'NLD', 'Suisse': 'CHE',
    'Autriche': 'AUT', 'Portugal': 'PRT', 'Grèce': 'GRC', 'Pologne': 'POL',
    'Suède': 'SWE', 'Norvège': 'NOR', 'Danemark': 'DNK', 'Finlande': 'FIN',
    'Irlande': 'IRL', 'Islande': 'ISL', 'Luxembourg': 'LUX', 'Hongrie': 'HUN',
    'République tchèque': 'CZE', 'Roumanie': 'ROU', 'Bulgarie': 'BGR',
    'Croatie': 'HRV', 'Slovénie': 'SVN', 'Slovaquie': 'SVK', 'Estonie': 'EST',
    'Lettonie': 'LVA', 'Lituanie': 'LTU', 'Serbie': 'SRB', 'Ukraine': 'UKR',
    'Chine': 'CHN', 'Japon': 'JPN', 'Corée du Sud': 'KOR', 'Inde': 'IND',
    'Thaïlande': 'THA', 'Vietnam': 'VNM', 'Singapour': 'SGP', 'Malaisie': 'MYS',
    'Indonésie': 'IDN', 'Philippines': 'PHL', 'Hong Kong': 'HKG', 'Taïwan': 'TWN',
    'Australie': 'AUS', 'Nouvelle-Zélande': 'NZL', 'Papouasie-Nouvelle-Guinée': 'PNG',
    'Afrique du Sud': 'ZAF', 'Égypte': 'EGY', 'Maroc': 'MAR', 'Tunisie': 'TUN',
    'Algérie': 'DZA', 'Kenya': 'KEN', 'Nigeria': 'NGA', 'Éthiopie': 'ETH',
    'Russie': 'RUS', 'Turquie': 'TUR', 'Arabie Saoudite': 'SAU', 'Israël': 'ISR',
    'Émirats Arabes Unis': 'ARE', 'Qatar': 'QAT', 'Koweït': 'KWT', 'Liban': 'LBN',
    'Jordanie': 'JOR', 'Oman': 'OMN', 'Bahreïn': 'BHR', 'Pakistan': 'PAK',
    'Bangladesh': 'BGD', 'Sri Lanka': 'LKA', 'Népal': 'NPL', 'Afghanistan': 'AFG',
    'Iran': 'IRN', 'Irak': 'IRQ', 'Syrie': 'SYR', 'Yémen': 'YEM'
}

coords_regions = {
    'Europe': {'lat': 50, 'lon': 10},
    'Europe (hors France)': {'lat': 50, 'lon': 10},
    'Asie': {'lat': 35, 'lon': 105},
    'Amérique du Nord': {'lat': 45, 'lon': -100},
    'Amérique du Sud': {'lat': -15, 'lon': -60},
    'Amérique Centrale': {'lat': 15, 'lon': -90},
    'Afrique': {'lat': 0, 'lon': 20},
    'Océanie': {'lat': -25, 'lon': 135},
    'Moyen-Orient': {'lat': 30, 'lon': 45}
}

def create_layout(df_dict):
    """Analyse géographique avec cartes interactives des flux touristiques"""
    
    df = df_dict["frequentation_region"].copy()
    df['Mois'] = pd.to_datetime(df['Mois'], errors='coerce')
    
    dates = sorted(df['Mois'].dt.to_period('M').unique())
    dates_str = [str(d) for d in dates]
    
    return dbc.Container(fluid=True, children=[
        html.H2("Analyse Géographique du Tourisme", className="text-center mb-3"),
        html.P("Visualisation des flux touristiques par région du monde", 
               className="text-center text-muted mb-4"),
        
        dbc.Card(dbc.CardBody([
            html.H5("Filtres", className="mb-3"),
            
            html.Label("Période d'analyse", className="fw-bold mb-2"),
            dcc.RangeSlider(
                id='regional-date-slider',
                min=0,
                max=len(dates_str) - 1,
                value=[0, len(dates_str) - 1],
                marks={
                    i: dates_str[i][:4]
                    for i in range(len(dates_str))
                    if dates_str[i].endswith("-01")
                },
                tooltip={"placement": "bottom", "always_visible": False}
            ),
            
            html.Br(),
            
            html.Label("Indicateur à visualiser", className="fw-bold mb-2"),
            dcc.RadioItems(
                id='regional-indicator',
                options=[
                    {'label': ' Nombre de touristes', 'value': 'Nombre de touristes'},
                    {'label': ' Nuitées touristiques', 'value': 'Nuitées touristiques'},
                    {'label': ' Durée de séjour moyenne', 'value': 'Durée de séjour moyenne'}
                ],
                value='Nombre de touristes',
                labelStyle={'display': 'block', 'marginBottom': '8px'}
            )
        ]), className="mb-4"),
        
        dbc.Alert([
            html.Strong("💡 Astuce : "),
            "Survolez les pays et régions sur les cartes pour voir les détails. Utilisez les filtres pour explorer différentes périodes."
        ], color="info", className="mb-4"),
        
        html.H4("Cartes Interactives", className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                html.P("Carte mondiale par pays", className="text-muted small mb-2"),
                dcc.Graph(id='regional-world-map', style={'height': '450px'})
            ], md=6),
            dbc.Col([
                html.P("Vue par grandes régions", className="text-muted small mb-2"),
                dcc.Graph(id='regional-scatter-map', style={'height': '450px'})
            ], md=6)
        ], className="mb-4"),
        
        html.Hr(className="my-4"),
        
        dbc.Row([
            dbc.Col([
                html.H5("Top 10 Régions", className="mb-3"),
                dcc.Graph(id='regional-top-chart', style={'height': '350px'}, config={'displayModeBar': False})
            ], md=6),
            dbc.Col([
                html.H5("Durée Moyenne par Région", className="mb-3"),
                dcc.Graph(id='regional-duration-chart', style={'height': '350px'}, config={'displayModeBar': False})
            ], md=6)
        ], className="mb-4"),
        
        html.Hr(className="my-4"),
        
        # NOUVELLE SECTION : Histogrammes de distribution
        html.H4("Distributions Statistiques", className="mb-3"),
        html.P("Histogrammes montrant la répartition des pays selon différents critères", className="text-muted"),
        
        dbc.Row([
            dbc.Col([
                html.H6("Distribution des durées de séjour", className="mb-2 text-center"),
                dcc.Graph(id='regional-histogram-duree', style={'height': '350px'}, config={'displayModeBar': False})
            ], md=6),
            dbc.Col([
                html.H6("Distribution du volume de touristes", className="mb-2 text-center"),
                dcc.Graph(id='regional-histogram-volume', style={'height': '350px'}, config={'displayModeBar': False})
            ], md=6)
        ], className="mb-4"),
        
        html.Hr(className="my-4"),
        
        html.H4("Évolution Temporelle par Région", className="mb-3"),
        html.P("Comparez l'évolution de plusieurs régions dans le temps", className="text-muted"),
        dcc.Dropdown(
            id='regional-regions-dropdown',
            multi=True,
            placeholder="Sélectionnez une ou plusieurs régions...",
            style={'marginBottom': '15px'}
        ),
        dcc.Graph(id='regional-evolution-chart', style={'height': '350px'}, config={'displayModeBar': False}),
        
        html.Hr(className="my-4"),
        
        html.H5("Statistiques Clés (période sélectionnée)", className="mb-3"),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H6("Touristes", className="text-muted mb-2"),
                html.H4(id='kpi-touristes', className="text-primary mb-0")
            ]), className="text-center"), md=3),
            
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H6("Nuitées", className="text-muted mb-2"),
                html.H4(id='kpi-nuitees', className="text-success mb-0")
            ]), className="text-center"), md=3),
            
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H6("Pays", className="text-muted mb-2"),
                html.H4(id='kpi-pays', className="text-warning mb-0")
            ]), className="text-center"), md=3),
            
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H6("Durée moyenne", className="text-muted mb-2"),
                html.H4(id='kpi-duree', className="text-info mb-0")
            ]), className="text-center"), md=3),
        ]),
        
        dcc.Store(id='regional-dates-store', data=dates_str)
    ])

def register_callbacks(app, df_dict):
    """Enregistre les callbacks pour l'interactivité des graphiques"""
    
    @app.callback(
        [
            Output('regional-world-map', 'figure'),
            Output('regional-scatter-map', 'figure'),
            Output('regional-top-chart', 'figure'),
            Output('regional-duration-chart', 'figure'),
            Output('regional-histogram-duree', 'figure'),
            Output('regional-histogram-volume', 'figure'),
            Output('regional-regions-dropdown', 'options'),
            Output('kpi-touristes', 'children'),
            Output('kpi-nuitees', 'children'),
            Output('kpi-pays', 'children'),
            Output('kpi-duree', 'children')
        ],
        [
            Input('regional-date-slider', 'value'),
            Input('regional-indicator', 'value'),
            Input('regional-dates-store', 'data')
        ]
    )
    def update_page(date_range, indicator, dates_str):
        
        df = df_dict["frequentation_region"].copy()
        df['Mois'] = pd.to_datetime(df['Mois'], errors='coerce')
        
        start = pd.to_datetime(dates_str[date_range[0]])
        end = pd.to_datetime(dates_str[date_range[1]])
        df = df[(df['Mois'] >= start) & (df['Mois'] <= end)]
        
        agg_map = {
            'Nombre de touristes': 'sum',
            'Nuitées touristiques': 'sum',
            'Durée de séjour moyenne': 'mean'
        }
        
        df_pays = df.groupby('Pays', as_index=False).agg({indicator: agg_map[indicator]})
        df_pays['ISO3'] = df_pays['Pays'].map(iso3_mapping)
        df_pays_valides = df_pays.dropna(subset=['ISO3'])
        
        nb_pays_total = len(df_pays)
        nb_pays_affiches = len(df_pays_valides)
        
        if not df_pays_valides.empty:
            fig_world = px.choropleth(
                df_pays_valides,
                locations='ISO3',
                color=indicator,
                hover_name='Pays',
                hover_data={indicator: ':,.0f'},
                color_continuous_scale='Blues',
                title=f"{indicator} par pays ({nb_pays_affiches}/{nb_pays_total} pays affichés)"
            )
            fig_world.update_layout(
                geo=dict(
                    showframe=True,
                    showcoastlines=True,
                    projection_type='natural earth'
                ),
                height=420,
                margin=dict(l=0, r=0, t=30, b=0),
                template="plotly_white"
            )
        else:
            fig_world = go.Figure().add_annotation(
                text="Aucune donnée avec code pays disponible",
                showarrow=False,
                font=dict(size=14)
            )
        
        df_reg = df.groupby('Region', as_index=False).agg({indicator: agg_map[indicator]})
        df_reg['lat'] = df_reg['Region'].map(lambda x: coords_regions.get(x, {}).get('lat'))
        df_reg['lon'] = df_reg['Region'].map(lambda x: coords_regions.get(x, {}).get('lon'))
        df_reg_valides = df_reg.dropna(subset=['lat'])
        
        if not df_reg_valides.empty:
            fig_scatter = px.scatter_geo(
                df_reg_valides,
                lat='lat',
                lon='lon',
                size=indicator if indicator != 'Durée de séjour moyenne' else None,
                color=indicator,
                hover_name='Region',
                hover_data={
                    'lat': False,
                    'lon': False,
                    indicator: ':,.1f'
                },
                size_max=50,
                color_continuous_scale='Oranges',
                title=f"Répartition géographique par région"
            )
            fig_scatter.update_layout(
                geo=dict(
                    projection_type='natural earth',
                    showland=True,
                    landcolor='rgb(243, 243, 243)',
                    coastlinecolor='rgb(204, 204, 204)',
                    showocean=True,
                    oceancolor='rgb(230, 245, 255)'
                ),
                height=420,
                margin=dict(l=0, r=0, t=30, b=0),
                template="plotly_white"
            )
        else:
            fig_scatter = go.Figure().add_annotation(
                text="Aucune donnée régionale disponible",
                showarrow=False,
                font=dict(size=14)
            )
        
        top = df_reg.nlargest(10, indicator).sort_values(indicator, ascending=True)
        
        fig_top = px.bar(
            top,
            x=indicator,
            y='Region',
            orientation='h',
            color=indicator,
            color_continuous_scale='Greens',
            text=indicator
        )
        fig_top.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_top.update_layout(
            showlegend=False,
            height=320,
            margin=dict(l=0, r=100, t=0, b=30),
            xaxis_title="",
            yaxis_title="",
            yaxis={'fixedrange': True},
            xaxis={'fixedrange': True},
            template="plotly_white"
        )
        
        df_duree = df.groupby('Region', as_index=False).agg({
            'Durée de séjour moyenne': 'mean',
            'Nombre de touristes': 'sum'
        })
        df_duree_top = df_duree.nlargest(10, 'Nombre de touristes').sort_values('Durée de séjour moyenne', ascending=True)
        
        fig_duree = px.bar(
            df_duree_top,
            x='Durée de séjour moyenne',
            y='Region',
            orientation='h',
            color='Durée de séjour moyenne',
            color_continuous_scale='Purples',
            text='Durée de séjour moyenne'
        )
        fig_duree.update_traces(texttemplate='%{text:.1f}j', textposition='outside')
        fig_duree.update_layout(
            showlegend=False,
            height=320,
            margin=dict(l=0, r=100, t=0, b=30),
            xaxis_title="Jours",
            yaxis_title="",
            yaxis={'fixedrange': True},
            xaxis={'fixedrange': True},
            template="plotly_white"
        )
        
        # HISTOGRAMME 1 : Distribution des durées de séjour
        df_pays_duree = df.groupby('Pays', as_index=False)['Durée de séjour moyenne'].mean()
        
        # Définir les intervalles (bins)
        bins_duree = [0, 5, 10, 15, 20, 25, 30, 100]
        labels_duree = ['0-5j', '5-10j', '10-15j', '15-20j', '20-25j', '25-30j', '30+j']
        
        df_pays_duree['Intervalle'] = pd.cut(
            df_pays_duree['Durée de séjour moyenne'], 
            bins=bins_duree, 
            labels=labels_duree,
            include_lowest=True
        )
        
        # Compter le nombre de pays par intervalle
        hist_duree = df_pays_duree.groupby('Intervalle', observed=True).size().reset_index(name='Nombre de pays')
        
        fig_hist_duree = px.bar(
            hist_duree,
            x='Intervalle',
            y='Nombre de pays',
            color='Nombre de pays',
            color_continuous_scale='Blues',
            text='Nombre de pays'
        )
        fig_hist_duree.update_traces(textposition='outside')
        fig_hist_duree.update_layout(
            showlegend=False,
            height=320,
            margin=dict(l=50, r=20, t=20, b=50),
            xaxis_title="Durée de séjour (jours)",
            yaxis_title="Nombre de pays",
            template="plotly_white"
        )
        
        # HISTOGRAMME 2 : Distribution du volume de touristes
        df_pays_volume = df.groupby('Pays', as_index=False)['Nombre de touristes'].sum()
        
        # Définir les intervalles (bins) en milliers
        bins_volume = [0, 1000, 5000, 10000, 20000, 50000, 200000]
        labels_volume = ['0-1M', '1-5M', '5-10M', '10-20M', '20-50M', '50M+']
        
        df_pays_volume['Intervalle'] = pd.cut(
            df_pays_volume['Nombre de touristes'], 
            bins=bins_volume, 
            labels=labels_volume,
            include_lowest=True
        )
        
        # Compter le nombre de pays par intervalle
        hist_volume = df_pays_volume.groupby('Intervalle', observed=True).size().reset_index(name='Nombre de pays')
        
        fig_hist_volume = px.bar(
            hist_volume,
            x='Intervalle',
            y='Nombre de pays',
            color='Nombre de pays',
            color_continuous_scale='Greens',
            text='Nombre de pays'
        )
        fig_hist_volume.update_traces(textposition='outside')
        fig_hist_volume.update_layout(
            showlegend=False,
            height=320,
            margin=dict(l=50, r=20, t=20, b=50),
            xaxis_title="Volume de touristes (milliers)",
            yaxis_title="Nombre de pays",
            template="plotly_white"
        )
        
        return (
            fig_world,
            fig_scatter,
            fig_top,
            fig_duree,
            fig_hist_duree,
            fig_hist_volume,
            [{'label': r, 'value': r} for r in sorted(df['Region'].unique())],
            f"{df['Nombre de touristes'].sum()/1000:.1f}M",
            f"{df['Nuitées touristiques'].sum()/1000:.1f}M",
            str(df['Pays'].nunique()),
            f"{df['Durée de séjour moyenne'].mean():.1f}j"
        )
    
    @app.callback(
        Output('regional-evolution-chart', 'figure'),
        Input('regional-regions-dropdown', 'value')
    )
    def update_evolution(regions):
        
        if not regions:
            return go.Figure().add_annotation(
                text="Sélectionnez une ou plusieurs régions ci-dessus",
                showarrow=False,
                font=dict(size=14, color="gray")
            )
        
        df = df_dict["frequentation_region"].copy()
        df['Mois'] = pd.to_datetime(df['Mois'], errors='coerce')
        df = df[df['Region'].isin(regions)]
        
        df_agg = df.groupby(['Mois', 'Region'], as_index=False)['Nombre de touristes'].sum()
        
        fig = px.line(
            df_agg,
            x='Mois',
            y='Nombre de touristes',
            color='Region',
            markers=True,
            title="Évolution mensuelle du nombre de touristes"
        )
        fig.update_layout(
            hovermode='x unified',
            height=320,
            margin=dict(l=0, r=0, t=0, b=40),
            yaxis={'fixedrange': True},
            xaxis={'fixedrange': True},
            template="plotly_white",
            xaxis_title="",
            yaxis_title="Touristes (milliers)"
        )
        
        return fig