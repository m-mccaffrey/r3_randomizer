from r3patch import *
import mmap
from shutil import copyfile
from tkinter import ttk

from controls import *

# Parameters grouped by function, for the notebook tabs below. Every
# non-name Patch parameter must appear in exactly one group.
PARAM_GROUPS = [
    ('Common', ['voicemode', 'octave', 'splitkey', 'unisonsw', 'unisondetune',
                'unisonspread', 'pitchbendrange', 'voiceassign', 'vibratointensity']),
    ('Oscillators', ['analog', 'osc1wave', 'osc2wave', 'osc1dwgs', 'osc1lfo1mod',
                      'timb1osc1level', 'timb1osc2level', 'noiselevel']),
    ('Filters', ['filter2tnr', 'filter1balance', 'filter1cutoff', 'filter1res',
                 'filter1eg1int', 'filter1velsens', 'filter2cutoff', 'filter2res',
                 'filter2eg1int', 'filter2velsens']),
    ('Amp & Waveshape', ['waveshapea', 'waveshapeb', 'waveshapedepth', 'punch']),
    ('Envelopes', ['eg1attack', 'eg1decay', 'eg1sustain', 'eg1release', 'eg1velo',
                   'eg2attack', 'eg2decay', 'eg2sustain', 'eg2release', 'eg2velo',
                   'eg3attack', 'eg3decay', 'eg3sustain', 'eg3release', 'eg3velo']),
    ('LFO', ['lfo1wavea', 'lfo1waveb', 'lfo1freq', 'lfo2wavea', 'lfo2waveb', 'lfo2freq']),
    ('Effects', ['fx1', 'fx2']),
    ('Virtual Patches', ['vp1src', 'vp2src', 'vp3src', 'vp4src', 'vp5src', 'vp6src',
                          'vp1dst', 'vp2dst', 'vp3dst', 'vp4dst', 'vp5dst', 'vp6dst',
                          'vp1int', 'vp2int', 'vp3int', 'vp4int', 'vp5int', 'vp6int']),
]
SLIDER_COLUMNS = 2

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

def close_resources():
    mm.flush()
    mm.close()
    f.close()

def quit_app():
    close_resources()
    gui.destroy()

def rand_all():
    status_var.set('Randomizing...')
    gui.update_idletasks()
    for n in range(128):
        patch = Patch(n)
        for timbre in [1, 2]:
            patch.randomize()
            patch.write(mm, timbre)
    mm.flush()
    status_var.set('Saved 128 patches to rand.r3l')


gui = Tk()
gui.title('R3 Randomizer')
gui.geometry('1400x800')
gui.minsize(900, 600)
gui.protocol('WM_DELETE_WINDOW', quit_app)

style = ttk.Style()
if 'clam' in style.theme_names():
    style.theme_use('clam')

nb = ttk.Notebook(gui)
nb.pack(fill=BOTH, expand=1, padx=8, pady=8)

gui_patch = Patch(-1)
params_by_index = {param.index: param for param in gui_patch.parameters}

grouped_indexes = [name for _, names in PARAM_GROUPS for name in names]
all_indexes = [param.index for param in gui_patch.parameters if param.index != 'name']
if sorted(grouped_indexes) != sorted(all_indexes):
    missing = set(all_indexes) - set(grouped_indexes)
    extra = set(grouped_indexes) - set(all_indexes)
    raise RuntimeError(f'PARAM_GROUPS out of sync with Patch.parameters: missing={missing} extra={extra}')

for group_name, param_names in PARAM_GROUPS:
    tab = ttk.Frame(nb)
    nb.add(tab, text=group_name)

    scroll = ScrollableFrame(tab)
    scroll.pack(fill=BOTH, expand=1)

    group_params = [params_by_index[name] for name in param_names]
    sliders = [param for param in group_params if param.control == 'slider']
    checkboxes = [param for param in group_params if param.control == 'checkbox']

    if sliders:
        slider_area = ttk.Frame(scroll.body)
        slider_area.pack(fill=X, anchor=N)
        slider_cols = [ttk.Frame(slider_area) for _ in range(SLIDER_COLUMNS)]
        for col in slider_cols:
            col.pack(side=LEFT, anchor=N, fill=BOTH, expand=1)
        for i, param in enumerate(sliders):
            param.add_slider(slider_cols[i % SLIDER_COLUMNS])

    if checkboxes:
        checkbox_area = ttk.Frame(scroll.body)
        checkbox_area.pack(fill=X, anchor=N)
        for param in checkboxes:
            param.add_checkbank(checkbox_area)

bottom = ttk.Frame(gui)
bottom.pack(fill=X, padx=8, pady=(0, 8))

status_var = StringVar(value='Ready')
ttk.Label(bottom, textvariable=status_var).pack(side=LEFT)

ttk.Button(bottom, text='Quit', command=quit_app).pack(side=RIGHT)
ttk.Button(bottom, text='Randomize All 128 Patches', command=rand_all).pack(side=RIGHT, padx=(0, 8))

gui.mainloop()
