from qgis.core import *
from pathlib import Path
import os.path

PROJECT = QgsProject.instance()
ROOT = PROJECT.layerTreeRoot()
GROUP_LAYER = None
DIR_INPUT = None
DIR_OUTPUT = None
DIR_OUTPUT_ = None
DIR_PLUGIN = os.path.normpath(os.path.dirname(__file__))
DIR_STYLES = DIR_PLUGIN + os.sep + 'styles'
PATH_ABSOLUTE_PROJECT = os.path.normpath(PROJECT.readPath("./"))
ETUDES = None
LAYERS_NAME = {
                'APPUIS_COMAC':('appuis_comac', 'plugin'),
                'APPUIS_CAPFT':('appuis_capft', 'plugin'),
                'SITES_SUPPORTS':('sites_supports', 'main'),
                'CONTOURS_COMMUNES':('contours_communes', 'main'),
                'ZONE_DE_PA':('zone_de_pa', 'main'),
                'ZONE_DE_PM':('zone_de_pm', 'main'),
                'ZONE_DE_NRO':('zone_de_nro', 'main'),
                'POINT_PB':('point_pb', 'maj_pf'),
                'POINT_PA':('point_pa', 'project'),
                'POINT_PEP':('point_pep', 'project'),
                'SUPPORTS_RAS_PC':('supports_ras_pc', 'project'),
                'CABLE':('cable', 'maj_pf'),
                'INFRASTRUCTURE':('infrastructure', 'project'),
            }
GROUP_NAME = 'ETUDES_AERIENNES'
