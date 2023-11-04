# Build your Dash layouts with HTML snippets 

This package allows you to craft your Dash application layouts
by writing HTML instead of a cascade of Python objects.

## Installation

You can install the package with pip:

```bash
pip install dash-htmlayout
```

## Introduction

It's a bit counterproductive to force users to build dashboard
layouts using Python, when most component classes are translated
into HTML.

Having to write code such as the following:

```python
app.layout = html.Section()
app.layout.children = [
    html.H1("Dashboard component.", className="mb-5"),
    html.Div(
        className="row",
        children=[
            html.Div(
                className="col-3",
                children=[
                    html.Div(
                        className="form-group mb-3",
                        children=[
                            html.Label("Genres filter"),
                            dcc.Dropdown(
                                id="genre-list",
                                placeholder="Filter genres",
                                multi=True,
                            ),
                        ],
                    ),
                    html.Div(
                        className="form-group mb-3",
                        children=[
                            html.Label("Max results"),
                            dcc.Slider(
                                id="genre-limit", min=5, max=15, step=1, value=10
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className="col-5 d-flex align-items-stretch",
                children=[
                    html.Div(className="card flex-fill", children=[
                        html.H2("Genre information", className="text-center card-header"),
                        html.Div(className="card-body", children=[
                            dcc.Graph(id="genre-info"),
                        ]),
                    ]),
                ],
            ),
            html.Div(
                className="col-4 d-flex align-items-stretch flex-fill",
                children=[
                    html.Div(className="card flex-fill", children=[
                        html.H2("Artists", className="text-center card-header"),
                        dcc.Markdown(id="artist-info", className="card-body"),
                    ]),
                ],
            ),
        ],
    ),
]
```

should almost be considered malpractice in Python when there is a language
and a document type that addresses this exact need; HTML.

Instead, this package provides a simple class to generate layouts
from a partial HTML document. For example, we could partially reproduce the above
example with such a file:

```html
<section>
    <h1 class="mb-5">Dashboard component.</h1>
    <div class="row">
        <div class="col-3">
            <div class="form-group mb-3">
                <label for="">Genres filter</label>
                <dcc.dropdown id="genre-list" placeholder="Filter genres" multi/>
            </div>
            <div class="form-group mb-3">
                <label for="">Max results</label>
                <dcc.slider id="genre-limit" min=5 max=15 step=1 value=10/>
            </div>
        </div>
        ...
    </div>
</section>
```
