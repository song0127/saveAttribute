# -*- coding: utf-8 -*-
"""
/***************************************************************************
 saveAttrivutes_V2
                                 A QGIS plugin
 this plugin save the attribute of the selected vector layer as CSV
                             -------------------
        begin                : 2017-07-03
        copyright            : (C) 2017 by song
        email                : teemo91256@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load saveAttrivutes_V2 class from file saveAttrivutes_V2.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .save_attrivutes import saveAttrivutes_V2
    return saveAttrivutes_V2(iface)
