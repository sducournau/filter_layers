from qgis.core import *
from pathlib import Path
import os.path
import json


PROJECT = QgsProject.instance()
ROOT = PROJECT.layerTreeRoot()
DIR_PLUGIN = os.path.normpath(os.path.dirname(__file__))
PATH_ABSOLUTE_PROJECT = os.path.normpath(PROJECT.readPath("./"))
data = None

with open(DIR_PLUGIN + '/config/config.json') as f:
  data = json.load(f)

LAYERS_NAME = data['LAYERS_NAME']
FIELDS_NAME = data['FIELDS_NAME']
