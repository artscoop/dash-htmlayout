# Build your Dash layouts with HTML snippets 

This package allows you to craft your Dash application layouts
by writing HTML instead of a cascade of Python objects.

## Installation

You can install the package with pip:

```bash
pip install dash-htmlayout
```

## Documentation

[Read documentation to learn more](https://artscoop.github.io/dash-htmlayout/htmlayout.html)

## Introduction

It's a bit counterproductive to force users to build dashboard
layouts using Python, when most component classes are translated
into HTML.

Having to write code with deeply nested object instances to mimic HTML
should almost be considered malpractice in Python when there is a language
and a document type that addresses this exact need; HTML.

This package provides a simple class to generate layouts
from a partial HTML snippet. For example, we could partially reproduce a classic
layout with the following document:

```html
<!-- Example with Bootstrap classes and some components -->
<section>
    <h1 class="mb-5">Dashboard component.</h1>
    <div class="row">
        <div class="col-3">
            <div class="form-group mb-3">
                <label for="">Genres filter</label>
                <dcc-dropdown id="genre-list" placeholder="Filter genres" data-multi="True"/>
            </div>
            <div class="form-group mb-3">
                <label for="">Max results</label>
                <dcc-slider id="genre-limit" data-value="1" data-min="0" data-max="10"/>
            </div>
        </div>
        ...
    </div>
</section>
```

### In Python

```python
from dash import Dash
from dash.htmlayout import Builder

application = Dash("appname")
builder = Builder(file="myfile.html")
application.layout = builder.layout

...
```
