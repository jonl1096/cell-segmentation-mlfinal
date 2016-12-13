import numpy as np
import cv2
import nibabel as nib

import plotly
import plotly.graph_objs as graphobjs

import os
import errno

def local_hist_equilization(file_path, num_points, resolution=(0.01872, 0.01872, 0.005)):
    """ Applies local histogram equilization on a .nii file, returns a numpy array of coordinates and intensities. """

    im = nib.load(file_path)

    im = im.get_data()
    img = im[:,:,:]

    shape = im.shape
    #affine = im.get_affine()

    x_value = shape[0]
    y_value = shape[1]
    z_value = shape[2]

    img_flat = img.reshape(-1)

    img_grey = np.array(img_flat * 255, dtype=np.uint8)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

    temp = clahe.apply(img_grey)

    lhe_img_data = temp.reshape(x_value, y_value, z_value)

    return img_data_to_array(lhe_img_data, 10000)

def img_data_to_array(img_data, num_points):
    """ Converts nibabel img data to a numpy array of coordinates and intensities. """
    ## Convert into np array (or memmap in this case)
    temp_data = img_data
    # temp_shape = temp_img.shape
    temp_max = np.max(temp_data)

    print('shape:')
    print temp_data.shape
    print type(temp_data)

    print('max:')
    print(temp_max)

    # print(temp_data)

    temp_threshold = 0.025
    filt = temp_data > temp_threshold * temp_max
    # filt = temp_data

    data_points = np.where(filt)
    x = data_points[0]
    y = data_points[1]
    z = data_points[2]

    intens = temp_data[filt]
    intens = np.int16(255 * (np.float32(intens) / np.float32(temp_max)))

    intens_shape = intens.shape

    total_points = intens.shape[0]

    print('total points: %d' % total_points)

    fraction = num_points / float(total_points)

    if fraction < 1.0:
        # np.random.random returns random floats in the half-open interval [0.0, 1.0)
        filt = np.random.random(size=intens_shape) < fraction
        print('v.shape:')
        print(intens_shape)
        print('x.size before filter: %d' % x.size)
        print('y.size before filter: %d' % y.size)
        print('z.size before filter: %d' % z.size)
        print('v.size before filter: %d' % intens.size)
        x = x[filt]
        y = y[filt]
        z = z[filt]
        intens = intens[filt]
        print('x.size after filter: %d' % x.size)
        print('y.size after filter: %d' % y.size)
        print('z.size after filter: %d' % z.size)
        print('v.size after filter: %d' % intens.size)

    temp_points = np.vstack([x, y, z, intens])
    temp_points = np.transpose(temp_points)
    print("Num Points: %d" % (temp_points.shape[0]))

    return temp_points


def make_sure_path_exists(path):
    """Check if the directory a file is going to be written to exists, and if not, create the directory."""
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def array_to_plot(points, resolution=(0.01872, 0.01872, 0.005), point_size=1.2, outfile_name="", outfile_dir_path="plots/"):
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
        x=[x * xResolution for x in thedata[:, 0]],
        y=[x * yResolution for x in thedata[:, 1]],
        z=[x * zResolution for x in thedata[:, 2]],
        mode='markers',
        marker=dict(
            size=point_size,
            color='cyan',  # set color to an array/list of desired values
            colorscale='Viridis',  # choose a colorscale
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

    # dir path should take the form 'plots/'
    make_sure_path_exists(outfile_dir_path)

    plotly.offline.plot(fig, filename=outfile_dir_path + outfile_name + "_plot.html")

    # if outfile_dir== "":
    #     plotly.offline.plot(fig, filename='plots/' + token + "_plot.html")
    # else:
        # plotly.offline.plot(fig, filename='plots/' + outfile_name + "_plot.html")


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



