from r3patch import *
import json
import mmap
import os
from shutil import copyfile
from tkinter import ttk, filedialog, messagebox

from controls import *

DEFAULT_SETTINGS_PATH = 'r3_settings.json'

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


def serialize_settings():
    """Capture the current slider ranges and checkbox selections."""
    settings = {}
    for param in gui_patch.parameters:
        if param.index == 'name':
            continue
        if param.control == 'slider':
            settings[param.index] = {
                'type': 'slider',
                'min': min(param.options),
                'max': max(param.options),
            }
        elif param.options == ['']:
            settings[param.index] = {
                'type': 'nibble',
                'highnibbles': list(param.highnibbles),
                'lownibbles': list(param.lownibbles),
            }
        else:
            settings[param.index] = {
                'type': 'checklist',
                'options': list(param.options),
            }
    return settings


def apply_settings(settings):
    """Push a loaded settings dict back into the GUI. Returns how many
    parameters were recognized and applied."""
    applied = 0
    for index, data in settings.items():
        param = params_by_index.get(index)
        if param is None or not hasattr(param, 'interface'):
            continue
        if param.control == 'slider' and data.get('type') == 'slider':
            param.interface.set_range(data['min'], data['max'])
            applied += 1
        elif param.control == 'checkbox' and data.get('type') in ('nibble', 'checklist'):
            param.interface.set_selected(data)
            applied += 1
    return applied


settings_path = None

def write_settings_to(path):
    global settings_path
    with open(path, 'w') as settings_file:
        json.dump(serialize_settings(), settings_file, indent=2)
    settings_path = path
    status_var.set('Saved settings to ' + os.path.basename(path))

def save_settings_as():
    path = filedialog.asksaveasfilename(
        title='Save Randomizer Settings',
        defaultextension='.json',
        filetypes=[('JSON files', '*.json'), ('All files', '*.*')],
        initialfile=os.path.basename(settings_path or DEFAULT_SETTINGS_PATH),
    )
    if path:
        write_settings_to(path)

def save_settings():
    write_settings_to(settings_path or DEFAULT_SETTINGS_PATH)

def read_settings_from(path):
    global settings_path
    try:
        with open(path) as settings_file:
            data = json.load(settings_file)
    except (OSError, ValueError) as error:
        messagebox.showerror('Load Settings', f'Could not load settings from {path}:\n{error}')
        return
    applied = apply_settings(data)
    settings_path = path
    status_var.set(f'Loaded {applied} parameter settings from ' + os.path.basename(path))

def load_settings():
    path = filedialog.askopenfilename(
        title='Load Randomizer Settings',
        filetypes=[('JSON files', '*.json'), ('All files', '*.*')],
    )
    if path:
        read_settings_from(path)


gui = Tk()
gui.title('R3 Randomizer')
gui.geometry('1400x800')
gui.minsize(900, 600)
gui.protocol('WM_DELETE_WINDOW', quit_app)

style = ttk.Style()
if 'clam' in style.theme_names():
    style.theme_use('clam')

menubar = Menu(gui)
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label='Load Settings...', command=load_settings, accelerator='Ctrl+O')
file_menu.add_command(label='Save Settings', command=save_settings, accelerator='Ctrl+S')
file_menu.add_command(label='Save Settings As...', command=save_settings_as, accelerator='Ctrl+Shift+S')
file_menu.add_separator()
file_menu.add_command(label='Quit', command=quit_app, accelerator='Ctrl+Q')
menubar.add_cascade(label='File', menu=file_menu)
gui.config(menu=menubar)

gui.bind_all('<Control-o>', lambda event: load_settings())
gui.bind_all('<Control-s>', lambda event: save_settings())
gui.bind_all('<Control-Shift-S>', lambda event: save_settings_as())
gui.bind_all('<Control-q>', lambda event: quit_app())

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

if os.path.exists(DEFAULT_SETTINGS_PATH):
    read_settings_from(DEFAULT_SETTINGS_PATH)

gui.mainloop()
