# src/layouts/international_layout.py
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

iso3_mapping = {
    'Canada': 'CAN', 'États-Unis': 'USA', 'États-Unis (y compris Hawaii)': 'USA',
    'Hawaii': 'USA', 'USA': 'USA',
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

def create_layout(df_dict):
    df_hotel = df_dict["frequentation_hoteliere"].copy()
    
    if 'Année' in df_hotel.columns:
        df_hotel['Année'] = pd.to_numeric(df_hotel['Année'], errors='coerce')
    
    regions_dispo = ['Tous'] + sorted(df_hotel['Region'].unique().tolist())
    
    annees = []
    if 'Année' in df_hotel.columns:
        annees = sorted(df_hotel['Année'].dropna().unique().astype(int).tolist())
    
    layout = dbc.Container([
        html.H2("Analyse Internationale par Pays", className="text-center mb-3"),
        html.P("Analyse détaillée et comparaison pays par pays", 
               className="text-center text-muted mb-4"),
        
        dbc.Card([
            dbc.CardBody([
                html.H5("Filtres Avancés", className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        html.Label("Filtrer par région", className="fw-bold mb-2"),
                        dcc.Dropdown(
                            id='intl-region-filter',
                            options=[{'label': r, 'value': r} for r in regions_dispo],
                            value='Tous',
                            clearable=False
                        )
                    ], md=4),
                    
                    dbc.Col([
                        html.Label("Filtrer par année", className="fw-bold mb-2"),
                        dcc.Dropdown(
                            id='intl-year-filter',
                            options=[{'label': str(y), 'value': y} for y in annees],
                            value=annees[-1] if annees else None,
                            clearable=False
                        ) if annees else html.Div("Aucune donnée temporelle", className="text-muted")
                    ], md=4),
                    
                    dbc.Col([
                        html.Label("Métrique à analyser", className="fw-bold mb-2"),
                        dcc.Dropdown(
                            id='intl-metric',
                            options=[
                                {'label': 'Touristes', 'value': 'Nombre de touristes'},
                                {'label': 'Nuitées', 'value': 'Nuitées touristiques'},
                                {'label': 'Durée séjour', 'value': 'Durée de séjour moyenne'}
                            ],
                            value='Nombre de touristes',
                            clearable=False
                        )
                    ], md=4)
                ])
            ])
        ], className="mb-4"),
        
        html.H4("Carte Mondiale", className="mb-3"),
        dcc.Graph(id='intl-world-map', style={'height': '500px'}, config={'displayModeBar': False}),
        html.Div(id='intl-pays-manquants', className="mb-4"),
        
        html.Hr(className="my-4"),
        
        html.H4("Liste Détaillée des Pays", className="mb-3"),
        html.Div(id='intl-table-pays', className="mb-4", style={'maxHeight': '400px', 'overflowY': 'auto'}),
        
        html.Hr(className="my-4"),
        
        html.H4("Classement Personnalisable", className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Label("Nombre de pays", className="fw-bold mb-3"),
                        dcc.Slider(
                            id='intl-top-n',
                            min=5,
                            max=50,
                            step=5,
                            value=20,
                            marks={5: '5', 10: '10', 20: '20', 30: '30', 40: '40', 50: '50'},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                        
                        html.Br(),
                        html.Label("Ordre", className="fw-bold mt-3"),
                        dcc.RadioItems(
                            id='intl-order',
                            options=[
                                {'label': ' Plus élevé en premier', 'value': 'desc'},
                                {'label': ' Plus faible en premier', 'value': 'asc'}
                            ],
                            value='desc',
                            labelStyle={'display': 'block', 'marginTop': '8px'}
                        )
                    ])
                ])
            ], md=3),
            
            dbc.Col([
                dcc.Graph(id='intl-top-chart', style={'height': '600px'}, config={'displayModeBar': False})
            ], md=9)
        ], className="mb-4"),
        
        html.Hr(className="my-4"),
        
        html.H4("Comparaison Multi-Pays", className="mb-3"),
        
        dcc.Dropdown(
            id='intl-pays-compare',
            options=[],
            multi=True,
            placeholder="Choisissez 2 à 5 pays à comparer...",
            style={'marginBottom': '20px'}
        ),
        
        dbc.Row([
            dbc.Col([
                html.H6("Graphique Radar (vue normalisée)", className="text-center mb-2"),
                dcc.Graph(id='intl-radar-chart', style={'height': '380px'}, config={'displayModeBar': False})
            ], md=6),
            
            dbc.Col([
                html.H6("Comparaison directe", className="text-center mb-2"),
                dcc.Graph(id='intl-compare-chart', style={'height': '380px'}, config={'displayModeBar': False})
            ], md=6)
        ], className="mb-4"),
        
        html.Hr(className="my-4"),
        
        html.H5("Statistiques Clés", className="mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Total Pays", className="text-muted mb-2"),
                        html.H4(id='intl-kpi-nb-pays', className="text-primary mb-0")
                    ])
                ], className="text-center")
            ], md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Total Touristes", className="text-muted mb-2"),
                        html.H4(id='intl-kpi-total', className="text-success mb-0")
                    ])
                ], className="text-center")
            ], md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("1er pays", className="text-muted mb-2"),
                        html.H4(id='intl-kpi-top', className="text-warning mb-0")
                    ])
                ], className="text-center")
            ], md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Durée moy.", className="text-muted mb-2"),
                        html.H4(id='intl-kpi-duree', className="text-info mb-0")
                    ])
                ], className="text-center")
            ], md=3)
        ])
        
    ], fluid=True)
    
    return layout

