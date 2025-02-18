import openai
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext

# OpenAI API Key (Replace with your own key)
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
openai.api_key = OPENAI_API_KEY

# Initialize Speech Recognition & Text-to-Speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to get AI response
def naina_reply(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Function to handle user input (Text)
def handle_text_input():
    user_input = text_input.get()
    text_input.delete(0, tk.END)
    
    if user_input.lower() in ["exit", "quit"]:
        root.destroy()
    
    response = naina_reply(user_input)
    chat_display.insert(tk.END, f"You: {user_input}\nNaina: {response}\n\n")
    speak(response)

# Function to handle voice input
def handle_voice_input():
    with sr.Microphone() as source:
        chat_display.insert(tk.END, "Listening...\n")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        chat_display.insert(tk.END, f"You (Voice): {command}\n")
        response = naina_reply(command)
        chat_display.insert(tk.END, f"Naina: {response}\n\n")
        speak(response)
    except sr.UnknownValueError:
        chat_display.insert(tk.END, "Naina: Sorry, I couldn't understand.\n\n")

# Function to make Naina speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# GUI Setup
root = tk.Tk()
root.title("Naina - AI Assistant")
root.geometry("500x600")

chat_display = scrolledtext.ScrolledText(root, width=60, height=20, wrap=tk.WORD)
chat_display.pack(pady=10)

text_input = tk.Entry(root, width=50)
text_input.pack(pady=5)

send_button = tk.Button(root, text="Send", command=handle_text_input)
send_button.pack()

voice_button = tk.Button(root, text="🎤 Speak", command=handle_voice_input)
voice_button.pack()

root.mainloop()
