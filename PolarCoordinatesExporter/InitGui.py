"""Initialization of the PolarCoordinatesExporter workbench (graphical interface)."""

import FreeCAD
import FreeCADGui
import path_utils

from PySide.QtCore import QT_TRANSLATE_NOOP

FreeCADGui.addPreferencePage(path_utils.get_workbench_file_path("preferences-export.ui"), QT_TRANSLATE_NOOP("PolarCoordinatesExporter", "Import-Export"))