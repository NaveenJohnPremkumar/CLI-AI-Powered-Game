import os
import ollama

# # List all images in the current directory
# images = "/home/naveenjp/eecs449/CLI-AI-Powered-Text-Adventure-Game/adventure-arid-barren-210307.jpg"

# # Loop through each image and process it
# for image in images:
#     print(f"Processing image: {image}")

    # Step 1: Describe the image
res = ollama.chat(
    model="llava",
    messages=[
        {
            'role': 'user',
            'content': 'Describe this image',
            'images': [f'./adventure-arid-barren-210307.jpg']
        }
    ]
)

# Extract the description from the response
meal_description = res['message']['content']
print("Meal Description:", meal_description)

# print("--------------")

# # Step 2: Use Llama model to count calories based on the description
# res_calories = ollama.chat(
#     model="llama3.1:8b",
#     messages=[
#         {
#             'role': 'user',
#             'content': f'Read ingrediens and estimate calories for each meal and return it as json: {meal_description}'
#         }
#     ]
# )

#     # Print the calorie count in JSON format
# print("Calorie Estimate:", res_calories['message']['content'])