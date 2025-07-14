# from openai import OpenAI
# from dotenv import load_dotenv
# import azure.cognitiveservices.speech as speechsdk
# import os
# import textwrap


# #Functions
# def create_full_ssml(chatgpt_ssml_snippet: str, voice_name: str) -> str:
#     return f"""
#         <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" 
#            xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
#         <voice name="{voice_name}">
#         {chatgpt_ssml_snippet}
#         </voice>
#         </speak>
#         """
# #Setup
# load_dotenv()
# client = OpenAI()

# #OpenAI() automatically loads OPENAI_API_KEY from .env file so it doesnt need its own variable
# speech_key = os.getenv("AZURE_SPEECH_KEY")
# service_region = os.getenv("AZURE_REGION")
# voice_names = {
#     "1": "en-US-AndrewNeural",
#     "2": "en-US-EmmaNeural",
#     "3": "en-US-TonyNeural",
#     "4": "en-GB-EthanNeural",
#     "5": "en-GB-HollieNeural"
# }

# topic = input("Enter the topic for the TED Talk: ")
# length_minutes = input("Enter the desired length in minutes: ")

# output_dir = "outputs"
# os.makedirs(output_dir, exist_ok=True)
# filename = os.path.join(output_dir, f"{topic.lower().replace(' ', '_')}")
# filename_text = filename + ".txt"
# filename_save = filename + ".mp3"

# speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# audio_config = speechsdk.audio.AudioOutputConfig(filename=filename_save)
# synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)


# while True:
#     voice = input("Enter the desired voice out of:\n1. Andrew - US\n2. Emma - US\n3. Tony - US\n4. Ethan - GB\n5. Hollie - GB\n")
#     if voice in ["1","2","3","4","5"]:
#         break
#     print("Answer one of the numbers.")

# system_prompt = """
# You are an expert TED Talk speaker tasked with generating high-quality talks in SSML format, based on topics I provide. Your responses must return only the inner SSML content, excluding <speak> or <voice> tags — I will handle those myself.

# The talk should be between 5–10 minutes long when read aloud, and must prioritize:

# Clear and structured explanation of the topic

# As much useful detail as time allows

# Minimal generalizations, filler, or fluff

# You should not waste time with vague introductions or flowery conclusions. Go straight to the point. Any intro or outro should contain new, informative content or context — never empty scene-setting.

# Assume the listener is intelligent but unfamiliar with the topic. Explain necessary terms and concepts when appropriate, clearly and concisely.

# Use Azure-supported SSML to enhance delivery, including:

# <mstts:express-as style="narration-professional"> for the base style

# <prosody rate="medium"> or "fast" for pacing (never "slow")

# <emphasis> to highlight ideas

# <break time="xxxms"/> to add rhythm where it improves comprehension

# Avoid excessive use of <emphasis> or <break>. Use them deliberately where they improve naturalness and clarity.

# Return only the content inside the <mstts:express-as> block. Do not include any external tags, notes, or formatting explanations. Keep your tone intelligent, professional, and efficient — like a well-prepared expert speaking with purpose.
# """
# user_prompt = f"""
# Give a TED-style talk about {topic}, meant to be spoken aloud in {length_minutes} minutes.
# Focus on clear explanation and depth — no filler, no generic intro/outro.
# Format as valid SSML inside a single <mstts:express-as style="narration-professional">...</mstts:express-as> block.
# Output only that inner content.
# """


# if __name__ == "__main__":
#     #get response from ChatGPT
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt}
#         ],
#         temperature=0.3,
#     )

#     #creates full SSML with voice and outer tags
#     talk_script = response.choices[0].message.content.strip()
#     talk_script = create_full_ssml(talk_script, voice_names[voice])
    
#     #writes response to text file
#     with open(filename_text, "w", encoding="utf-8") as f:
#         f.write(talk_script)

