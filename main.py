import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc

# Text-to-speech setup
engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# Voice input using sounddevice (no PyAudio)
def listen():
    fs = 44100
    seconds = 4

    print("Listening...")
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()

    wav.write("input.wav", fs, recording)

    r = sr.Recognizer()
    with sr.AudioFile("input.wav") as source:
        audio = r.record(source)

    try:
        command = r.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except:
        print("Could not understand")
        return ""

# Open applications
def open_app(command):
    if "notepad" in command:
        os.system("notepad")
        speak("Opening Notepad")
    elif "calculator" in command:
        os.system("calc")
        speak("Opening Calculator")

# Open websites in Edge
def open_website(command):
    edge_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s"

    if "youtube" in command:
        webbrowser.get(edge_path).open("https://www.youtube.com")
        speak("Opening YouTube")
    elif "google" in command:
        webbrowser.get(edge_path).open("https://www.google.com")
        speak("Opening Google")

# Control volume
def control_volume(command):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    if "volume up" in command:
        volume.SetMasterVolumeLevelScalar(1.0, None)
        speak("Volume increased")
    elif "volume down" in command:
        volume.SetMasterVolumeLevelScalar(0.2, None)
        speak("Volume decreased")

# Control brightness
def control_brightness(command):
    if "brightness" in command:
        try:
            level = int([int(s) for s in command.split() if s.isdigit()][0])
            sbc.set_brightness(level)
            speak(f"Brightness set to {level}")
        except:
            speak("Couldn't set brightness")

# Main loop
def main():
    speak("Assistant started")

    while True:
        command = listen()

        if command == "":
            continue

        if "open" in command:
            open_app(command)
            open_website(command)

        elif "volume" in command:
            control_volume(command)

        elif "brightness" in command:
            control_brightness(command)

        elif "stop" in command or "exit" in command:
            speak("Goodbye")
            break

        else:
            speak("Command not recognized")

# Run assistant
if __name__ == "__main__":
    main()
