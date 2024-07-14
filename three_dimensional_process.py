import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt


def givens_rotation_x(theta):
    return np.array([[1, 0, 0],
                     [0, np.cos(theta), -np.sin(theta)],
                     [0, np.sin(theta), np.cos(theta)]])

def givens_rotation_y(theta):
    return np.array([[np.cos(theta), 0, np.sin(theta)],
                     [0, 1, 0],
                     [-np.sin(theta), 0, np.cos(theta)]])

def givens_rotation_z(theta):
    return np.array([[np.cos(theta), -np.sin(theta), 0],
                     [np.sin(theta), np.cos(theta), 0],
                     [0, 0, 1]])

def rotate_image_3d(volume, angles):
    # Convert angles to radians
    theta_x, theta_y, theta_z = np.radians(angles)
    
    # Get the Givens rotation matrices for each axis
    R_x = givens_rotation_x(theta_x)
    R_y = givens_rotation_y(theta_y)
    R_z = givens_rotation_z(theta_z)
    
    # Combined rotation matrix
    R = R_z @ R_y @ R_x
    
    # Get the dimensions of the volume
    (d, h, w) = volume.shape
    
    # Get the center of the volume
    center = np.array([w / 2, h / 2, d / 2])
    
    # Create an output volume filled with zeros (black)
    rotated = np.zeros_like(volume)
    
    # Iterate through each voxel in the output volume
    for z in range(d):
        for y in range(h):
            for x in range(w):
                # Compute the coordinates of the voxel relative to the center
                relative_coords = np.array([x, y, z]) - center
                
                # Apply the inverse rotation to the coordinates
                original_coords = np.dot(R.T, relative_coords) + center
                
                # Get the nearest voxel in the original volume
                original_x, original_y, original_z = original_coords.astype(int)
                
                # Check if the original coordinates are within bounds
                if 0 <= original_x < w and 0 <= original_y < h and 0 <= original_z < d:
                    rotated[z, y, x] = volume[original_z, original_y, original_x]
    
    return rotated

def plot_slices(image, title = None):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    mid = np.array(image.shape) // 2
    slices = [image[mid[0], :, :], image[:, mid[1], :], image[:, :, mid[2]]]
    
    for ax, slice_ in zip(axes, slices):
        ax.imshow(slice_, cmap='gray')
        ax.axis('on')
    
    if title:
        fig.suptitle(title)
    return fig

def load_nifti_file(filepath):
    nifti_img = nib.load(filepath)
    image_np = np.asanyarray(nifti_img.dataobj)
    return image_np

# def load_and_store_dicom_series(directory, session_key):
#     if session_key not in st.session_state:
#         reader = sitk.ImageSeriesReader()
#         dicom_names = reader.GetGDCMSeriesFileNames(directory)
#         reader.SetFileNames(dicom_names)
#         image_sitk = reader.Execute()
#         image_np = sitk.GetArrayFromImage(image_sitk)
#         st.session_state[session_key] = image_np
#     return st.session_state[session_key]




# image = nib.load(file_path).get_fdata()

# Define rotation angles (in degrees) for each axis (x, y, z)
# angles = (30, 45, 60)

# Rotate the 3D image
# rotated_image = rotate_image_3d(image, angles)