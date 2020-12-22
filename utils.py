from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.core import *
from qgis.utils import *
import os.path
from pathlib import Path
import re
from .config import *

class FilterLayers_(QgsTask):


    def __init__(self, description, dockwidget, action, current_index):

        QgsTask.__init__(self, description)

        self.exception = None
        self.dockwidget = dockwidget
        self.action = action
        self.current_index = current_index
        self.populate = populateComboBox(self.dockwidget)

        self.filter_from = self.dockwidget.checkBox_filter_from.checkState()
        print(self.current_index)

    def create_expressions(self, field):

        def create_expression_za_nro(field):

            list_za_nro = {}
            list_za_nro['sql'] = []
            list_za_nro['shape'] = []

            for item in self.selected_za_nro_data:
                list_za_nro['sql'].append(field + ' ~ \'' + str(item) + '$\'' + ' OR ' +  field + ' ~ \''  + str(item) + ',\'' )
                list_za_nro['shape'].append(field + ' LIKE \'' + str(item) + '\'' )
            self.filter_za_nro['sql'] = ' OR '.join(list_za_nro['sql'])
            self.filter_za_nro['shape'] = ' OR '.join(list_za_nro['shape'])

        def create_expression_za_zpm(field):

            list_za_zpm = {}
            list_za_zpm['sql'] = []
            list_za_zpm['shape'] = []

            list_za_nro = {}
            list_za_nro['sql'] = []
            list_za_nro['shape'] = []

            for item in self.selected_za_zpm_data:

                field = '"za_zpm"'
                list_za_zpm['sql'].append(field + ' ~ \'' + str(item) + '$\'' + ' OR ' +  field + ' ~ \''  + str(item) + ',\'' )
                list_za_zpm['shape'].append(field + ' LIKE \'' + str(item) + '\'' )

                field = '"za_nro"'
                list_za_nro['sql'].append(field + ' ~ \'' + str(item[:5]) + '$\'' + ' OR ' +  field + ' ~ \''  + str(item[:5]) + ',\'' )
                list_za_nro['shape'].append(field + ' LIKE \'' + str(item[:5]) + '\'' )

            self.filter_za_zpm['sql'] = ' OR '.join(list_za_zpm['sql'])
            self.filter_za_zpm['shape'] = ' OR '.join(list_za_zpm['shape'])


            self.filter_za_nro['sql'] = ' OR '.join(list_za_nro['sql'])
            self.filter_za_nro['shape'] = ' OR '.join(list_za_nro['shape'])


        def create_expression_za_zpa(field):

            list_za_zpa = {}
            list_za_zpa['sql'] = []
            list_za_zpa['shape'] = []

            list_za_zpm = {}
            list_za_zpm['sql'] = []
            list_za_zpm['shape'] = []

            list_za_nro = {}
            list_za_nro['sql'] = []
            list_za_nro['shape'] = []

            for item in self.selected_za_zpa_data:
                item_zpm = re.search('[A-Z0-9_]*_PA',item)[0][:-3]

                field = '"za_zpa"'
                list_za_zpa['sql'].append(field + ' ~ \'' + str(item) + '$\'' + ' OR ' +  field + ' ~ \'' + str(item) + ',\'' )
                list_za_zpa['shape'].append(field + ' LIKE \'' + str(item) + '\'' )

                field = '"za_zpm"'
                list_za_zpm['sql'].append(field + ' ~ \'' + str(item_zpm) + '$\'' + ' OR ' +  field + ' ~ \''  + str(item_zpm) + ',\'' )
                list_za_zpm['shape'].append(field + ' LIKE \'' + str(item_zpm) + '\'' )

                field = '"za_nro"'
                list_za_nro['sql'].append(field + ' ~ \'' + str(item[:5]) + '$\'' + ' OR ' +  field + ' ~ \''  + str(item[:5]) + ',\'' )
                list_za_nro['shape'].append(field + ' LIKE \'' + str(item[:5]) + '\'' )

            self.filter_za_zpa['sql'] = ' OR '.join(list_za_zpa['sql'])
            self.filter_za_zpa['shape'] = ' OR '.join(list_za_zpa['shape'])

            self.filter_za_zpm['sql'] = ' OR '.join(list_za_zpm['sql'])
            self.filter_za_zpm['shape'] = ' OR '.join(list_za_zpm['shape'])

            self.filter_za_nro['sql'] = ' OR '.join(list_za_nro['sql'])
            self.filter_za_nro['shape'] = ' OR '.join(list_za_nro['shape'])


        def create_expression_commune(field):

            list_commune = {}
            list_commune['sql'] = []
            list_commune['shape'] = []

            for item in self.selected_commune_data:

                field = '"commune"'
                list_commune['sql'].append(field + ' ~ \'' + str(item) + '$\'' + ' OR ' +  field + ' ~ \''  + str(item) + ',\'' )
                list_commune['shape'].append(field + ' LIKE \'' + str(item) + '\'')
            self.filter_commune['sql'] = ' OR '.join(list_commune['sql'])
            self.filter_commune['shape'] = ' OR '.join(list_commune['shape'])



        if field == 'za_nro':
            create_expression_za_nro(field)

        elif field == 'za_zpm':
            create_expression_za_zpm(field)

        if field == 'za_zpa':
            create_expression_za_zpa(field)

        if field == 'commune':
            create_expression_commune(field)





    def filter_basic(self):

        if len(self.selected_za_nro_data) > 0:

            self.create_expressions('za_nro')

            for layer in self.layers['sql']:
                field_zpm_idx = layer.fields().indexFromName('za_nro')
                if field_zpm_idx != -1:
                    layer.setSubsetString(self.filter_za_nro['sql'])

            for layer in self.layers['shape']:
                field_zpm_idx = layer.fields().indexFromName('za_nro')
                if field_zpm_idx != -1:
                    layer.setSubsetString(self.filter_za_nro['shape'])

            if len(self.selected_za_zpm_data) < 1:
                self.populate.populate_za_zpm()
            if len(self.selected_za_zpa_data) < 1:
                self.populate.populate_za_zpa()
            if len(self.selected_commune_data) < 1:
                self.populate.populate_commune()


        if len(self.selected_za_zpm_data) > 0:

            self.create_expressions('za_zpm')

            for layer in self.layers['sql']:
                field_zpm_idx = layer.fields().indexFromName('za_zpm')
                if field_zpm_idx == -1:
                    layer.setSubsetString(self.filter_za_nro['sql'])
                else:
                    layer.setSubsetString(self.filter_za_zpm['sql'])

            for layer in self.layers['shape']:
                field_zpm_idx = layer.fields().indexFromName('za_zpm')
                if field_zpm_idx == -1:
                    layer.setSubsetString(self.filter_za_nro['shape'])
                else:
                    layer.setSubsetString(self.filter_za_zpm['shape'])

            if len(self.selected_commune_data) < 1:
                self.populate.populate_commune()
            if len(self.selected_za_zpa_data) < 1:
                self.populate.populate_za_zpa()



        if len(self.selected_za_zpa_data) > 0:

            self.create_expressions('za_zpa')

            for layer in self.layers:
                for layer in self.layers['sql']:
                    field_zpm_idx = layer.fields().indexFromName('za_zpm')
                    field_zpa_idx = layer.fields().indexFromName('za_zpa')
                    if field_zpa_idx != -1 and field_zpm_idx != -1:
                        layer.setSubsetString(self.filter_za_zpa['sql'])
                    elif field_zpa_idx == -1 and field_zpm_idx != -1:
                        layer.setSubsetString(self.filter_za_zpm['sql'])
                    elif field_zpm_idx == -1:
                        layer.setSubsetString(self.filter_za_nro['sql'])


                for layer in self.layers['shape']:
                    field_zpm_idx = layer.fields().indexFromName('za_zpm')
                    field_zpa_idx = layer.fields().indexFromName('za_zpa')
                    if field_zpa_idx != -1 and field_zpm_idx != -1:
                        layer.setSubsetString(self.filter_za_zpa['shape'])
                    elif field_zpa_idx == -1 and field_zpm_idx != -1:
                        layer.setSubsetString(self.filter_za_zpm['shape'])
                    elif field_zpm_idx == -1:
                        layer.setSubsetString(self.filter_za_nro['shape'])


        if len(self.selected_commune_data) > 0:

            self.create_expressions('commune')

            field_name = 'za_zpm'
            from_layer = PROJECT.mapLayersByName(LAYERS_NAME['CONTOURS_COMMUNES'][0])[0]
            if 'dbname' in from_layer.dataProvider().dataSourceUri():
                layer_type = 'sql'
                expression = self.filter_commune['sql']
            else:
                layer_type = 'shape'
                expression = self.filter_commune['shape']
            self.filter_from = 2
            self.filter_advanced(expression,from_layer, field_name)





    def filter_advanced(self, expression, from_layer, field_name):



        print(expression)
        if self.filter_from == 2:

            if len(self.selected_za_nro_data) > 0:
                from_layer.setSubsetString('(' + self.filter_za_nro[layer_type] + ') AND ' + expression)

            elif len(self.selected_za_zpm_data) > 0:
                from_layer.setSubsetString('(' + self.filter_za_zpm[layer_type] + ') AND ' + expression)

            elif len(self.selected_za_zpa_data) > 0:
                from_layer.setSubsetString('(' + self.filter_za_zpa[layer_type] + ') AND ' + expression)

            else:
                from_layer.setSubsetString(expression)


            idx = from_layer.fields().indexFromName(field_name)
            list_items = []

            selected_items = {}
            selected_items['sql'] = []
            selected_items['shape'] = []

            self.filter_items = {}
            self.filter_items['sql'] = ''
            self.filter_items['shape'] = ''

            for feature in from_layer.getFeatures():
                feature_field = feature.attributes()[idx]
                if feature_field != NULL:
                    if ',' in feature_field:
                        feature_array = feature_field.split(',')
                        for feat_field in feature_array:
                            if feat_field not in list_items:
                                list_items.append(feat_field)

                    else:
                        if feature_field not in list_items:
                            list_items.append(feature_field)


            for item in list_items:
                selected_items['sql'].append('"' + str(field_name) + '" ~ \'' + str(item) + '$\'' + ' OR "' +  str(field_name) + '" ~ \'' + str(item) + ',\'' )
                selected_items['shape'].append('"' + str(field_name) + '" LIKE \'' + str(item) + '\'')

            self.filter_items['sql'] = ' OR '.join(selected_items['sql'])
            self.filter_items['shape'] = ' OR '.join(selected_items['shape'])

            for layer in self.layers['sql']:
                if layer.name() != from_layer.name():
                    field_idx = layer.fields().indexFromName(field_name)
                    if field_idx == -1:
                        print('Le champ ' + field_name + ' non présent dans la couche ' + layer.name())
                    else:
                        layer.setSubsetString(self.filter_items['sql'])

            for layer in self.layers['shape']:
                if layer.name() != from_layer.name():
                    field_idx = layer.fields().indexFromName(field_name)
                    if field_idx == -1:
                        print('Le champ ' + field_name + ' non présent dans la couche ' + layer.name())
                    else:
                        layer.setSubsetString(self.filter_items['shape'])




        else:
            if len(self.selected_za_nro_data) > 0:
                from_layer.setSubsetString('(' + self.filter_za_nro[layer_type] + ') AND ' + expression)

            elif len(self.selected_za_zpm_data) > 0:


                field_idx = layer.fields().indexFromName(field_name)
                if field_idx == -1:
                    print('Le champ ' + field_name + ' non présent dans la couche ' + layer.name())
                else:
                    from_layer.setSubsetString('(' + self.filter_za_zpm[layer_type] + ') AND ' + expression)

            elif len(self.selected_za_zpa_data) > 0:


                field_zpm_idx = layer.fields().indexFromName('za_zpm')
                field_zpa_idx = layer.fields().indexFromName('za_zpa')
                if field_zpa_idx == -1 and field_zpm_idx != -1:
                    from_layer.setSubsetString('(' + self.filter_za_zpm[layer_type] + ') AND ' + expression)
                elif field_zpm_idx == -1:
                    from_layer.setSubsetString('(' + self.filter_za_nro[layer_type] + ') AND ' + expression)
                else:
                    from_layer.setSubsetString('(' + self.filter_za_zpa[layer_type] + ') AND ' + expression)

            elif len(self.selected_commune_data) > 0:
                from_layer.setSubsetString(self.filter_commune[layer_type] + ' AND ' + expression)
            else:
                from_layer.setSubsetString(expression)




    def run(self):

        try:
            self.layers = {}
            self.layers['sql'] = []
            self.layers['shape'] = []

            selected_layers_data = self.dockwidget.comboBox_select_layers.checkedItems()

            for item in selected_layers_data:

                layer =  PROJECT.mapLayersByName(item)[0]
                if 'dbname' in layer.dataProvider().dataSourceUri():
                    self.layers['sql'].append(layer)

                else:
                    self.layers['shape'].append(layer)




            if self.action == 'start':

                self.selected_za_nro_data = self.dockwidget.comboBox_select_za_nro.checkedItems()
                self.selected_za_zpm_data = self.dockwidget.comboBox_select_za_zpm.checkedItems()
                self.selected_za_zpa_data = self.dockwidget.comboBox_select_za_zpa.checkedItems()
                self.selected_commune_data = self.dockwidget.comboBox_select_commune.checkedItems()

                self.filter_za_nro = {}
                self.filter_za_nro['sql'] = ''
                self.filter_za_nro['shape'] = ''

                self.filter_za_zpm = {}
                self.filter_za_zpm['sql'] = ''
                self.filter_za_zpm['shape'] = ''

                self.filter_za_zpa = {}
                self.filter_za_zpa['sql'] = ''
                self.filter_za_zpa['shape'] = ''

                self.filter_commune = {}
                self.filter_commune['sql'] = ''
                self.filter_commune['shape'] = ''


                if self.current_index != 3:

                    self.filter_basic()


                elif self.current_index == 3:

                    expression = self.dockwidget.plainTextEdit_expression.toPlainText()
                    expression = expression.replace("'", "\'")
                    layer_name = self.dockwidget.comboBox_multi_layers.currentText()
                    field_name = self.dockwidget.mFieldComboBox_multi_fields.currentText()
                    from_layer = PROJECT.mapLayersByName(layer_name)[0]
                    self.filter_advanced(expression, from_layer, field_name)

            if self.action == 'end':
                for layer in self.layers['sql']:
                    if isinstance(layer, QgsVectorLayer):
                        iface.vectorLayerTools().stopEditing(layer,False)
                        layer.setSubsetString('')
                for layer in self.layers['shape']:
                    if isinstance(layer, QgsVectorLayer):
                        iface.vectorLayerTools().stopEditing(layer,False)
                        layer.setSubsetString('')
                self.populate.populate_za_nro()
                self.populate.populate_za_zpm()
                self.populate.populate_za_zpa()
                self.populate.populate_commune()

            return True
        except Exception as e:
            self.exception = e
            print(self.exception)
            return False


    def finished(self, result):
        """This function is called automatically when the task is completed and is
        called from the main thread so it is safe to interact with the GUI etc here"""
        if result is False:
            if self.exception is None:
                iface.messageBar().pushMessage('Task was cancelled')
            else:
                iface.messageBar().pushMessage('Errors occured')
                print(self.exception)

        else:
            print('Couches filtrées')


