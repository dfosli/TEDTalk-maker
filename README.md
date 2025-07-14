# TEDTalk Generator CLI 🎙️

Generate TED-style spoken audio files on any topic using OpenAI GPT and Azure Text-to-Speech.

## 💡 Why I Made This
I wanted a way to learn about any topic hands-free — like listening to a TED talk — even offline. This tool lets you generate short, informative talks about anything you're curious about.

## 🚀 What It Does
- Ask ChatGPT to generate a detailed script on any topic
- Formats it using SSML for expressive speech
- Uses Azure TTS to create a lifelike `.mp3` file
- Outputs audio to the `outputs/` folder

## 🛠️ How To Use
1. Clone this repo  
2. Install dependencies  
3. Add your `.env` file with:
    OPENAI_API_KEY=your_openai_key
    AZURE_SPEECH_KEY=your_azure_key
    AZURE_REGION=your_azure_region
4. Run the CLI:
    python main.py
5. Enter a topic and length. It will save an .mp3 to outputs/.

##📦 Requirements
- pip install -r requirements.txt