def filter_individual_countries(df):
    """Filtre pour garder uniquement les pays individuels"""
    if 'ISO3' in df.columns:
        df['ISO3_clean'] = df['ISO3'].fillna('').str.strip()
        df['ISO3_mapped'] = df.apply(
            lambda row: row['ISO3_clean'] if row['ISO3_clean'] != '' 
            else iso3_mapping.get(row['Pays'], None), 
            axis=1
        )
    else:
        df['ISO3_mapped'] = df['Pays'].map(iso3_mapping)
    
    df_filtered = df[df['ISO3_mapped'].notna()].copy()
    return df_filtered

def register_callbacks(app, df_dict):
    
    @app.callback(
        [Output('intl-world-map', 'figure'),
         Output('intl-pays-compare', 'options'),
         Output('intl-pays-manquants', 'children'),
         Output('intl-table-pays', 'children'),
         Output('intl-kpi-nb-pays', 'children'),
         Output('intl-kpi-total', 'children'),
         Output('intl-kpi-top', 'children'),
         Output('intl-kpi-duree', 'children')],
        [Input('intl-region-filter', 'value'),
         Input('intl-year-filter', 'value'),
         Input('intl-metric', 'value')]
    )
    def update_intl_map_and_kpis(region_filter, year_filter, metric):
        df_hotel = df_dict["frequentation_hoteliere"].copy()
        
        if 'Année' in df_hotel.columns:
            df_hotel['Année'] = pd.to_numeric(df_hotel['Année'], errors='coerce')
        
        df_filtered = df_hotel.copy()
        
        if region_filter != 'Tous':
            df_filtered = df_filtered[df_filtered['Region'] == region_filter]
        
        if year_filter and 'Année' in df_filtered.columns:
            df_filtered = df_filtered[df_filtered['Année'] == year_filter]
        
        df_pays_only = filter_individual_countries(df_filtered)
        
        df_pays = df_pays_only.groupby('Pays', as_index=False).agg({
            'Nombre de touristes': 'sum',
            'Nuitées touristiques': 'sum',
            'Durée de séjour moyenne': 'mean',
            'Region': 'first',
            'ISO3_mapped': 'first'
        })
        
        df_pays.rename(columns={'ISO3_mapped': 'ISO3'}, inplace=True)
        
        nb_total = len(df_pays)
        
        if not df_pays.empty:
            fig_map = px.choropleth(
                df_pays,
                locations='ISO3',
                color=metric,
                hover_name='Pays',
                hover_data={
                    'ISO3': False,
                    'Region': True,
                    'Nombre de touristes': ':,.0f',
                    'Nuitées touristiques': ':,.0f',
                    'Durée de séjour moyenne': ':.1f'
                },
                color_continuous_scale='Viridis',
                title=f"{metric} - {nb_total} pays affichés"
            )
            fig_map.update_layout(
                height=470,
                margin=dict(l=0, r=0, t=40, b=0),
                template="plotly_white",
                geo=dict(
                    showframe=True,
                    showcoastlines=True,
                    projection_type='natural earth'
                )
            )
        else:
            fig_map = go.Figure().add_annotation(
                text="Aucune donnée disponible pour ces filtres",
                showarrow=False,
                font=dict(size=14, color="gray")
            )
        
        pays_options = [{'label': p, 'value': p} for p in sorted(df_pays['Pays'].unique())]
        
        pays_manquants_info = dbc.Alert(
            f"{nb_total} pays individuels affichés (agrégations régionales exclues)",
            color="success",
            className="mb-0"
        )
        
        df_pays_sorted = df_pays.sort_values('Nombre de touristes', ascending=False)
        
        table_pays = dbc.Table([
            html.Thead([
                html.Tr([
                    html.Th("Rang"),
                    html.Th("Pays"),
                    html.Th("Région"),
                    html.Th("Touristes", className="text-end"),
                    html.Th("Nuitées", className="text-end"),
                    html.Th("Durée moy.", className="text-end"),
                    html.Th("ISO3", className="text-center")
                ])
            ]),
            html.Tbody([
                html.Tr([
                    html.Td(f"#{i+1}"),
                    html.Td(row['Pays']),
                    html.Td(row['Region']),
                    html.Td(f"{row['Nombre de touristes']:,.0f}", className="text-end"),
                    html.Td(f"{row['Nuitées touristiques']:,.0f}", className="text-end"),
                    html.Td(f"{row['Durée de séjour moyenne']:.1f}j", className="text-end"),
                    html.Td(str(row['ISO3']), className="text-center text-success")
                ]) for i, (_, row) in enumerate(df_pays_sorted.head(100).iterrows())
            ])
        ], bordered=True, hover=True, responsive=True, striped=True, size="sm")
        
        nb_pays_kpi = f"{nb_total}"
        total = f"{df_pays_only['Nombre de touristes'].sum()/1000:.1f}M"
        top_pays = df_pays.loc[df_pays['Nombre de touristes'].idxmax(), 'Pays'] if not df_pays.empty else "N/A"
        duree_moy = f"{df_pays_only['Durée de séjour moyenne'].mean():.1f}j"
        
        return fig_map, pays_options, pays_manquants_info, table_pays, nb_pays_kpi, total, top_pays, duree_moy
    
    @app.callback(
        Output('intl-top-chart', 'figure'),
        [Input('intl-region-filter', 'value'),
         Input('intl-year-filter', 'value'),
         Input('intl-metric', 'value'),
         Input('intl-top-n', 'value'),
         Input('intl-order', 'value')]
    )
    def update_top_chart(region_filter, year_filter, metric, top_n, order):
        df_hotel = df_dict["frequentation_hoteliere"].copy()
        
        if 'Année' in df_hotel.columns:
            df_hotel['Année'] = pd.to_numeric(df_hotel['Année'], errors='coerce')
        
        df_filtered = df_hotel.copy()
        if region_filter != 'Tous':
            df_filtered = df_filtered[df_filtered['Region'] == region_filter]
        if year_filter and 'Année' in df_filtered.columns:
            df_filtered = df_filtered[df_filtered['Année'] == year_filter]
        
        df_pays_only = filter_individual_countries(df_filtered)
        
        df_pays = df_pays_only.groupby('Pays', as_index=False).agg({
            'Nombre de touristes': 'sum',
            'Nuitées touristiques': 'sum',
            'Durée de séjour moyenne': 'mean'
        })
        
        if order == 'desc':
            df_top = df_pays.nlargest(top_n, metric).sort_values(metric, ascending=True)
        else:
            df_top = df_pays.nsmallest(top_n, metric).sort_values(metric, ascending=False)
        
        fig = px.bar(
            df_top,
            x=metric,
            y='Pays',
            orientation='h',
            color=metric,
            color_continuous_scale='Teal',
            text=metric
        )
        
        fig.update_traces(
            texttemplate='%{text:,.0f}' if metric != "Durée de séjour moyenne" else '%{text:.1f}j',
            textposition='outside'
        )
        
        hauteur = max(400, top_n * 25)
        
        fig.update_layout(
            showlegend=False,
            height=hauteur,
            margin=dict(l=0, r=100, t=20, b=30),
            yaxis={'fixedrange': True},
            xaxis={'fixedrange': True},
            template="plotly_white",
            xaxis_title="",
            yaxis_title=""
        )
        
        return fig
    
    @app.callback(
        [Output('intl-radar-chart', 'figure'),
         Output('intl-compare-chart', 'figure')],
        [Input('intl-pays-compare', 'value'),
         Input('intl-region-filter', 'value'),
         Input('intl-year-filter', 'value')]
    )
    def update_comparison(pays_selected, region_filter, year_filter):
        if not pays_selected:
            empty_fig = go.Figure().add_annotation(
                text="Sélectionnez 2 à 5 pays ci-dessus",
                showarrow=False,
                font=dict(size=14, color="gray")
            )
            return empty_fig, empty_fig
        
        df_hotel = df_dict["frequentation_hoteliere"].copy()
        
        if 'Année' in df_hotel.columns:
            df_hotel['Année'] = pd.to_numeric(df_hotel['Année'], errors='coerce')
        
        df_filtered = df_hotel.copy()
        if region_filter != 'Tous':
            df_filtered = df_filtered[df_filtered['Region'] == region_filter]
        if year_filter and 'Année' in df_filtered.columns:
            df_filtered = df_filtered[df_filtered['Année'] == year_filter]
        
        df_pays_only = filter_individual_countries(df_filtered)
        df_compare = df_pays_only[df_pays_only['Pays'].isin(pays_selected)]
        
        df_compare_agg = df_compare.groupby('Pays', as_index=False).agg({
            'Nombre de touristes': 'sum',
            'Nuitées touristiques': 'sum',
            'Durée de séjour moyenne': 'mean'
        })
        
        fig_radar = go.Figure()
        
        metrics_radar = ['Touristes', 'Nuitées', 'Durée séjour']
        
        for _, row in df_compare_agg.iterrows():
            max_t = df_compare_agg['Nombre de touristes'].max()
            max_n = df_compare_agg['Nuitées touristiques'].max()
            max_d = df_compare_agg['Durée de séjour moyenne'].max()
            
            values = [
                row['Nombre de touristes'] / max_t * 100 if max_t > 0 else 0,
                row['Nuitées touristiques'] / max_n * 100 if max_n > 0 else 0,
                row['Durée de séjour moyenne'] / max_d * 100 if max_d > 0 else 0
            ]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=metrics_radar + [metrics_radar[0]],
                fill='toself',
                name=row['Pays']
            ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            height=350,
            margin=dict(l=0, r=0, t=0, b=0),
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        
        fig_compare = go.Figure()
        
        fig_compare.add_trace(go.Bar(
            name='Touristes',
            x=df_compare_agg['Pays'],
            y=df_compare_agg['Nombre de touristes'],
            marker_color='#2E86AB'
        ))
        
        fig_compare.add_trace(go.Bar(
            name='Nuitées',
            x=df_compare_agg['Pays'],
            y=df_compare_agg['Nuitées touristiques'],
            marker_color='#A23B72'
        ))
        
        fig_compare.update_layout(
            barmode='group',
            height=350,
            margin=dict(l=0, r=0, t=0, b=40),
            yaxis={'fixedrange': True},
            xaxis={'fixedrange': True},
            template="plotly_white",
            xaxis_title="",
            yaxis_title="Milliers",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        
        return fig_radar, fig_compare