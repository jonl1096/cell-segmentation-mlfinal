import numpy as np

import plotly
import plotly.graph_objs as graphobjs

import os
import errno

def make_sure_path_exists(path):
    """Check if the directory a file is going to be written to exists, and if not, create the directory."""
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def array_to_plot(points, token, resolution, outfile_name=""):
    """Generates the plotly from the numpy array."""
    # Type in the path to your csv file here
    
    thedata = points
#     print(thedata)

    # Set tupleResolution to resolution input parameter
    tupleResolution = resolution;

    # EG: for Aut1367, the spacing is (0.01872, 0.01872, 0.005).
    xResolution = tupleResolution[0]
    yResolution = tupleResolution[1]
    zResolution = tupleResolution[2]
    # Now, to get the mm image size, we can multiply all x, y, z
    # to get the proper mm size when plotting.
    
#     print('asdf')
#     x = [x * xResolution for x in thedata[:, 0]]
#     print(x)

    trace1 = graphobjs.Scatter3d(
        x = [x * xResolution for x in thedata[:, 0]],
        y = [x * yResolution for x in thedata[:, 1]],
        z = [x * zResolution for x in thedata[:, 2]],
        mode='markers',
        marker=dict(
            size=1.2,
            color='cyan',                # set color to an array/list of desired values
            colorscale='Viridis',   # choose a colorscale
            opacity=0.15
        )
    )

    data = [trace1]
    layout = graphobjs.Layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        ),
        paper_bgcolor='rgb(0,0,0)',
        plot_bgcolor='rgb(0,0,0)'
    )

    fig = graphobjs.Figure(data=data, layout=layout)
#     print(self._token + "plotly")

    make_sure_path_exists('plots')
    
    if outfile_name == "":
        plotly.offline.plot(fig, filename= 'plots/' + token + "_plot.html")
    else:
        plotly.offline.plot(fig, filename= 'plots/' + outfile_name + "_plot.html")


def load_csv(path):
    """Method for getting a numpy array from the csv file"""
    points = []
    with open(path, 'r') as infile:
        for line in infile:
            line = line.strip().split(',')
            entry = [int(line[0]), int(line[1]), int(line[2]), int(line[3])]
            points.append(entry)
    points = np.array(points)
    return points