class barProgress:

    def __init__(self):
        self.prog = 0
        self.bar = None
        self.type = type
        iface.messageBar().clearWidgets()
        self.init()
        self.bar.show()

    def init(self):
        self.bar = QProgressBar()
        self.bar.setMaximum(100)
        self.bar.setValue(self.prog)
        iface.mainWindow().statusBar().addWidget(self.bar)

    def show(self):
        self.bar.show()


    def update(self, prog):
        self.bar.setValue(prog)

    def hide(self):
        self.bar.hide()

class msgProgress:

    def __init__(self):
        self.messageBar = iface.messageBar().createMessage('Doing something time consuming...')
        self.progressBar = QProgressBar()
        self.progressBar.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.cancelButton = QPushButton()
        self.cancelButton.setText('Cancel')
        self.messageBar.layout().addWidget(self.progressBar)
        self.messageBar.layout().addWidget(self.cancelButton)
        iface.messageBar().pushWidget(self.messageBar, Qgis.Info)


    def update(self, prog):
        self.progressBar.setValue(prog)

    def reset(self):
        self.progressBar.setValue(0)

    def setText(self, text):
        self.messageBar.setText(text)




def zoom_to_features(layer, t0):
    end = time.time() - t0
    iface.mainWindow().setWindowTitle("DONE" + " IN " + str(end) + " s.")
    canvas = iface.mapCanvas()
    canvas.setExtent(layer.extent())
    canvas.refresh()


