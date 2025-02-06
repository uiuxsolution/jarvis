import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import requests
import datetime
import random
import wikipedia
import math
import smtplib
import winshell
import pyautogui
import subprocess
import psutil
import socket
import screen_brightness_control as sbc
import wolframalpha
import json
import cv2
import speedtest

# Initialize engines and APIs
engine = pyttsx3.init()
recognizer = sr.Recognizer()
wolframalpha_client = wolframalpha.Client("YOUR_WOLFRAMALPHA_API_KEY")
openweather_api_key = "428cea1c90b563227f08bd279c2794a3"

def speak(text):
    """Convert text to speech"""
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to voice commands"""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print("User said:", command)
            return command
        except Exception as e:
            print(f"Error: {e}")
            return ""

def execute_command(command):
    """Execute extensive voice commands"""
    # System & Application Control
    if any(cmd in command for cmd in ["open notepad", "launch notepad"]):
        speak("Opening Notepad")
        os.system("notepad")

    elif any(cmd in command for cmd in ["open chrome", "launch chrome"]):
        speak("Opening Google Chrome")
        os.system("start chrome")

    elif any(cmd in command for cmd in ["open calculator", "launch calculator"]):
        speak("Opening Calculator")
        os.system("calc")

    # Browser & Search Commands
    elif "search youtube" in command:
        query = command.replace("search youtube", "").strip()
        speak(f"Searching YouTube for {query}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")

    elif "search google" in command:
        query = command.replace("search google", "").strip()
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")

    # System Information
    elif "system info" in command:
        speak(f"CPU Usage: {psutil.cpu_percent()}%")
        speak(f"Memory Usage: {psutil.virtual_memory().percent}%")
        speak(f"Disk Usage: {psutil.disk_usage('/').percent}%")

    # Network & Internet Commands
    elif "internet speed" in command:
        speak("Testing internet speed. Please wait.")
        st = speedtest.Speedtest()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        speak(f"Download speed: {download_speed:.2f} Mbps")
        speak(f"Upload speed: {upload_speed:.2f} Mbps")

    # Advanced Search & Information
    elif "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            speak(f"According to Wikipedia: {result}")
        except:
            speak("Sorry, couldn't find information on that topic.")

    elif "calculate" in command:
        query = command.replace("calculate", "").strip()
        try:
            # Use WolframAlpha for advanced calculations
            res = wolframalpha_client.query(query)
            answer = next(res.results).text
            speak(f"The result is {answer}")
        except:
            speak("Sorry, I couldn't perform the calculation")

    # Entertainment & Utility
    elif "tell me a joke" in command:
        jokes = [
            "Why do programmers prefer dark mode? Light attracts bugs!",
            "I told my computer I needed a break, and now it won't stop sending me Kit-Kat ads.",
            "Why do Java developers wear glasses? Because they can't C#."
        ]
        speak(random.choice(jokes))

    # Weather Commands
    elif "weather" in command:
        city = "New York"  # Default city, can be made dynamic
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_api_key}&units=metric"
        response = requests.get(url).json()
        
        if response.get("main"):
            temp = response["main"]["temp"]
            description = response["weather"][0]["description"]
            speak(f"In {city}, it's {temp}°C with {description}")
        else:
            speak("Couldn't fetch weather information")

    # Screen & System Control
    elif "screenshot" in command:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        pyautogui.screenshot(f"screenshot_{timestamp}.png")
        speak(f"Screenshot saved as screenshot_{timestamp}.png")

    elif "lock computer" in command:
        speak("Locking computer")
        os.system("rundll32.exe user32.dll,LockWorkStation")

    elif "shutdown" in command:
        speak("Shutting down the computer")
        os.system("shutdown /s /t 1")

    # Exit Command
    elif "exit" in command or "goodbye" in command:
        speak("Goodbye! JARVIS signing off.")
        exit()

def jarvis():
    """Main JARVIS loop"""
    speak("JARVIS is online. Say 'Hello Jarvis' to activate.")
    while True:
        command = listen()
        if "hello jarvis" in command:
            speak("Yes, sir? How can I help you?")
            while True:
                command = listen()
                if command:
                    execute_command(command)

if __name__ == "__main__":
    jarvis()
