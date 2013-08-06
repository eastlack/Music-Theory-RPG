import pygame, sys
from pygame.locals import *

import pygame.midi
pygame.init()
pygame.midi.init()
from time import sleep
import random

DISPLAY = pygame.display.set_mode((1500, 750), 0, 32)

port = pygame.midi.get_default_output_id()
midi_out = pygame.midi.Output(port, 0)
midi_out.set_instrument(0)

WHITE = (255, 255, 255)
LGREY = (200, 200, 200)
DGREY = (55, 55, 55)
BLACK = (0, 0, 0)

class Interval(object):
    def __init__(self):
        self.aminor2nd = 1
        self.dminor2nd = -1
        self.time1 = 0
        self.time2 = 0
        self.note1 = 0
        self.note2 = 0
        self.rnote1 = 0
        self.rnote2 = 0
        self.increment = 0
        self.accuracy = 0
        self.started = False

    def start_interval(self, time):
        #if self.new == True:
        self.time1 = time
        self.started = True
        self.note1 = random.randrange(74, 87)
        if self.note1 == 86:
            self.increment = random.randrange(-2, 0)
        elif self.note1 == 74:
            self.increment = random.randrange(1, 3)
        else:
            majmin = random.randrange(1,3)
            if majmin == 1:
                self.increment = random.randrange(-1, 2, 2)
            if majmin == 2:
                self.increment = random.randrange(-2, 3, 4)
        self.note2 = self.note1 + self.increment
           # print("reset note")
        #print(self.note1)
        #print(self.note2)
        print(self.increment),
        print(self.note1),
        print (self.note2)

    def play_interval(self, time):
        if self.started == True:
            if time - self.time1 == 0:
            #increment = random.randrange(-1, 1, 2)
                midi_out.note_on(self.note1, 127)
                #print("play")
            
            if time - self.time1 == 300:
                midi_out.note_off(self.note1, 127)
                midi_out.note_on(self.note2, 127)
            #self.time1 = time
                #print("play2")

            if time - self.time1 == 600:
                midi_out.note_off(self.note2, 127)
                self.started = False
                #self.increment = 0

    def response(self, note, time):
        if self.increment == 0:
            print ("no increment")
            return
        
        if time - self.time1 < 600:
            self.rnote1 = 0
            self.rnote2 = 0

        if time - self.time1 >= 600 and self.note1 > 0:
            if self.rnote1 == 0:
                self.rnote1 = note
                print(self.rnote1)
                return
            else:
                self.rnote2 = note
                answer = self.rnote2 - self.rnote1
                print(answer)
                if abs(self.increment) == abs(answer):
                    self.accuracy += .5
                    print("same increment")
                else:
                    self.accuracy = 0
                    print ("wrong"),
                    print (self.accuracy)
                    self.rnote1 = 0
                    self.rnote2 = 0
                    return
                
                '''if self.increment == 0:
                    self.accuracy += 0'''
                    
                if answer < 0:
                    if self.increment < 0:
                        self.accuracy += .5
                        print ("decension")
                if answer > 0:
                    if self.increment > 0:
                        self.accuracy += .5
                        #notetemp = self.note1
                        print ("acension")


                if self.rnote1 == self.note1 and self.rnote2 == self.note2:
                    self.accuracy += .2
                    print("same notes")

                self.rnote1 = 0
                self.rnote2 = 0
                print(self.accuracy)
                self.increment = 0
                self.accuracy = 0
                return accuracy
            
        

class PianoKeys(object):
    def __init__(self, color, note):
        self.time = 0
        self.type = color
        self.note = note

        if color == "WHITE":
            self.color = (255, 255, 255)
            self.width = 31
            self.height = 192

        if color == "BLACK":
            self.color = (0, 0, 0)
            self.width = 22
            self.height = 122

    def pressed(self, time):
        self.time = time
        midi_out.note_on(self.note, 127)

        if self.type == "WHITE":
            self.color = (200, 200, 200)

        if self.type == "BLACK":
            self.color = (100, 100, 100)

    def unpressed(self, time):
        #midi_out.note_off(self.note, 127)
        if time - self.time >= 15:
            midi_out.note_off(self.note, 127)

            if self.type == "WHITE":
                self.color = (255, 255, 255)

            if self.type == "BLACK":
                self.color = (0, 0, 0)



