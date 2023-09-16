# This is the main logic file that contains hugging face model interaction

# This model is for detecting food in the image.
# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("image-classification", model="microsoft/resnet-50")
result = pipe("./man-holding-banana.jpeg")
print(result[0]['label'])


pipe = pipeline("text-generation", model="tiiuae/falcon-7b-instruct", trust_remote_code=True)
result = pipe("what can I make with apple, orange, and potato?")
print("this is the query result.")
