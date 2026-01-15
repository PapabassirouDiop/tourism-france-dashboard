# src/layouts/economic_layout.py
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_layout(df_dict):
    """
    Crée le layout de la page économique
    """
    df_region = df_dict["frequentation_region"]
    
    # Options régions
    regions_dispo = ['Tous'] + sorted(df_region['Region'].unique().tolist())
    
    layout = dbc.Container([
        html.H2(" Impact Économique du Tourisme", className="text-center mb-4"),
        html.P("Analyse des retombées économiques : nuitées, durée de séjour, intensité", 
               className="text-center text-muted mb-4"),
        
        # Filtres
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5(" Filtres", className="card-title"),
                        
                        dbc.Row([
                            dbc.Col([
                                html.Label(" Région d'origine", className="fw-bold"),
                                dcc.Dropdown(
                                    id='eco-region-filter',
                                    options=[{'label': r, 'value': r} for r in regions_dispo],
                                    value='Tous',
                                    clearable=False,
                                    style={'minWidth': '250px'}
                                )
                            ], width=12, md=4),
                            
                            dbc.Col([
                                dbc.Alert([
                                    html.I(className="bi bi-info-circle me-2"),
                                    "Sélectionnez une région pour filtrer l'analyse économique"
                                ], color="light", className="mb-0 py-2")
                            ], width=12, md=8)
                        ])
                    ])
                ])
            ], width=12, className="mb-4")
        ]),
        
        # KPIs économiques
        html.H4(" Indicateurs Économiques Clés", className="mt-4 mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(" Nuitées Totales"),
                        html.H4(id='eco-kpi-nuitees', className="text-primary")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(" Touristes"),
                        html.H4(id='eco-kpi-touristes', className="text-success")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(" Séjour Moyen"),
                        html.H4(id='eco-kpi-duree', className="text-info")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(" Intensité"),
                        html.H4(id='eco-kpi-intensite', className="text-warning")
                    ])
                ])
            ], width=3)
        ], className="mb-4"),
        
        # Graphique intensité
        html.H4(" Rentabilité Économique par Région", className="mt-4 mb-3"),
        dbc.Alert([
            html.Strong("L'intensité économique"),
            " mesure le nombre de nuitées générées par touriste. Plus ce ratio est élevé, plus l'impact économique est important."
        ], color="info", className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='eco-intensity-chart')
            ])
        ], className="mb-4"),
        
        # Scatter plot
        html.H4(" Volume vs Qualité du Séjour", className="mt-4 mb-3"),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='eco-scatter-chart')
            ], width=12, md=8),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(" Interprétation", className="card-title"),
                        html.P([
                            html.Strong("Quadrant sup. droit 🟢"), html.Br(),
                            "→ Volume ET durée élevés", html.Br(),
                            "→ Marchés à fort potentiel", html.Br(), html.Br(),
                            
                            html.Strong("Quadrant sup. gauche 🟡"), html.Br(),
                            "→ Faible volume mais longue durée", html.Br(),
                            "→ Marchés de niche à développer", html.Br(), html.Br(),
                            
                            html.Strong("Quadrant inf. droit 🟠"), html.Br(),
                            "→ Volume élevé mais courte durée", html.Br(),
                            "→ Optimiser la durée de séjour", html.Br(), html.Br(),
                            
                            html.Strong("Quadrant inf. gauche 🔴"), html.Br(),
                            "→ Faible volume ET courte durée", html.Br(),
                            "→ Marchés à faible priorité"
                        ], style={'fontSize': '0.85rem'})
                    ])
                ])
            ], width=12, md=4)
        ], className="mb-4"),
        
        # Évolution économique
        html.H4(" Évolution de l'Impact Économique", className="mt-4 mb-3"),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='eco-evolution-chart')
            ])
        ], className="mb-4"),
        
        # Classement
        html.H4(" Classement par Impact Économique", className="mt-4 mb-3"),
        dbc.Row([
            dbc.Col([
                html.Label("Critère de classement"),
                dcc.RadioItems(
                    id='eco-critere',
                    options=[
                        {'label': ' Nuitées totales', 'value': 'Nuitées touristiques'},
                        {'label': ' Intensité économique', 'value': 'Intensité économique'},
                        {'label': ' Durée de séjour', 'value': 'Durée de séjour moyenne'}
                    ],
                    value='Nuitées touristiques',
                    inline=True,
                    className='mb-3'
                ),
                
                html.Label("Nombre de pays"),
                dcc.Slider(
                    id='eco-top-n',
                    min=5,
                    max=20,
                    step=5,
                    value=10,
                    marks={i: str(i) for i in range(5, 25, 5)}
                )
            ], width=12, md=3),
            
            dbc.Col([
                dcc.Graph(id='eco-ranking-chart')
            ], width=12, md=9)
        ], className="mb-4"),
        
        # Comparaison
        html.H4("⚖️ Analyse Comparative", className="mt-4 mb-3"),
        html.P("Comparez l'impact économique de différents marchés", className="text-muted"),
        
        dbc.Row([
            dbc.Col([
                html.Label("Sélectionnez des pays à comparer"),
                dcc.Dropdown(
                    id='eco-pays-compare',
                    options=[],
                    multi=True,
                    placeholder="Choisir des pays..."
                )
            ])
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='eco-compare-chart')
            ])
        ], className="mb-4"),
        
        # Insights stratégiques
        html.H4(" Insights Stratégiques", className="mt-4 mb-3"),
        dbc.Row([
            dbc.Col([
                html.Div(id='eco-insights-high')
            ], width=12, md=6),
            
            dbc.Col([
                html.Div(id='eco-insights-low')
            ], width=12, md=6)
        ], className="mb-4")
        
    ], fluid=True)
    
    return layout

