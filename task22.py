import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import time
import subprocess

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

def speak(audio):
    """Speaks the provided audio using the text-to-speech engine."""
    engine.say(audio)
    engine.runAndWait()

def greetings():
    """Greets the user based on the current time of day."""
    hour = int(sr.Recognizer().listen(sr.Microphone()).recognize_google())
    if 4 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

def take_command():
    """Listens for user input using speech recognition and returns it as text."""
    try:
        print("Listening...")
        query = sr.Recognizer().listen(sr.Microphone(), timeout=5).recognize_google(language="en-US")
        print("You:", query)
    except sr.UnknownValueError:
        print("Sorry I didn't understand that. Could you please repeat?")
        query = input("You: ")
    return query

def process_query(query):
    """Processes the user's query and performs the appropriate action."""
    if "wikipedia" in query.lower():
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    elif "open youtube" in query.lower():
        speak("Opening YouTube...")
        webbrowser.open("youtube.com")
    elif "search in youtube" in query.lower():
        speak("What would you like to search for?")
        video_name = input("You : ")
        speak(f"Showing results for {video_name} on YouTube.")
        url = f'https://www.youtube.com/results?search_query={video_name}'
        webbrowser.open(url)
    elif "play music" in query.lower():
        speak("Playing music")
        music_dir = "C:/Users/HPO2PCH/Music"  # Replace with your music directory
        if os.path.exists(music_dir):
            os.system(f"start {music_dir}")  # Open the music directory in your default player
        else:
            speak("Music directory not found. Please specify a valid directory.")
    elif "show time" in query.lower():
        speak("It is time to...")  # Add a more engaging phrase before the time
        from datetime import datetime
        now = datetime.now()
        strTime = now.strftime("%H:%M:%S")
        speak(strTime)
    elif 'what\'s up?' in query.lower() or 'how are you?' in query.lower():
        stmts = ['Just doing my thing...', 'I am fine, thanks for asking. How about you?']
        speak(random.choice(stmts))
    elif "shutdown" in query.lower():
        speak('Are you sure you want to shut down?')
        ans = take_command().lower()
        if 'yes' in ans:
            speak('Alright, holding the switches off for 10 seconds.')
            time.sleep(10)
            subprocess.call(['shutdown', '/s'])  # Safely shut down the PC
        else:
            speak('Okay, I will not shut down your PC. Carry on!')
    else:
        try:
            details = wikipedia.summary(query, sentences=3)
            speak(details)
        except Exception as e:
            speak("Sorry, I couldn't find anything related to that on Wikipedia.")
            speak("Would you like me to search the web instead?")
            web_search = take_command().lower()
            if 'yes' in web_search:
                speak("Searching the web...")
                webbrowser.open(f"https://www.google.com/search?q={query}")
            else:
                speak("No problem. Let me know if you have any other questions.")

greetings()