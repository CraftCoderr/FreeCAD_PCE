"""Initialization of the PolarCoordinatesExporter workbench (graphical interface)."""

import FreeCAD
import FreeCADGui

from PySide.QtCore import QT_TRANSLATE_NOOP

FreeCADGui.addPreferencePage("Mod/PolarCoordinatesExporter/preferences-export.ui", QT_TRANSLATE_NOOP("PolarCoordinatesExporter", "Import-Export"))