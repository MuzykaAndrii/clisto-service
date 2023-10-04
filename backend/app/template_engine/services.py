from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)

from app.config import BASE_DIR


class TemplateEngineService:
    @staticmethod
    def get_engine(templates_path: str) -> Environment:
        engine = Environment(
            loader=FileSystemLoader(BASE_DIR / templates_path),
            autoescape=select_autoescape(["html", "xml"]),
        )

        return engine
