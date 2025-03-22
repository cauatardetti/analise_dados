import pandas as pd
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
import matplotlib.pyplot as plt
import seaborn as sns
import dash
from dash import dcc, html
import plotly.express as px
import dash_labs as dl
import plotly.graph_objects as go


ACCESS_TOKEN = 'EAB3ZBJEYSgY8BOZBVFOV7MZAcdpeeSCvlnw9XZBlByKVvLQDMXrd7unCZC9pGB9BW5IjVTzhLhkTcdqXg7nJkdrpbMkcFjqPJObZB0FuI1s66XiKEnG9T3mJtdusFZCTXX8zrilyjit6aNZCZB3yXCRWmVsjZANwwUxC8qPvG2ntEe4TSVLyq2f1kW4H3M'
AD_ACCOUNT_ID = 'act_1573818712988395'

FacebookAdsApi.init(access_token=ACCESS_TOKEN)

fields = {
    'impressions',
    'clicks',
    'ctr',
    'actions',
    'date_start',
}

params = {
    'time_range': {'since': '2024-10-01', 'until': '2025-02-24'},
    'level': 'campaign',
    'breakdowns': ['age', 'gender'],
    'limit': 10000,
    'time_increment': 1,
}

ad_account = AdAccount(AD_ACCOUNT_ID)
ads = ad_account.get_insights(fields=fields, params=params)

data = []

for ad in ads:
    if 'actions' in ad:
        leads = sum(int(action['value']) for action in ad['actions'] if action['action_type'] == 'lead')
    
    else:
        leads = 0
    
    data.append({
        'impressions': ad.get('impressions', 0),
        'clicks': ad.get('clicks', 0),
        'ctr': ad.get('ctr', 0),
        'leads': leads,
        'date_start': ad.get('date_start'),
        'gender': ad.get('gender'),
        'age': ad.get('age')
    })
df = pd.DataFrame(data)

df['impressions'] = pd.to_numeric(df['impressions'], errors='coerce')
df['clicks'] = pd.to_numeric(df['clicks'], errors='coerce')
df['ctr'] = pd.to_numeric(df['ctr'], errors='coerce')
df['leads'] = pd.to_numeric(df['leads'], errors='coerce')

df['date_start'] = pd.to_datetime(df['date_start'], format='%Y-%m-%d')

fig_line = go.Figure()

fig_line.add_trace(
    go.Scatter(
        x=df['date_start'], y=df['leads'],
        mode='lines+markers',
        line=dict(color='#00CC96', width=1, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(0, 204, 150, 0.2)',
    )
)

fig_line.update_layout(
    title='Crescimento de Ads ao Longo do Tempo',
    title_font=dict(size=20, color='white'),
    xaxis=dict(
        showgrid=True, 
        title='Data',
        tickformat='%d/%m',
        tickfont=dict(color='white'),
        gridcolor="#283747"
    ),
    yaxis=dict(
        title='Valor',
        tickfont=dict(color='white'),
        gridcolor="#283747"
    ),
    plot_bgcolor='#192734',  # Fundo escuro
    paper_bgcolor='#192734',
    font=dict(color='white'),
    hovermode='x unified',
    margin=dict(l=40, r=40, t=40, b=40)
)

fig_barra = go.Figure()

gender_colors = {'female': 'rgb(255, 0, 128)', 'male': 'rgb(0, 30, 255)', 'unknown': 'rgb(255, 215, 0)'}

for gender in df['gender'].unique():
    df_gender = df[df['gender'] == gender]

    fig_barra.add_trace(go.Histogram(
        x=df_gender['age'],
        y=df_gender['clicks'],
        marker_color=gender_colors[gender],
        name=gender,
        marker=dict(
            colorscale='viridis',
            line=dict(color='white', width=1)
        ),
        text=df_gender['clicks'],
        textposition='outside'
    ))

fig_barra.update_layout(
    barmode='group',
    plot_bgcolor="#192734", 
    paper_bgcolor="#192734",
    font=dict(color="white"),
    title="Cliques por Idade e Gênero",
    xaxis=dict(showgrid=False, gridcolor="#283747"),
    yaxis=dict(gridcolor="#283747"),
    xaxis_title="Idade",
    yaxis_title="Cliques",
)



app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('Dashboard de Desempenho Meta Ads Famex', style={'textAlign': 'center', 'color': 'white', "fontFamily": "Roboto"}),
    
    html.Div(
        children=[
           
            dcc.Graph(figure=fig_line),
            dcc.Graph(figure=fig_barra),
        ],
        style={
            'display': 'flex',
            'flexDirection': 'column',
            'gap': '20px',
            'justifyContent': 'center',
            'background': '#0c1830',
            'padding': '20px'
        }
    )
], style={'background': '#0c1830', 'padding': '20px'})



if __name__ == '__main__':
    app.run_server(debug=True)