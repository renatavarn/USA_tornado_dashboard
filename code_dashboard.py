from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

tornadoes = pd.read_csv('data.csv')

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1('Tornadoes in the USA, 1954 - 2013',
            style={'textAlign': 'left',
                   'fontFamily': 'Avenir',
                   'fontSize': 40,
                   'color': 'white'}),
    html.Label('State: ', style={'textAlign': 'left',
                                 'fontFamily': 'Avenir',
                                 'fontSize': 25,
                                 'color': 'white'}),
    dcc.Dropdown(id='state-dropdown',
                 options=[{'label': i, 'value': i} for i in tornadoes.ST.unique()],
                 value='TX',
                 style={'backgroundColor': '#111111', 'borderColor': 'gray'}),
    dbc.Row([
        dbc.Col(dcc.Graph(id='Yearly', figure={}), width=6),
        dbc.Col(dcc.Graph(id='Fat_Inj', figure={}), width=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='Mag', figure={}), width=6),
        dbc.Col(dcc.Graph(id='Tornado map', figure={}), width=6),
    ]),
], style={'backgroundColor': '#111111', 'border': 'thin lightgrey', 'padding': '8px 0px 0px 8px'}
)


####### YEARLY INCIDENCE GRAPH ########

@app.callback(
    Output('Yearly', 'figure'),
    Input('state-dropdown', 'value')
)
def update_graph1(selected_state):
    df_state = tornadoes[tornadoes.ST == selected_state]
    yearly_tx = df_state.groupby('YR')[['MO']].size().reset_index(name='No. of tornadoes')
    yearly_fig = px.area(yearly_tx, x="YR", y='No. of tornadoes', template="plotly_dark", width=700, height=400)
    yearly_fig.update_layout(
        title=f"Yearly incidence in {selected_state} state",
        xaxis_title="Year", yaxis_title='No. of tornadoes',
        xaxis=dict(title_font=dict(size=16), tickfont=dict(size=14)),
        yaxis=dict(title_font=dict(size=16), tickfont=dict(size=14)))
    return yearly_fig


####### INJURIES AND FATALITIES GRAPH ########

@app.callback(
    Output('Fat_Inj', 'figure'),
    Input('state-dropdown', 'value')
)
def update_graph2(selected_state):
    df_state = tornadoes[tornadoes.ST == selected_state]
    fat_inj = df_state.groupby('YR')[['INJ', 'FAT']].sum()
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=fat_inj.index, y=fat_inj['FAT'], fill='tonexty', name='Fatalities',
                             fillcolor="#e74c3c", line=dict(color='#e74c3c', width=2)))
    fig.add_trace(go.Scatter(x=fat_inj.index, y=fat_inj['INJ'], fill='tonexty', name='Injuries',
                             fillcolor="#9b59b6", line=dict(color='#9b59b6', width=2)))

    fig.update_layout(title=f"Yearly injuries and fatalities in {selected_state} state",
                      template='plotly_dark', width=700, height=400,
                      xaxis_title="Year", yaxis_title="No. of injuries/fatalities",
                      xaxis=dict(title_font=dict(size=16), tickfont=dict(size=14)),
                      yaxis=dict(title_font=dict(size=16), tickfont=dict(size=14)))
    return fig


####### PROPORTION OF MAGNITUDE OF TORNADOES ########


@app.callback(
    Output('Mag', 'figure'),
    Input('state-dropdown', 'value')
)
def update_graph3(selected_state):
    df_state = tornadoes[tornadoes.ST == selected_state]
    mag_count = df_state['MAG'].value_counts().reset_index()
    mag_count.columns = ['MAG', 'Counts']
    mag_count.set_index('MAG', inplace=True)
    mag_count['Normalized'] = mag_count.apply(lambda col: ((col['Counts'] / mag_count.Counts.sum()) * 100).round(2),
                                              axis=1)
    pie_chart = px.pie(mag_count, values='Normalized', names=mag_count.index, hole=.3, template="plotly_dark",
                       width=700, height=400, color_discrete_sequence=px.colors.sequential.Plasma,
                       title=f"Relative magnitude of tornadoes in {selected_state} state")
    pie_chart.update_layout(
        legend_font=dict(size=14))
    return pie_chart


####### MAP OF TORNADOES FOR EACH STATE ########

@app.callback(
    Output('Tornado map', 'figure'),
    Input('state-dropdown', 'value')
)
def update_graph4(selected_state):
    maps = px.scatter_geo(tornadoes[tornadoes.ST == selected_state],
                          lat="SLAT",
                          lon="SLON",
                          # title=f"Tornadoes in {selected_state} state",
                          template="plotly_dark",
                          size="MAG",
                          size_max=10,
                          color="INJ",
                          animation_frame='YR',
                          width=700,
                          height=400,
                          range_color=[tornadoes['INJ'].min(), tornadoes['INJ'].max()],
                          labels={'MAG': 'Magnitude',
                                  'FAT': 'Fatalities',
                                  'INJ': 'Injuries',
                                  'YR': 'Year'
                                  })
    maps.update_layout(
        title=f"Geospatial incidence in {selected_state} state",
        geo_scope='usa',
        showlegend=True
    )
    maps.update_geos(visible=True, resolution=50)
    return maps


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