def register_callbacks(app, df_dict):
    """
    Enregistre les callbacks pour l'interactivité
    """
    
    @app.callback(
        [Output('eco-kpi-nuitees', 'children'),
         Output('eco-kpi-touristes', 'children'),
         Output('eco-kpi-duree', 'children'),
         Output('eco-kpi-intensite', 'children'),
         Output('eco-intensity-chart', 'figure'),
         Output('eco-pays-compare', 'options')],
        [Input('eco-region-filter', 'value')]
    )
    def update_eco_kpis_and_intensity(region_filter):
        df_hotel = df_dict["frequentation_hoteliere"].copy()
        
        # Filtrage
        if region_filter != 'Tous':
            df_filtered = df_hotel[df_hotel['Region'] == region_filter]
        else:
            df_filtered = df_hotel
        
        # KPIs
        total_nuitees = df_filtered['Nuitées touristiques'].sum()
        total_touristes = df_filtered['Nombre de touristes'].sum()
        duree_moy = df_filtered['Durée de séjour moyenne'].mean()
        intensite = total_nuitees / total_touristes if total_touristes > 0 else 0
        
        kpi_nuitees = f"{total_nuitees/1000:.1f}M"
        kpi_touristes = f"{total_touristes/1000:.1f}M"
        kpi_duree = f"{duree_moy:.1f} j"
        kpi_intensite = f"{intensite:.1f}"
        
        # Graphique intensité PAR RÉGION (vue macro)
        df_region = df_dict["frequentation_region"].copy()
        if region_filter != 'Tous':
            df_region = df_region[df_region['Region'] == region_filter]
        
        df_ratio = df_region.groupby('Region', as_index=False).agg({
            'Nombre de touristes': 'sum',
            'Nuitées touristiques': 'sum',
            'Durée de séjour moyenne': 'mean'
        })
        
        df_ratio['Intensité économique'] = df_ratio['Nuitées touristiques'] / df_ratio['Nombre de touristes']
        df_ratio = df_ratio.sort_values('Intensité économique', ascending=False)
        
        fig_intensity = px.bar(
            df_ratio,
            x='Intensité économique',
            y='Region',
            orientation='h',
            color='Intensité économique',
            color_continuous_scale='RdYlGn',
            text='Intensité économique',
            title="Intensité économique par région (nuitées/touriste)"
        )
        
        fig_intensity.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_intensity.update_layout(showlegend=False, height=400)
        
        # Options pays depuis frequentation_hoteliere
        pays_options = [{'label': p, 'value': p} for p in sorted(df_filtered['Pays'].unique())]
        
        return kpi_nuitees, kpi_touristes, kpi_duree, kpi_intensite, fig_intensity, pays_options
    
    @app.callback(
        Output('eco-scatter-chart', 'figure'),
        [Input('eco-region-filter', 'value')]
    )
    def update_scatter(region_filter):
        df_hotel = df_dict["frequentation_hoteliere"].copy()
        
        if region_filter != 'Tous':
            df_filtered = df_hotel[df_hotel['Region'] == region_filter]
        else:
            df_filtered = df_hotel
        
        # Agrégation par pays
        df_scatter = df_filtered.groupby('Pays', as_index=False).agg({
            'Nombre de touristes': 'sum',
            'Durée de séjour moyenne': 'mean',
            'Nuitées touristiques': 'sum',
            'Region': 'first'
        })
        
        # Top 20 pour lisibilité
        df_scatter = df_scatter.nlargest(20, 'Nombre de touristes')
        
        fig_scatter = px.scatter(
            df_scatter,
            x='Nombre de touristes',
            y='Durée de séjour moyenne',
            size='Nuitées touristiques',
            color='Region',
            hover_name='Pays',
            title="Volume de touristes vs Durée moyenne de séjour (Top 20 pays)"
        )
        
        # Lignes de référence
        median_t = df_scatter['Nombre de touristes'].median()
        median_d = df_scatter['Durée de séjour moyenne'].median()
        
        fig_scatter.add_hline(y=median_d, line_dash="dash", line_color="gray")
        fig_scatter.add_vline(x=median_t, line_dash="dash", line_color="gray")
        
        fig_scatter.update_layout(height=500)
        
        return fig_scatter
    
    @app.callback(
        Output('eco-evolution-chart', 'figure'),
        [Input('eco-region-filter', 'value')]
    )
    def update_evolution(region_filter):
        df_region = df_dict["frequentation_region"].copy()
        
        if 'Mois' in df_region.columns:
            df_region['Mois'] = pd.to_datetime(df_region['Mois'])
        
        if region_filter != 'Tous':
            df_filtered = df_region[df_region['Region'] == region_filter]
        else:
            df_filtered = df_region
        
        # Agrégation mensuelle
        df_monthly = df_filtered.groupby('Mois', as_index=False).agg({
            'Nombre de touristes': 'sum',
            'Nuitées touristiques': 'sum'
        })
        
        df_monthly['Intensité'] = df_monthly['Nuitées touristiques'] / df_monthly['Nombre de touristes']
        
        # Graphique double axe
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_monthly['Mois'],
            y=df_monthly['Nuitées touristiques'],
            name='Nuitées',
            marker_color='lightblue',
            yaxis='y'
        ))
        
        fig.add_trace(go.Scatter(
            x=df_monthly['Mois'],
            y=df_monthly['Intensité'],
            name='Intensité économique',
            line=dict(color='red', width=3),
            mode='lines+markers',
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Évolution des nuitées et de l'intensité économique",
            xaxis_title="Mois",
            yaxis=dict(title="Nuitées (milliers)", side='left'),
            yaxis2=dict(title="Intensité (nuitées/touriste)", side='right', overlaying='y'),
            hovermode='x unified',
            height=400
        )
        
        return fig
    
    @app.callback(
        Output('eco-ranking-chart', 'figure'),
        [Input('eco-region-filter', 'value'),
         Input('eco-critere', 'value'),
         Input('eco-top-n', 'value')]
    )
    def update_ranking(region_filter, critere, top_n):
        df_hotel = df_dict["frequentation_hoteliere"].copy()
        
        if region_filter != 'Tous':
            df_filtered = df_hotel[df_hotel['Region'] == region_filter]
        else:
            df_filtered = df_hotel
        
        # Agrégation par pays
        df_classement = df_filtered.groupby('Pays', as_index=False).agg({
            'Nombre de touristes': 'sum',
            'Nuitées touristiques': 'sum',
            'Durée de séjour moyenne': 'mean'
        })
        
        df_classement['Intensité économique'] = (
            df_classement['Nuitées touristiques'] / df_classement['Nombre de touristes']
        )
        
        df_top = df_classement.nlargest(top_n, critere)
        df_top = df_top.sort_values(critere, ascending=True)
        
        fig = px.bar(
            df_top,
            x=critere,
            y='Pays',
            orientation='h',
            color=critere,
            color_continuous_scale='Viridis',
            text=critere,
            title=f"Top {top_n} pays - {critere}"
        )
        
        fig.update_traces(texttemplate='%{text:,.1f}', textposition='outside')
        fig.update_layout(showlegend=False, height=450)
        
        return fig
    
    @app.callback(
        Output('eco-compare-chart', 'figure'),
        [Input('eco-pays-compare', 'value'),
         Input('eco-region-filter', 'value')]
    )
    def update_comparison(pays_selected, region_filter):
        if not pays_selected:
            return go.Figure().add_annotation(text="Sélectionnez des pays", showarrow=False)
        
        df_hotel = df_dict["frequentation_hoteliere"].copy()
        
        if region_filter != 'Tous':
            df_filtered = df_hotel[df_hotel['Region'] == region_filter]
        else:
            df_filtered = df_hotel
        
        df_compare = df_filtered[df_filtered['Pays'].isin(pays_selected)]
        
        df_compare_agg = df_compare.groupby('Pays', as_index=False).agg({
            'Nombre de touristes': 'sum',
            'Nuitées touristiques': 'sum'
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Touristes (milliers)',
            x=df_compare_agg['Pays'],
            y=df_compare_agg['Nombre de touristes'],
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name='Nuitées (milliers)',
            x=df_compare_agg['Pays'],
            y=df_compare_agg['Nuitées touristiques'],
            marker_color='lightcoral'
        ))
        
        fig.update_layout(
            barmode='group',
            title="Comparaison : Touristes vs Nuitées",
            height=400
        )
        
        return fig
    
    @app.callback(
        [Output('eco-insights-high', 'children'),
         Output('eco-insights-low', 'children')],
        [Input('eco-region-filter', 'value')]
    )
    def update_insights(region_filter):
        df_hotel = df_dict["frequentation_hoteliere"].copy()
        
        if region_filter != 'Tous':
            df_filtered = df_hotel[df_hotel['Region'] == region_filter]
        else:
            df_filtered = df_hotel
        
        # Filtrer les agrégations régionales
        agregations = ['Autre Asie', 'Autre Amérique du Sud', 'Autre Amérique Centrale', 
                      'Europe (hors France)', 'Asie', 'Pacifique', 'Afrique', 
                      'Amérique du Sud', 'Amérique Centrale', 'Autres Pays']
        df_filtered = df_filtered[~df_filtered['Pays'].isin(agregations)]
        
        df_classement = df_filtered.groupby('Pays', as_index=False).agg({
            'Nombre de touristes': 'sum',
            'Nuitées touristiques': 'sum',
            'Durée de séjour moyenne': 'mean'
        })
        
        df_classement['Intensité économique'] = (
            df_classement['Nuitées touristiques'] / df_classement['Nombre de touristes']
        )
        
        # Top intensité
        df_top_intensite = df_classement.nlargest(3, 'Intensité économique')
        
        insight_high = dbc.Alert([
            html.H5(" Marchés à forte intensité économique", className="alert-heading"),
            html.P("Ces pays génèrent le plus de nuitées par touriste :"),
            html.Ul([
                html.Li(f"{row['Pays']} : {row['Intensité économique']:.1f} nuitées/touriste")
                for _, row in df_top_intensite.iterrows()
            ]),
            html.P("→ Priorité : fidéliser ces marchés", className="mb-0")
        ], color="success")
        
        # Faible durée mais volume élevé
        df_faible_duree = df_classement[
            df_classement['Nombre de touristes'] > df_classement['Nombre de touristes'].median()
        ].nsmallest(3, 'Durée de séjour moyenne')
        
        if not df_faible_duree.empty:
            insight_low = dbc.Alert([
                html.H5(" Marchés à potentiel d'amélioration", className="alert-heading"),
                html.P("Ces marchés ont du volume mais une courte durée :"),
                html.Ul([
                    html.Li(f"{row['Pays']} : {row['Durée de séjour moyenne']:.1f} jours")
                    for _, row in df_faible_duree.iterrows()
                ]),
                html.P("→ Opportunité : allonger les séjours", className="mb-0")
            ], color="warning")
        else:
            insight_low = html.Div()
        
        return insight_high, insight_low