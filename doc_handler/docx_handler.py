from pathlib import Path
import config
from docxtpl import DocxTemplate, InlineImage
import jinja2
from doc_handler.filters import filters
from doc_handler.jinja_env_functions import global_functions
from docx.shared import Mm
import config
import models as md


class SubdocFunction:
    def __init__(self, tpl, templates_folder):
        self.tpl = tpl
        self.templates_folder = templates_folder

    def __call__(self, template, context):
        path = self.templates_folder / f"{template}.docx"
        if not path.exists():
            print(f"Não foi encontrado o arquivo {path}")
            return
        subtpl = DocxTemplate(str(path))
        subtpl.render(context)
        sd = self.tpl.new_subdoc()
        sd.subdocx = subtpl.docx
        print(f"SUBDOC {path}")
        return sd


class SInlineImage:
    def __init__(self, tpl):
        self.tpl = tpl

    def __call__(self, file, width):
        path = Path(file)
        if not path.exists():
            return
        return InlineImage(self.tpl, file, width=Mm(width))


class DocxHandler:
    def __init__(self, model_name):
        self.model_name = model_name
        path = config.models_folder / model_name
        if not path.exists():
            raise Exception(f"Model {model_name} doesn't exist.")
        self.templates_folder = path / "templates"

    def make_jinja_env(self, tpl):
        jinja_env = jinja2.Environment()
        for filter_ in filters:
            jinja_env.filters[filter_.__name__] = filter_
        for function_ in global_functions:
            jinja_env.globals[function_.__name__] = function_
        jinja_env.globals['subdoc'] = SubdocFunction(
            tpl, self.templates_folder)
        jinja_env.globals['image'] = SInlineImage(tpl)
        return jinja_env

    def pre(self, context):
        function = getattr(md, self.model_name).pre.pre
        function(context)

    def render(self, context, file):
        path = self.templates_folder / "Main.docx"
        if not path.exists():
            raise Exception(f"Template {path} not found.")
        tpl = DocxTemplate(str(path))
        jinja_env = self.make_jinja_env(tpl)
        self.pre(context)
        tpl.render(context, jinja_env)
        tpl.save(file)
        return file
