import streamlit as st
import cv2
import os

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
    else:
        displayRecipes()

def displayRecipes():
    items = [
        {"title": "Item 1", "content": "Content for Item 1."},
        {"title": "Item 2", "content": "Content for Item 2."},
        {"title": "Item 3", "content": "Content for Item 3."}
    ]

    for item in items:
        with st.expander(item["title"]):
            st.write(item["content"])

def videoCapture():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        st.error("Error: Unable to access the webcam.")
        return

    st.write("Click 'Capture Image' to capture an image.")

    # Display a placeholder for the video stream
    video_placeholder = st.empty()

    if st.button("Capture Image"):
        # Read a frame from the webcam
        ret, frame = cap.read()

        if not ret:
            st.error("Error: Unable to read frame from the webcam.")
        else:
            # Save the captured frame as an image
            image_path = "captured_image.jpg"
            cv2.imwrite(image_path, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            st.write("Image captured and saved as", image_path)

            # Display the captured image
            st.image(image_path, use_column_width=True)

    # Release the VideoCapture and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
