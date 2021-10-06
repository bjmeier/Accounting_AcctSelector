# -*- coding: utf-8 -*-
import dash
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import flask
import datetime
from dfHelpers import cleanDf
import pandas as pd

############  Add ALL and make into radio buttons

FDIR = f'Q:\OdooMigration\Accounting\AcctSelector\\'
FNAME = 'OdooAN_2021_10_8.xlsx'
SHEET = 'ACSelect'

TITLE = 'Account Selection'
INPUTSTYLE = {"margin-left": "4px",
              "margin-right": "2px"}

now = datetime.datetime.now()
dtstr = now.strftime("%m/%d/%Y, %H:%M:%S %p")

############ Read and format dataframe
inputDf = pd.read_excel(FDIR+FNAME,sheet_name=SHEET)
df = inputDf[inputDf['SELECTABLE']==1]
intList = ['SELECTABLE','SHIPPING','TAXES']
df = cleanDf(inputDf, intList)
df.sort_values(by=['orderANs', 'PrintOrder'],inplace=True)
df.drop(columns=['orderANs','PrintOrder'],inplace=True)
df = df[df['SELECTABLE']==1]
df.drop(columns=['SELECTABLE'],inplace=True)
df.reset_index(drop=True,inplace=True)

df=df[['Name','Type','OdooAcctCode','Parent', 'Code','Notes','BUILDING','COST_CENTER','SHIPPING','TAXES']]

############ Gather checkbox info
checkboxDict = {'types':list(df['Type'].unique()), 'buildings': list(df['BUILDING'].unique()), 'cost_centers': list(df['COST_CENTER'].unique())}
binaryList = ['SELECTABLE', 'SHIPPING','TAXES']

def btn_options(choices):
    opt = []
    for c in choices:
        opt.append({'label':c,'value':c})
    return opt

flask_server = flask.Flask(__name__)
#app = dash.Dash(__name__,server=flask_server)
app = dash.Dash(__name__, server=flask_server, title=TITLE)

app.layout = html.Div([
            html.Div([
                html.H1(TITLE,className='title'),
                ],className='header'),
                html.Div([
                    html.Div([
                        dcc.Checklist(
                            id=f'checklist-{list(checkboxDict.keys())[0]}',
                            options=btn_options(checkboxDict[list(checkboxDict.keys())[0]]),
                            value=['Expense', 'Other Income', 'Cost of Revenue'],
                            className='check',
                            inputStyle=INPUTSTYLE,
                        ),
                        dcc.Checklist(
                            id=f'checklist-{list(checkboxDict.keys())[1]}',
                            options=btn_options(checkboxDict[list(checkboxDict.keys())[1]]),
                            value=checkboxDict[list(checkboxDict.keys())[1]],
                            className='check',
                            inputStyle=INPUTSTYLE,
                        ),
                        dcc.Checklist(
                            id=f'checklist-{list(checkboxDict.keys())[2]}',
                            options=btn_options(checkboxDict[list(checkboxDict.keys())[2]]),
                            value=checkboxDict[list(checkboxDict.keys())[2]],
                            className='check',
                            inputStyle=INPUTSTYLE,
                        ),
                        #dcc.Checklist(
                        #    id=f'checklist-{binaryList[0]}',
                        #    options=btn_options([0,1]),
                        #    value=[1],
                        #    className='check',
                        #    inputStyle=INPUTSTYLE,
                        #),  html.P(binaryList[0]),
                        dcc.Checklist(
                            id=f'checklist-{binaryList[1]}',
                            options=btn_options([0,1]),
                            value=[0,1],
                            className='check',
                            inputStyle=INPUTSTYLE,
                        ), html.P(binaryList[1]),
                        dcc.Checklist(
                            id=f'checklist-{binaryList[2]}',
                            options=btn_options([0,1]),
                            value=[0,1],
                            className='check',
                            inputStyle=INPUTSTYLE,
                        ), html.P(binaryList[2]),
                    ], className='radio-check'),
                    html.Img(src='assets/rcp-logo.png',
                             width='231px',
                             height='176px',
                             alt='RCP Logo',
                             className='logo'),
                ],className='radio-check-logo'),
                html.Div([
                    html.Div(id='table'),
                    html.P(f'{dtstr}')
                    ], className='dtable'),
                html.Div([
                    #html.P(u'\u00a9'+' Copyright 2021, Richardson Cooling Packages, LLC'),
                    html.P(u'Richardson Cooling Packages, LLC'),
                    html.A('website',
                           href='https://www.coolingpackages.com/',
                           target='RCP website'),
                    html.A('e-mail',
                           href='mailto:info.coolingpackages.com/',
                           target='RCP website'),
                    html.A('tel: 724.652.5655',
                           href='tel:+1724-652-5655',
                           target='RCP Phone'),
                ], className='footer')
            ], className='page')

@app.callback(
    Output(component_id='table', component_property='children'),
    Input(component_id=f'checklist-{list(checkboxDict.keys())[0]}', component_property='value'),
    Input(component_id=f'checklist-{list(checkboxDict.keys())[1]}', component_property='value'),
    Input(component_id=f'checklist-{list(checkboxDict.keys())[2]}', component_property='value'),
    #Input(component_id=f'checklist-{binaryList[0]}', component_property='value'),
    Input(component_id=f'checklist-{binaryList[1]}', component_property='value'),
    Input(component_id=f'checklist-{binaryList[2]}', component_property='value'),
)
def update_output_div(inpType, inpBUILDING, inpCOST_CENTER, inpSHIPPING, inpTAXES):
    dfOut = df
    dfOut = dfOut[dfOut['Type'].isin(inpType)]
    dfOut = dfOut[dfOut['BUILDING'].isin(inpBUILDING)]
    dfOut = dfOut[dfOut['COST_CENTER'].isin(inpCOST_CENTER)]
    #dfOut = dfOut[dfOut['SELECTABLE'].isin(inpSELECTBALE)]
    dfOut = dfOut[dfOut['SHIPPING'].isin(inpSHIPPING)]
    dfOut = dfOut[dfOut['TAXES'].isin(inpTAXES)]

    dfOut.drop(columns=['SHIPPING','TAXES'],inplace=True)

    tbl = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in dfOut.columns],
        style_cell={'textAlign': 'left',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    #'maxWidth': 0,
                    #'fontSize':10,
                    'font-family':"Open Sans"},
        fixed_rows={'headers': True},
        style_header={
            'font-family':"Open Sans",
            'backgroundColor': '#98A09E',
            'fontWeight': 'bold'
        },
        style_table={'height': 400,
                     'overflowX': 'auto',
                     'overflowY': 'auto'},
        page_action='none',
        data=dfOut.to_dict('records'),
        export_format='xlsx',
        export_headers='display',
    )
    return tbl

if __name__ == "__main__":
    app.title = TITLE
    app.run_server(debug=True)

#  to run:
#  python waitress_config.py
#  If running on surface:  http://RCP-X-BMEIE2:8099