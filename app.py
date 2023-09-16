# This is the main logic file that contains hugging face model interaction

# This model is for detecting food in the image.
# Use a pipeline as a high-level helper
from transformers import pipeline
import os
import openai
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


