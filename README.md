# TEDTalk-generator

Generate TED-style spoken audio files on any topic and any length using OpenAI GPT and Azure Text-to-Speech.

## 💡 Why I Made This
I wanted to learn to program with an Ai API. I made this small audio file generator to get some learning experience 
to work on even bigger projects in the future. The idea for this was to be able to listen to "podcasts" anywhere, by created audio files
while online, and being able to bring these offline, for example using a shared folder between your computer and phone.


## 🚀 What It Does
It has a CLI-based interface.
- It will ask you for a topic, duration, and voice (between 5 different as it is now)
- Sends a prompt to ChatGPT, asking for a "TedTalk-like" script
- Returns a script formatted in SSML to simulate expressive speech
- Uses Azure TTS to create a lifelike `.mp3` file
- Outputs audio to the `outputs/` folder.

## 🛠️ How To Use
1. Clone this repo  
2. Install dependencies  
3. Add your `.env` file with:
    
    OPENAI_API_KEY=your_openai_key
    
    AZURE_SPEECH_KEY=your_azure_key
    
    AZURE_REGION=your_azure_region

    OpenAI API and Azure can be a little troublesome to set up. the links to the websites are below. there are also lots of guides to help set this up.
4. Run the CLI:
    python main.py
5. Enter a topic, length and voice-number. It will save an .mp3 to outputs/.

##📦 Requirements
- pip install -r requirements.txt

I used ChatGPT-3.5-turbo as this is the cheapest to use, costing about $0.001 per i minute of script generated (basically free)
https://openai.com/api/

AzureTTS has a free plan of 500 000 characters per month for Neural voices, which is the one i used. this can be changed to "normal" voices
for 5 million characters a month.
https://azure.microsoft.com/en-us/

Sample audio here: https://github.com/dfosli/TEDTalk-maker/releases/download/v1.0/history_of_ai.mp3