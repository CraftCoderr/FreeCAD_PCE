
import FreeCAD
import math

if FreeCAD.GuiUp:
    from PySide import QtGui
    import FreeCADGui
    gui = True
else:
    gui = False

if open.__module__ in ['__builtin__', 'io']:
    pythonopen = open

COMMAND_FORMAT = "C{:.3f}X{:.2f}"

def cartesian_to_polar(x, y):
    r = math.sqrt(x ** 2 + y ** 2)
    fi = 0.0
    if y >= 0 and r != 0:
        fi = math.acos(x / r)
    elif y < 0:
        fi = -math.acos(x / r)

    return r, fi

def to_degrees(a):
    return a * (180.0 / math.pi) + 180.0

def export(exportList, filename):
    """Export custom format.
    Parameters
    ----------
    exportList : list
        List of document objects to export.
    filename : str
        Path to the new file.
    Returns
    -------
    None
        If `exportList` doesn't have shapes to export.
    """


    _prefs = "User parameter:BaseApp/Preferences/Mod/PolarCoordinatesExporter"
    parameters = FreeCAD.ParamGet(_prefs)

    step = parameters.GetFloat('discretizationStep')
    x_accuracy = parameters.GetFloat('xCoordinateAccuracyThreshold')
    c_accuracy = parameters.GetFloat('cCoordinateAccuracyThreshold')
    x_scaling = parameters.GetBool('halfXCoordinate')

    FreeCAD.Console.PrintMessage('step: {}, x_ac: {}, c_ac: {}, x_scaling: {}'.format(step, x_accuracy, c_accuracy, x_scaling))

    x_accuracy = min(x_accuracy, step)
    c_accuracy = min(c_accuracy, step)

    # Use the native Python open which was saved as `pythonopen`
    output_file = pythonopen(filename, 'w')

    # Write paths
    for ob in exportList:

        prev_point = None
        for point in ob.Shape.discretize(Distance=step):
            r, fi = cartesian_to_polar(point.x, point.y)
            fi = to_degrees(fi)

            if x_scaling:
                r = r / 2.0

            point = (r, fi)

            append_point = (prev_point is None or (abs(prev_point[0] - point[0]) > x_accuracy and abs(prev_point[1] - point[1]) > c_accuracy))

            if append_point:
                prev_point = point
                output_file.write(COMMAND_FORMAT.format(point[1], point[0]))
                output_file.write('\n')

    # Close the file
    output_file.close()
