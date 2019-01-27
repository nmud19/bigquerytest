# This is where the secret JSON would go

# Set Up the google credentials
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "BigQuerySecretJson.json"


# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        "https://codepen.io/chriddyp/pen/brPBPO.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions']=True
# Loading screen CSS
# app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

app.layout = html.Div([
    html.Div([
        html.H1("Nikhil Mudhalwadkar's BigQuery Assignment"),
    ],
        style= {
            'align' : 'center'
        }
    ),
    html.Div([
        html.H5("Title         "),
        dcc.Input(id='title', type='text', value=''),
    ]),
    html.Div([
        html.H5("Search String "),
        dcc.Input(id='search-string', type='text', value=''),
    ]),
    html.Div([
        html.H5("Hit the search button to get results!"),
        html.P(""),
        html.P(""),
        html.Button(id='submit-button', n_clicks=0, children='Submit'),
    ]),
    html.Div([
        html.H5("Results"),
        html.Mark("Assumption:"),
        html.Mark("Since it was ambigious in the assignment I have used the 'like' operator for query "),
        html.Label("Example query could be - select * from table_name where title like 'SOMESTRING%' "),
        html.Div(id='output-state')
    ])
],
    style={
        'width': '80%',
        'fontFamily': 'Sans-Serif',
        'margin-left': 'auto',
        'margin-right': 'auto'
    }
)


@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('title', 'value'),
               State('search-string', 'value')])
def update_output(n_clicks, input1, input2):
    """
    This function will intrepret the query results
    :param n_clicks:
    :param input1:
    :param input2:
    :return:
    """
    ans = "basic string"
    if (input1 == "") & (input2 == "") :
        ans = "No input values detected! Please try populating either textbox"
    elif (input1 != "") & (input2 == "") :
        # Query does not contain search string
        query = "select * from `bigquery-public-data.hacker_news.stories` where title like '{}%'".format(input1)
        ans = run_query(query=query,is_from_dash = 1)

    elif (input1 == "") & (input2 != "") :
        query = "select * from `bigquery-public-data.hacker_news.stories` where text like '{}%'".format(input2)
        ans = run_query(query=query ,is_from_dash = 1)
        # Query does not contain title

    elif (input1 != "") & (input2 != "") :
        # Query would contain both
        query = "select * from `bigquery-public-data.hacker_news.stories` where title like '{}%' and text like '{}%'".format(input1, input2)
        ans = run_query(query = query,is_from_dash = 1)

    else:
        ans = "Something went wrong with the parameters, please refresh the page."
    # u'''
    #     The Button has been pressed {} times,
    #     Input 1 is "{}",
    #     and Input 2 is "{}"
    # '''.format(n_clicks, input1, input2)
    return ans


def run_query(query=10, parameters=10, max_rows = 5, is_from_dash = 0) :
    #
    # Call the API
    from google.cloud import bigquery
    from pandas import DataFrame
    client = bigquery.Client()

    # query = (
    #     "select * from `bigquery-public-data.hacker_news.stories` limit 10"
    # )

    query = (query)
    query_job = client.query(
        query,
        # Location must match that of the dataset(s) referenced in the query.
        location="US",
    )  # API request - starts the query

    df = DataFrame(
        [(x['title'], x['url'], x['time_ts'], x['text']) for x in query_job],
        columns=['Title', 'URL', 'Timestamp', 'Text']
    )


    if is_from_dash ==0 :
        # This is form the backend
        pass
    else:

        # Create table
        df = DataFrame(
            [(x['title'], x['url'], x['time_ts'], x['text']) for x in query_job],
            columns=['Title', 'URL', 'Timestamp', 'Text']
        )
        return html.Div([
            html.H5('Query generated is : {}'.format(query)),
            html.Table(
                # Header
                [html.Tr([html.Th(col) for col in df.columns])] +

                # Body
                [html.Tr([
                    html.Td(df.iloc[i][col]) for col in df.columns
                ]) for i in range(min(len(df), max_rows))]
            )
        ])


if __name__ == '__main__':
    app.run_server(debug=True, port = 8000)