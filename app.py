import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

app = dash.Dash(
        __name__,
        meta_tags=[
            {"name": "viewport", "content":"width=device-width, initial-scale=1.0"}
            ],
        )


## Right side plot
def Discovery(x, s, S, z):
    return z**2*x/(S**2-(s*x)**2)

def Measure(x, s, S, z):
    return z**2*(x+S)/(S**2-(s*x)**2)

def makeplot(S, blim, **kwargs):
    useDisc = kwargs.get("useDisc", True)
    Z = kwargs.get("Z", 3)
    cap = kwargs.get("cap", 6)
    sigmas = np.linspace(0, 1.0, 100)
    chis = np.linspace(0.0, blim, 100)
    SS, XX = np.meshgrid(sigmas, chis)
    ## The divide by 30 is to turn days into months
    if useDisc:
        F = Discovery(XX*S, SS, S, Z)/30
    else:
        F = Measure(XX*S, SS, S, Z)/30
    F[F<0] = cap
    F[F>=cap] = cap
    #return SS, XX, F
    return sigmas, chis, F



app.layout = html.Div(
    className="ait",
    children=[
        html.Div(
            id="left",
            className="leftcolumn",
            children=[
                html.P("Signal Rate (per day)"),
                dcc.Input(
                    id='input-signal-rate',
                    value=0.5,
                    min=0.0,
                    type='number'
                ),
                html.P("Y-axis Limit"),
                dcc.Input(
                    id='input-ylim',
                    step=0.1,
                    value=10.0,
                    type='number'
                ),
                html.P("Sensitivity Equation"),
                dcc.RadioItems(
                    id='radio-senstype',
                    options=[{'label': i, 'value': i} for i in ['Discovery', 'Measurement']],
                    value='Discovery',
                    labelStyle={'display': 'block'}
                ),
                html.P("Target σ"),
                dcc.Input(
                    id='input-sigma',
                    value=3.0,
                    type='number'
                ),
                html.P("Max Months"),
                dcc.Input(
                    id='input-months',
                    value=6.0,
                    type='number'
                ),
            ],
        ),
        html.Div(
            id="graph",
            className="rightgraph",
            children=dcc.Graph(
                id="sens",
            )
        )
    ]
)

@app.callback(
        Output('sens', 'figure'),
        Input('input-signal-rate', 'value'),
        Input('input-ylim', 'value'),
        Input('radio-senstype', 'value'),
        Input('input-sigma', 'value'),
        Input('input-months', 'value'),
        )
def update_figure(sig, blim, discVal, sigma, months):
    useDisc = True if discVal == 'Discovery' else False
    x, y, z = makeplot(sig, blim, useDisc=useDisc, Z=sigma, cap=months)

    fig = go.Figure( data =
            go.Contour(
                x=x,
                y=y,
                z=z,
                colorbar=dict(
                    title='Months to Detection',
                    titleside='right'
                ),
                #colorscale='Turbo',
                colorscale='Blackbody',
                contours=dict(start=0.001,end=months+0.001,size=1),
            ),
          )
    fig.update_xaxes(title_text="Fractional Background Uncertainty")
    fig.update_yaxes(title_text="Background counts per signal count")
    fig.update_layout(width=800, height=600)
    return fig


app.title = "AIT Sensitivity"
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
