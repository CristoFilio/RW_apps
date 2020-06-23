from pynput.keyboard import Key, Controller
import time
import os
from gtts import gTTS
import playsound
keyboard = Controller()

with open('text.txt') as text:
    to_type = text.readlines()

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)


time.sleep(5)
for line in to_type:
    print(line)
    if line[:3] == 'say':

        speak(line[5:])
    if line[:3] == 'ter':
        keyboard.press(Key.alt)
        keyboard.press('0')
        keyboard.release(Key.alt)
        keyboard.release('0')
        time.sleep(1)
        continue
    if line[:3] == 'esc':
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)
        time.sleep(1)
        continue
    if line[:3] == 'run':
        time.sleep(1)
        keyboard.press(Key.ctrl_l)
        keyboard.press(Key.shift_l)
        keyboard.press(Key.f10)
        keyboard.release(Key.ctrl_l)
        keyboard.release(Key.shift_l)
        keyboard.release(Key.f10)
    for character in line:
        time.sleep(0.08)
        keyboard.press(character)
        keyboard.release(character)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
