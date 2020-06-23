from pynput.keyboard import Key, Controller
import time
import pyttsx3
converter = pyttsx3.init()
keyboard = Controller()
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
converter.setProperty('voice', voice_id)
converter.runAndWait()
converter.setProperty('rate', 200)
converter.setProperty('volume', 0.7)
with open('text.txt') as text:
    to_type = text.readlines()

time.sleep(5)
for line in to_type:
    print(line)
    if line[:3] == 'say':
        print('found say')
        converter.say(line[5:])
        converter.runAndWait()
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

converter.runAndWait()

