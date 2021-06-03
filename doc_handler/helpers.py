from datetime import datetime
import config
import doc_handler.settings as settings
from docx.shared import Pt, Mm, Cm
import re


def random_docx():
    aux = int(datetime.now().timestamp())
    return config.TEMPFOLDER / f"{aux}.docx"


def set_defaults_attrib(el):
    keys = el.attrib.keys()
    if el.tag in settings.defaults.keys():
        for key, value in settings.defaults[el.tag].items():
            if key not in keys:
                el.attrib[key] = value


def to_points(value):
    value = value.replace(" ", "")
    if value.endswith('cm'):
        w = float(value.replace("cm", ""))
        return float(w) * 0.393701 * 72
    if "/" in value:
        n, d = value.split("/")
        return (int(n) / int(d)) * settings.doc_width * 0.393701 * 72
    return (float(value) * settings.doc_width * 0.393701) * 72


def convert_value_unity(value):
    unities = {
        "pt": Pt,
        "mm": Mm,
        "cm": Cm
    }
    value = value.replace(" ", "")
    number, unity = re.search(r'(\d+(?:\.\d+)?)(.*)', value).groups()
    try:
        return unities[unity.lower()](float(number))
    except:
        pass
