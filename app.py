from flask import Flask, render_template #this has changed

import plotly
import plotly.graph_objs as go
#import chart_studio.plotly as py

import pandas as pd
import numpy as np
import json

app = Flask(__name__)


def create_plot():


    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
    '''
    data = [
        go.Line(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        ),
        go.Line(
            x=df['x'], # assign x as the dataframe column 'x'
            y = np.random.randn(len(df['x']))
        )
    ]
    '''

    trace1 = { 
        'x': df['x'],
        'y': df['y'],
        'name': 'Blue Trace',
        'type': 'line'
    }
    
    trace2 = { 
        'x': df['x'],
        'y': np.random.randn(len(df['x'])),
        'name': 'Orange Trace',
        'type': 'line'
    }
    # https://plotly.com/javascript/configuration-options/
    data = [trace1, trace2]
    #graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON = tojson(data)

    layout = {'title': 'Two lines on the plot'}
    layoutJSON = tojson(layout)

    config = {'displaylogo': False, 'displayModeBar': True}
    configJSON = tojson(config)
   
    return graphJSON, layoutJSON, configJSON


def tojson(data):
    return json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)


def create_multiple_plots():
    # https://github.com/plotly/plotlyjs-flask-example/blob/master/app.py
    N = 40
    x = np.linspace(0, 1, N)

    trace1 = { 
        'x': x,
        'y': np.random.randn(N),
        'name': 'Trace 1',
        'type': 'line'
    }
    
    trace2 = { 
        'x': x,
        'y': np.random.randn(N),
        'name': 'Trace 2',
        'type': 'line'
    }

    data1 = [trace1, trace2]
    layout1 = {'title': '1: Two lines on the plot'}
    
    trace3 = { 
        'x': x,
        'y': np.random.randn(N),
        'name': 'Trace 3',
        'type': 'bar'
    }
    
    trace4 = { 
        'x': x,
        'y': np.random.randn(N),
        'name': 'Trace 4',
        'type': 'scatter'
    }

    data2 = [trace3, trace4]
    layout2 = {'title': '2: Bars ans scatter on the plot'}

    config1 = {'displaylogo': False, 'displayModeBar': True}
    config2 = {'displaylogo': False, 'displayModeBar': True}

    graphs = [{'data': data1, 'layout': layout1, 'config': config1},
              {'data': data2, 'layout': layout2, 'config': config2}]

    graphJSON = tojson(graphs)

    ids = ['graph-{}'.format(i + 1) for i, _ in enumerate(graphs)]

    return graphJSON, ids

@app.route('/')
def index():

    bar, layout, config = create_plot()
    return render_template('index.html', plot=bar, layout=layout, 
                           config=config)

@app.route('/twoplots')
def twoplots():

    graphJSON, ids = create_multiple_plots()
    return render_template('multiple_plots.html',
                    ids=ids,
                    graphJSON=graphJSON)

if __name__ == '__main__':
    app.run()