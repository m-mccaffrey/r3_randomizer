from controls import *

offset = 192
patchsize = 2336
timbre2 = 228

class parameter:
    def __init__(self, index, label, control, location, options, length=1, dependency=None,
                 checks=None, highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None, numrows=8):

        self.numrows = numrows
        self.index = index
        self.label = label
        self.control = control
        self.length = length
        self.options = options
        self.enabled = options
        self.value = options[0]
        self.dependency = dependency
        self.location = location
        self.checks = checks
        self.highchecks = highchecks
        self.lowchecks = lowchecks
        self.highnibbles = highnibbles
        self.lownibbles = lownibbles

        if control == 'slider':
            pass
        elif control == 'check':
            pass


    def add_slider(self, parent):
        self.interface = Slider(parent, self)
        return self.interface

    def add_checkbank(self, parent):
        self.interface = Checkbank(parent, self, self.numrows)
        return self.interface


class Patch:

    number = 0
    # params = {}

    name = parameter('name', 'Name (8 characters)', 'field', 32, ['Testing'], checks=None, highchecks=None,
                     lowchecks=None, highnibbles=None, lownibbles=None)
    voicemode = parameter('voicemode', 'Voice Mode', 'checkbox', 49, list(range(0, 255, 64)),
                          checks=['Single', 'Layer', 'Split', 'Multi'], highchecks=None, lowchecks=None,
                          highnibbles=None, lownibbles=None)
    octave = parameter('octave', 'Octave', 'slider', 53, range(5, 12), checks=None, highchecks=None, lowchecks=None,
                       highnibbles=None, lownibbles=None)
    splitkey = parameter('splitkey', 'Split Key', 'slider', 87, range(0, 128), checks=None, highchecks=None,
                         lowchecks=None, highnibbles=None, lownibbles=None)
    unisonsw = parameter('unisonsw', 'Unison Switch', 'checkbox', 88, [''], checks=None, highchecks=['On', 'Off'],
                         lowchecks=['2', '3', '4'], highnibbles=[112, 240], lownibbles=list(range(0, 3)))
    unisondetune = parameter('unisondetune', 'Unison Detune', 'slider', 89, range(0, 99), checks=None, highchecks=None,
                             lowchecks=None, highnibbles=None, lownibbles=None)
    unisonspread = parameter('unisonspread', 'Unison Spread', 'slider', 90, range(0, 128), checks=None, highchecks=None,
                             lowchecks=None, highnibbles=None, lownibbles=None)
    pitchbendrange = parameter('pitchbendrange', 'Pitch Bend Range', 'slider', 91, range(52, 77), checks=None,
                               highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    voiceassign = parameter('voiceassign', 'Voice Assign', 'checkbox', 102, [48, 112, 240],
                            checks=['Mono 1', 'Mono 2', 'Poly'], highchecks=None, lowchecks=None, highnibbles=None,
                            lownibbles=None)
    vibratointensity = parameter('vibratointensity', 'Vibrato Intensity', 'slider', 107, range(0, 128), checks=None,
                                 highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    analog = parameter('analog', 'Analog Tuning', 'slider', 114, range(0, 32), checks=None, highchecks=None,
                       lowchecks=None, highnibbles=None, lownibbles=None)
    timb1osc1level = parameter('timb1osc1level', 'Oscillator 1 Level', 'slider', 126, range(0, 128), checks=None,
                               highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    timb1osc2level = parameter('timb1osc2level', 'Oscillator 2 Level', 'slider', 127, range(0, 128), checks=None,
                               highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    noiselevel = parameter('noiselevel', 'Noise Level', 'slider', 128, range(0, 16), checks=None, highchecks=None,
                           lowchecks=None, highnibbles=None, lownibbles=None)
    filter2tnr = parameter('filter2tnr', 'Filter 2 Type and Filter Routing', 'checkbox', 129, [''], checks=None,
                           highchecks=['LPF', 'HPF', 'BPF', 'Comb'],
                           lowchecks=['Single', 'Serial', 'Parallel', 'Individual'], highnibbles=list(range(64, 128, 16)),
                           lownibbles=list(range(12, 16)))
    filter1balance = parameter('filter1balance', 'Filter 1 Balance', 'slider', 130, range(0, 128), checks=None,
                               highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    filter1cutoff = parameter('filter1cutoff', 'Filter 1 Cutoff', 'slider', 131, range(0, 128), checks=None,
                              highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    filter1res = parameter('filter1res', 'Filter 1 Resonance', 'slider', 132, range(0, 128), checks=None,
                           highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    filter1eg1int = parameter('filter1eg1int', 'Filter 1 EG1 Intensity', 'slider', 133, range(0, 128), checks=None,
                              highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    filter1velsens = parameter('filter1velsens', 'Filter 1 Velocity Sencsitivity', 'slider', 135, range(0, 128),
                               checks=None, highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    filter2cutoff = parameter('filter2cutoff', 'Filter 2 Cutoff', 'slider', 136, range(0, 128), checks=None,
                              highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    filter2res = parameter('filter2res', 'Filter 2 Resonance', 'slider', 137, range(0, 128), checks=None,
                           highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    filter2eg1int = parameter('filter2eg1int', 'Filter 2 EG1 Intensity', 'slider', 138, range(0, 128), checks=None,
                              highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    filter2velsens = parameter('filter2velsens', 'Filter 2 Velocity Sensitivity', 'slider', 140, range(0, 128),
                               checks=None, highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    waveshapea = parameter('waveshapea', 'Wave Shape Position', 'checkbox', 142, [''], checks=None,
                           highchecks=['Pre-Filter 1', 'Pre-Amp'], lowchecks=['Off', 'Drive', 'Decimator'],
                           highnibbles=[0, 16], lownibbles=list(range(0, 3)))
    waveshapeb = parameter('waveshapeb', 'Wave Shape Type', 'checkbox', 143, list(range(0, 10)),
                           checks=['HardClip', 'OctSaw', 'MultiTri', 'MultiSin', 'SubOsc Saw', 'SubOsc Tri',
                                   'SubOsc Squ', 'SubOsc Sin', 'Pickup', 'Level Boost'], highchecks=None,
                           lowchecks=None, highnibbles=None, lownibbles=None)
    waveshapedepth = parameter('waveshapedepth', 'Wave Shape Depth', 'slider', 144, range(0, 128), checks=None,
                               highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    punch = parameter('punch', 'Punch Level', 'slider', 147, range(0, 128), checks=None, highchecks=None,
                      lowchecks=None, highnibbles=None, lownibbles=None)
    eg1attack = parameter('eg1attack', 'Env. Gen. 1 Attack', 'slider', 148, range(0, 48), checks=None, highchecks=None,
                          lowchecks=None, highnibbles=None, lownibbles=None)
    eg1decay = parameter('eg1decay', 'Env. Gen. 1 Decay', 'slider', 149, range(0, 128), checks=None, highchecks=None,
                         lowchecks=None, highnibbles=None, lownibbles=None)
    eg1sustain = parameter('eg1sustain', 'Env. Gen. 1 Sustain', 'slider', 150, range(0, 128), checks=None,
                           highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    eg1release = parameter('eg1release', 'Env. Gen. 1 Release', 'slider', 151, range(0, 128), checks=None,
                           highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    eg1velo = parameter('eg1velo', 'Env. Gen. 1 Velocity Sensitivity', 'slider', 153, range(0, 128), checks=None,
                        highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    eg2attack = parameter('eg2attack', 'Env. Gen. 2 Attack', 'slider', 156, range(0, 128), checks=None, highchecks=None,
                          lowchecks=None, highnibbles=None, lownibbles=None)
    eg2decay = parameter('eg2decay', 'Env. Gen. 2 Decay', 'slider', 157, range(0, 128), checks=None, highchecks=None,
                         lowchecks=None, highnibbles=None, lownibbles=None)
    eg2sustain = parameter('eg2sustain', 'Env. Gen. 2 Sustain', 'slider', 158, range(0, 128), checks=None,
                           highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    eg2release = parameter('eg2release', 'Env. Gen. 2 Release', 'slider', 159, range(0, 128), checks=None,
                           highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    eg2velo = parameter('eg2velo', 'Env. Gen. 2 Velocity Sensitivity', 'slider', 161, range(0, 128), checks=None,
                        highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    eg3attack = parameter('eg3attack', 'Env. Gen. 3 Attack', 'slider', 164, range(0, 128), checks=None, highchecks=None,
                          lowchecks=None, highnibbles=None, lownibbles=None)
    eg3decay = parameter('eg3decay', 'Env. Gen. 3 Decay', 'slider', 165, range(0, 128), checks=None, highchecks=None,
                         lowchecks=None, highnibbles=None, lownibbles=None)
    eg3sustain = parameter('eg3sustain', 'Env. Gen. 3 Sustain', 'slider', 166, range(0, 128), checks=None,
                           highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    eg3release = parameter('eg3release', 'Env. Gen. 3 Release', 'slider', 167, range(0, 128), checks=None,
                           highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    eg3velo = parameter('eg3velo', 'Env. Gen. 3 Velocity Sensitivity', 'slider', 169, range(0, 128), checks=None,
                        highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    lfo1wavea = parameter('lfo1wavea', 'LFO 1 Wave A', 'checkbox', 172, list(range(0, 4)),
                          checks=['Saw', 'Square', 'Triangle', 'S&H'], highchecks=None, lowchecks=None,
                          highnibbles=None, lownibbles=None)
    lfo1waveb = parameter('lfo1waveb', 'LFO 1 Wave B', 'checkbox', 173, [64, 127], checks=['Wave', 'Random'],
                          highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    lfo1freq = parameter('lfo1freq', 'LFO 1 Frequency', 'slider', 174, list(range(0, 128)), checks=None, highchecks=None,
                         lowchecks=None, highnibbles=None, lownibbles=None)
    lfo2wavea = parameter('lfo2wavea', 'LFO 2 Wave A', 'checkbox', 177, list(range(0, 4)),
                          checks=['Saw', 'Square', 'Triangle', 'S&H'], highchecks=None, lowchecks=None,
                          highnibbles=None, lownibbles=None)
    lfo2waveb = parameter('lfo2waveb', 'LFO 2 Wave B', 'checkbox', 178, [64, 127], checks=['Wave', 'Random'],
                          highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    lfo2freq = parameter('lfo2freq', 'LFO 2 Wave Frequency', 'slider', 179, list(range(0, 128)), checks=None, highchecks=None,
                         lowchecks=None, highnibbles=None, lownibbles=None)
    osc1wave = parameter('osc1wave', 'Oscillator 1 Wave', 'checkbox', 118, [''], checks=None,
                         highchecks=['Waveform', 'Cross', 'Unison', 'VPM'],
                         lowchecks=['Saw', 'Pulse', 'Triangle', 'Sine', 'Formant', 'Noise', 'DWGS'],
                         highnibbles=list(range(128, 192, 16)), lownibbles=list(range(0, 7)))
    osc2wave = parameter('osc2wave', 'Oscillator 2 Wave', 'checkbox', 123, [''], checks=None,
                         highchecks=['None', 'Ring', 'Sync', 'Ring & Sync'],
                         lowchecks=['Saw', 'Square', 'Triangle', 'Sine'], highnibbles=list(range(0, 64, 16)),
                         lownibbles=list(range(0, 4)))
    osc1dwgs = parameter('osc1dwgs', 'DWGS Type', 'checkbox', 121, list(range(0, 64)), checks=[str(i) for i in range(0,64)], highchecks=None,
                         lowchecks=None, highnibbles=None, lownibbles=None)
    fx1 = parameter('fx1', 'Effect 1', 'checkbox', 200, list(range(128, 157)), checks=[str(i) for i in range(0,29)], highchecks=None, lowchecks=None,
                    highnibbles=None, lownibbles=None)
    fx2 = parameter('fx2', 'Effect 2', 'checkbox', 224, list(range(128, 157)), checks=[str(i) for i in range(0,29)], highchecks=None, lowchecks=None,
                    highnibbles=None, lownibbles=None)
    vp1src = parameter('vp1src', 'V. Patch 1 Source', 'checkbox', 182, list(range(0, 8)),
                       checks=['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp2src = parameter('vp2src', 'V. Patch 2 Source', 'checkbox', 185, list(range(0, 8)),
                       checks=['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp3src = parameter('vp3src', 'V. Patch 3 Source', 'checkbox', 188, list(range(0, 8)),
                       checks=['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp4src = parameter('vp4src', 'V. Patch 4 Source', 'checkbox', 191, list(range(0, 8)),
                       checks=['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp5src = parameter('vp5src', 'V. Patch 5 Source', 'checkbox', 194, list(range(0, 8)),
                       checks=['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp6src = parameter('vp6src', 'V. Patch 6 Source', 'checkbox', 197, list(range(0, 8)),
                       checks=['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp1dst = parameter('vp1dst', 'V. Patch 1 Destination', 'checkbox', 183, list(range(0, 8)),
                       checks=['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level', 'Noise Level',
                               'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance', 'Filter 2 Cutoff',
                               'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency', 'LFO2 Frequency'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp2dst = parameter('vp2dst', 'V. Patch 2 Destination', 'checkbox', 186, list(range(0, 8)),
                       checks=['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level', 'Noise Level',
                               'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance', 'Filter 2 Cutoff',
                               'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency', 'LFO2 Frequency'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp3dst = parameter('vp3dst', 'V. Patch 3 Destination', 'checkbox', 189, list(range(0, 8)),
                       checks=['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level', 'Noise Level',
                               'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance', 'Filter 2 Cutoff',
                               'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency', 'LFO2 Frequency'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp4dst = parameter('vp4dst', 'V. Patch 4 Destination', 'checkbox', 192, list(range(0, 8)),
                       checks=['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level', 'Noise Level',
                               'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance', 'Filter 2 Cutoff',
                               'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency', 'LFO2 Frequency'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp5dst = parameter('vp5dst', 'V. Patch 5 Destination', 'checkbox', 195, list(range(0, 8)),
                       checks=['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level', 'Noise Level',
                               'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance', 'Filter 2 Cutoff',
                               'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency', 'LFO2 Frequency'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp6dst = parameter('vp6dst', 'V. Patch 6 Destination', 'checkbox', 198, list(range(0, 8)),
                       checks=['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level', 'Noise Level',
                               'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance', 'Filter 2 Cutoff',
                               'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency', 'LFO2 Frequency'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp1int = parameter('vp1int', 'V. Patch 1 Intensity', 'slider', 184, range(0, 128), checks=None, highchecks=None,
                       lowchecks=None, highnibbles=None, lownibbles=None)
    vp2int = parameter('vp2int', 'V. Patch 2 Intensity', 'slider', 187, range(0, 128), checks=None, highchecks=None,
                       lowchecks=None, highnibbles=None, lownibbles=None)
    vp3int = parameter('vp3int', 'V. Patch 3 Intensity', 'slider', 190, range(0, 128), checks=None, highchecks=None,
                       lowchecks=None, highnibbles=None, lownibbles=None)
    vp4int = parameter('vp4int', 'V. Patch 4 Intensity', 'slider', 193, range(0, 128), checks=None, highchecks=None,
                       lowchecks=None, highnibbles=None, lownibbles=None)
    vp5int = parameter('vp5int', 'V. Patch 5 Intensity', 'slider', 196, range(0, 128), checks=None, highchecks=None,
                       lowchecks=None, highnibbles=None, lownibbles=None)
    vp6int = parameter('vp6int', 'V. Patch 6 Intensity', 'slider', 199, range(0, 128), checks=None, highchecks=None,
                       lowchecks=None, highnibbles=None, lownibbles=None)
    osc1lfo1mod = parameter('osc1lfo1mod', 'Oscillator 1 LFO1 Mod ', 'slider', 120, range(0, 128), checks=None,
                            highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)

    parameters = [
    name,
    voicemode,
    octave,
    splitkey,
    unisonsw,
    unisondetune,
    unisonspread,
    pitchbendrange,
    voiceassign,
    vibratointensity,
    analog,
    timb1osc1level,
    timb1osc2level,
    noiselevel,
    filter2tnr,
    filter1balance,
    filter2tnr,
    filter1cutoff,
    filter1res,
    filter1eg1int,
    filter1velsens,
    filter2cutoff,
    filter2res,
    filter2eg1int,
    filter2velsens,
    waveshapea,
    waveshapeb,
    waveshapedepth,
    punch,
    eg1attack,
    eg1decay,
    eg1sustain,
    eg1release,
    eg1velo,
    eg2attack,
    eg2decay,
    eg2sustain,
    eg2release,
    eg2velo,
    eg3attack,
    eg3decay,
    eg3sustain,
    eg3release,
    eg3velo,
    lfo1wavea,
    lfo1waveb,
    lfo1freq,
    lfo2wavea,
    lfo2waveb,
    lfo2freq,
    osc1wave,
    osc2wave,
    osc1dwgs,
    fx1,
    fx2,
    vp1src,
    vp2src,
    vp3src,
    vp4src,
    vp5src,
    vp6src,
    vp1dst,
    vp2dst,
    vp3dst,
    vp4dst,
    vp5dst,
    vp6dst,
    vp1int,
    vp2int,
    vp3int,
    vp4int,
    vp5int,
    vp6int,
    osc1lfo1mod]


    def __init__(self, number):
        self.number = number
        for param in self.parameters:
            if not param.index == 'name':
                if not param.options == None:
                    param.value = random.choice(param.options)
                else:
                    param.value = random.choice(param.highnibbles) | random.choice(param.lownibbles)
            else:
                param.value = 'Rand ' + str(number).zfill(3)

    def randomize(self):
        for param in self.parameters:
            if param.index != 'name':
                if param.options != ['']:
                    param.value = random.choice(param.options)
                else:
                    param.value = random.choice(param.highnibbles) | random.choice(param.lownibbles)

    def write(self, mm, timbre):
        for param in self.parameters:
            if param.index == 'name':
                mm[self.number * patchsize + offset + param.location:self.number * patchsize + offset + param.location + 8] = ('Rand ' + str(self.number).zfill(3)).encode()
            else:
                mm[(timbre-1)*timbre2 + self.number * patchsize + offset + param.location] = param.value
