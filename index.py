import streamlit as st
import cv2
import os
from app import *

# Create a folder to save captured images
if not os.path.exists("captured_images"):
    os.makedirs("captured_images")

# Initialize the session state
session_state = st.session_state
if 'ingredientsList' not in session_state:
    session_state['ingredientsList'] = []

def main():
    
    st.title('RecipeMate')
    
    st.sidebar.header('Ingredients & Nutrition')
    # List of items
    items = ['Item 1', 'Item 2', 'Item 3']

    # Define content for each item
    content = {
        'Item 1': "This is the content for Item 1",
        'Item 2': "This is the content for Item 2",
        'Item 3': "This is the content for Item 3"
    }

    # Display expanders for each item
    for item in items:
        with st.sidebar.expander(item):
            st.write(content[item])
    # Create a VideoCapture object to access the webcam
    cap = cv2.VideoCapture(0)

    # Set the video frame width and height (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        st.error("Error: Unable to access the webcam.")
        return

    # Display a placeholder for the video stream
    video_placeholder = st.empty()
    # Button to capture image
    if st.button("Capture Image"):
        image_path = capture_image()
        classification = classifyImage(image_path)
        session_state['ingredientsList'].append(classification)

    # Button to indicate done
    done_button = st.sidebar.button('Done')

    # Display the captured ingredients
    st.write("Captured Ingredients:", session_state['ingredientsList'])
    
    # Display recipes if "Done" is clicked
    while not done_button:
    # Read a frame from the webcam
        ret, frame = cap.read()

        if not ret:
            st.error("Error: Unable to read frame from the webcam.")
            break

        # Display the frame in the Streamlit app
        video_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", use_column_width=True)
    if done_button:
        cap.release()
        if session_state['ingredientsList']:
            session_state['ingredientsList'].pop()
        displayRecipes(session_state['ingredientsList'])

def displayRecipes(ingredientsList):
    items = []
    #now we are gonna send the ingredient list to ask gpt
    prompt = f"I have following Ingredients :{','.join(ingredientsList)}. What can I make with these \
            Ingredients? give me possible list of recipes with Nutrition Facts per 100g from \
            highest nutrition value to lowest. Give me results in \
            followig format:\
            ['title': 'Recipe title', 'content': 'recipe and nutritional facts per 100g']"
    LLMResult = askGPT(prompt)
    lystOfRecipes = LLMResult.split('\n\n')
    for recipe in range(1, len(lystOfRecipes)-1):
        items.append({"title": f"Recipe {recipe}", "content": lystOfRecipes[recipe]})
    # Display the items with expanding boxes
    for item in items:
        with st.expander(item["title"]):
            st.write(item["content"])
    

def capture_image():
    # Create a VideoCapture object to access the webcam
    cap = cv2.VideoCapture(0)

    # Set the video frame width and height (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        st.error("Error: Unable to access the webcam.")
        return

    # Read a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        st.error("Error: Unable to read frame from the webcam.")
        return

    # Save the frame as an image
    image_path = f"captured_images/captured_image_{len(os.listdir('captured_images')) + 1}.jpg"
    cv2.imwrite(image_path, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    st.success(f"Image captured and saved as {image_path}")

    # Release the VideoCapture and close the OpenCV window
    cap.release()
    
    return image_path


if __name__ == '__main__':
    main()
