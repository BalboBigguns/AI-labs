import plotly.graph_objects as go
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html

GRAPH_PARAMETERS = {
    "class_a": {
        "name": "Class A",
        "modes": 3,
        "samples": 20,
        "data": []
    },
    "class_b": {
        "name": "Class B",
        "modes": 2,
        "samples": 20,
        "data": []
    }
}

def create_mode(samples, x=None, y=None, mean=None, std_dev=None):
    if not x:
        x = np.random.random() * 8 + 1

    if not y:
        y = np.random.random() * 8 + 1

    if not mean:
        mean = np.random.random() * 2 - 1

    if not std_dev:
        std_dev = 0.07 #np.random.random() / 3

    samples = np.random.normal(mean, std_dev, (samples, 2))

    def set_position(point):
        point[0] += x
        point[1] += y
        return point

    return list(map(set_position, samples))


def generate_trace(class_props, new_data=False):
    if (new_data):
        class_props["data"] = []
        for _ in range(class_props["modes"]):
            class_props["data"] += create_mode(class_props["samples"])
    
    return go.Scatter(
        x=[point[0] for point in class_props["data"]],
        y=[point[1] for point in class_props["data"]],
        mode="markers",
        name=class_props["name"]
    )


app = dash.Dash(__name__)
app.layout = html.Div(
    className="root",
    children=[
        html.H1(children="Artificial Intelligence Fundamentals Laboratory - Michal Okrasa CS 227422"),
        dcc.Graph(
            id="graph"
        ),
        html.Div(
            className="inputs-container",
            children=[
                html.Div(
                    className="class-inputs",
                    children=[
                        html.H2(
                            id="header-a",
                            children="Class A"
                        ),
                        html.Label("Number of modes:"),
                        dcc.Input(
                            className="input",
                            id="a-modes",
                            type="number",
                            value=GRAPH_PARAMETERS["class_a"]["modes"],
                            debounce=True
                        ),
                        html.Label("Number of samples per mode:"),
                        dcc.Input(
                            className="input",
                            id="a-samples",
                            type="number",
                            value=GRAPH_PARAMETERS["class_a"]["samples"],
                            debounce=True
                        )
                    ]
                ),
                html.Div(
                    className="class-inputs",
                    children=[
                        html.H2(
                            id="header-b",
                            children="Class B"
                        ),
                        html.Label("Number of modes:"),
                        dcc.Input(
                            className="input",
                            id="b-modes",
                            type="number",
                            value=GRAPH_PARAMETERS["class_b"]["modes"],
                            debounce=True
                        ),
                        html.Label("Number of samples per mode:"),
                        dcc.Input(
                            className="input",
                            id="b-samples",
                            type="number",
                            value=GRAPH_PARAMETERS["class_b"]["samples"],
                            debounce=True
                        )
                    ]
                )
            ]
        ),
        html.Button(
            id="update-button",
            children="Update",
            n_clicks=0
        )
    ]
)

@app.callback(
    dash.dependencies.Output("graph", "figure"),
    [dash.dependencies.Input("update-button", "n_clicks")],
    [dash.dependencies.State("a-samples", "value"),
    dash.dependencies.State("b-samples", "value"),
    dash.dependencies.State("a-modes", "value"),
    dash.dependencies.State("b-modes", "value"),]
)
def update_graph(n_clicks, a_samples, b_samples, a_modes, b_modes):
    if (n_clicks != 0):
        a_changes = False
        b_changes = False
        fig = go.Figure()

        if (a_samples != GRAPH_PARAMETERS["class_a"]["samples"] or 
            a_modes != GRAPH_PARAMETERS["class_a"]["modes"]
        ):
            GRAPH_PARAMETERS["class_a"]["samples"] = a_samples
            GRAPH_PARAMETERS["class_a"]["modes"] = a_modes
            fig.add_trace(generate_trace(GRAPH_PARAMETERS["class_a"], new_data=True))
            a_changes = True

        if (b_samples != GRAPH_PARAMETERS["class_b"]["samples"] or 
            b_modes != GRAPH_PARAMETERS["class_b"]["modes"]
        ):
            GRAPH_PARAMETERS["class_b"]["samples"] = b_samples
            GRAPH_PARAMETERS["class_b"]["modes"] = b_modes
            fig.add_trace(generate_trace(GRAPH_PARAMETERS["class_b"], new_data=True))
            b_changes = True

        if (a_changes and not b_changes):
            fig.add_trace(generate_trace(GRAPH_PARAMETERS["class_b"]))
        elif (b_changes and not a_changes):
            fig.add_trace(generate_trace(GRAPH_PARAMETERS["class_a"]))
        elif (not a_changes and not b_changes):
            fig.add_trace(generate_trace(GRAPH_PARAMETERS["class_a"], new_data=True))
            fig.add_trace(generate_trace(GRAPH_PARAMETERS["class_b"], new_data=True))  
    
        return fig

    fig = go.Figure()
    fig.add_trace(generate_trace(GRAPH_PARAMETERS["class_a"], new_data=True))
    fig.add_trace(generate_trace(GRAPH_PARAMETERS["class_b"], new_data=True))

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
