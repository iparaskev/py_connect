"""m2t.py

The m2t enginge for producing code for handling the code generation.
"""

from jinja2 import Environment, FileSystemLoader


def generate():
    """Generate code"""
    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader)

    import_tmpl = env.get_template("pidevices_import.py.tmpl")
