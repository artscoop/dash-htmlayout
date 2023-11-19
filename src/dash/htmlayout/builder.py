"""Build layouts from HTML snippets."""
import re
import sys
from importlib import import_module
from os import PathLike
from typing import Optional, Type, Any

from dash.development.base_component import Component
from lxml import etree
from lxml.etree import _Element

from .converters import evaluate


class Builder:
    """
    Class to build layouts using HTML snippets.

    Objects of this class allow loading HTML files describing
    a Dash application layout. All tag names of HTML5 are supported
    by default. Components that are not strictly matching an HTML
    component, but are available in Dash are also supported using
    a prefix.

    ```python
    from dash import Dash
    from dash.htmlayout import Builder

    app = Dash("myapp")
    builder = Builder("URL or filename")
    dropdown = builder.get_component("test-dropdown")
    app.layout = builder.layout
    app.run(debug=True)
    ```

    ```html
    <div>
        <h1>Simple Dashboard</h1>
        <div class="content">
            <dcc.dropdown id="test-dropdown"/>
        </div>
    </div>
    ```
    """

    _module_registry = {
        "dash.html": None,
        "dash.dcc": "dcc",
        "dash.dash_table": "table",
        "dash_daq": "daq",
        "dash_bio": "bio",
        "dash_slicer": "slicer",
        "dash_player": "player",
        "dash_bootstrap_components": "bootstrap",
    }
    _component_registry: dict[str, type] = {}
    # List of modules with already autodetected components
    _autodetected_modules: set = set()
    # Components with id
    _components: dict[str, Component] = {}
    # Layout root component
    layout: Optional[Component] = None

    def __new__(cls, *args, file: PathLike = None, **kwargs) -> "Builder":
        """
        Instanciate a new LayoutBuilder object.

        Every new object will start an autodetection.

        See Also:
            `Builder.autodetect`
        """
        instance = super().__new__(cls, *args, **kwargs)
        cls._autodetect_components()
        if file is not None:
            instance.load(file)
        return instance

    @classmethod
    def _autodetect_components(cls):
        """
        Autodetect and register components from the module registry.

        This class method registers *all* the Dash `Component` classes
        found in various modules, mainly the default ones provided with
        Dash.

        All those classes will be recognized as HTML tags in input documents.
        The name of the tag is derived from the name of the component class,
        but all lowercase. When the component class is not in the `dash.html`
        module, the name must be prefixed with a namespace. For example:

        ```
        dash.html.Section → <section>
        dash_daq.ColorPicker → <daq-colorpicker>
        ```

        When there is a prefix, it is derived from the name of the module
        it represents, but without the redundant `dash` name. Words like
        `component` or `components` are also removed from the prefix.

        Notes:
            This method is called automatically when instantiating your
            first `Builder` object, and everytime you register a new library
            of components with `Builder.register_library`.
        """
        for module_name, prefix in cls._module_registry.items():
            try:
                if module_name not in cls._autodetected_modules:
                    module = import_module(module_name)
                    cls._autodetected_modules.add(module_name)
                    for attribute in dir(module):
                        symbol = getattr(module, attribute)
                        if isinstance(symbol, type) and issubclass(symbol, Component):
                            full_prefix: str = f"{prefix}-" if prefix else ""
                            tag_name: str = f"{symbol.__name__.lower()}"
                            full_name: str = f"{full_prefix}{tag_name}"
                            cls._component_registry[full_name] = symbol
            except ImportError:
                print(
                    f"Warning: {module_name} is listed in LayoutBuilder "
                    f"registry but could not be imported.",
                    file=sys.stderr,
                )

    @classmethod
    def register_library(
            cls, path: str, prefix: Optional[str], replace: bool = False
    ) -> bool:
        """
        Register a new module providing Dash components.

        A sensible default is already provided for known libraries,
        but you can custom libraries with this method. You just have to
        call this by passing a module path and a prefix to apply to detected
        components:

        ```python
        from dash.htmlayout import Builder

        Builder.register_library("dash_colorful_lib", "colorful")
        ```
        """
        if path not in cls._module_registry or replace:
            cls._module_registry[path] = prefix
            cls._autodetect_components()
            return True
        return False

    def load(self, path: PathLike) -> Component:
        """
        Build a layout from an HTML file.

        Returns:
            The root of the layout tree with all its descendants.
        """
        parser = etree.XMLParser(
            remove_comments=True, ns_clean=True, remove_pis=True,
            resolve_entities=False, remove_blank_text=True)
        root = etree.parse(path, parser=parser).getroot()
        self._components = {}
        if root:
            self.layout = self._build_tree(root)
        return self.layout

    def get_component(self, identifier: str) -> Optional[Component]:
        """
        Get component instance in the loqded lqyout given an ID.

        Args:
            identifier: id given to the component.

        Returns:
            If found, the component with the given id.
            `None` if the id is not found in the current layout.
        """
        return self._components.get(identifier)

    @classmethod
    def _to_component(cls, tag: str, **options) -> Optional[Component]:
        """Build a component from an HTML tag, with options."""
        component: Optional[Type[Component]] = cls._component_registry.get(
            tag.lower(), None
        )
        if component is not None:
            component: Component = component(**options)
        return component

    def _build_tree(self, element: _Element):
        """
        Build a layout recursively from an HTML element.

        Returns:
            A Dash component with children and attributes.
        """
        tag_name: str = element.tag
        tag_text: str = (element.text or "").strip()
        tag_children: list = list(filter(None, [tag_text]))
        tag_attrs: dict = self._convert_data_attributes(element.attrib)
        tag_id: Optional[str] = element.attrib.get("id")
        component: Component = self._to_component(tag_name, **tag_attrs)
        if tag_id is not None:
            self._components[tag_id] = component
        if hasattr(component, "children"):
            component.children = tag_children
            for child in element.getchildren():  # type: _Element
                child_component: Component = self._build_tree(child)
                component.children.append(child_component)
        return component

    @classmethod
    def _convert_data_attributes(cls, attributes: dict) -> dict:
        """
        Convert `data-attr` attributes to `attr` as an evaluated literal

        Args:
            attributes: dictionary of HTML/XML attributes.

        Returns:
            Dictionary of attributes with `data-*` attributes
            converted to Python objects.
        """
        output: dict[str, Any] = dict(sorted(attributes.items()))
        converted_keys: set = set()
        generated_keys: dict = {}
        for key in output:
            key = key.lower()
            # Match keys named data-<name> and create a python object from that
            matching = re.match(r"^(data-)(\w+)", key)
            if matching:
                new_key = matching.groups()[1]
                generated_keys[new_key]: Any = evaluate(output[key])
                converted_keys.add(key)
        output.update(generated_keys)
        for key in converted_keys:
            del output[key]
        return output
