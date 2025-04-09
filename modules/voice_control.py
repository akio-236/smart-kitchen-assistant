import speech_recognition as sr
from gtts import gTTS
import sounddevice as sd
import soundfile as sf
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
            "how many grams": self._unit_conversion,
        }

    def listen(self):
        try:
            print("Listening...")
            recording = sd.rec(
                int(3 * self.sample_rate), samplerate=self.sample_rate, channels=2
            )
            sd.wait()

            sf.write("temp.wav", recording, self.sample_rate)

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
        current_step = self.recipe_manager.get_current_step()
        self.speak(f"Moving to next step: {current_step}")

    def _previous_step(self, command):
        self.recipe_manager.previous_step()
        current_step = self.recipe_manager.get_current_step()
        self.speak(f"Going back to previous step: {current_step}")

    def _set_timer(self, command):
        try:
            parts = command.split()
            duration = int(parts[parts.index("for") + 1])
            unit = parts[parts.index("for") + 2]

            if "minute" in unit:
                duration *= 60
            self.timer_manager.add_timer(duration, "Timer completed!")
            self.speak(f"Timer set for {duration} seconds")
        except Exception as e:
            print(f"Timer error: {e}")
            self.speak("Could not set timer. Please try again")

    def _set_reminder(self, command):
        try:
            parts = command.split()
            duration = int(parts[parts.index("in") + 1])
            unit = parts[parts.index("in") + 2]
            reminder_text = " ".join(parts[parts.index("to") + 1 :])

            if "minute" in unit:
                duration *= 60
            self.timer_manager.add_timer(duration, reminder_text)
            self.speak(f"Reminder set: {reminder_text} in {duration} seconds")
        except Exception as e:
            print(f"Reminder error: {e}")
            self.speak("Could not set reminder. Please try again")

    def _stop_timer(self, command):
        # Implementation would go here
        self.speak("Timer stopping functionality not yet implemented")

    def _unit_conversion(self, command):
        # Basic conversion examples
        conversions = {
            "cup of sugar": "200 grams",
            "tablespoon of butter": "14 grams",
            "teaspoon of salt": "5 grams",
        }

        for item, conversion in conversions.items():
            if item in command:
                self.speak(f"One {item} is approximately {conversion}")
                return

        self.speak("Conversion not available for that ingredient")

    def speak(self, text):
        try:
            tts = gTTS(text=text, lang="en")
            tts.save("temp.mp3")
            os.system("start temp.mp3")  # Windows
            time.sleep(0.5)  # Let the file save
        except Exception as e:
            print(f"Speech error: {e}")