#     #formats text file, this is done just so the entire response isnt on one line in the .txt
#     with open(filename_text, "r+", encoding="utf-8") as f:
#         content = f.read()
#         f.seek(0)
#         f.write(textwrap.fill(content, width=120))
#         f.truncate()
#     print(f"\n📝 Story saved to {filename}")

#     #read the text file, and gives it to Azure API
#     with open(filename_text, "r", encoding="utf-8") as f:
#         content = f.read()

#     content_clean = content.replace("\n", " ").strip()

#     result = synthesizer.speak_ssml_async(content_clean).get()

#     if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#         print(f"✅ TED-style audio generated successfully: {filename_save}")
#     else:
#         print("❌ Speech synthesis failed.")
#         print(result.cancellation_details.error_details)
from openai import OpenAI
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import os

# -------------- Setup --------------
load_dotenv()
client = OpenAI()
speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_REGION")

voice_names = {
    "1": "en-US-AndrewNeural",
    "2": "en-US-EmmaNeural",
    "3": "en-US-TonyNeural",
    "4": "en-GB-EthanNeural",
    "5": "en-GB-HollieNeural"
}

# -------------- Helpers --------------
def create_full_ssml(chatgpt_ssml_snippet: str, voice_name: str) -> str:
    return f"""
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" 
       xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
  <voice name="{voice_name}">
    {chatgpt_ssml_snippet}
  </voice>
</speak>
""".strip()

def sanitize_filename(name: str) -> str:
    return "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip().replace(" ", "_")

# -------------- Prompts --------------
system_prompt = """You are an expert TED Talk speaker tasked with generating high-quality talks in SSML format, based on topics I provide. Your responses must return only the inner SSML content, excluding <speak> or <voice> tags — I will handle those myself.
The talk should be about the specified amount of minutes long when read aloud, and must prioritize:
• Clear and structured explanation of the topic
• As much useful detail as time allows
• Minimal generalizations, filler, or fluff
You should not waste time with vague introductions or flowery conclusions. Go straight to the point. Explain necessary terms and concepts clearly and concisely.
Use Azure-supported SSML to enhance delivery, including:
<mstts:express-as style="narration-professional">, <prosody>, <emphasis>, and <break>
Avoid overusing these — use them deliberately where they improve clarity.
Return only the content inside the <mstts:express-as> block. Do not include any external tags or notes."""

# -------------- Main --------------
if __name__ == "__main__":
    # get user input
    topic = input("Enter the topic for the TED Talk: ")
    length_minutes = input("Enter the desired length in minutes: ")

    while True:
        voice = input("Choose a voice:\n1. Andrew (US)\n2. Emma (US)\n3. Tony (US)\n4. Ethan (GB)\n5. Hollie (GB)\n> ")
        if voice in voice_names:
            break
        print("❌ Invalid selection, try again.")

    safe_topic = sanitize_filename(topic)
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    filename_base = os.path.join(output_dir, safe_topic.lower())
    filename_txt = filename_base + ".txt"
    filename_mp3 = filename_base + ".mp3"

    # user prompt
    user_prompt = f"Give a TED-style talk about {topic}, meant to be spoken aloud in {length_minutes} minutes. Focus on clear explanation and depth — no filler. Format as valid SSML inside a single <mstts:express-as style=\"narration-professional\">...</mstts:express-as> block."

    print("\n📡 Generating content...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
    )

    inner_ssml = response.choices[0].message.content.strip()
    full_ssml = create_full_ssml(inner_ssml, voice_names[voice])

    # Save to .txt
    with open(filename_txt, "w", encoding="utf-8") as f:
        f.write(full_ssml)

    # Azure TTS
    print("🎙️ Synthesizing speech...")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename_mp3)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = synthesizer.speak_ssml_async(full_ssml).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"✅ TED-style audio generated successfully: {filename_mp3}")
    else:
        print("❌ Speech synthesis failed.")
        print(result.cancellation_details.error_details)