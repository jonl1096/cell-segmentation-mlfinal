import numpy as np
import nibabel as nib

inToken = 'Fear199'

# full image
# temp_file_path = "img/" + inToken + ".nii"

# Downsampled image
temp_file_path = "img/" + inToken + "_ds.nii"

temp_img = nib.load(temp_file_path)

## Sanity check for shape
temp_img.shape

## Convert into np array (or memmap in this case)
temp_data = temp_img.get_data()
temp_shape = temp_img.shape
temp_max = np.max(temp_data)

print('shape:')
print temp_data.shape
print type(temp_data)

print('max:')
print(temp_max)

# print(temp_data)

temp_threshold = 0.5
# filt = temp_data > temp_threshold * temp_max
filt = temp_data

data_points = np.where(filt)
x = data_points[0]
y = data_points[1]
z = data_points[2]
intens = temp_data[filt]

intens = np.int16(255 * (np.float32(intens) / np.float32(temp_max)))


temp_points = np.vstack([x, y, z, intens])
temp_points = np.transpose(temp_points)
print("Num Points: %d"%(temp_points.shape[0]))

# Saving points

path = 'points/' + inToken + ".csv"
np.savetxt(path, temp_points, fmt='%d', delimiter=',')
