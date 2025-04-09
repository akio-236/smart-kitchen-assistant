import speech_recognition as sr
from gtts import gTTS
import sounddevice as sd
import soundfile as sf
import numpy as np
import os
import time


class VoiceControl:
    def __init__(self, recipe_manager, timer_manager):
        self.recognizer = sr.Recognizer()
        self.recipe_manager = recipe_manager
        self.timer_manager = timer_manager
        self.sample_rate = 44100
        self.commands = {
            "next": self._next_step,
            "previous": self._previous_step,
            "set timer": self._set_timer,
            "remind me": self._set_reminder,
            "stop": self._stop_timer,
        }

    def listen(self):
        try:
            # Record audio using sounddevice
            print("Listening...")
            recording = sd.rec(
                int(3 * self.sample_rate), samplerate=self.sample_rate, channels=2
            )
            sd.wait()

            # Save as WAV file
            sf.write("temp.wav", recording, self.sample_rate)

            # Process with SpeechRecognition
            with sr.AudioFile("temp.wav") as source:
                audio = self.recognizer.record(source)

            text = self.recognizer.recognize_google(audio).lower()
            print(f"Heard: {text}")
            return text

        except Exception as e:
            print(f"Error: {e}")
            return None

    def process_command(self, command):
        for cmd, action in self.commands.items():
            if cmd in command:
                action(command)
                return True
        self.speak("Command not recognized")
        return False

    def _next_step(self, command):
        self.recipe_manager.next_step()
        self.speak("Next step")

    def speak(self, text):
        tts = gTTS(text=text, lang="en")
        tts.save("temp.mp3")
        os.system("start temp.mp3")  # Works on Windows