class populateComboBox:

    def __init__(self, dockwidget):
        self.dockwidget = dockwidget
        self.exception = None


    def checkState(self, combobox):


        print(combobox.itemCheckState(0))
        if combobox.itemCheckState(0) == 2:
            combobox.selectAllOptions()
        elif combobox.itemCheckState(0) == 0:
            combobox.deselectAllOptions()


    def populate_layers(self):

        layers = PROJECT.mapLayers().values()



        list_layers = []
        for layer in layers:
            if isinstance(layer, QgsVectorLayer):
                layer_name = layer.name()
                list_layers.append(layer_name)




        self.dockwidget.comboBox_multi_layers.clear()
        self.dockwidget.comboBox_select_layers.clear()
        self.dockwidget.comboBox_multi_layers.addItems(list_layers)
        self.dockwidget.comboBox_select_layers.addItems(list_layers)
        self.dockwidget.comboBox_select_layers.selectAllOptions()


    def populate_fields_multi(self, layer_name):
        try:
            print(layer_name)
            if layer_name != '':
                layer = PROJECT.mapLayersByName(layer_name)[0]
                self.dockwidget.mFieldComboBox_multi_fields.setLayer(layer)

        except Exception as e:
            self.exception = e
            print(self.exception)
            return False


    def populate_za_nro(self):


        try:
            print('populate_nro')
            list_za_nro = []

            layer = PROJECT.mapLayersByName(LAYERS_NAME['ZONE_DE_NRO'][0])[0]
            idx = layer.fields().indexFromName('za_nro')

            for feature in layer.getFeatures():

                if feature.attributes()[idx] not in list_za_nro:
                    list_za_nro.append(str(feature.attributes()[idx]))


            list_za_nro = sorted(list_za_nro)
            self.dockwidget.comboBox_select_za_nro.clear()
            self.dockwidget.comboBox_select_za_nro.addItems(list_za_nro)

        except Exception as e:
            self.exception = e
            print(self.exception)
            return False

    def populate_za_zpm(self):

        try:
            print('populate_pmz')
            list_za_zpm = []

            layer = PROJECT.mapLayersByName(LAYERS_NAME['ZONE_DE_PM'][0])[0]
            idx = layer.fields().indexFromName('za_zpm')

            selected_za_nro_data = self.dockwidget.comboBox_select_za_nro.checkedItems()
            selected_za_nro = []

            if len(selected_za_nro_data) > 0:
                for item in selected_za_nro_data:
                    selected_za_nro.append('"za_nro"  ILIKE \'' + str(item) + '\'')
                filter_za_nro = ' OR '.join(selected_za_nro)

                layer.selectByExpression(filter_za_nro, QgsVectorLayer.SetSelection)
                layer_selection = layer.selectedFeatures()

            else:
                layer_selection = layer.getFeatures()

            for feature in layer_selection:
                if feature.attributes()[idx] not in list_za_zpm:
                    list_za_zpm.append(str(feature.attributes()[idx]))

            layer.removeSelection()




            list_za_zpm = sorted(list_za_zpm)
            self.dockwidget.comboBox_select_za_zpm.clear()
            self.dockwidget.comboBox_select_za_zpm.addItems(list_za_zpm)

        except Exception as e:
            self.exception = e
            print(self.exception)
            return False

    def populate_za_zpa(self):

        try:
            print('populate_zpa')
            list_za_zpa = []

            layer = PROJECT.mapLayersByName(LAYERS_NAME['ZONE_DE_PA'][0])[0]
            idx = layer.fields().indexFromName('za_zpa')

            selected_za_nro_data = self.dockwidget.comboBox_select_za_nro.checkedItems()
            selected_za_zpm_data = self.dockwidget.comboBox_select_za_zpm.checkedItems()
            selected_za_nro = []
            selected_za_zpm = []


            if len(selected_za_nro_data) > 0 and len(selected_za_zpm_data) < 1:
                for item in selected_za_nro_data:
                    selected_za_nro.append('"za_nro"  ILIKE \'' + str(item) + '\'')
                filter_za_nro = ' OR '.join(selected_za_nro)
                layer.selectByExpression(filter_za_nro, QgsVectorLayer.SetSelection)
                layer_selection = layer.selectedFeatures()

            elif (len(selected_za_zpm_data) > 0 and len(selected_za_nro_data) < 1) or (len(selected_za_zpm_data) > 0 and len(selected_za_nro_data) > 0):
                for item in selected_za_zpm_data:
                    selected_za_zpm.append('"za_zpm"  ILIKE \'' + str(item) + '\'')
                filter_za_zpm = ' OR '.join(selected_za_nro)
                layer.selectByExpression(filter_za_zpm, QgsVectorLayer.SetSelection)
                layer_selection = layer.selectedFeatures()


            elif len(selected_za_nro_data) < 1 and len(selected_za_zpm_data) < 1:
                layer_selection = layer.getFeatures()

            for feature in layer_selection:
                if feature.attributes()[idx] not in list_za_zpa:
                    list_za_zpa.append(str(feature.attributes()[idx]))

            layer.removeSelection()




            list_za_zpa = sorted(list_za_zpa)
            self.dockwidget.comboBox_select_za_zpa.clear()
            self.dockwidget.comboBox_select_za_zpa.addItems(list_za_zpa)

        except Exception as e:
            self.exception = e
            print(self.exception)
            return False
    def populate_commune(self):

        try:
            print('populate_commune')
            list_commune = []

            layer = PROJECT.mapLayersByName(LAYERS_NAME['CONTOURS_COMMUNES'][0])[0]
            idx = layer.fields().indexFromName('commune')

            selected_za_nro_data = self.dockwidget.comboBox_select_za_nro.checkedItems()
            selected_za_nro = []

            if len(selected_za_nro_data) > 0:
                for item in selected_za_nro_data:
                    selected_za_nro.append('"za_nro"  ILIKE \'' + str(item) + '\'')
                filter_za_nro = ' OR '.join(selected_za_nro)

                layer.selectByExpression(filter_za_nro, QgsVectorLayer.SetSelection)
                layer_selection = layer.selectedFeatures()

            else:
                layer_selection = layer.getFeatures()

            for feature in layer_selection:
                if feature.attributes()[idx] not in list_commune:
                    list_commune.append(str(feature.attributes()[idx]))

            layer.removeSelection()


            list_commune = sorted(list_commune)
            self.dockwidget.comboBox_select_commune.clear()
            self.dockwidget.comboBox_select_commune.addItems(list_commune)

        except Exception as e:
            self.exception = e
            print(self.exception)
            return False
