# Third Party Imports
import numpy as np
import matplotlib.pyplot as plt

# kMap.py Imports
from kmap.library.plotdata import PlotData
from kmap.model.crosshair_model import CrosshairAnnulusModel


# This script demonstrates the working and functionality for crosshairs
# in kmap on a simple 9x11 grid.


# New Crosshair
x, y, radius, width = 0, 0, 1.5, 1.5
crosshair = CrosshairAnnulusModel(x=x, y=y, radius=radius, width=width)

# Use 7x7 as data from which we cut to better demonstrate working
# The data goes from 0-49 and the pixel center acts is the whole number
global data
data = PlotData(np.reshape(np.array(range(99)), (9, 11)),
                [[-5, 5], [-4, 4]])
global extent
extent = data.range.flatten() + [-0.5, 0.5, -0.5, 0.5]

export = {}


def plot(axis, x, y, r, w, region, inverted, title=''):
    # Helper Function plotting crosshair and data

    # Set Crosshair
    crosshair.x = x
    crosshair.y = y
    crosshair.radius = r
    crosshair.width = w

    if region == None:
        cut = data
    else:
        cut = crosshair.cut_from_data(data,
                                      region=region,
                                      inverted=inverted)

    export.update({title: cut.data})
    # Labels
    axis.set_title(title)
    axis.set_xlabel('x')
    axis.set_ylabel('y')

    # Plot x line
    axis.plot([x, x], extent[:2], color='black')
    # Plot y line
    axis.plot(extent[2:], [y, y], color='black')
    # Plot ROI
    axis.plot(r * np.cos(theta) + x, r *
              np.sin(theta) + y, color='black')
    # Plot Annulus
    axis.plot((r + w) * np.cos(theta) + x, (r + w) *
              np.sin(theta) + y, color='black')
    # Plot Data
    # Origin needs to be set to lower because we defined both axes
    # as starting from minimum to maximum
    axis.imshow(cut.data, extent=extent, vmin=0, vmax=99, origin='lower')


global theta
theta = np.linspace(0, 2 * np.pi, 1000)

####################    Line Cuts   ####################
figure, axes = plt.subplots(2, 3)
figure.suptitle('Line Cuts')
# Raw Data
plot(axes[0][0], x=0, y=0, r=1.5, w=1.5,
     region=None, inverted=False, title='Data')
# x-Line
plot(axes[0][1], x=0, y=0, r=1.5, w=1.5,
     region='x', inverted=False, title='x-Line')
# y-Line
plot(axes[0][2], x=0, y=0, r=1.5, w=1.5,
     region='y', inverted=False, title='y-Line')
# x-Line Inverted
plot(axes[1][0], x=0, y=0, r=1.5, w=1.5, region='x',
     inverted=True, title='x-Line Inverted')
# x-Line 2
plot(axes[1][1], x=1, y=0, r=1.5, w=1.5,
     region='x', inverted=False, title='x-Line 2')
# y-Line Edge Case: 0.5 is right on the edge.
plot(axes[1][2], x=0, y=0.5, r=1.5, w=1.5, region='y',
     inverted=False, title='y-Line Edge Case 2')


####################    ROI Cuts   ####################
figure, axes = plt.subplots(2, 3)
figure.suptitle('ROI Cuts')
# Raw Data
plot(axes[0][0], x=0, y=0, r=1.5, w=1.5, region=None,
     inverted=False, title='Data')
# ROI Cut
plot(axes[0][1], x=0, y=0, r=1.5, w=1.5, region='roi',
     inverted=False, title='ROI Cut')
# ROI Cut Inverted
plot(axes[0][2], x=0, y=0, r=1.5, w=1.5, region='roi',
     inverted=True, title='ROI Cut Inverted')
# Moved ROI
plot(axes[1][0], x=1, y=1, r=3, w=1.5, region='roi',
     inverted=False, title='Moved ROI')
# ROI Cut Edge Case: 2 touches the pixel at the cardinal directions
# but it does not include them (center of pixel needs to be inside)
plot(axes[1][1], x=0, y=0, r=2, w=1.5, region='roi',
     inverted=False, title='ROI Edge Case')
