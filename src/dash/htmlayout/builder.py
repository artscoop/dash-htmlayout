"""Build layouts from HTML snippets."""
import sys
from importlib import import_module
from os import PathLike
from typing import Optional, Type

from dash.development.base_component import Component
from lxml import etree
from lxml.etree import _Element


class LayoutBuilder:
    """Build layouts using HTML snippets."""
    _module_registry = {
        "dash.html": None,
        "dash.dcc": "dcc",
        "dash.dash_table": "table",
        "dash_daq": "daq",
        "dash_bio": "bio",
        "dash_slicer": "slicer",
        "dash_player": "player",
        "dash_bootstrap_components": "bootstrap"
    }
    _component_registry: dict[str, type] = {}
    # List of modules with already autodetected components
    _autodetected_modules: set = set()
    # Layout root
    layout: Optional[Component] = None
    # Components with id
    _components: dict[str, Component] = {}

    def __new__(cls, *args, **kwargs):
        """Create a new LayoutBuilder object."""
        cls.autodetect()
        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def autodetect(cls):
        """Autodetect and register components from the module registry."""
        for module_name, prefix in cls._module_registry.items():
            try:
                if module_name not in cls._autodetected_modules:
                    module = import_module(module_name)
                    cls._autodetected_modules.add(module_name)
                    for attribute in dir(module):
                        symbol = getattr(module, attribute)
                        if isinstance(symbol, type) and issubclass(symbol, Component):
                            full_prefix: str = f"{prefix}." if prefix else ""
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
    def register_library(cls, path: str, prefix: Optional[str]) -> bool:
        """Register a new module providing Dash components."""
        if path not in cls._module_registry:
            cls._module_registry[path] = prefix
            cls.autodetect()
            return True
        return False

    def load_layout(self, path: PathLike) -> Component:
        """
        Build a layout from an HTML file.

        Returns:
            The root of the layout tree.
        """
        parser = etree.XMLParser(remove_comments=True, ns_clean=True, remove_pis=True)
        root = etree.parse(path, parser=parser).getroot()
        self._components = {}
        self.layout = self._build_tree(root)
        return self.layout

    def get_component(self, identifier: str) -> Optional[Component]:
        """Get component instance given an ID."""
        return self._components.get(identifier)

    @classmethod
    def to_component(cls, tag: str, **options) -> Optional[Component]:
        """Get a component from an HTML tag."""
        component: Optional[Type[Component]] = cls._component_registry.get(tag.lower(), None)
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
        tag_text: Optional[str] = element.text.strip() if element.text else None
        tag_children: list = [tag_text] if tag_text else []
        tag_attrs: dict = element.attrib
        tag_id: Optional[str] = element.attrib.get("id")
        component: Component = self.to_component(tag_name, **tag_attrs)
        if tag_id is not None:
            self._components[tag_id] = component
        if hasattr(component, "children"):
            component.children = tag_children
            for child in element.getchildren():  # type: _Element
                child_component: Component = self._build_tree(child)
                component.children.append(child_component)
        return component
