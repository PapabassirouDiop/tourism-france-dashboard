# src/layouts/home_layout.py
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_layout(df_dict):
    """Page d'accueil avec vue d'ensemble du tourisme international en France"""
    
    df_region = df_dict["frequentation_region"].copy()
    
    if 'Mois' in df_region.columns:
        df_region['Mois'] = pd.to_datetime(df_region['Mois'], errors='coerce')
    
    total_touristes = df_region['Nombre de touristes'].sum()
    total_nuitees = df_region['Nuitées touristiques'].sum()
    duree_moyenne = df_region['Durée de séjour moyenne'].mean()
    nb_pays = df_region['Pays'].nunique()
    nb_regions = df_region['Region'].nunique()
    
    df_region_agg = df_region.groupby('Region', as_index=False).agg({
        'Nombre de touristes': 'sum'
    }).sort_values('Nombre de touristes', ascending=False)
    
    fig_regions = px.bar(
        df_region_agg,
        x='Nombre de touristes',
        y='Region',
        orientation='h',
        color='Nombre de touristes',
        color_continuous_scale='Blues',
        text='Nombre de touristes',
        title="Répartition par région d'origine"
    )
    fig_regions.update_traces(texttemplate='%{text:,.0f}k', textposition='outside')
    fig_regions.update_layout(
        showlegend=False, 
        height=400,
        xaxis_title="Nombre de touristes (milliers)",
        yaxis_title="",
        template="plotly_white"
    )
    
    df_pays = df_region.groupby('Pays', as_index=False).agg({
        'Nombre de touristes': 'sum'
    })
    df_top10 = df_pays.nlargest(10, 'Nombre de touristes')
    
    fig_top10 = px.bar(
        df_top10.sort_values('Nombre de touristes', ascending=True),
        x='Nombre de touristes',
        y='Pays',
        orientation='h',
        color='Nombre de touristes',
        color_continuous_scale='Oranges',
        text='Nombre de touristes',
        title="Top 10 des pays émetteurs"
    )
    fig_top10.update_traces(texttemplate='%{text:,.0f}k', textposition='outside')
    fig_top10.update_layout(
        showlegend=False, 
        height=400,
        xaxis_title="Nombre de touristes (milliers)",
        yaxis_title="",
        template="plotly_white"
    )
    
    fig_evolution = None
    if 'Mois' in df_region.columns:
        df_monthly = df_region.groupby('Mois', as_index=False).agg({
            'Nombre de touristes': 'sum'
        })
        
        fig_evolution = go.Figure()
        fig_evolution.add_trace(go.Scatter(
            x=df_monthly['Mois'],
            y=df_monthly['Nombre de touristes'],
            mode='lines+markers',
            name='Touristes',
            line=dict(color='#2E86AB', width=3),
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor='rgba(46, 134, 171, 0.1)'
        ))
        fig_evolution.update_layout(
            title="Évolution mensuelle des arrivées",
            xaxis_title="",
            yaxis_title="Touristes (milliers)",
            hovermode='x unified',
            height=400,
            template="plotly_white"
        )
    
    layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2(" Tourisme International en France", className="text-center mb-3"),
                html.P("Analyse des flux touristiques et de leur impact économique", 
                       className="text-center text-muted mb-4")
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5(" Objectif", className="card-title"),
                        html.P([
                            "Ce dashboard analyse le tourisme international en France pour éclairer ",
                            "les décideurs publics et les acteurs économiques sur l'origine géographique ",
                            "des touristes, l'évolution des flux et leur impact économique."
                        ], className="mb-0")
                    ])
                ], className="mb-4")
            ])
        ]),
        
        html.H4(" Indicateurs Clés", className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(" Touristes", className="text-muted mb-2"),
                        html.H3(f"{total_touristes/1000:.1f}M", className="text-primary mb-0")
                    ])
                ], className="text-center")
            ], width=12, md=2),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(" Nuitées", className="text-muted mb-2"),
                        html.H3(f"{total_nuitees/1000:.1f}M", className="text-success mb-0")
                    ])
                ], className="text-center")
            ], width=12, md=2),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(" Séjour moyen", className="text-muted mb-2"),
                        html.H3(f"{duree_moyenne:.1f}j", className="text-info mb-0")
                    ])
                ], className="text-center")
            ], width=12, md=2),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(" Pays", className="text-muted mb-2"),
                        html.H3(f"{nb_pays}", className="text-warning mb-0")
                    ])
                ], className="text-center")
            ], width=12, md=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(" Régions", className="text-muted mb-2"),
                        html.H3(f"{nb_regions}", className="text-danger mb-0")
                    ])
                ], className="text-center")
            ], width=12, md=3)
        ], className="mb-4"),
        
        html.Hr(className="my-4"),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_regions)
            ], width=12, md=6),
            
            dbc.Col([
                dcc.Graph(figure=fig_top10)
            ], width=12, md=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_evolution) if fig_evolution else html.Div("Données temporelles non disponibles", className="text-muted text-center p-4")
            ])
        ], className="mb-4"),
        
        html.Hr(className="my-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5(" Analyse géographique", className="card-title"),
                        html.Ul([
                            html.Li("D'où viennent les touristes ?"),
                            html.Li("Quelle est la répartition par continent ?"),
                            html.Li("Quels sont les marchés émergents ?")
                        ], className="mb-0")
                    ])
                ], className="h-100")
            ], width=12, md=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5(" Impact économique", className="card-title"),
                        html.Ul([
                            html.Li("Quel volume de nuitées générées ?"),
                            html.Li("Quelle durée moyenne par marché ?"),
                            html.Li("Quels touristes restent le plus longtemps ?")
                        ], className="mb-0")
                    ])
                ], className="h-100")
            ], width=12, md=6)
        ], className="mb-4"),
        
        dbc.Alert([
            html.Strong(" Conseil : "),
            "Utilisez les onglets ci-dessus pour explorer les analyses détaillées par région, par pays, et l'impact économique."
        ], color="info", className="mb-0")
        
    ], fluid=True)
    
    return layout