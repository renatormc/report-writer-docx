import doc_handler.helpers as hp
import doc_handler.settings as settings
from pathlib import Path
from docxtpl import DocxTemplate, InlineImage


class SubdocGen:
    def __init__(self, jinja_env, tpl, widget):
        self.jinja_env = jinja_env
        self.tpl = tpl
        self.widget = widget

    def gen(self, item):
        self.sd = self.tpl.new_subdoc()
        for el in item:
            if el is None or el.text is None:
                continue
            hp.set_defaults_attrib(el)

            if el.tag == 'p':
                self.insert_paragraph(el)
            elif el.tag == 'li':
                self.insert_li(el)
            elif el.tag in ['h1', 'h2', 'h3', 'h4']:
                self.insert_heading(el)
            elif el.tag == 'img':
                self.insert_image(el)
            elif el.tag == 'caption':
                self.insert_caption(el)
        return self.sd

    def insert_paragraph(self, el):
        p = self.sd.add_paragraph(style=el.attrib['style'])
        # p.style = self.sd.styles[el.attrib['style']
        if el.attrib['indent'].lower() == 'false':
            p.paragraph_format.first_line_indent = settings.noindent
        if len(el) > 1:
            for el_ in el:
                self.gen(el_)
        else:
            lines = el.text.strip().split("\n")
            text= " ".join([line.strip() for line in lines if not line.isspace()])
            p.add_run(text)

    def insert_li(self, el):
        p = self.sd.add_paragraph(style='Enumeração')
        p.paragraph_format.first_line_indent = settings.noindent
        lines = el.text.strip().split("\n")
        text = " ".join([line.strip() for line in lines])
        p.add_run(text)

    def insert_heading(self, el):
        p = self.sd.add_paragraph()
        lines = el.text.split("\n")
        text = " ".join([line.strip() for line in lines])
        name = f"Heading {el.tag[1]}"
        p.style = self.sd.styles[name]
        p.add_run(text)

    def insert_image(self, el):
        width = hp.convert_value_unity(el.attrib['width'])
        path = self.widget.get_files_folder() / el.attrib['file']
        p = self.sd.add_paragraph()
        r = p.add_run()
        r.add_picture(str(path), width=width)
        # return InlineImage(tpl, str(path), width=width)

    def insert_caption(self, el):
        p = settings.subdoc_temp_folder / "caption.docx"
        tpl = DocxTemplate(str(p))
        tpl.render({'caption': el.text.strip()})
        for paragraph in tpl.get_docx().paragraphs:
            self.sd.add_paragraph(paragraph.text)
        # sd = self.tpl.new_subdoc()
        # sd.subdocx = tpl.get_docx()
