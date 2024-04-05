import dash
from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.express as px
import numpy as np

df = pd.read_csv(r"C:\Users\Usmaan\OneDrive - National Institute of Business Management\Documents\dashboard\Dashboard_Final\Dataset\cleaned_dash.csv")
lbl = ['', 'January', 'February', 'March']
T3 = df.groupby(['month', 'date', 'day']).agg(count=pd.NamedAgg('day','count'),
                                                        actual=pd.NamedAgg('actual_productivity', 'sum'),target=pd.NamedAgg('targeted_productivity', 'sum')).reset_index()

t3 = df.groupby(['month', 'date', 'department']).agg(workers=pd.NamedAgg('no_of_workers', 'sum'),
                                                        actual=pd.NamedAgg('actual_productivity', 'sum'),target=pd.NamedAgg('targeted_productivity', 'sum')).reset_index()




Intro= html.Div([
    html.Br(),
    html.Br(),
    html.P("The garment industry plays a pivotal role in our global economy. With its labor-intensive processes and intricate workflows, understanding and optimizing employee productivity is crucial for the industry’s success. In this dashboard, we delve into the fascinating world of garment manufacturing, exploring the factors that impact productivity and uncovering valuable insights.", style={'margin': '0 20%', 'text-align': 'center', 'font-size': 'large', 'color':'white'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.H3("This Dashboard Includes Below Tabs", style={'text-align': 'center'}),
        html.Ul([
            html.Li("Time Series Analysis in Productivity and Work in Progress"),
            html.Br(),
            html.Li("Correlation between Actual Productivity and SMV"),
            html.Br(),
            html.Li("How Productivity changes by Day"),
            html.Br(),
            html.Li("Departments' Productivity")
        ], style={'margin': '0 35%', 'font-size': '17.5px', 'color':'white'})
    ])
])


T1_elements = html.Div([
    # T1 : Component to slider and drop down and Graph
    html.Div([
        # Div to slider
        html.Div([
            html.H4("Select the Month"),
            dcc.Slider(
                min=df["month"].min(),
                max=df["month"].max(),
                step=1,
                id='T1slider',
                value=df["month"].min(),
                marks={str(i): {'label': lbl[i],
                                'style': {
                                    'transform-origin': 'left bottom',
                                    'color': 'white',
                                    'font-weight': 'bold',
                                    'font-size': 14}} for i in df["month"].unique()}
            )],
            id='T11slider'),

        # Div to dropdown
        html.Div([
            html.H4("Select the features"),
            dcc.Dropdown(
                id='T1D1',
                options=[
                    {'label': 'Actual Productivity', 'value': 'actual'},
                    {'label': 'Target Productivity', 'value': 'target'},
                    {'label': 'Work in Progress', 'value': 'wip'},
                ],
                value=None,
                multi=True,
                clearable=True,
                searchable=True,
            ),
        ], id='T11drop'), html.Br(), html.Br(), html.Br(),
        # Div to graph
        html.Div([
            dcc.Graph(id='T1graph')
        ])
    ]),
],style={'margin': '0', 'padding': '0'})

T2_elements = html.Div([
    # T2 : Radio Button and Graph
    html.Div([
        html.Div([
            html.H4("Select a Feature to Check Correlation with Actual Productivity"),
            dcc.RadioItems(
                id='T2radio',
                options=[
                    {'label': 'Standard Minute Value (SMV)', 'value': 'smv'},
                    {'label': 'Incentive', 'value': 'incentive'},
                    {'label': 'Overtime', 'value': 'over_time'}
                ],
                value='over_time',
                labelStyle={'display': 'inline-block', 'margin-right': '0.5rem', 'textAlign': 'center', 'color':'white'}),
            html.Br(),
            dcc.Graph(id="T2scatter")
        ], id='T2Compo')
    ])
],style={'margin': '0', 'padding': '0'})


