import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

mathjax = ['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML']

app = dash.Dash(
        __name__,
        meta_tags=[
            {"name": "viewport", "content":"width=device-width, initial-scale=1.0"}
            ],
        external_scripts=mathjax,
        )


def SensitivityTime(s, b, c, d, z):
    return (b+d*s)*z**2/(s**2-(c*b*z)**2)

def makeplot(S, blim, **kwargs):
    useMeasure = kwargs.get("useMeasure", True)
    bgfrac = kwargs.get("bgfrac", True)
    Z = kwargs.get("Z", 3)
    cap = kwargs.get("cap", 6)

    sigmas = np.linspace(0, 1.0, 100)
    chis = np.linspace(0.0, blim, 100)
    SS, XX = np.meshgrid(sigmas, chis)
    XX = XX*S if bgfrac else XX
    ## The divide by 30 is to turn days into months
    F = SensitivityTime(S, XX, SS, useMeasure, Z)/30
    F[F<0] = cap+1
    F[F>=cap+1] = cap+1
    return sigmas, chis, F

plotbody = html.Div(
    className="ait",
    children=[
        html.Div(
            id="left",
            className="leftcolumn",
            children=[
                html.H4("Signal Rate (per day)"),
                dcc.Input(
                    id='input-signal-rate',
                    value=0.2,
                    min=0.0,
                    type='number'
                ),
                html.H4("Y-axis Limit"),
                dcc.Input(
                    id='input-ylim',
                    value=1.0,
                    type='number'
                ),
                html.H4("Sensitivity Equation"),
                html.H4("$$ Z = \\frac{st}{\sqrt{bt+(\sigma t)^2}} $$", id="disceq"),
                html.H4("$$ Z = \\frac{st}{\sqrt{bt+st+(\sigma t)^2}} $$", id="measeq"),
                dcc.RadioItems(
                    id='radio-senstype',
                    options=[{'label': i, 'value': i} for i in ['Discovery', 'Measurement']],
                    value='Discovery',
                    labelStyle={'display': 'block'}
                ),
                html.H4("Y-Axis Toggle"),
                dcc.RadioItems(
                    id='radio-bgtoggle',
                    options=[{'label': i, 'value': i} for i in ['Background Total', 'Background Fraction']],
                    value='Background Total',
                    labelStyle={'display': 'block'}
                ),
                html.H4("Target σ"),
                dcc.Input(
                    id='input-sigma',
                    value=3.0,
                    type='number'
                ),
                html.H4("Max Months"),
                dcc.Input(
                    id='input-months',
                    value=6.0,
                    type='number'
                ),
                html.H4("Colorscheme"),
                dcc.Dropdown(
                    id='dropdown-color',
                    options=[{'label': i, 'value': i} for i in ['Blackbody', 'Turbo']],
                    value='Turbo',
                    clearable=False,
                ),
                dcc.Dropdown(
                    id='dropdown-lines',
                    options=[ {'label': 'Contour Lines', 'value': 'lines'},
                              {'label': 'Filled Contour', 'value': 'fill'},
                              {'label': 'Heatmap', 'value': 'heatmap'} ],
                    value='lines',
                    clearable=False,
                ),
            ],
        ),
        html.Div(
            id="graph",
            className="rightgraph",
            children=dcc.Graph(
                id="sens",
            )
        ),
    ]
)

equations = html.Div( 
    children= [
        html.H4("Sensitivity Equation"),
    ]
)

description = html.Div(
    children = [
        html.Hr()
    ]
)
with open("description.md") as readme:
    descriptionString = readme.read()
    description.children.append(dcc.Markdown(descriptionString))


app.layout = html.Div( children = [ plotbody, description ] )

@app.callback(
        Output('sens', 'figure'),
        Input('input-signal-rate', 'value'),
        Input('input-ylim', 'value'),
        Input('radio-senstype', 'value'),
        Input('input-sigma', 'value'),
        Input('input-months', 'value'),
        Input('radio-bgtoggle', 'value'),
        Input('dropdown-color', 'value'),
        Input('dropdown-lines', 'value'),
        )
def update_figure(sig, blim, discVal, sigma, months, bgtoggle, cs, clines):
    useMeasure = True if discVal == 'Measurement' else False
    useBGFrac = True if bgtoggle == "Background Fraction" else False
    x, y, z = makeplot(sig, blim, useMeasure=useMeasure, Z=sigma, cap=months, bgfrac=useBGFrac )

    fig = go.Figure( data =
            go.Contour(
                x=x,
                y=y,
                z=z,
                colorbar=dict(
                    title='Months to Detection',
                    titleside='right'
                ),
                colorscale=cs,
                line = dict(smoothing=1.0),
                contours=dict(start=0.0,end=months,size=1),
                contours_coloring=clines,
                line_width=2,
            ),
          )
    fig.update_xaxes(title_text="Fractional Background Uncertainty")
    yaxes = "Background per signal" if useBGFrac else "Background counts per day"
    fig.update_yaxes(title_text=yaxes)
    fig.update_layout(width=800, height=600)
    return fig

@app.callback(
        Output('disceq', 'style'),
        Input('radio-senstype', 'value'),
        )
def update_eq(eq):
    if eq == 'Measurement':
        return {'display': 'none'}
    return {'display': 'block'}

@app.callback(
        Output('measeq', 'style'),
        Input('radio-senstype', 'value'),
        )
def update_eq(eq):
    if eq == 'Discovery':
        return {'display': 'none'}
    return {'display': 'block'}

app.title = "AIT Sensitivity"
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
