# AI-Powered Text Adventure Game

This project is an AI-powered text adventure game that uses advanced language models to generate immersive stories and respond to player inputs. The game master is an AI that describes the world, reacts to player actions, and makes the game engaging.

## Features

- Generate background stories for the game.
- Allow players to influence the story with images.
- Provide help options based on the current game context.
- Interactive and dynamic storytelling.

## Setup Instructions

### Prerequisites

- Python 3.9.13
- Virtual environment tool (e.g., `venv` or `virtualenv`)

### Step-by-Step Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/CLI-AI-Powered-Text-Adventure-Game.git
   cd CLI-AI-Powered-Text-Adventure-Game
   ```

2. **Create a virtual environment:**

   ```sh
   python -m venv env
   ```

3. **Activate the virtual environment:**

   - On Windows:
     ```sh
     .\env\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source env/bin/activate
     ```

4. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

5. **Install Ollama:**

   ```sh
   pip install ollama
   ```

6. **Download the required models:**

   - **Whisper Model:**
     Download the `base.en.pt` model from [Whisper](https://github.com/openai/whisper) and place it in the main directory.
     "https://openaipublic.azureedge.net/main/whisper/models/25a8566e1d0c1e2231d1c762132cd20e0f96a85d16145c3a00adf5d1ac670ead/base.en.pt"

   - **LLaVA Model:**
     Ensure you have access to the `llava` and `deepseek-r1:14b` models from Ollama. You can download them using the following commands:
     ```sh
     ollama download llava
     ollama download deepseek-r1:14b
     ```

### Running the Game

To start the game, run the following command:

```sh
python game.py
```

### Using the Image Description Feature

To use an image to influence the story, you can run the `llava.py` script with the path to your image file:

```sh
python llava.py <image_path>
```

### Example Usage

1. Start the game:
   ```sh
   python game.py
   ```

2. Follow the prompts to generate a background story and interact with the game master.

3. To influence the story with an image, provide the path to your image file when prompted.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
