import streamlit as st
import cv2
import os

# Create a folder to save captured images
if not os.path.exists("captured_images"):
    os.makedirs("captured_images")

def main():
    st.title('NouriScan')

    st.sidebar.header('Ingredients & Nutrition')
    

    # List of items
    items = ['Banana', 'Apple', 'Orange']

    # Define content for each item
    content = {
        'Banana': "1o5 kcal/each, _ g Sugar, _ g Fat, _ g ",
        'Apple': "80 kcal/each",
        'Orange': "80 kcal/each"
    }

    # Display expanders for each item
    for item in items:
        with st.sidebar.expander(item):
            st.write(content[item])


    done_clicked = st.sidebar.button('Done')
    

    if done_clicked:
        displayRecipes()

        
    if not done_clicked:
        vidCapture()

def vidCapture():
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

    # Button to capture image
    capture_button_clicked = st.button("Capture Image")
    if capture_button_clicked:
        capture_image(cap)

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        if not ret:
            st.error("Error: Unable to read frame from the webcam.")
            break

        # Display the frame in the Streamlit app
        video_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", use_column_width=True)

    # Release the VideoCapture and close the OpenCV window
    cap.release()

    
def displayRecipes():
    
    items = [
    {"title": "Recipe 1", "content": "Content for Item 1."},
    {"title": "Recipe 2", "content": "Content for Item 2."},
    {"title": "Recipe 3", "content": "Content for Item 3."}
    ]

    # Display the items with expanding boxes
    for item in items:
        with st.expander(item["title"]):
            st.write(item["content"])


def capture_image(cap):
    # Read a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        st.error("Error: Unable to read frame from the webcam.")
        return

    # Save the frame as an image
    image_path = f"captured_images/captured_image_{len(os.listdir('captured_images')) + 1}.jpg"
    cv2.imwrite(image_path, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    st.success(f"Image captured and saved as {image_path}")

if __name__ == '__main__':
    main()
