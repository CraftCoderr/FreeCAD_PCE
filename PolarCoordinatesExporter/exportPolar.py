
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

C_COMMAND_FORMAT = "C{:.3f}"
X_COMMAND_FORMAT = "X{:.2f}"

def cartesian_to_polar(x, y):
    r = math.sqrt(x ** 2 + y ** 2)
    fi = 0.0
    if y >= 0 and r != 0:
        fi = math.acos(x / r)
    elif y < 0:
        fi = -math.acos(x / r)

    return r, fi

def to_degrees(a):
    return a * (180.0 / math.pi)

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

    FreeCAD.Console.PrintMessage('step: {}, x_ac: {}, c_ac: {}'.format(step, x_accuracy, c_accuracy))

    x_accuracy = min(x_accuracy, step)
    c_accuracy = min(c_accuracy, step)

    # Use the native Python open which was saved as `pythonopen`
    output_file = pythonopen(filename, 'w')

    # Write paths
    for ob in exportList:

        prev_r = None
        prev_fi = None
        for point in ob.Shape.discretize(Distance=step):
            r, fi = cartesian_to_polar(point.x, point.y)
            fi = to_degrees(fi)

            append_r = (prev_r is None) or (abs(prev_r - r) > x_accuracy)
            append_fi = (prev_fi is None) or (abs(prev_fi - fi) > c_accuracy)

            if append_fi:
                prev_fi = fi
                output_file.write(C_COMMAND_FORMAT.format(fi))

            if append_r:
                prev_r = r
                output_file.write(X_COMMAND_FORMAT.format(r))

            if append_fi or append_r:
                output_file.write('\n')


    # Close the file
    output_file.close()
