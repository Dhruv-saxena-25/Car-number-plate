import streamlit as st
from ultralytics import YOLO
from easyocr import Reader
import mysql.connector 
import cv2
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from detect import detect_number_plate, recognize_number_plate



# MySQL Connection

mydb= mysql.connector.connect(
    host= 'localhost',
    user= 'root',
    password= 'root@123',
    database= 'car_yolov8'
)

my_cursor=mydb.cursor()

st.set_page_config(page_title= "Automatic NPR", page_icon=":car:", layout="wide")
st.title('Automatic Number Plate Recognition System :car:')
st.markdown("---")

uploaded_file= st.file_uploader("Upload an Image 🚀", type=["png","jpg", "jpeg"])
upload_path = "uploads"

if uploaded_file is not None:
    # construct the path to the uploaded image
    # and then save it in the `uploads` folder
    image_path = os.path.sep.join([upload_path, uploaded_file.name])
    with open(image_path,"wb") as f:
        f.write((uploaded_file).getbuffer())
    with st.spinner("In progress ...🛠"):
    # load the model from the local directory
        model= YOLO("..//runs\\detect\\train\\weights\\best.pt")
        # runs\detect\train\weights\best.pt

        # initialize the EasyOCR reader
        reader = Reader(['en'], gpu=True)
        
        # convert the image from BGR to RGB
        image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        
        # make a copy of the image to draw on it
        image_copy = image.copy()
        
        # split the page into two columns
        col1, col2 = st.columns(2)
        
        # display the original image in the first column
        with col1:
            st.subheader("Original Image")
            st.image(image)

        number_plate_list = detect_number_plate(image, model)

        if number_plate_list != []:
            number_plate_list = recognize_number_plate(image_path, reader,
                                                        number_plate_list)
            for box, text in number_plate_list:
                cropped_number_plate = image_copy[box[1]:box[3],
                                                  box[0]:box[2]]

                cv2.rectangle(image, (box[0], box[1]),
                              (box[2], box[3]), (0, 255, 0), 2)
                cv2.putText(image, text, (box[0], box[3] + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # display the number plate detection in the second column
                with col2:
                    st.subheader("Number Plate Detection")
                    st.image(image)

                st.subheader("Cropped Number Plate")
                st.image(cropped_number_plate, width=300)
                st.success("Number plate text: **{}**".format(text))
            
            try:
                query1 = 'SELECT Num_plate FROM car_num WHERE Num_plate = %s'
                my_cursor.execute(query1, (text,))
                result = my_cursor.fetchone()

                if result is not None:
                    if text == str(result[0]):
                        query = "SELECT Name FROM car_num WHERE Num_plate = %s"
                        my_cursor.execute(query, (text,))
                        result = my_cursor.fetchone()

                        if result is not None:
                            st.success(f"Vechile Owner: {result[0]}")
                        else:
                            st.error('No matching name found')
                            # print("No matching name found")
                    else:
                        st.error("Text does not match Num_plate")
                        # print("Text does not match Num_plate")
                else:
                    st.error(f"Vechile Owner: {'Unknown'}")
                    # print("No matching Num_plate found")

            except mysql.connector.Error as err:
                print(f"Error executing query: {err}")
        else:
            st.error("No number plate detected.")
else:
    st.info("Please upload an image to get started.")

st.markdown("<br><hr><center>Made with ❤️ by "
            "<a href='https://dhruv-saxena-25.github.io/web/"
            "'><strong>Dhruv Saxena</strong></center><hr>",
            unsafe_allow_html=True)