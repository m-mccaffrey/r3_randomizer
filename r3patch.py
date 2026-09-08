import random

from controls import *

offset = 192
patchsize = 2336
timbre2 = 228
# Parameters at locations below this are patch-common (e.g. voice mode,
# octave, pitch bend range) and must be written once, not per-timbre.
# Per-timbre parameters (oscillators, filters, envelopes, LFOs, ...) start
# here and repeat every `timbre2` bytes for the second timbre.
per_timbre_start = 114

class Parameter:
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

    def add_slider(self, parent):
        self.interface = Slider(parent, self)
        return self.interface

    def add_checkbank(self, parent):
        self.interface = Checkbank(parent, self, self.numrows)
        return self.interface


class Patch:

    name = Parameter('name', 'Name (8 characters)', 'field', 32, ['Testing'], checks=None, highchecks=None,
                     lowchecks=None, highnibbles=None, lownibbles=None)
    voicemode = Parameter('voicemode', 'Voice Mode', 'checkbox', 49, list(range(0, 255, 64)),
                          checks=['Single', 'Layer', 'Split', 'Multi'], highchecks=None, lowchecks=None,
                          highnibbles=None, lownibbles=None)
    octave = Parameter('octave', 'Octave', 'slider', 53, range(5, 12), checks=None, highchecks=None, lowchecks=None,
                       highnibbles=None, lownibbles=None)
    splitkey = Parameter('splitkey', 'Split Key', 'slider', 87, range(0, 128), checks=None, highchecks=None,
                         lowchecks=None, highnibbles=None, lownibbles=None)
    unisonsw = Parameter('unisonsw', 'Unison Switch', 'checkbox', 88, [''], checks=None, highchecks=['On', 'Off'],
                         lowchecks=['2', '3', '4'], highnibbles=[112, 240], lownibbles=list(range(0, 3)))
    unisondetune = Parameter('unisondetune', 'Unison Detune', 'slider', 89, range(0, 99), checks=None, highchecks=None,
                             lowchecks=None, highnibbles=None, lownibbles=None)
    unisonspread = Parameter('unisonspread', 'Unison Spread', 'slider', 90, range(0, 128), checks=None, highchecks=None,
                             lowchecks=None, highnibbles=None, lownibbles=None)
    pitchbendrange = Parameter('pitchbendrange', 'Pitch Bend Range', 'slider', 91, range(52, 77), checks=None,
                               highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    voiceassign = Parameter('voiceassign', 'Voice Assign', 'checkbox', 102, [48, 112, 240],
                            checks=['Mono 1', 'Mono 2', 'Poly'], highchecks=None, lowchecks=None, highnibbles=None,
                            lownibbles=None)
    vibratointensity = Parameter('vibratointensity', 'Vibrato Intensity', 'slider', 107, range(0, 128), checks=None,
                                 highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    analog = Parameter('analog', 'Analog Tuning', 'slider', 114, range(0, 32), checks=None, highchecks=None,
                       lowchecks=None, highnibbles=None, lownibbles=None)
    timb1osc1level = Parameter('timb1osc1level', 'Oscillator 1 Level', 'slider', 126, range(0, 128), checks=None,
                               highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    timb1osc2level = Parameter('timb1osc2level', 'Oscillator 2 Level', 'slider', 127, range(0, 128), checks=None,
                               highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    noiselevel = Parameter('noiselevel', 'Noise Level', 'slider', 128, range(0, 16), checks=None, highchecks=None,
                           lowchecks=None, highnibbles=None, lownibbles=None)
    filter2tnr = Parameter('filter2tnr', 'Filter 2 Type and Filter Routing', 'checkbox', 129, [''], checks=None,
                           highchecks=['LPF', 'HPF', 'BPF', 'Comb'],
                           lowchecks=['Single', 'Serial', 'Parallel', 'Individual'], highnibbles=list(range(64, 128, 16)),
                           lownibbles=list(range(12, 16)))
    filter1balance = Parameter('filter1balance', 'Filter 1 Balance', 'slider', 130, range(0, 128), checks=None,
                               highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    filter1cutoff = Parameter('filter1cutoff', 'Filter 1 Cutoff', 'slider', 131, range(0, 128), checks=None,
                              highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    filter1res = Parameter('filter1res', 'Filter 1 Resonance', 'slider', 132, range(0, 128), checks=None,
                           highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    filter1eg1int = Parameter('filter1eg1int', 'Filter 1 EG1 Intensity', 'slider', 133, range(0, 128), checks=None,
                              highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    filter1velsens = Parameter('filter1velsens', 'Filter 1 Velocity Sensitivity', 'slider', 135, range(0, 128),
                               checks=None, highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    filter2cutoff = Parameter('filter2cutoff', 'Filter 2 Cutoff', 'slider', 136, range(0, 128), checks=None,
                              highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    filter2res = Parameter('filter2res', 'Filter 2 Resonance', 'slider', 137, range(0, 128), checks=None,
                           highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    filter2eg1int = Parameter('filter2eg1int', 'Filter 2 EG1 Intensity', 'slider', 138, range(0, 128), checks=None,
                              highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    filter2velsens = Parameter('filter2velsens', 'Filter 2 Velocity Sensitivity', 'slider', 140, range(0, 128),
                               checks=None, highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    waveshapea = Parameter('waveshapea', 'Wave Shape Position', 'checkbox', 142, [''], checks=None,
                           highchecks=['Pre-Filter 1', 'Pre-Amp'], lowchecks=['Off', 'Drive', 'Decimator'],
                           highnibbles=[0, 16], lownibbles=list(range(0, 3)))
    waveshapeb = Parameter('waveshapeb', 'Wave Shape Type', 'checkbox', 143, list(range(0, 10)),
                           checks=['HardClip', 'OctSaw', 'MultiTri', 'MultiSin', 'SubOsc Saw', 'SubOsc Tri',
                                   'SubOsc Squ', 'SubOsc Sin', 'Pickup', 'Level Boost'], highchecks=None,
                           lowchecks=None, highnibbles=None, lownibbles=None)
    waveshapedepth = Parameter('waveshapedepth', 'Wave Shape Depth', 'slider', 144, range(0, 128), checks=None,
                               highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    punch = Parameter('punch', 'Punch Level', 'slider', 147, range(0, 128), checks=None, highchecks=None,
                      lowchecks=None, highnibbles=None, lownibbles=None)
    eg1attack = Parameter('eg1attack', 'Env. Gen. 1 Attack', 'slider', 148, range(0, 48), checks=None, highchecks=None,
                          lowchecks=None, highnibbles=None, lownibbles=None)
    eg1decay = Parameter('eg1decay', 'Env. Gen. 1 Decay', 'slider', 149, range(0, 128), checks=None, highchecks=None,
                         lowchecks=None, highnibbles=None, lownibbles=None)
    eg1sustain = Parameter('eg1sustain', 'Env. Gen. 1 Sustain', 'slider', 150, range(0, 128), checks=None,
                           highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    eg1release = Parameter('eg1release', 'Env. Gen. 1 Release', 'slider', 151, range(0, 128), checks=None,
                           highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    eg1velo = Parameter('eg1velo', 'Env. Gen. 1 Velocity Sensitivity', 'slider', 153, range(0, 128), checks=None,
                        highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    eg2attack = Parameter('eg2attack', 'Env. Gen. 2 Attack', 'slider', 156, range(0, 128), checks=None, highchecks=None,
                          lowchecks=None, highnibbles=None, lownibbles=None)
    eg2decay = Parameter('eg2decay', 'Env. Gen. 2 Decay', 'slider', 157, range(0, 128), checks=None, highchecks=None,
                         lowchecks=None, highnibbles=None, lownibbles=None)
    eg2sustain = Parameter('eg2sustain', 'Env. Gen. 2 Sustain', 'slider', 158, range(0, 128), checks=None,
                           highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    eg2release = Parameter('eg2release', 'Env. Gen. 2 Release', 'slider', 159, range(0, 128), checks=None,
                           highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    eg2velo = Parameter('eg2velo', 'Env. Gen. 2 Velocity Sensitivity', 'slider', 161, range(0, 128), checks=None,
                        highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    eg3attack = Parameter('eg3attack', 'Env. Gen. 3 Attack', 'slider', 164, range(0, 128), checks=None, highchecks=None,
                          lowchecks=None, highnibbles=None, lownibbles=None)
    eg3decay = Parameter('eg3decay', 'Env. Gen. 3 Decay', 'slider', 165, range(0, 128), checks=None, highchecks=None,
                         lowchecks=None, highnibbles=None, lownibbles=None)
    eg3sustain = Parameter('eg3sustain', 'Env. Gen. 3 Sustain', 'slider', 166, range(0, 128), checks=None,
                           highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    eg3release = Parameter('eg3release', 'Env. Gen. 3 Release', 'slider', 167, range(0, 128), checks=None,
                           highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    eg3velo = Parameter('eg3velo', 'Env. Gen. 3 Velocity Sensitivity', 'slider', 169, range(0, 128), checks=None,
                        highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    lfo1wavea = Parameter('lfo1wavea', 'LFO 1 Wave A', 'checkbox', 172, list(range(0, 4)),
                          checks=['Saw', 'Square', 'Triangle', 'S&H'], highchecks=None, lowchecks=None,
                          highnibbles=None, lownibbles=None)
    lfo1waveb = Parameter('lfo1waveb', 'LFO 1 Wave B', 'checkbox', 173, [64, 127], checks=['Wave', 'Random'],
                          highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    lfo1freq = Parameter('lfo1freq', 'LFO 1 Frequency', 'slider', 174, list(range(0, 128)), checks=None, highchecks=None,
                         lowchecks=None, highnibbles=None, lownibbles=None)
    lfo2wavea = Parameter('lfo2wavea', 'LFO 2 Wave A', 'checkbox', 177, list(range(0, 4)),
                          checks=['Saw', 'Square', 'Triangle', 'S&H'], highchecks=None, lowchecks=None,
                          highnibbles=None, lownibbles=None)
    lfo2waveb = Parameter('lfo2waveb', 'LFO 2 Wave B', 'checkbox', 178, [64, 127], checks=['Wave', 'Random'],
                          highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    lfo2freq = Parameter('lfo2freq', 'LFO 2 Wave Frequency', 'slider', 179, list(range(0, 128)), checks=None, highchecks=None,
                         lowchecks=None, highnibbles=None, lownibbles=None)
    osc1wave = Parameter('osc1wave', 'Oscillator 1 Wave', 'checkbox', 118, [''], checks=None,
                         highchecks=['Waveform', 'Cross', 'Unison', 'VPM'],
                         lowchecks=['Saw', 'Pulse', 'Triangle', 'Sine', 'Formant', 'Noise', 'DWGS'],
                         highnibbles=list(range(128, 192, 16)), lownibbles=list(range(0, 7)))
    osc2wave = Parameter('osc2wave', 'Oscillator 2 Wave', 'checkbox', 123, [''], checks=None,
                         highchecks=['None', 'Ring', 'Sync', 'Ring & Sync'],
                         lowchecks=['Saw', 'Square', 'Triangle', 'Sine'], highnibbles=list(range(0, 64, 16)),
                         lownibbles=list(range(0, 4)))
    osc1dwgs = Parameter('osc1dwgs', 'DWGS Type', 'checkbox', 121, list(range(0, 64)), checks=['DWGS ' + str(i) for i in range(0, 64)], highchecks=None,
                         lowchecks=None, highnibbles=None, lownibbles=None, numrows=32)
    fx1 = Parameter('fx1', 'Effect 1', 'checkbox', 200, list(range(128, 157)), checks=['FX Type ' + str(i) for i in range(0, 29)], highchecks=None, lowchecks=None,
                    highnibbles=None, lownibbles=None, numrows=15)
    fx2 = Parameter('fx2', 'Effect 2', 'checkbox', 224, list(range(128, 157)), checks=['FX Type ' + str(i) for i in range(0, 29)], highchecks=None, lowchecks=None,
                    highnibbles=None, lownibbles=None, numrows=15)
    vp1src = Parameter('vp1src', 'V. Patch 1 Source', 'checkbox', 182, list(range(0, 8)),
                       checks=['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp2src = Parameter('vp2src', 'V. Patch 2 Source', 'checkbox', 185, list(range(0, 8)),
                       checks=['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp3src = Parameter('vp3src', 'V. Patch 3 Source', 'checkbox', 188, list(range(0, 8)),
                       checks=['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp4src = Parameter('vp4src', 'V. Patch 4 Source', 'checkbox', 191, list(range(0, 8)),
                       checks=['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp5src = Parameter('vp5src', 'V. Patch 5 Source', 'checkbox', 194, list(range(0, 8)),
                       checks=['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp6src = Parameter('vp6src', 'V. Patch 6 Source', 'checkbox', 197, list(range(0, 8)),
                       checks=['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp1dst = Parameter('vp1dst', 'V. Patch 1 Destination', 'checkbox', 183, list(range(0, 8)),
                       checks=['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level', 'Noise Level',
                               'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance', 'Filter 2 Cutoff',
                               'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency', 'LFO2 Frequency'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp2dst = Parameter('vp2dst', 'V. Patch 2 Destination', 'checkbox', 186, list(range(0, 8)),
                       checks=['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level', 'Noise Level',
                               'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance', 'Filter 2 Cutoff',
                               'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency', 'LFO2 Frequency'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp3dst = Parameter('vp3dst', 'V. Patch 3 Destination', 'checkbox', 189, list(range(0, 8)),
                       checks=['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level', 'Noise Level',
                               'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance', 'Filter 2 Cutoff',
                               'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency', 'LFO2 Frequency'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp4dst = Parameter('vp4dst', 'V. Patch 4 Destination', 'checkbox', 192, list(range(0, 8)),
                       checks=['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level', 'Noise Level',
                               'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance', 'Filter 2 Cutoff',
                               'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency', 'LFO2 Frequency'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp5dst = Parameter('vp5dst', 'V. Patch 5 Destination', 'checkbox', 195, list(range(0, 8)),
                       checks=['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level', 'Noise Level',
                               'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance', 'Filter 2 Cutoff',
                               'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency', 'LFO2 Frequency'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp6dst = Parameter('vp6dst', 'V. Patch 6 Destination', 'checkbox', 198, list(range(0, 8)),
                       checks=['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level', 'Noise Level',
                               'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance', 'Filter 2 Cutoff',
                               'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency', 'LFO2 Frequency'],
                       highchecks=None, lowchecks=None, highnibbles=None, lownibbles=None)
    vp1int = Parameter('vp1int', 'V. Patch 1 Intensity', 'slider', 184, range(0, 128), checks=None, highchecks=None,
                       lowchecks=None, highnibbles=None, lownibbles=None)
    vp2int = Parameter('vp2int', 'V. Patch 2 Intensity', 'slider', 187, range(0, 128), checks=None, highchecks=None,
                       lowchecks=None, highnibbles=None, lownibbles=None)
    vp3int = Parameter('vp3int', 'V. Patch 3 Intensity', 'slider', 190, range(0, 128), checks=None, highchecks=None,
                       lowchecks=None, highnibbles=None, lownibbles=None)
    vp4int = Parameter('vp4int', 'V. Patch 4 Intensity', 'slider', 193, range(0, 128), checks=None, highchecks=None,
                       lowchecks=None, highnibbles=None, lownibbles=None)
    vp5int = Parameter('vp5int', 'V. Patch 5 Intensity', 'slider', 196, range(0, 128), checks=None, highchecks=None,
                       lowchecks=None, highnibbles=None, lownibbles=None)
    vp6int = Parameter('vp6int', 'V. Patch 6 Intensity', 'slider', 199, range(0, 128), checks=None, highchecks=None,
                       lowchecks=None, highnibbles=None, lownibbles=None)
    osc1lfo1mod = Parameter('osc1lfo1mod', 'Oscillator 1 LFO1 Mod ', 'slider', 120, range(0, 128), checks=None,
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
        self.randomize()

    def randomize(self):
        for param in self.parameters:
            if param.index == 'name':
                param.value = 'Rand ' + str(self.number).zfill(3)
            elif param.options != ['']:
                param.value = random.choice(param.options)
            else:
                param.value = random.choice(param.highnibbles) | random.choice(param.lownibbles)

    def write(self, mm, timbre):
        patch_base = self.number * patchsize + offset
        for param in self.parameters:
            if param.index == 'name':
                addr = patch_base + param.location
                mm[addr:addr + 8] = param.value.encode()
            else:
                # Patch-common parameters live before the per-timbre block
                # and must not be shifted by the timbre offset, or the
                # write would land on unrelated bytes of the other timbre.
                timbre_offset = (timbre - 1) * timbre2 if param.location >= per_timbre_start else 0
                mm[patch_base + timbre_offset + param.location] = param.value
