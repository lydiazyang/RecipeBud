# This is the main logic file that contains hugging face model interaction

# This model is for detecting food in the image.
# Use a pipeline as a high-level helper
from transformers import pipeline
import os
import openai
import requests
import json

openai.organization = "org-5Z0c3Uk1VG7t3TsczN6M4FCi"
#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key_path ="./key.txt" 

def askGPT(prompt="what can I make with potato?"):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content":prompt 
        },
        {
          "role": "user",
          "content": ""
        }      ],
      temperature=1,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    result = response["choices"][0]["message"]["content"]
    return result

def classifyImage(image):
    pipe = pipeline("image-classification", model="microsoft/resnet-50")
    result = pipe(image)
    return result[0]['label']

def analyze_nutrition(ingredients):
    # Edamam API endpoint for nutrition analysis
    endpoint = "https://api.edamam.com/api/nutrition-data"
    # Edamam API application ID and key
    app_id = "26722303"
    app_key = "44f19a04e17d83e91706e4047804e690"

    for ingredient in ingredients:
        # Parameters for the API request
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "ingr": ingredient
        }
        print(ingredient)

        try:
            # Send a GET request to the API
            response = requests.get(endpoint, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Print the nutritional information for the ingredient
                print("Nutritional Information for", ingredient)
                print("Calories:", data['calories'])
                print("Calories from Protein:", data['totalNutrientsKCal']['PROCNT_KCAL']['quantity'])
                print("Calories from Fat:", data['totalNutrientsKCal']['FAT_KCAL']['quantity'])
                print("Calories from Carbohydrates:", data['totalNutrientsKCal']['CHOCDF_KCAL']['quantity'])
                print("Grams in Protein:", data['totalNutrients']['PROCNT']['quantity'])
                print("Grams in Carbohydrates:", data['totalNutrients']['CHOCDF']['quantity'])
                print()  # Add a newline for separation

            else:
                print("Error for", ingredient, ":", response.status_code)

        except requests.exceptions.RequestException as e:
            print("Error for", ingredient, ":", e)

# Example ingredients list
ingredients = ["Orange per 100 grams", "Apple per 100 grams", "Banana per 100 grams"]

# Analyze nutrition for all ingredients
analyze_nutrition(ingredients)
