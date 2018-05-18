from itertools import chain
import random
import mmap
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

f = open('init.r3l', 'r+b')
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
        p.write()

class patch():
    number = 0
    params = {}
    
    params['name']              =       {}
    params['voicemode']         =       {}
    params['octave']            =       {}
    params['splitkey']          =       {}
    params['unisonsw']          =       {}
    params['unisondetune']      =       {}
    params['unisonspread']      =       {}
    params['pitchbendrange']    =       {}
    params['voiceassign']       =       {}
    params['vibratointensity']  =       {}
    params['analog']            =       {}
    params['osc1modtype']       =       {}
    params['timb1osc1level']    =       {}
    params['timb1osc2level']    =       {}
    params['noiselevel']        =       {}
    params['filter2tnr']        =       {}
    params['filter1balance']    =       {}
    params['filter2tnr']        =       {}
    params['filter1cutoff']     =       {}
    params['filter1res']        =       {}
    params['filter1eg1int']     =       {}
    params['filter1velsens']    =       {}
    params['filter2cutoff']     =       {}
    params['filter2res']        =       {}
    params['filter2eg1int']     =       {}
    params['filter2velsens']    =       {}
    params['waveshapea']        =       {}
    params['waveshapeb']        =       {}
    params['waveshapedepth']    =       {}
    params['punch']             =       {}
    params['eg1attack']         =       {}
    params['eg1decay']          =       {}
    params['eg1sustain']        =       {}
    params['eg1release']        =       {}
    params['eg1velo']           =       {}
    params['eg2attack']         =       {}
    params['eg2decay']          =       {}
    params['eg2sustain']        =       {}
    params['eg2release']        =       {}
    params['eg2velo']           =       {}
    params['eg3attack']         =       {}
    params['eg3decay']          =       {}
    params['eg3sustain']        =       {}
    params['eg3release']        =       {}
    params['eg3velo']           =       {}
    params['lfo1wavea']         =       {}
    params['lfo1waveb']         =       {}
    params['lfo1freq']          =       {}
    params['lfo2wavea']         =       {}
    params['lfo2waveb']         =       {}
    params['lfo2freq']          =       {}
    params['timb1wave']         =       {}
    params['timb2wave']         =       {}
    params['fx1']               =       {}
    params['fx2']               =       {}
    params['vp1src']            =       {}
    params['vp2src']            =       {}
    params['vp3src']            =       {}
    params['vp4src']            =       {}
    params['vp5src']            =       {}
    params['vp6src']            =       {}
    params['vp1dst']            =       {}
    params['vp2dst']            =       {}
    params['vp3dst']            =       {}
    params['vp4dst']            =       {}
    params['vp5dst']            =       {}
    params['vp6dst']            =       {}
    params['vp1int']            =       {}
    params['vp2int']            =       {}
    params['vp3int']            =       {}
    params['vp4int']            =       {}
    params['vp5int']            =       {}
    params['vp6int']            =       {}
    params['waveform']          =       {}    
    params['waveform']          =       {} 
    params['lfo1mod']           =       {} 
    
    
    params['name']['location']                = 32
    params['name']['options']                 = ['Testing', 'One', 'Two']
    params['voicemode']['location']           = 49
    params['voicemode']['options']            = range(0,0xFF,0x40)
    params['octave']['location']              = 53
    params['octave']['options']               = range(5,12)
    params['splitkey']['location']            = 87
    params['splitkey']['options']             = range(0x00,0x80)
    params['unisonsw']['location']            = 88
    params['unisonsw']['options']             = [i for j in (range(0x70, 0x73), range(0xF0, 0xF3)) for i in j]
    params['unisondetune']['location']        = 89
    params['unisondetune']['options']         = range(0x00,0x38)
    params['unisonspread']['location']        = 90
    params['unisonspread']['options']         = range(0x00,0x80)
    params['pitchbendrange']['location']      = 91
    params['pitchbendrange']['options']       = range(0x34,0x4D)
    params['voiceassign']['location']         = 102
    params['voiceassign']['options']          = [0x30,0x70,0xF0]
    params['vibratointensity']['location']    = 107
    params['vibratointensity']['options']     = range(0x00, 0x80)
    params['timb1wave']['location']           = 118
    params['timb1wave']['options']            = [i for j in (range(0x80, 0x84), range(0x90, 0x94), range(0xA0, 0XA4), range(0xB0, 0xB4)) for i in j]
    params['waveform']['location']            = 119
    params['waveform']['options']             = range(0x00, 0x80)
    params['lfo1mod']['location']             = 120
    params['lfo1mod']['options']              = range(0x00, 0x80)
    params['timb2wave']['location']           = 123
    params['timb2wave']['options']            = [i for j in (range(0x00, 0x04), range(0x10, 0x14), range(0x20, 0x24), range(0x30, 0x34)) for i in j]
    params['analog']['location']              = 114
    params['analog']['options']               = range(0x00,0x20)
    params['osc1modtype']['location']         = 118
    params['osc1modtype']['options']          = range(0x80,0xC0,0x10)
    params['timb1osc1level']['location']      = 126    
    params['timb1osc1level']['options']       = range(0x00,0x80)
    params['timb1osc2level']['location']      = 127
    params['timb1osc2level']['options']       = range(0x00,0x80)
    params['noiselevel']['location']          = 128
    params['noiselevel']['options']           = range(0x00,0x80)
    
    params['noiselevel']['location']        =       128
    params['filter2tnr']['location']        =       129
    params['filter1balance']['location']    =       130
    params['filter1cutoff']['location']     =       131
    params['filter1res']['location']        =       132
    params['filter1eg1int']['location']     =       133
    params['filter1velsens']['location']    =       135
    params['filter2cutoff']['location']     =       136
    params['filter2res']['location']        =       137
    params['filter2eg1int']['location']     =       138
    params['filter2velsens']['location']    =       140
    params['waveshapea']['location']        =       142
    params['waveshapeb']['location']        =       143
    params['waveshapedepth']['location']    =       144
    params['punch']['location']             =       147
    params['eg1attack']['location']         =       148
    params['eg1decay']['location']          =       149
    params['eg1sustain']['location']        =       150
    params['eg1release']['location']        =       151
    params['eg1velo']['location']           =       153
    params['eg2attack']['location']         =       156
    params['eg2decay']['location']          =       157
    params['eg2sustain']['location']        =       158
    params['eg2release']['location']        =       159
    params['eg2velo']['location']           =       161
    params['eg3attack']['location']         =       164
    params['eg3decay']['location']          =       165
    params['eg3sustain']['location']        =       166
    params['eg3release']['location']        =       167
    params['eg3velo']['location']           =       169
    params['lfo1wavea']['location']         =       172
    params['lfo1waveb']['location']         =       173
    params['lfo1freq']['location']          =       174
    params['lfo2wavea']['location']         =       177
    params['lfo2waveb']['location']         =       178
    params['lfo2freq']['location']          =       179
    params['fx1']['location']               =       200
    params['fx2']['location']               =       224
    params['fx1']['options']                =       range(0x80, 0x9D)
    params['fx2']['options']                =       range(0x80, 0x9D)
    
    
    
    
    params['vp1src']['location']            =       182
    params['vp1src']['options']             =       range(0x00, 0x08)
    params['vp2src']['location']            =       185
    params['vp2src']['options']             =       range(0x00, 0x08)
    params['vp3src']['location']            =       188
    params['vp3src']['options']             =       range(0x00, 0x08)
    params['vp4src']['location']            =       191
    params['vp4src']['options']             =       range(0x00, 0x08)
    params['vp5src']['location']            =       194
    params['vp5src']['options']             =       range(0x00, 0x08)
    params['vp6src']['location']            =       197
    params['vp6src']['options']             =       range(0x00, 0x08)
    params['vp1dst']['location']            =       183
    params['vp1dst']['options']             =       range(0x00, 0x08)
    params['vp2dst']['location']            =       186
    params['vp2dst']['options']             =       range(0x00, 0x08)
    params['vp3dst']['location']            =       189
    params['vp3dst']['options']             =       range(0x00, 0x08)
    params['vp4dst']['location']            =       192
    params['vp4dst']['options']             =       range(0x00, 0x08)
    params['vp5dst']['location']            =       195
    params['vp5dst']['options']             =       range(0x00, 0x08)
    params['vp6dst']['location']            =       198
    params['vp6dst']['options']             =       range(0x00, 0x08)
    params['vp1int']['location']            =       184
    params['vp1int']['options']             =       range(0x00, 0x08)
    params['vp2int']['location']            =       187
    params['vp2int']['options']             =       range(0x00, 0x08)
    params['vp3int']['location']            =       190
    params['vp3int']['options']             =       range(0x00, 0x08)
    params['vp4int']['location']            =       193
    params['vp4int']['options']             =       range(0x00, 0x08)
    params['vp5int']['location']            =       196
    params['vp5int']['options']             =       range(0x00, 0x08)
    params['vp6int']['location']            =       199
    params['vp6int']['options']             =       range(0x00, 0x08)
    
        
    params['noiselevel']['options']        =       range(0x00,0x10)
    params['filter2tnr']['options']        =       [i for j in (range(0x4C, 0x50), range(0x5C, 0x60), range(0x6C, 0x70), range(0x7C, 0x80)) for i in j]
    params['filter1balance']['options']    =       range(0x00,0x80)
    params['filter1cutoff']['options']     =       range(0x00,0x80)
    params['filter1res']['options']        =       range(0x00,0x80)
    params['filter1eg1int']['options']     =       range(0x00,0x80)
    params['filter1velsens']['options']    =       range(0x00,0x80)
    params['filter2cutoff']['options']     =       range(0x00,0x80)
    params['filter2res']['options']        =       range(0x00,0x80)
    params['filter2eg1int']['options']     =       range(0x00,0x80)
    params['filter2velsens']['options']    =       range(0x00,0x80)
    params['waveshapea']['options']        =       [0x00, 0x01, 0x02, 0x10,0x11,0x12]
    params['waveshapeb']['options']        =       range(0x00,0x0B)
    params['waveshapedepth']['options']    =       range(0x00,0x80)
    params['punch']['options']             =       range(0x00,0x80)
    params['eg1attack']['options']         =       range(0x00,0x30)
    params['eg1decay']['options']          =       range(0x00,0x80)
    params['eg1sustain']['options']        =       range(0x00,0x80)
    params['eg1release']['options']        =       range(0x00,0x80)
    params['eg1velo']['options']           =       range(0x00,0x80)
    params['eg2attack']['options']         =       range(0x00,0x80)
    params['eg2decay']['options']          =       range(0x00,0x80)
    params['eg2sustain']['options']        =       range(0x00,0x80)
    params['eg2release']['options']        =       range(0x00,0x80)
    params['eg2velo']['options']           =       range(0x00,0x80)
    params['eg3attack']['options']         =       range(0x00,0x80)
    params['eg3decay']['options']          =       range(0x00,0x80)
    params['eg3sustain']['options']        =       range(0x00,0x80)
    params['eg3release']['options']        =       range(0x00,0x80)
    params['eg3velo']['options']           =       range(0x00,0x80)
    params['lfo1wavea']['options']         =       range(0x00,0x04)
    params['lfo1waveb']['options']         =       [0x40, 0x7F]
    params['lfo1freq']['options']          =       range(0x00,0x80)
    params['lfo2wavea']['options']         =       range(0x00,0x04)
    params['lfo2waveb']['options']         =       [0x40, 0x7F]   
    params['lfo2freq']['options']          =       range(0x00,0x80)
        
    def __init__(self,number):
#        print(len(self.params))
        self.number = number
        for param in self.params:
            if not param == 'name':
                self.params[param]['value'] = random.choice(self.params[param]['options'])
        self.params['name']['value'] = 'Rand ' + str(number).zfill(3)
        
        
    def randomize(self):
        for param in self.params:
            if param != 'name':
                self.params[param]['value'] = random.choice(self.params[param]['options'])
            
    def write(self):
        for param in self.params:
#            print(self.number * patchsize + offset + self.params[param]['location'], param, self.params[param]['value'])
            if param == 'name':
                mm[self.number * patchsize + offset + self.params[param]['location']:self.number * patchsize + offset + self.params[param]['location']+8] = 'Rand ' + str(self.number).zfill(3)
            else:
                mm[self.number * patchsize + offset + self.params[param]['location']] = chr(self.params[param]['value'])
        
program = []
for i in range(128):
    program.append(patch(i))
    
    
rand_all(program)

#mm[224:232] = patch1.params['name']['value']

#for parameter in patch1:
#    random['parameter'] = patch[parameter]
#    random['address'] = parameter['location']
#    random['value'] = random['value'].sample(parameter['value'],1)
#    print(parameter)

#print(patch)
