import ollama
import sys


def describe_image(image_path):
    
    prompt = """Look carefully at the provided image and describe it in detail. Include specific details about the environment, objects, characters, and any notable features you can see in 1 paragraph.
    
    Then imagine you are a character in an adventure game. Describe in 3 sentences in another paragraph what a character would do in the setting based off this image. 
    Use first person perspective and include details about the actions you would take. Pay no attention to whether or not a character is in the image.

    Just state exactly what a person would do in this scenario.
    """
    
    description = ""
    inside_think = False

    res = ollama.chat(
        model="llava",
        messages=[
            {
                'role': 'user',
                'content': prompt,
                'images': [f'./adventure-arid-barren-210307.jpg']
            }
        ]
        )
    
    description = res['message']['content']
    return description

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python llava.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    try:
        description = describe_image(image_path)
        print("\nImage Description:\n", description)
    except Exception as e:
        print(f"Error processing image: {e}")
        sys.exit(1)
