# -*- coding: utf-8 -*-
#ゴール後ブザーを鳴らしゴールを周知する
import RPi.GPIO as GPIO
import time
import csv

buzzerpin=4

tempo = 146
note_length = 60/tempo

pitch_dic = {
        'C3':131,     'C#3':139,    'D3':147,
        'D#3':155,    'E3':165,     'F3':175,
        'F#3':185,    'G3':196,     'G#3':208,
        'A3':220,
        'A#3': 233,   'B3': 246,    'C4': 261,
        'C#4': 277,   'D4': 293,    'D#4': 311,
        'E4': 329,    'F4': 349,    'F#4': 370,
        'G4': 392,    'G#4': 415,   'A4': 440,
        'A#4': 466,   'B4': 493,    'C5': 523,
        'C#5': 554,   'D5': 587,    'D#5': 622,
        'E5': 659,    'F5': 698,    'F#5': 740,
        'G5': 783,  'G#5': 830,   'A5': 880,
        'A#5': 932,   'B5': 987,    'C6': 1046,
        'C#6': 1108,  'D6': 1174,   'D#6': 1244,
        'E6': 1318,   'F6': 1396,   'F#6': 1480,
        'G6': 1568,   'G#6': 1661,  'A6': 1760,
        'A#6': 1864,  'B6': 1975,   'C7': 2093
    }

duration_dic = {
    'whole': 1,            'half' : 0.5,
    'one-third' : 1/3,     'quarter' : 0.25,
    'dotted_eighth':0.75,'rest_little':1/60,
    'dotted_double':2.5,'double':2,
    'dotted_whole':1.5
}

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzerpin,GPIO.OUT)
    global buzzer
    buzzer=GPIO.PWM(buzzerpin,500)

def buzz():
    buzzer.start(0)
    time.sleep(1)
    buzzer.ChangeDutyCycle(50)
    ##########################

    for i in range(0, 5):
        music_Mario()

def read_music(filename:str):
    global tempo, note_length
    with open(filename, mode = "r") as f:
        reader = csv.reader(f)
        sheet = [row for row in reader]
    buzzer.start(0)
    time.sleep(1)
    buzzer.ChangeDutyCycle(50)
    tempo = int(sheet[0][0])
    note_lenght = 60/tempo
    sheet.pop(0)
    for notes in sheet:
        if notes == []:
            return
        note1, note2, note3,duration = notes
        if note1 == 'rest':
            rest(duration)
        else:
            triad(note1, note2, note3, duration)
            rest("rest_little")

def music_Mario():
    coard('C4', 'G4', 'one-third')
    coard('E4', 'C5', 'one-third')
    coard('G4', 'E5', 'one-third')
    coard('C5', 'G5', 'one-third')
    coard('E5', 'C6', 'one-third')
    coard('G5', 'E6', 'one-third')
    coard('E6', 'G6', 'whole')
    coard('C6', 'E6', 'whole')
    coard('C4', 'G#4', 'one-third')
    coard('D#4', 'C5', 'one-third')
    coard('G#4', 'D#5', 'one-third')
    coard('C5', 'G#5', 'one-third')
    coard('D#5', 'C6', 'one-third')
    coard('G#5', 'D#6', 'one-third')
    coard('D#6', 'G#6', 'whole')
    coard('C6', 'D#6', 'whole')
    coard('D4', 'A#4', 'one-third')
    coard('F4', 'D5', 'one-third')
    coard('A#4', 'F5', 'one-third')
    coard('D5', 'A#5', 'one-third')
    coard('F5', 'D6', 'one-third')
    coard('A#5', 'F6', 'one-third')
    coard('F6', 'A#6', 'whole')
    coard('D6', 'A#6', 'one-third')
    coard('D6', 'A#6', 'one-third')
    coard('D6', 'A#6', 'one-third')
    coard('C6', 'C7', 'whole')
    coard('C6', 'C7', 'whole')
    for i in range(0, 3):
        rest('whole')

def note(pitch, duration):
    buzzer.ChangeFrequency(pitch_dic[pitch])
    time.sleep(note_length * duration_dic[duration])

def rest(duration):
    buzzer.ChangeDutyCycle(0)
    time.sleep(note_length * duration_dic[duration])
    buzzer.ChangeDutyCycle(50)

def coard(pitch1, pitch2, duration):
    count = 0
    while True:
        buzzer.ChangeFrequency(pitch_dic[pitch1])
        time.sleep(0.02)
        buzzer.ChangeFrequency(pitch_dic[pitch2])
        time.sleep(0.02)
        count += 1
        if(note_length * duration_dic[duration] <= count*0.04):
            break

def triad(pitch1, pitch2, pitch3, duration):
    count = 0
    while True:
        buzzer.ChangeFrequency(pitch_dic[pitch1])
        time.sleep(0.02)
        buzzer.ChangeFrequency(pitch_dic[pitch2])
        time.sleep(0.02)
        buzzer.ChangeFrequency(pitch_dic[pitch3])
        time.sleep(0.02)
        count += 1
        if(note_length * duration_dic[duration] <= count*0.06):
            break

def main():
    init()
    read_music("music.csv")
    #buzz()

if __name__ == "__main__":
    main()
