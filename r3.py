from r3patch import patch
import mmap
from shutil import copyfile
from tkinter import *
''' 
510p starts patch (byte 0), preamble is 32 bytes

first patch starts at byte 192

byte: function

32-39: patch name

49: voice mode
    single (00) layer (04) split (08) multi (C0)

53: octave 
    (-3 : 3) , (05 : 0B)

87:  split key 
    (C-1 : G9) (00 : 7F)

88: Unison SW
    Nibble 1: Off/On (7/F)
    Nibble 2: 2 - 4 (0 - 2)
    
89: Unison Detune
    (00 : 63)
    
90: Unison Spread
    (00 : 7F)
    
91: Pitch Bend Range
    34 - (40) - 4C
    


102:
    Nibble 1: Voice Assign
        3: Mono 1
        7: Mono 2
        F: Poly
        
105: Pitch Transpose
    10 - (40) - 70
    
106: Tune
    0E - (40) - 72
    
107: Vibrato Intensity
    01 : 7F



114: Analog 
    (00 : 7F)

118: 
    Nibble 1: Osc 1 Mod Type
        8: Waveform
        9: Cross
        10: Unison
        11: VPM

119: Osc 1 Param 1

120: Osc 1 LFO 1 Mod

126: Timbre 1 Osc 1 Level 
    00 : 7F
127: Timbre 2 Osc 2 Level
    00 : 7F
    
128: Noise Level
    00 : 7F
    
129:
    Nibble 1: Filter 2 Type:
        4: HP
        5: LP
        6: BP
        7: Comb
    Nibble 2: Filter Routing
        C: Single
        D: Serial
        E: Parallel
        F: Individual
        
130: Filter 1 Balance

131: Filter 1 Cutoff

132: Filter 1 Resonance

133: Filtar 1 EG 1 Intensity

134: Filter 1 KeyTrack

135: Filter 1 Vel Sens.

136: Filter 2 Cutoff

137: Filter 2 Resonance

138: Filter 2 EG1 Intensity

139: Filter 2 Key Track

140: Filter 2 Vel Sens.

141: Amp Level

142-143: 
    Nibble 1: Wave Shape Position
        0: Pre Filter 1
        1: Pre Amp
    Nibble 2,3,4: Wave ShapeType
        0xx:Off
        100: Drive
        200-20A: Others

144: Amp Waveshape Depth

145: Amp Pan

146: Amp Key Track

147: Punch Level
    
148-151: EG 1 ADSR

153: EG 1 LV. Velo

156-159: EG 2 ADSR

161: EG 2 LV. Velo

164-167: EG 3 ADSR

169: EG 3 LV. Velo

172-173: LFO 1 Wave
    0: Saw
    1: Square
    2: Triangle
    3: 173:
        40: S&H
        7f: Random
        
174: LFO 1 Freq

175: BPM Sync & Key Sync

176: LFO 1 Sync Note

177-178: LFO 1 Wave
    0: Saw
    1: Square
    2: Triangle
    3: 173:
        40: S&H
        7f: Random
        
179: LFO 1 Freq

180: BPM Sync & Key Sync

181: LFO 1 Sync Note

182-199: V Patches

Next patch starts at 2528
Patch is 2336 bytes long
'''
copyfile('init.r3l', 'rand.r3l')
f = open('rand.r3l', 'r+b')
mm = mmap.mmap(f.fileno(), 0)
offset = 192
patchsize = 2336
timbre2 = 228

def rand_all(prog):
    print(len(prog))
    for p in prog:
        print(p.number)
        p.randomize()
#        print(p.params['name']['value'],p.params['voicemode']['value'])  
        p.write(mm)

program = []
for i in range(128):
    program.append(patch(i))


gui_patch = patch(-1)

gui = Tk()
gui.geometry('600x600')
gui.title('R3 Randomizer')

rand_button = Button(gui, text='Randomize', command=lambda: rand_all(program))
rand_button.pack()

gui.mainloop()

#mm[224:232] = patch1.params['name']['value']

#for parameter in patch1:
#    random['parameter'] = patch[parameter]
#    random['address'] = parameter['location']
#    random['value'] = random['value'].sample(parameter['value'],1)
#    print(parameter)

#print(patch)
