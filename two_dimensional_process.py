import numpy as np

def givens_rotation(theta):
    G = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])
    return G

def rotate_image_givens(image, angle):
    # Convert angle to radians
    theta = np.radians(angle)
    
    # Get the Givens rotation matrix
    G = givens_rotation(theta)
    
    # Get the dimensions of the image
    (h, w) = image.shape[:2]
    
    # Get the center of the image
    center = np.array([w / 2, h / 2])
    
    # Create an output image filled with zeros (black)
    rotated = np.zeros_like(image)
    
    # Iterate through each pixel in the output image
    for i in range(h):
        for j in range(w):
            # Compute the coordinates of the pixel relative to the center
            relative_coords = np.array([j, i]) - center
            
            # Apply the inverse Givens rotation to the coordinates
            original_coords = np.dot(G.T, relative_coords) + center
            
            # Get the nearest pixel in the original image
            original_x, original_y = original_coords.astype(int)
            
            # Check if the original coordinates are within bounds
            if 0 <= original_x < w and 0 <= original_y < h:
                rotated[i, j] = image[original_y, original_x]
    
    return rotated