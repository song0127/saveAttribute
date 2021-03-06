# -*- coding: utf-8 -*-
"""
/***************************************************************************
 saveAttrivutes_V2
                                 A QGIS plugin
 this plugin save the attribute of the selected vector layer as CSV
                              -------------------
        begin                : 2017-07-03
        git sha              : $Format:%H$
        copyright            : (C) 2017 by song
        email                : teemo91256@gmail.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from save_attrivutes_dialog import saveAttrivutes_V2Dialog
import os.path
from PyQt4 import QtGui


class saveAttrivutes_V2:
    """QGIS Plugin Implementation."""
    
    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        self.dlg = saveAttrivutes_V2Dialog()
        
        
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'saveAttrivutes_V2_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&save Attrivutes_V2')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'saveAttrivutes_V2')
        self.toolbar.setObjectName(u'saveAttrivutes_V2')
        
        self.dlg.lineEdit.clear()
        self.dlg.pushButton.clicked.connect(self.select_output_file)
        self.dlg.checkBox_3.stateChanged.connect(self.open_close_layer)
        
        #self.initGUI()
        
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
        return QCoreApplication.translate('saveAttrivutes_V2', message)

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
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/saveAttrivutes_V2/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Save attributes_V2 as CSV'),
            callback=self.run,
            parent=self.iface.mainWindow())
        
        
       
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&save Attrivutes_V2'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def select_output_file(self):
        filename = QFileDialog.getSaveFileName(self.dlg, "Select output file ","", '*.txt')
        self.dlg.lineEdit.setText(filename)
        
    def open_close_layer(self,value):
        legend = self.iface.legendInterface()
        if value:
            legend.setLayerVisible(layers[i], True)
            self.dlg.label_3.setText(str(layers[0]))
        else :
            legend.setLayerVisible(layers[0], False)
            self.dlg.label_3.setText("UNCHECKED!")
            
     
            
    def run(self):
        """Run method that performs all the real work"""
        global selectedLayerIndex
        #selectedLayerIndex = self.dlg.comboBox.currentIndex()
        #selectedLayerIndex = 0
        #global selectedLayer
        global layers
        layers = self.iface.legendInterface().layers()
        layer_list = []
        for layer in layers:
            layer_list.append(layer.name())
        #selectedLayer = layers[selectedLayerIndex]
        
        # show the dialog
        self.dlg.show()
        grid = self.dlg.gridLayout
        
        for i in range(0,len(layer_list)):
            #checkBox = QtGui.QCheckBox(layer_list[i])
            locals()['checkBox'+str(i)] = QtGui.QCheckBox(layer_list[i])
            #checkBox.setObjectName(layer[i])
            grid.addWidget(locals()['checkBox'+str(i)],i,0)
            locals()['checkBox'+str(i)].stateChanged.connect(self.open_close_layer)
        
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            filename = self.dlg.lineEdit.text()
            output_file = open(filename, 'w')
            fields = selectedLayer.pendingFields()
            fieldnames = [field.name() for field in fields]			

            for f in selectedLayer.getFeatures():
                line = ','.join(unicode(f[x]) for x in fieldnames) + '\n'
                unicode_line = line.encode('utf-8')
                output_file.write(unicode_line)
            output_file.close()