T3_elements=[
    # T3 : Slider in bottom
    html.Div([
        html.H4("Select the month"),
        dcc.Slider(min = T3["month"].min(), max = T3["month"].max(), step = 1, id= 'T3slider', value=T3["month"].min(),
                marks={str(i): {'label': lbl[i], 
                            'style': {
                                        'transform-origin': 'left bottom',
                                        'color':'white',
                                        'font-weight': 'bold',
                                        'font-size':12}} for i in T3["month"].unique()})

    ],id='T33slider',style={'height':'4vh','color':'white'}),html.Br(),

    #T3 Pie and Line
    html.Div([
    html.Div([
        html.H4('Departments'),
        dcc.Graph(id='T3pie')
    ],style={'textAlign': 'center','width': '45%', 'display': 'inline-block'}),
    html.Div([
        html.H4("Actual Productivity by infulencing style"),
        dcc.Graph(id='T3line')
    ],style={'textAlign': 'center','width': '45%', 'display': 'inline-block', 'float': 'right'})
    ])
]

T4_elements=[
    # T4 : Slider in bottom
    html.Div([
        html.H5("Select the month"),
        dcc.Slider(min=t3["month"].min(), max=t3["month"].max(), step=1, id='T4slider', value=t3["month"].min(),
                   marks={str(i): {'label': lbl[i],
                                   'style': {
                                       'transform-origin': 'left bottom',
                                       'color': 'white',
                                       'font-weight': 'bold',
                                       'font-size': 12}} for i in t3["month"].unique()})

    ], id='T44slider', style={'height': '3vh'}),html.Br(),html.Br(),

    # T4 Pie and Line
    html.Div([
        html.Div([
            html.H5('Departments'),
            dcc.Graph(id='T4pie')
        ], style={'textAlign': 'center','width': '33%', 'display': 'inline-block'}),
        html.Div([
            html.H5("Actual Productivity of the Department"),
            dcc.Graph(id='T4line')
        ], style={'textAlign': 'center','width': '33%', 'display': 'inline-block'}),
        html.Div([
            html.H5("Target Productivity of the Department"),
            dcc.Graph(id='T4line2')
        ], style={'textAlign': 'center','width': '33%', 'display': 'inline-block'})
    ]) 
]




app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Productivity of Garment Employees", id='T1title', style={'height': '6vh', 'textAlign':'center', 'color':'white'}),
    dcc.Tabs([
        dcc.Tab(label='Introduction', value='tab0', children=Intro, style={'backgroundColor': 'black', 'color': 'white'}),
        dcc.Tab(label='Productivity & WIP', value='tab1', children=T1_elements, style={'backgroundColor': 'black', 'color': 'white'}),
        dcc.Tab(label='Correlation Analysis', value='tab2', children=T2_elements, style={'backgroundColor': 'black', 'color': 'white'}),
        dcc.Tab(label='Productivity changes in Days', value='tab3', children=T3_elements, style={'backgroundColor': 'black', 'color': 'white'}),
        dcc.Tab(label="Departments' Productivity", value='tab4', children=T4_elements, style={'backgroundColor': 'black', 'color': 'white'}),
    ])
], style={'background-color': '#002966', 'height': '100vh',  'margin': '0', 'padding': '8px'})



# Functions and Call Backs 

# T1 Call back ; dropdown and slider
@app.callback(
    Output(component_id='T1graph', component_property='figure'),
    Input(component_id= 'T1slider', component_property= 'value'),
    Input(component_id= 'T1D1', component_property= 'value')
)
# T1 define function; line plot with slider and multi drop down
def t1graph(_month,T1D1):
    T1fill=df.groupby(['month','date']).agg(actual = pd.NamedAgg('actual_productivity', 'sum'),
                                 target = pd.NamedAgg('targeted_productivity', 'sum'),
                                 wip = pd.NamedAgg('wipt', 'sum')).reset_index()
    T1df = T1fill[T1fill['month'] == _month]
    fig1 = px.line(T1df, x="date", y=T1D1 ,hover_data={"date": "|%B %d, %Y"}, template='plotly_dark',color_discrete_sequence=["#00FFFF","#FFFF00",'#FFA500'])
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)',title="Productivity and Work in Progress",title_x=0.5,
                       xaxis_title="Date",
                       yaxis_title="Value")
    return fig1
