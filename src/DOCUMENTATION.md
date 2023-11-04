# Dash HTMLayout

This package provides the ability to build dashboard layouts in Dash by writing HTML documents.

## Installation

You can install this package by using a tool like `pip`:

```bash
pip install dash-htmlayout
```

## How to use

### In Python code

To load an HTML layout for your Dash application, you need to instantiate a `dash.htmlayout.Builder` object with an HTML
file path. URLs are supported through the `lxml` library.

```python
from dash import Dash
from dash.htmlayout import Builder

app = Dash()
builder = Builder(file="dash_app.html")
app.layout = builder.layout
```

### In the HTML file

Since the usual way to build a Dash layout does not involve making the whole HTML5 structure but only what's in the
`<body>` tag, the same has to be observed in your HTML file. For example:

```html
<section>
    <h1 id="dash-title">Title</h1>
    <dcc.dropdown id="select-1" data-list-options-0="Red" data-list-options-1="Blue"/>
</section>
```

Any parameter for a component class can be defined as a tag attribute, as long as it is a
`str`. 

Parameters of type `list[str]` can be provided in HTML using the following scheme:

```html
<div data-list-parameter-0="first item" data-list-parameter-1="second item" ...>
```

Parameters of type `bool` can be provided in HTML using the following scheme:

```html
<div data-bool-parameter1="1">
```

**Note**: Text that will be considered `True` is `"1"`, `"true"`, `"yes"` or `"on"`



### What tag names to use for non-HTML components?

By default, any component that is not in the `dash.html` module has to be named with a prefix.
Generally, the prefix is the most relevant part of the module name, eg. `table` for the `dash_table` module.
The prefix must be used as following:

```html
<dcc.dropdown/>
<table.datatable/>
<daq.booleanswitch on=false/>
```
