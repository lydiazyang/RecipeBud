import streamlit as st
import cv2
# import pandas as pd
# import numpy as np
def main():
    st.title('NouriScan')

    st.sidebar.header('Ingredients & Nutrition')
    

    option1 = st.sidebar.checkbox('Banana')
    option2 = st.sidebar.checkbox('Strawberry')
    option3 = st.sidebar.checkbox('Kale')
    option4 = st.sidebar.checkbox('Orange Juice')
    option5 = st.sidebar.checkbox('Almond Milk')
    button_clicked = st.sidebar.button('Done')
    if not button_clicked:
        videoCapture()
    if button_clicked:
        displayRecipes()

def displayRecipes():
    items = [
    {"title": "Item 1", "content": "Content for Item 1."},
    {"title": "Item 2", "content": "Content for Item 2."},
    {"title": "Item 3", "content": "Content for Item 3."}
    ]

    # Display the items with expanding boxes
    for item in items:
        with st.expander(item["title"]):
            st.write(item["content"])

    

def videoCapture():
    
    # Create a VideoCapture object to access the webcam
    cap = cv2.VideoCapture(0)

    # Set the video frame width and height (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        st.error("Error: Unable to access the webcam.")
        return

    # Display a placeholder for the video stream
    video_placeholder = st.empty()

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        if not ret:
            st.error("Error: Unable to read frame from the webcam.")
            break

        # Display the frame in the Streamlit app
        video_placeholder.image(frame, channels="BGR", use_column_width=True)

        # Check if the user pressed the 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()
    



if __name__ == '__main__':
    main()