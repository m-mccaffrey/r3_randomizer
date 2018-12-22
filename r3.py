from r3patch import *
import mmap
from shutil import copyfile
from tkinter import ttk

from controls import *

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

def save_file():
    f.close()
    exit(0)

def rand_all():
    program = [0*i for i in range(128)]
    for n in range(128):
        program[n] = Patch(n)
        print(program[n].name.value)
        for timbre in [1,2]:
            program[n].randomize()
            program[n].write(mm, timbre)
    save_file()


gui = Tk()
gui.geometry('1300x750')
gui.title('R3 Randomizer')

nb = ttk.Notebook(gui)
slider_tab = ttk.Frame(nb)
checkbox_tabs = []

nb.add(slider_tab, text="Sliders")
nb.pack(fill=BOTH, expand=1)

gui_patch = Patch(-1)
slider_cols = []
slider_frames = []
sliders_min = []
sliders_max = []
slider_frame = Frame(slider_tab)
label_frames = []
labels = []
pFrames = []
num_slider_rows = 12

checkbox_tabs.append(ttk.Frame(nb))
nb.add(checkbox_tabs[-1], text="Checkboxes " + str(len(checkbox_tabs) - 1))

checkbox_cols = []
checkbox_frames = []
checkboxes = []
num_checkbox_rows = 1

check_vars = []
max_slide_vars = []
min_slide_vars = []

slider_sets = []
checkbanks = []


for param in gui_patch.parameters:


    if param.control == 'slider':
        if len(slider_frames)%num_slider_rows == 0:
            slider_cols.append(Frame(slider_frame))

        pFrames.append(Frame(slider_cols[-1], relief=GROOVE, bd=2))

        slider_frames.append(Frame(pFrames[-1]))

        slider_sets.append(param.add_slider(slider_frames[-1]))

        label_frames.append(Frame(pFrames[-1]))

        labels.append(Label(label_frames[-1], text=param.label))

        slider_frames[-1].pack(side=TOP)

        label_frames[-1].pack(side=TOP)

        labels[-1].pack(side=TOP)

        slider_cols[-1].pack(side=LEFT)

        pFrames[-1].pack()

        # param.control = slider_sets[-1]

    elif param.control == 'checkbox':
        if param.label in ('LFO 1 Wave A', 'DWGS Type', 'Effect 1', 'V. Patch 1 Destination'):
            checkbox_tabs.append(ttk.Frame(nb))
            nb.add(checkbox_tabs[-1], text="Checkboxes " + str(len(checkbox_tabs) - 1))
        if len(checkbox_frames) % num_checkbox_rows == 0:
            checkbox_cols.append(Frame(checkbox_tabs[-1], relief=GROOVE, bd=2))
            checkbanks.append(param.add_checkbank(checkbox_cols[-1]))


slider_frame.pack(side=TOP)
rand_button = Button(gui, text='Randomize', command=lambda: rand_all())
rand_button.pack(side=BOTTOM)

gui.mainloop()

#mm[224:232] = patch1.params['name']['value']

#for parameter in patch1:
#    random['parameter'] = patch[parameter]
#    random['address'] = parameter['location']
#    random['value'] = random['value'].sample(parameter['value'],1)
#    print(parameter)

#print(patch)