C4 = 74 #0
Db4 = 75 #1
D4 = 76 #2
Eb4 = 77 #3
E4 = 78 #4
F4 = 79 #5
Gb4 = 80 #6
G4 = 81 #7
Ab4 = 82 #8
A4 = 83 #9
Bb4 = 84 #10
B4 = 85 #11
C5 = 86 #12

#WHITE: 0, 2, 4, 5, 7, 9, 11, 12
#BLACK: 1, 3, 6, 8, 10
note = 74

pianokeys = []
for i in range (13):
    if i <=4 and i%2 == 0:
       key = PianoKeys("WHITE", note)
       #print(note)

    elif i > 4 and i % 2 == 1:
        key = PianoKeys("WHITE", note)
        #print (note)

    elif i == 12:
        key = PianoKeys("WHITE", note)
        #print (note)

    else:
        key = PianoKeys("BLACK", note)
        print (note)

    note += 1

    pianokeys.append(key)


WHITE = (255, 255, 255)
GREY = (200, 200, 200)
time = 0
interval = Interval()
note1 = 0
note2 = 0

accuracy = 0

while True:

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_a:
                pianokeys[0].pressed(time)
                accuracy = interval.response(pianokeys[0].note, time)
            if event.key == K_w:
                pianokeys[1].pressed(time)
                accuracy = interval.response(pianokeys[1].note, time)
            if event.key == K_s:
                pianokeys[2].pressed(time)
                accuracy = interval.response(pianokeys[2].note, time)
            if event.key == K_e:
                pianokeys[3].pressed(time)
                accuracy = interval.response(pianokeys[3].note, time)
            if event.key == K_d:
                pianokeys[4].pressed(time)
                accuracy = interval.response(pianokeys[4].note, time)
            if event.key == K_f:
                pianokeys[5].pressed(time)
                accuracy = interval.response(pianokeys[5].note, time)
            if event.key == K_t:
                pianokeys[6].pressed(time)
                accuracy = interval.response(pianokeys[6].note, time)
            if event.key == K_g:
                pianokeys[7].pressed(time)
                accuracy = interval.response(pianokeys[7].note, time)
            if event.key == K_y:
                pianokeys[8].pressed(time)
                accuracy = interval.response(pianokeys[8].note, time)
            if event.key == K_h:
                pianokeys[9].pressed(time)
                accuracy = interval.response(pianokeys[9].note, time)
            if event.key == K_u:
                pianokeys[10].pressed(time)
                accuracy = interval.response(pianokeys[10].note, time)
            if event.key == K_j:
                pianokeys[11].pressed(time)
                accuracy = interval.response(pianokeys[11].note, time)
            if event.key == K_k:
                pianokeys[12].pressed(time)
                accuracy = interval.response(pianokeys[12].note, time)

            if event.key == K_p:
                interval.start_interval(time)

        if event.type == KEYUP:
            for i in range(13):
                pianokeys[i].unpressed(time)

        if event.type == QUIT:
            del midi_out
            pygame.midi.quit()
            pygame.quit()
            sys.exit()

    xpos = 5

    #print (accuracy)

    
    interval.play_interval(time)

    for i in range(13):
        #pianokeys[i].unpressed(time)
        if pianokeys[i].type == "WHITE":
            #print (pianokeys[i].note)
            pygame.draw.rect(DISPLAY, (0, 0, 0), (xpos, 20, pianokeys[i].width, pianokeys[i].height))
            pygame.draw.rect(DISPLAY, pianokeys[i].color, (xpos + 1, 21, pianokeys[i].width - 2, pianokeys[i].height - 2, ))
            xpos += 31

    xpos = 26

    for i in range(13):
        if pianokeys[i].type == "BLACK":
            pygame.draw.rect(DISPLAY, (0, 0, 0,), (xpos, 20, pianokeys[i].width, pianokeys[i].height))
            pygame.draw.rect(DISPLAY, pianokeys[i].color, (xpos + 1, 21, pianokeys[i].width - 2, pianokeys[i].height - 2))
            if i == 3:
                xpos += 62
            else:
                xpos += 31

    time += 1

    pygame.display.update()