#-----------------------------------------------------------------------------------------------
# T2 : call back to multi variable scatter plot
@app.callback(
    Output('T2scatter', 'figure'),
    [Input('T2radio', 'value')]
)
# T2 : Define function to scatter plot
def update_graph(selected_value):
    correlation = df['actual_productivity'].corr(df[selected_value])
    if selected_value == 'smv':
        fig2 = px.scatter(df, x='actual_productivity', y='smv',
                          template='plotly_dark',color_discrete_sequence=["#00FFFF"],
                          title=f'Actual Productivity vs {selected_value}, Correlation is {correlation:.2f}')
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)',title_x=0.5,
                       xaxis_title="Actual Productivity", yaxis_title="Standard Minute Value")

    elif selected_value == 'incentive':
        fig2 = px.scatter(df, x='actual_productivity', y='incentive',
                          template='plotly_dark',color_discrete_sequence=["#00FFFF"],
                          title=f'Actual Productivity vs {selected_value}, Correlation is {correlation:.2f}')
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)',title_x=0.5,
                       xaxis_title="Actual Productivity", yaxis_title="Incentive")

    else:
        fig2 = px.scatter(df, x='actual_productivity', y='over_time',
                          template='plotly_dark',color_discrete_sequence=["#00FFFF"],
                          title=f'Actual Productivity vs {selected_value}, Correlation is {correlation:.2f}')
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)',title_x=0.5,
                       xaxis_title="Actual Productivity", yaxis_title="Over Time")

    return fig2

#-------------------------------------------------------------------------------------------------------------
# T3 : Define callback to update chart
@app.callback(
    Output('T3pie', 'figure'),
    [Input('T3slider', 'value')]
)
# T3 : Define function to pie chart wih slider
def update_bar_chart(_month):
    T33 = T3[T3['month'] == _month]
    figT3= px.pie(values=T33['count'], names=T33['day'], template='plotly_dark',color_discrete_sequence=["#DDA0DD","#BC8F8F","#7FFFD4", "#66CDAA", "#F0E68C", "#FA8072"])
    figT3.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    return figT3

# T3 : Define cllback to hover 
@app.callback(
    Output('T3line', 'figure'),
    [Input('T3pie', 'hoverData'), Input('T3slider', 'value')]
)
# T3 : Define function to hover data
def update_line_chart(hoverData, _month):
    if hoverData is None:
        return {}
    else:
        style = hoverData['points'][0]['label'] 
        filtered_df = T3[(T3['month'] == _month) & (T3['day'] == style)]
        figT3b = px.line(filtered_df, template='plotly_dark', x='date', y=['actual','target'], color_discrete_sequence=["#00FFFF","#FFFF00"],
                         title=f'Actual and Target Productivity for =  {style}')
        figT3b.update_layout(plot_bgcolor='rgba(0,0,0,0)',title_x=0.5)
        return figT3b

#---------------------------------------------------------------------------------
# T4 : Define callback to update pie chart
@app.callback(
    Output('T4pie', 'figure'),
    [Input('T4slider', 'value')]
)
def pie_chart(_month):
    t33 = t3[t3['month'] == _month]
    figT41 = px.pie(values=t33['workers'], names=t33['department'], title='Months available in Dataset',color_discrete_sequence=["#66CDAA", "#FFFFE0"],
                         template='plotly_dark')
    figT41.update_layout(plot_bgcolor='rgba(0,0,0,0)',title_x=0.5)
    return figT41

# T4 : Define Actual Productivity
@app.callback(
    Output('T4line', 'figure'),
    [Input('T4pie', 'hoverData'),Input('T4slider', 'value')]
)
def update_line_chart(hoverData,_month):
    if hoverData is None:
        return {}
    else:
        department = hoverData['points'][0]['label']
        filtered_df = t3[(t3['department'] == department) & (t3['month'] == _month)]
        figT42 = px.line(filtered_df, x='date', y='actual', title=f'Actual Productivity for Department {department}', color_discrete_sequence=["#00FFFF"],
                         template='plotly_dark')
        figT42.update_layout(plot_bgcolor='rgba(0,0,0,0)',title_x=0.5)
        return figT42

# T4 : Define callback to update pie chart
@app.callback(
    Output('T4line2', 'figure'),
    [Input('T4pie', 'clickData'),Input('T4slider', 'value')]
)
def update_line_chart(clickData,_month):
    if clickData is None:
        return {}
    else:
        department = clickData['points'][0]['label']
        filtered_df = t3[(t3['department'] == department) & (t3['month'] == _month)]
        figT43 = px.line(filtered_df, x='date', y='target', title=f'Target Productivity for Department {department}',color_discrete_sequence=["#FFFF00"],
                         template='plotly_dark')
        figT43.update_layout(plot_bgcolor='rgba(0,0,0,0)',title_x=0.5)
        return figT43    

app.run()
if __name__ == '__main__':
    app.run_server(debug=True)
