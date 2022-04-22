import matplotlib.pyplot as plt
import argparse
import re
import math

parser = argparse.ArgumentParser(description='Plot polar coordinates from program file.')
parser.add_argument('input', type=str, help='program file')

args = parser.parse_args()

with open(args.input, 'r') as input_file:
    lines = input_file.readlines()

points_r = []
points_fi = []
points_x = []
points_y = []

current_r = None
current_fi = None

for line in lines:
    m = re.search("(C-?\d*\.\d*)?(X-?\d*\.\d*)?", line)

    if m.lastindex is not None:
        for i in range(m.lastindex):
            matched = m.group(i + 1)
            if matched is None:
                continue

            val = float(matched[1:])
            if matched[0] == 'C':
                current_fi = val
            elif matched[0] == 'X':
                current_r = val

        if current_r is not None and current_fi is not None:
            points_r.append(current_r)
            points_fi.append(current_fi)
            points_x.append(current_r * math.cos(current_fi / 180.0 * math.pi))
            points_y.append(current_r * math.sin(current_fi / 180.0 * math.pi))

            # points_x.append(current_r)
            # points_y.append(current_fi)

# fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
# ax.plot(points_fi, points_r, 'ro')

plt.scatter(points_x, points_y)

plt.show()

print('Done')
