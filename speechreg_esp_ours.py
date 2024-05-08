# import speech_recognition as sr
# import serial
# import websocket
# import time
# import os

# r = sr.Recognizer()

# def send_command_to_esp32(command):
#     websocket_url = "ws://192.168.207.71:81"  # Replace with your ESP32 WebSocket server URL
#     ws = websocket.create_connection(websocket_url)
#     ws.send(command)
#     ws.close()

# def recognize_speech():
#     # send_command_to_esp32("off")
#     with sr.Microphone() as source:
#         print("Say something!")
#         audio = r.listen(source,10,5)  # Records for a maximum of 5 seconds


#     try:
#         print("po")
#         text = r.recognize_google(audio)
#         # text = r.recognize_sphinx(audio)
        

#         print("You said: " + text)
#         if "on" in text:
#             # ser.write(b'1')  # Sending '1' to turn on the LED
#             send_command_to_esp32("on")
#             print('Sent 1')
#         elif "off" in text:
#             # ser.write(b'0')  # Sending '0' to turn off the LED
#             send_command_to_esp32("off")
#             print('Sent 0')


#     except sr.UnknownValueError:
#         print("Google Speech Recognition could not understand audio")
#     except sr.RequestError as e:
#         print("Could not request results from Google Speech Recognition service; {0}".format(e))

# # Continuously listen for speech
# send_command_to_esp32("off")
# while True:
#     recognize_speech()

# import openai
# import speech_recognition as sr
# import websocket

# openai.api_key = 'sk-'  # Replace with your actual API key

# r = sr.Recognizer()

# def send_command_to_esp32(command):
#     websocket_url = "ws://192.168.207.71:81"  # Replace with your ESP32 WebSocket server URL
#     ws = websocket.create_connection(websocket_url)
#     ws.send(command)
#     ws.close()

# def get_light_control_response(prompt):
#     response = openai.Completion.create(
#         engine="gpt-3.5-turbo-16k",
#         prompt=prompt,
#         max_tokens=50  # Adjust as needed
#     )

#     return response.choices[0].text.strip()

# def recognize_speech():
#     with sr.Microphone() as source:
#         print("Say something!")
#         audio = r.listen(source, 10, 5)  # Records for a maximum of 5 seconds

#     try:
#         print("Processing speech...")
#         text = r.recognize_google(audio)
#         print("You said: " + text)

#         # Use ChatGPT to determine on or off
#         chat_prompt = f"The user said: {text}. Should I turn the lights on or off?"
#         chat_response = get_light_control_response(chat_prompt)

#         if "on" in chat_response.lower():
#             send_command_to_esp32("on")
#             print('Sent "on" to ESP32')
#         elif "off" in chat_response.lower():
#             send_command_to_esp32("off")
#             print('Sent "off" to ESP32')

#     except sr.UnknownValueError:
#         print("Google Speech Recognition could not understand audio")
#     except sr.RequestError as e:
#         print("Could not request results from Google Speech Recognition service; {0}".format(e))

# # Continuously listen for speech
# send_command_to_esp32("off")
# while True:
#     recognize_speech()

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

import openai
import speech_recognition as sr
import websocket
import http.client
import json
import requests

r = sr.Recognizer()

def send_command_to_esp32(command):
    websocket_url = "wss://192.168.31.139:81"  # Replace with your ESP32 WebSocket server URL
    ws = websocket.create_connection(websocket_url)
    ws.send(command)
    ws.close()

def gemini (text):

    # genai.configure(api_key=GOOGLE_API_KEY)
    # model = genai.GenerativeModel('gemini-pro')
    # prompt="The user said"+text+"now, should i on or off the light??"
    # response = model.generate_content(prompt)
    # to_markdown(response.text)
    # print(response.text)
    # if "on" in response.text:
        return 1
    # if "off" in response.text:
    #     return 0
def recognize_speech():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source, 10, 5)  # Records for a maximum of 5 seconds

    try:
        print("Processing speech...")
        text = r.recognize_google(audio)
        print("You said: " + text)

        # Use ChatGPT to determine on or off
        # chat_prompt = f"The user said: {text}. Should I turn the lights on or off?"
        # response = perform_sentiment_analysis(text)
        response=gemini(text)

        if response=='1':
            send_command_to_esp32("on")
            print('Sent "on" to ESP32')
        elif response=='0':
            send_command_to_esp32("off")
            print('Sent "off" to ESP32')

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Continuously listen for speech
send_command_to_esp32("off")
while True:
    recognize_speech()
