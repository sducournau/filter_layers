# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FilterLayers
                                 A QGIS plugin
 Un plugin qui permet de filtrer les couches de votre projet FTTH
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-12-09
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Simon Ducournau
        email                : simon.ducournau@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt import QtGui
from qgis.PyQt.QtWidgets import *
from qgis.core import *
from qgis.gui import *
from qgis.utils import iface
from functools import partial
from qgis.PyQt.QtWidgets import QApplication

# Initialize Qt resources from file resources.py
from .resources import *
import os
# Import the code for the DockWidget
from .filter_layers_dockwidget import FilterLayersDockWidget
import os.path
from .utils import *

from qgis.PyQt.QtGui import QIcon

class FilterLayers:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """

        # app = QApplication.instance()
        # app.setStyleSheet(".QWidget {color: yellow; background-color: dark;}")
        # You can even read the stylesheet from a file




        # iface.mainWindow().setWindowTitle("WELCOME ... to ... CIRCET CORPORATION")

        # Save reference to the QGIS interface
        self.iface = iface
        self.current_index = 0
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'FilterLayers_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Outils Circet')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'FilterLayers')
        self.toolbar.setObjectName(u'FilterLayers')

        #print "** INITIALIZING FilterLayers"

        self.pluginIsActive = False
        self.dockwidget = None


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('FilterLayers', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/filter_layers/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Filtrer les couches'),
            callback=self.run,
            parent=self.iface.mainWindow())

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING FilterLayers"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False

    def managerTask(self, task_name):




        self.task_name = task_name
        t0 = time.time()
        print("FILTRING...")
        self.task_filter = FilterLayers_('Filtrer les couches' ,self.dockwidget, self.task_name,self.current_index)
        QgsApplication.taskManager().addTask(self.task_filter)

        self.populate.populate_za_nro
        self.populate.populate_za_zpm
        self.populate.populate_za_zpa
        self.populate.populate_commune

        selected_za_nro_data = self.dockwidget.comboBox_select_za_nro.checkedItems()
        selected_za_zpm_data = self.dockwidget.comboBox_select_za_zpm.checkedItems()
        selected_za_zpa_data = self.dockwidget.comboBox_select_za_zpa.checkedItems()
        selected_commune_data = self.dockwidget.comboBox_select_commune.checkedItems()

        if self.task_name == 'start':
            if len(selected_za_zpa_data) > 0:
                self.layer_zoom = PROJECT.mapLayersByName(LAYERS_NAME['ZONE_DE_PA'][0])[0]
            elif len(selected_za_zpm_data) > 0:
                self.layer_zoom = PROJECT.mapLayersByName(LAYERS_NAME['ZONE_DE_PM'][0])[0]
            elif len(selected_za_nro_data) > 0:
                self.layer_zoom = PROJECT.mapLayersByName(LAYERS_NAME['ZONE_DE_NRO'][0])[0]
            elif len(selected_commune_data) > 0:
                self.layer_zoom = PROJECT.mapLayersByName(LAYERS_NAME['CONTOURS_COMMUNES'][0])[0]
            else:
                self.layer_zoom = PROJECT.mapLayersByName(LAYERS_NAME['ZONE_DE_PM'][0])[0]




            self.task_filter.taskCompleted.connect(lambda: zoom_to_features(self.layer_zoom, t0))





    def select_tab_index(self, i):
        self.current_index = i

        if self.current_index == 0:
            self.populate.populate_layers()

        # elif self.current_index == 2:
        #     self.populate.populate_za_nro()
        #     self.populate.populate_za_zpm()
        #     self.populate.populate_za_zpa()
        #     self.populate.populate_commune()

    def update_expression(self, text):

        def get_text_cursor():
            return self.dockwidget.plainTextEdit_expression.textCursor()

        def set_text_cursor_pos(value):
            tc = get_text_cursor()
            tc.setPosition(value, QtGui.QTextCursor.KeepAnchor)
            self.dockwidget.plainTextEdit_expression.setTextCursor(tc)

        def get_text_cursor_pos():
            return get_text_cursor().position()

        def get_text_selection():
            cursor = get_text_cursor()
            return cursor.selectionStart(), cursor.selectionEnd()

        def set_text_selection(start, end):
            cursor = get_text_cursor()
            cursor.setPosition(start)
            cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
            self.dockwidget.plainTextEdit_expression.setTextCursor(cursor)


        expression = self.dockwidget.plainTextEdit_expression.toPlainText()
        pos = get_text_cursor_pos()
        pos1, pos2 = get_text_selection()
        print(pos1, pos2)
        if pos2 > 0:

            if pos1 < 1:
                expression  = text+expression[pos2:]
            else:
                expression  = expression[:pos1]+text+expression[pos2:]
        else:
            expression  = expression[:pos]+text+expression[pos:]
        self.dockwidget.plainTextEdit_expression.setPlainText(expression)
        set_text_selection(len(expression),len(expression))
        set_text_cursor_pos(len(expression))


    def insert_field(self):
        field_name = self.dockwidget.mFieldComboBox_insert_fields.currentText()
        expression = self.dockwidget.plainTextEdit_expression.toPlainText()
        expression += '"'+ field_name + '" '
        self.dockwidget.plainTextEdit_expression.setPlainText(expression)


    def resources_path(self, *args):
            """Get the path to our resources folder.

            :param args List of path elements e.g. ['img', 'logos', 'image.png']
            :type args: str

            :return: Absolute path to the resources folder.
            :rtype: str
            """
            path = str(self.plugin_dir) + str(os.sep()) + 'images'

            for item in args:
                path = path + str(os.sep()) + item


            return path


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD FilterLayers"

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Filtrage des couches'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    #--------------------------------------------------------------------------------#
    #                                 PLUGINS                                        #
    #--------------------------------------------------------------------------------#


    def change_background_color(self):
        color = self.dockwidget.mColorButton.color()
        color_value = color.name()
        style = "QWidget { background-color: %s; }" % color_value
        self.dockwidget.toolBox_filtre.setAutoFillBackground(True)
        self.dockwidget.toolBox_filtre.setStyleSheet(style)
        self.dockwidget.toolBox_filtre.update()


    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING FilterLayers"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = FilterLayersDockWidget()





                # comboBox_select_layers = CustomCheckableComboBox()
                # comboBox_select_layers.setObjectName('comboBox_select_layers')
                # comboBox_select_layers.setGeometry(200, 150, 120, 50)
                # comboBox_select_layers.setEditable(True)
                # comboBox_select_layers.setDefaultText('Couches à filtrer')
                #
                #
                # comboBox_select_za_nro = CustomCheckableComboBox()
                # comboBox_select_za_nro.setObjectName('comboBox_select_za_nro')
                # comboBox_select_za_nro.setGeometry(200, 150, 120, 50)
                # comboBox_select_za_nro.setEditable(True)
                # comboBox_select_za_nro.setDefaultText('NRO')
                #
                #
                # comboBox_select_za_zpm = CustomCheckableComboBox()
                # comboBox_select_za_zpm.setObjectName('comboBox_select_za_zpm')
                # comboBox_select_za_zpm.setGeometry(200, 150, 120, 50)
                # comboBox_select_za_zpm.setEditable(True)
                # comboBox_select_za_zpm.setDefaultText('PMZ')
                #
                #
                # comboBox_select_commune = CustomCheckableComboBox()
                # comboBox_select_commune.setObjectName('comboBox_select_commune')
                # comboBox_select_commune.setGeometry(200, 150, 120, 50)
                # comboBox_select_commune.setEditable(True)
                # comboBox_select_commune.setDefaultText('Commune')
                #
                # self.dockwidget.verticalLayout_header.addWidget(comboBox_select_layers)
                # self.dockwidget.formLayout_basique.addWidget(comboBox_select_za_nro)
                # self.dockwidget.formLayout_basique.addWidget(comboBox_select_za_zpm)
                # self.dockwidget.formLayout_basique.addWidget(comboBox_select_commune)
                #
                # self.dockwidget.comboBox_select_layers = self.dockwidget.findChild(QComboBox, 'comboBox_select_layers')
                # self.dockwidget.comboBox_select_za_nro = self.dockwidget.findChild(QComboBox, 'comboBox_select_za_nro')
                # self.dockwidget.comboBox_select_za_zpm = self.dockwidget.findChild(QComboBox, 'comboBox_select_za_zpm')
                # self.dockwidget.comboBox_select_commune = self.dockwidget.findChild(QComboBox, 'comboBox_select_commune')

                self.populate = populateComboBox(self.dockwidget)
                self.populate.populate_layers()
                self.populate.populate_za_nro()
                self.populate.populate_za_zpm()
                self.populate.populate_za_zpa()
                self.populate.populate_commune()

                self.dockwidget.comboBox_select_za_nro.currentIndexChanged.connect(self.populate.populate_za_zpm)
                self.dockwidget.comboBox_select_za_nro.currentIndexChanged.connect(self.populate.populate_za_zpa)
                self.dockwidget.comboBox_select_za_nro.currentIndexChanged.connect(self.populate.populate_commune)

                self.dockwidget.comboBox_select_za_zpm.currentIndexChanged.connect(self.populate.populate_za_zpa)

                self.dockwidget.pushButton_filter_start.clicked.connect(partial(self.managerTask,'start'))
                self.dockwidget.pushButton_filter_end.clicked.connect(partial(self.managerTask,'end'))
                self.dockwidget.toolBox_filtre.currentChanged.connect(self.select_tab_index)

                self.dockwidget.pushButton_equal.clicked.connect(partial(self.update_expression,self.dockwidget.pushButton_equal.text()))
                self.dockwidget.pushButton_and.clicked.connect(partial(self.update_expression,self.dockwidget.pushButton_and.text()))
                self.dockwidget.pushButton_ilike.clicked.connect(partial(self.update_expression,self.dockwidget.pushButton_ilike.text()))
                self.dockwidget.pushButton_in.clicked.connect(partial(self.update_expression,self.dockwidget.pushButton_in.text()))
                self.dockwidget.pushButton_inferior.clicked.connect(partial(self.update_expression,self.dockwidget.pushButton_inferior.text()))
                self.dockwidget.pushButton_inferior_or_equal.clicked.connect(partial(self.update_expression,self.dockwidget.pushButton_inferior_or_equal.text()))
                self.dockwidget.pushButton_joker.clicked.connect(partial(self.update_expression,self.dockwidget.pushButton_joker.text()))
                self.dockwidget.pushButton_like.clicked.connect(partial(self.update_expression,self.dockwidget.pushButton_like.text()))
                self.dockwidget.pushButton_not.clicked.connect(partial(self.update_expression,self.dockwidget.pushButton_not.text()))
                self.dockwidget.pushButton_not_equal.clicked.connect(partial(self.update_expression,self.dockwidget.pushButton_not_equal.text()))
                self.dockwidget.pushButton_concat.clicked.connect(partial(self.update_expression,self.dockwidget.pushButton_concat.text()))
                self.dockwidget.pushButton_regex.clicked.connect(partial(self.update_expression,self.dockwidget.pushButton_regex.text()))
                self.dockwidget.pushButton_null.clicked.connect(partial(self.update_expression,self.dockwidget.pushButton_null.text()))
                self.dockwidget.pushButton_or.clicked.connect(partial(self.update_expression,self.dockwidget.pushButton_or.text()))
                self.dockwidget.pushButton_superior.clicked.connect(partial(self.update_expression,self.dockwidget.pushButton_superior.text()))
                self.dockwidget.pushButton_superior_or_equal.clicked.connect(partial(self.update_expression,self.dockwidget.pushButton_superior_or_equal.text()))

                icon = QtGui.QIcon(os.path.join(DIR_PLUGIN,  "images/filter.png"))
                self.dockwidget.pushButton_filter_start.setIcon(icon)


                icon = QtGui.QIcon(os.path.join(DIR_PLUGIN,  "images/filter_erase.png"))
                self.dockwidget.pushButton_filter_end.setIcon(icon)



                icon = QtGui.QIcon(os.path.join(DIR_PLUGIN,  "images/filter_multi.png"))


                self.dockwidget.checkBox_filter_from.setIcon(icon)


                #plugins

                self.dockwidget.pushButton_color.clicked.connect(self.change_background_color)



                self.dockwidget.comboBox_multi_layers.currentTextChanged.connect(self.populate.populate_fields_multi)
            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()
