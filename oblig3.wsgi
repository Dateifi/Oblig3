#!/usr/bin/python
activate_this = '/stud/mha665/public_html/oblig3/oblig3/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/stud/mha665/public_html/oblig3/")
sys.path.insert(1,"/stud/mha665/public_html/oblig3/oblig3/")

from oblig3 import app as application