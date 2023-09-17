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
    #items = ['Item 1', 'Item 2', 'Item 3']

    #list to of Ingredients camptured
    ingredientsList =["apple", "orange", "mango", "potato", "cabbage", "carrot", "lentils"] #list()

    # Define content for each item
    content = {}
    for ingredient in ingredientsList:
        content[ingredient] = askGPT(f"Give me your estimate the calories, grams of sugar, grams of fat, and grams of carbohydrates per 100g of {ingredient} as a list")

    # Display expanders for each item
    for ingredient in ingredientsList:
        with st.sidebar.expander(ingredient):
            st.write(content[ingredient])
    
    
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
        st.write("Updated Ingredients List:", session_state['ingredientsList'])

        displayRecipes(session_state['ingredientsList'])

def displayRecipes(ingredientsList):
    items = []
    #now we are gonna send the ingredient list to ask gpt
    prompt = f"I have following Ingredients :{','.join(ingredientsList)}. What can I make with these \
            Ingredients? Give me A list of detailed recipes with measurements containing these ingredients with Nutrition Facts per 100g based on the widely accepted nutritional value of each of these ingredients. Rank the list from \
            highest nutritional value to lowest. Give me results in \
            following format and do not deviate from this format:\
            ['Recipe title', 'content of recipe and nutritional facts per 100g']. Only give me the list. Do not add commentary or personalized responses."
    LLMResult = askGPT(prompt)
    lystOfRecipes = LLMResult.split('\n\n')
    print(lystOfRecipes)
    for recipe in range(1,len(lystOfRecipes)-1):
        items.append({"title": lystOfRecipes[recipe].split(":")[0], "content": ""})
    # Display the items with =expanding boxes
    for item in items:
        #for side bar's item
        #with st.sidebar.expander(item):
            #st.write("man-holding-banana.jpeg")
        #main page items
        with st.expander(item["title"]):
            st.write(askGPT(f"Give me a detailed recipe for a dish called {item['title']} containing all of the following ingredients: {','.join(ingredientsList)}. Make sure your response is easy to follow and comprehensive."))
    

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
