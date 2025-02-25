# import whisper
# import warnings
# from langchain import LangChainDepreciationWarning
# warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
# import ollama
#from langchain.chains import ConversationChain
from langchain_ollama import OllamaLLM
#from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from ollama import generate
#from langchain.schema import SystemMessage
# from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
#from langchain.chains import create_history_aware_retriever
#from PIL import Image
import base64
import io
from llava import describe_image
from voice import waveform_from_mic, speech_to_text



def generate_story_text():
    game_prompt = """
    Generate the background for a text-based adventure game. The world should be filled with mystery and challenges, and the player will uncover its history as they explore. 

    ### Structure:
    1. **Setting:** 
    - Describe a unique world (e.g., fantasy, sci-fi, post-apocalyptic).  
    - Establish the current state of the world and any major conflicts.  

    2. **Main Objective:**  
    - Define the player’s overarching goal (e.g., escape, find an artifact, solve a mystery).  

    3. **Key Locations & NPCs:**  
    - Create 3-5 major locations with distinct challenges.  
    - Introduce key NPCs and factions that shape the story.  

    4. **Sidekick:**  
    - Introduce a sidekick character who accompanies the player.  
    - Describe their background, abilities, and how they assist the player.  

    5. **Dynamic Elements:**  
    - Ensure the world evolves based on the player’s choices.  
    - Leave room for AI-generated details to emerge during gameplay.  

    Keep descriptions immersive but brief. The game world should unfold naturally as the player interacts with it.
    Output should be in paragraph format. Limit the output to 3 paragraphs. Use natural language like since you are explaining directly to the player.
    """

    
    inside_think = False
    
    story = ""
    for part in generate(model='deepseek-r1:14b', prompt=game_prompt, stream=True):
        response = part['response']
        if '<think>' in response:
            inside_think = True
        if '</think>' in response:
            inside_think = False
            continue
        if not inside_think:
            print(response, end="", flush=True)
            story += response

    return story

def generate_help_options(current_context=""):
    prompt = f"""Based on the current game situation, act as the player's sidekick and provide a brief description of the current situation, 1 piece of dialogue,
    followed by 4 numbered command options that would be most relevant for the player right now.
    Each option should be a single sentence command followed by a brief description.
    Format each option on a new line starting with a number (1-4).
    Make the commands practical and useful for the current game situation.
    Keep the descriptions clear and concise.
    Only output the brief description of the situation and the 4 numbered options and descriptions, nothing else.

    Your Output should be like this:

    [Brief description of the current situation]
    --------------------
    1. [Command 1]: [Description]
    2. [Command 2]: [Description]
    3. [Command 3]: [Description]
    4. [Command 4]: [Description]
    

    Current game context: {current_context}"""
    
    help_text = ""
    inside_think = False
    
    for part in generate(model='deepseek-r1:14b', prompt=prompt, stream=True):
        response = part['response']
        if '<think>' in response:
            inside_think = True
        if '</think>' in response:
            inside_think = False
            continue
        if not inside_think:
            help_text += response
            
    return help_text

def main():
    print("Welcome to the AI-Powered Adventure Game!")
    print("Type 'exit' or 'quit' to end the game.")
    print("Type 'help' to see available from sidekick.")
    
    # Generate background story
    print("\nGenerating AI story... (might take a while)")
    background = generate_story_text()
    
    # Initialize help options with the background context
    current_help_options = None
    
    llm_prompt = f"""
    You are the Game Master of a text-based adventure game, similar to a Dungeons and Dragons campaign.
    The player is an adventurer in a mysterious dungeon filled with secrets, treasures, and dangers.
    Your job is to describe the world, react to player actions, and make the game engaging.
    Keep responses immersive, creative, and interactive.

    The game starts with the following background story:
    {background}

    As the Game Master, you will advance the story based on the player's actions, describing the consequences and current situation.
    Do not generate any options for the player. Instead, stop at a point where the player needs to decide their next action.
    Remember the player's actions and use them to shape the story dynamically. Occasionally, consider explaining what the sidekick is doing or thinking in the situations.
    Only respond when you receive a user input. Limit response to 1 paragraph.
    """

    llm = OllamaLLM(model="deepseek-r1:14b",
                     temperature=0.1)
    
    conversation_history = []

    # Create the conversation chain
    prompt = ChatPromptTemplate.from_messages([
        ("system", llm_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    def show_help():
        print("\nAvailable commands:")
        print(current_help_options)
        print("\nYou can also type 'help' to see this menu again or 'exit' to quit the game.")
    
    while True:
        print('\n')
        use_image = input("Do you want to influence the story with an image? (yes/no): ").strip().lower()

        user_input = ""
        if use_image == "yes":
            image_path = input("Enter the path to your image file: ").strip()
            try:
                image_description = describe_image(image_path)
                print("\nYour action based on image:\n", image_description)
                user_input = f"{image_description}]"
            except Exception as e:
                print(f"Error processing image: {e}")
        else:
            use_voice = input("Do you want to use your voice to influence the story? (yes/no): ").strip().lower()
            if use_voice == "yes":
                print("Speak your command:\n")
                
                waveform = waveform_from_mic()
                if len(waveform) == 0:
                    print("No audio recorded.")
                    return

                text = speech_to_text(waveform)
                print("Transcription:", text)
                user_input = text
            else:
                user_input = input("Type Your command: ").strip()
        
        if user_input.lower() in ["exit", "quit"]:
            print("\nGame Master: Thanks for playing! Goodbye!")
            break
            
        if user_input.lower() == "help":
            current_help_options = generate_help_options(conversation_history)
            show_help()
            continue
        
        # Ask user if they want to influence the story with an image
        
        
        ai_response = ""
        inside_think = False
        
        # Get the chat history
        chat_history = conversation_history
        
        # Generate response using the chain
        for part in chain.stream({"input": user_input, "history": chat_history}):
            if '<think>' in part:
                inside_think = True
            if '</think>' in part:
                inside_think = False
                continue
            if not inside_think:
                print(part, end="", flush=True)
                ai_response += part
        
        print()  # Print a newline after the streamed response
        
        # Save the interaction to memory
        conversation_history.append({"role": "human", "content": user_input})
        conversation_history.append({"role": "ai", "content": ai_response})

if __name__ == "__main__":
    main()