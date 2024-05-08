import speech_recognition as sr
import serial
import websocket
import time
import os
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import Markdown

r = sr.Recognizer()

def send_command_to_esp32(command):
    websocket_url = "ws://192.168.31.139:81"  # Replace with your ESP32 WebSocket server URL
    ws = websocket.create_connection(websocket_url)
    ws.send(command)
    ws.close()

def recognize_speech():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source,10,5)

    try:
        text = r.recognize_google(audio)
        # text = r.recognize_sphinx(audio)
        
        print("You said: " + text)
        return text

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def get_gemini_response(text):
    response = model.generate_content(text)
    return response.text

# Configure Geminai
GOOGLE_API_KEY=os.getenv('Google_api')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Continuously listen for speech and control the light accordingly
send_command_to_esp32("off")
while True:
    spoken_text = recognize_speech()
    if spoken_text:
        action_prompt = "What do you want me to do? Turn the light on or off?"
        spoken_text += " " + action_prompt
        gemini_response = get_gemini_response(spoken_text)
        print("Gemini says: ", gemini_response)
        if "on" in gemini_response or "down" in  gemini_response:
            send_command_to_esp32("on")
            print('Sent 1')
        elif "off" in gemini_response:
            send_command_to_esp32("off")
            print('Sent 0')
