# This is the main logic file that contains hugging face model interaction

# This model is for detecting food in the image.
# Use a pipeline as a high-level helper
from transformers import pipeline
import os
import openai

openai.organization = "org-5Z0c3Uk1VG7t3TsczN6M4FCi"
#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key_path ="./key.txt" 
print(openai.api_key)
print(openai.Model.list())


pipe = pipeline("image-classification", model="microsoft/resnet-50")
result = pipe("./man-holding-banana.jpeg")
print(result[0]['label'])