# ROI Cut Edge Case 2
plot(axes[1][2], x=0, y=0, r=2.01, w=1.5, region='roi',
     inverted=False, title='ROI Edge Case 2')

####################    Border Cuts   ####################
figure, axes = plt.subplots(2, 3)
figure.suptitle('Border Cuts')
# Raw Data
plot(axes[0][0], x=0, y=0, r=1.5, w=1.5, region=None,
     inverted=False, title='Data')
# Border Cut
plot(axes[0][1], x=0, y=0, r=1.5, w=1.5, region='border',
     inverted=False, title='Border Cut')
# Moved Border Cut
plot(axes[0][2], x=1, y=1, r=2, w=1.5, region='border',
     inverted=False, title='Moved Border Cut')
# Inverted Border Cut
plot(axes[1][0], x=0, y=0, r=1.5, w=1.5, region='border',
     inverted=True, title='Inverted Border Cut')
# Border Cut Edge Case: Sqrt(0.5^2 + 0.5^2) > 0.70
plot(axes[1][1], x=0, y=0, r=0.70, w=1.5, region='border',
     inverted=False, title='Border Edge Case')
# Border Cut Edge Case 2: Sqrt(1.5^2 + 1.5^2) < 2.13
plot(axes[1][2], x=0, y=0, r=2.13, w=1.5, region='border',
     inverted=False, title='Border Edge Case 2')


####################    Ring Cuts   ####################
figure, axes = plt.subplots(2, 3)
figure.suptitle('Ring Cuts')
# Raw Data
plot(axes[0][0], x=0, y=0, r=1.5, w=1.5, region=None,
     inverted=False, title='Data')
# Ring Cut
plot(axes[0][1], x=0, y=0, r=1.5, w=1.5, region='ring',
     inverted=False, title='Ring Cut')
# Moved Ring Cut
plot(axes[0][2], x=1, y=1, r=2, w=1.5, region='ring',
     inverted=False, title='Moved Ring Cut')
# Inverted Ring Cut
plot(axes[1][0], x=0, y=0, r=1.5, w=1.5, region='ring',
     inverted=True, title='Inverted Ring Cut')
# Ring Cut Edge Case: Ring = ROI with 'radius' = r+w - ROI with radius = r
plot(axes[1][1], x=0, y=0, r=1, w=2.00, region='ring',
     inverted=False, title='Ring Edge Case')
# Ring Cut Edge Case 2
plot(axes[1][2], x=0, y=0, r=2.01, w=1.5, region='ring',
     inverted=False, title='Ring Edge Case 2')

####################    Other Cuts   ####################
figure, axes = plt.subplots(2, 3)
figure.suptitle('Other Cuts')
# Raw Data
plot(axes[0][0], x=0, y=0, r=1.5, w=1.5, region=None,
     inverted=False, title='Data')
# Center Cut: Behaves like 2 line cuts
plot(axes[0][1], x=1, y=1, r=2, w=1.5, region='center',
     inverted=False, title='Center Cut')
# Center Edge Case
plot(axes[0][2], x=0.5, y=0.5, r=1.5, w=1.5, region='center',
     inverted=False, title='Center Edge Case')
# Outer Border Cut: Is equivalent to 'border' with radius = r+w
plot(axes[1][0], x=0, y=0, r=1.5, w=1.5, region='outer_border',
     inverted=False, title='Outer Border Cut')
# Outer Border Edge Case: Sqrt(0.5^2 + 0.5^2) > 0.70
plot(axes[1][1], x=0, y=0, r=0.00, w=0.7, region='outer_border',
     inverted=False, title='Outer Border Edge Case')
# Outer Border Cut Edge Case 2: Sqrt(1.5^2 + 1.5^2) < 2.13
plot(axes[1][2], x=0, y=0, r=0.00, w=2.13, region='outer_border',
     inverted=False, title='Outer Border Edge Case 2')


np.save('data.npy', export)
plt.show()
