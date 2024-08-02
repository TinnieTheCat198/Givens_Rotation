from three_dimensional_process import load_nifti_file, plot_slices, rotate_image_3d
from two_dimensional_process import rotate_image_givens
import streamlit as st
import os
import numpy as np
import tempfile
import cv2

def inject_custom_css():
    with open('assets/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.set_page_config(page_title='AlgivensStream', layout="wide", page_icon="assets/crab.ico")

inject_custom_css()
# st.image("assets/flowing-badge-app.png", width=100)
# with st.container():
with st.container(border=True):
    # st.image('assets/crab.png',width=50,output_format="PNG")
    st.markdown("""
        <div class="website-title">
            <img src="https://i.ibb.co/Z8SGy46/crab.png" width="50">
            <h1 style="font-family:'Arial'; font-weight:500"><span style="color:#e6331f">Algivens</span><span style="color:#ffa32c">Stream</span></h1>
        </div>
        <h2 class="subtitle">A Visual Tool to Understand Givens Rotations</h2>
    """,True)

# Load a real 3D image (e.g., NIfTI file)
# file_path = './testcase/zstat1.nii'  # Replace with your 3D image file path
with st.container(border=True):
    uploaded_file = st.file_uploader("Choose an image file", accept_multiple_files=False, type=["dcm", "nii", "nii.gz", "jpg", "DCM"], key="file_uploader",)
    # st.rerun()    
    if uploaded_file:
        is_nifti = False
        is_2d_image = False
        is_2d_dicom = False
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = tempfile.mkdtemp()
            path = os.path.join(temp_dir, uploaded_file.name)
            with open(path,"wb") as f:
                f.write(uploaded_file.getvalue())
            print(f)
        
        if uploaded_file.name.endswith(('.nii', '.nii.gz')):
            is_nifti = True
        if uploaded_file.name.endswith(('.jpg', '.jpeg', '.png', '.DCM')):
            is_2d_image = True
        if uploaded_file.name.endswith(('.DCM')):
            is_2d_dicom = True
        
        c = st.container(border=True,height=230 if is_2d_image else 380)
        c.subheader("Input For Rotation")
        if (is_2d_image == False):
            x_input = c.number_input("x = ", min_value=0, max_value=360, value=0, step=1)
            y_input = c.number_input("y = ", min_value=0, max_value=360, value=0, step=1)
            z_input = c.number_input("z = ", min_value=0, max_value=360, value=0, step=1)
        else:
            angle = c.number_input("Angle of rotation = ", min_value=0, max_value=360, value=0, step=1)
        submit_button = c.button(label="Submit",key="submit")
        
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            if (is_2d_image == False and is_2d_dicom == False):
                image_np = load_nifti_file(path)
                fig = plot_slices(image_np)
                st.pyplot(fig, clear_figure=True)   
            else:
                st.image(uploaded_file)

        with col2:
            if submit_button:
                st.subheader("Result")
                with st.spinner("In progress..."):
                    if (is_2d_image == False):
                        st.pyplot(plot_slices(rotate_image_3d(image_np,angles=(x_input,y_input,z_input))), clear_figure=True)
                    else:
                        image_np = cv2.imread(path)
                        image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
                        rotated_image = rotate_image_givens(image_np,angle)
                        st.image(rotated_image,use_column_width=True)
        

footer_html = """<div class="footer" style='text-align: center;'>
  <p>Developed with <span style="color:#ff4b4c; font-weight:bold">Streamlit</span></p>
  <a href="https://github.com/TinnieTheCat198/Givens_Rotation">
  <svg width="20px" height="20px" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 496 512"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="#f36944" d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3 .3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5 .3-6.2 2.3zm44.2-1.7c-2.9 .7-4.9 2.6-4.6 4.9 .3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3 .7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3 .3 2.9 2.3 3.9 1.6 1 3.6 .7 4.3-.7 .7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3 .7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3 .7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"/>
  </svg>
  </a>
  <a href="https://www.facebook.com/tinnielovie">
  <svg width="20px" height="20px" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="#f36944" d="M512 256C512 114.6 397.4 0 256 0S0 114.6 0 256C0 376 82.7 476.8 194.2 504.5V334.2H141.4V256h52.8V222.3c0-87.1 39.4-127.5 125-127.5c16.2 0 44.2 3.2 55.7 6.4V172c-6-.6-16.5-1-29.6-1c-42 0-58.2 15.9-58.2 57.2V256h83.6l-14.4 78.2H287V510.1C413.8 494.8 512 386.9 512 256h0z"/></svg>
  </a>
</div>"""
st.markdown(footer_html, unsafe_allow_html=True)


