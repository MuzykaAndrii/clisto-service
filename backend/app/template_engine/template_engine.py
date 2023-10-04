from typing import Mapping

from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)

from app.config import BASE_DIR


class TemplateEngine:
    def __init__(self, templates_path: str) -> None:
        self._engine = self._get_engine(templates_path)

    def _get_engine(self, templates_path: str) -> Environment:
        engine = Environment(
            loader=FileSystemLoader(BASE_DIR / templates_path),
            autoescape=select_autoescape(["html", "xml"]),
        )

        return engine

    def render_template(self, template_name: str, **fields: Mapping):
        template = self._engine.get_template(template_name)

        content = template.render(**fields)

        return content
