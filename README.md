# Basketball Play Generator

This is a Streamlit app that generates basketball plays using OpenAI's GPT-4 model.

## Installation

1. Clone this repository.
2. Install the requirements: `pip install -r requirements.txt`
3. Set your OpenAI API key as an environment variable: `export OPENAI_API_KEY=your-api-key`

## Usage

1. Run the app with: `streamlit run app/main.py`
2. Use the selection boxes to specify the type of play you want to generate.
3. Click the 'Generate Plays' button to generate play descriptions.
4. Select a play from the dropdown to view its description.
5. Click the 'Generate Play-by-Play' button to generate a detailed, step-by-step, play-by-play description of the selected play.
6. Click the 'Generate Animation' button to generate an animation of the play-by-play.

## Note

The generated plays, play-by-play descriptions, and animations are saved in the [assets](file:///Users/kylemcgraw/Documents/Hackathon-2023/hack-2023-basketball-play-generator/app/main.py#80%2C20-80%2C20) directory.