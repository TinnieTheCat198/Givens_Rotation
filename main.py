from three_dimensional_process import load_nifti_file, plot_slices, rotate_image_3d
from two_dimensional_process import rotate_image_givens
import cv2
import os
import SimpleITK as sitk
import streamlit as st
import numpy as np

st.set_page_config(page_title='Givens Rotation Illustration', layout="wide", page_icon="assets/logo.ico")

# st.image('assets/pycad.png', width=350)
st.title("Givens Rotation in Image Processing")

# Load a real 3D image (e.g., NIfTI file)
# file_path = './testcase/zstat1.nii'  # Replace with your 3D image file path
uploaded_files = st.file_uploader("Choose an image file", accept_multiple_files=True, type=["dcm", "nii", "nii.gz", "jpg"], key="file_uploader")
    
if uploaded_files:
    is_nifti = False
    is_jpg = False
    for uploaded_file in uploaded_files:
        # bytes_data = uploaded_file.read()
        file_name = uploaded_file.name
        file_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(file_dir, file_name)
        # with open(file_path, 'wb') as f:
        #     f.write(bytes_data)
        if uploaded_file.name.endswith(('.nii', '.nii.gz')):
            is_nifti = True
        if uploaded_file.name.endswith(('.jpg')):
            is_jpg = True
        
        if is_nifti:
            image_np = load_nifti_file(file_path)
        # else:
        #     image_np = load_and_store_dicom_series(temp_dir, "dicom_image_data")
    # axial_slice_num = st.slider(' ', 0, image_np.shape[2] - 1, 0, key="axial_slider")
    st.header("Original Image")
    if (is_jpg == False):
        fig = plot_slices(image_np)
        st.pyplot(fig, clear_figure=True)
    else:
        st.image(uploaded_file)

    st.header("Input For Rotation")
    if (is_jpg == False):
        x_input = st.number_input("x = ", min_value=0, max_value=360, value=0, step=1)
        y_input = st.number_input("y = ", min_value=0, max_value=360, value=0, step=1)
        z_input = st.number_input("z = ", min_value=0, max_value=360, value=0, step=1)
    else:
        angle = st.number_input("Angle of rotation = ", min_value=0, max_value=360, value=0, step=1)
    if st.button("Submit"):
        st.header("Result: ")
        if (is_jpg == False):
            st.pyplot(plot_slices(rotate_image_3d(image_np,angles=(x_input,y_input,z_input))), clear_figure=True)
        else:
            image_np = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
            rotated_image = rotate_image_givens(image_np,angle)
            cv2.imwrite('output.jpg', rotated_image)
            st.image('output.jpg')


