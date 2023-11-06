# Dash HTMLayout

This package provides the ability to build dashboard layouts in Dash by writing HTML documents.

## Installation

The package is published on 

![PyPI](https://img.shields.io/badge/pypi-3775A9?style=for-the-badge&logo=pypi&logoColor=white)

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
`<body>` tag, the same has to be observed in your HTML/XML file. For example:

```html
<section>
    <h1 id="dash-title">Title</h1>
    <dcc-dropdown id="select-1" data-options="['Red', 'Blue']"/>
</section>
```

Only HTML comments and tags backed up by a component offered by the Dash libraries would be
accepted in your document.

### Non-string parameters

Any parameter for a component class can be defined as a tag attribute, as long as it is a
`str`. Parameters that are not of type `str` can be provided in HTML using the following scheme:

```html
<div data-parameter="python literal to evaluate" ...>
```

For example, the `Dropdown` and `Slider` components from `dash.dcc` accept some arguments that are lists or integers, like `options` and `value`. You may pass those in HTML like follows:

```html
<dcc-slider data-value="1" data-min="0" data-max="10" data-step="5" />
<dcc-dropdown data-options="['Option 1', 'Option 2']" />
```

Every attribute starting with the name `data-<name>` will be treated as the argument `<name>`, with its text value
evaluated as a Python literal.

### What tag names to use for non-HTML components?

By default, any component that is not in the `dash.html` module has to be named with a prefix.
Generally, the prefix is the most relevant part of the module name, eg. `table` for the `dash_table` module.
The prefix must be used as following:

```html
<dcc-dropdown/>
<table-datatable/>
<daq-booleanswitch data-on="False"/>
```

Dot notation is not used for prefixing because it interferes with content editor helpers like Emmet, and
will be considered as a class.
