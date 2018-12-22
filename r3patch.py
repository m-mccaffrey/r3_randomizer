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

    # params['name'] = {}
    # params['voicemode'] = {}
    # params['octave'] = {}
    # params['splitkey'] = {}
    # params['unisonsw'] = {}
    # params['unisondetune'] = {}
    # params['unisonspread'] = {}
    # params['pitchbendrange'] = {}
    # params['voiceassign'] = {}
    # params['vibratointensity'] = {}
    # params['analog'] = {}
    # # params['osc1modtype'] = {}
    # params['timb1osc1level'] = {}
    # params['timb1osc2level'] = {}
    # params['noiselevel'] = {}
    # params['filter2tnr'] = {}
    # params['filter1balance'] = {}
    # params['filter2tnr'] = {}
    # params['filter1cutoff'] = {}
    # params['filter1res'] = {}
    # params['filter1eg1int'] = {}
    # params['filter1velsens'] = {}
    # params['filter2cutoff'] = {}
    # params['filter2res'] = {}
    # params['filter2eg1int'] = {}
    # params['filter2velsens'] = {}
    # params['waveshapea'] = {}
    # params['waveshapeb'] = {}
    # params['waveshapedepth'] = {}
    # params['punch'] = {}
    # params['eg1attack'] = {}
    # params['eg1decay'] = {}
    # params['eg1sustain'] = {}
    # params['eg1release'] = {}
    # params['eg1velo'] = {}
    # params['eg2attack'] = {}
    # params['eg2decay'] = {}
    # params['eg2sustain'] = {}
    # params['eg2release'] = {}
    # params['eg2velo'] = {}
    # params['eg3attack'] = {}
    # params['eg3decay'] = {}
    # params['eg3sustain'] = {}
    # params['eg3release'] = {}
    # params['eg3velo'] = {}
    # params['lfo1wavea'] = {}
    # params['lfo1waveb'] = {}
    # params['lfo1freq'] = {}
    # params['lfo2wavea'] = {}
    # params['lfo2waveb'] = {}
    # params['lfo2freq'] = {}
    # params['osc1wave'] = {}
    # params['osc2wave'] = {}
    # params['osc1dwgs'] = {}
    # params['fx1'] = {}
    # params['fx2'] = {}
    # params['vp1src'] = {}
    # params['vp2src'] = {}
    # params['vp3src'] = {}
    # params['vp4src'] = {}
    # params['vp5src'] = {}
    # params['vp6src'] = {}
    # params['vp1dst'] = {}
    # params['vp2dst'] = {}
    # params['vp3dst'] = {}
    # params['vp4dst'] = {}
    # params['vp5dst'] = {}
    # params['vp6dst'] = {}
    # params['vp1int'] = {}
    # params['vp2int'] = {}
    # params['vp3int'] = {}
    # params['vp4int'] = {}
    # params['vp5int'] = {}
    # params['vp6int'] = {}
    # params['osc1lfo1mod'] = {}
    #
    # params['name']['label']             = 'Name (8 characters)'
    # params['voicemode']['label']        = 'Voice Mode'
    # params['octave']['label']           = 'Octave'
    # params['splitkey']['label']         = 'Split Key'
    # params['unisonsw']['label']         = 'Unison Switch'
    # params['unisondetune']['label']     = 'Unison Detune'
    # params['unisonspread']['label']     = 'Unison Spread'
    # params['analog']['label']           = 'Analog Tuning'
    # params['pitchbendrange']['label']   = 'Pitch Bend Range'
    # params['voiceassign']['label']      = 'Voice Assign'
    # params['vibratointensity']['label'] = 'Vibrato Intensity'
    # params['timb1osc1level']['label']   = 'Oscillator 1 Level'
    # params['timb1osc2level']['label']   = 'Oscillator 2 Level'
    # params['noiselevel']['label']       = 'Noise Level'
    # params['filter2tnr']['label']       = 'Filter 2 Type and Filter Routing'
    # params['filter1balance']['label']   = 'Filter 1 Balance'
    # params['filter1cutoff']['label']    = 'Filter 1 Cutoff'
    # params['filter1res']['label']       = 'Filter 1 Resonance'
    # params['filter1eg1int']['label']    = 'Filter 1 EG1 Intensity'
    # params['filter1velsens']['label']   = 'Filter 1 Velocity Sencsitivity'
    # params['filter2cutoff']['label']    = 'Filter 2 Cutoff'
    # params['filter2res']['label']       = 'Filter 2 Resonance'
    # params['filter2eg1int']['label']    = 'Filter 2 EG1 Intensity'
    # params['filter2velsens']['label']   = 'Filter 2 Velocity Sensitivity'
    # params['waveshapea']['label']       = 'Wave Shape Position'
    # params['waveshapeb']['label']       = 'Wave Shape Type'
    # params['waveshapedepth']['label']   = 'Wave Shape Depth'
    # params['punch']['label']            = 'Punch Level'
    # params['eg1attack']['label']        = 'Env. Gen. 1 Attack'
    # params['eg1decay']['label']         = 'Env. Gen. 1 Decay'
    # params['eg1sustain']['label']       = 'Env. Gen. 1 Sustain'
    # params['eg1release']['label']       = 'Env. Gen. 1 Release'
    # params['eg1velo']['label']          = 'Env. Gen. 1 Velocity Sensitivity'
    # params['eg2attack']['label']        = 'Env. Gen. 2 Attack'
    # params['eg2decay']['label']         = 'Env. Gen. 2 Decay'
    # params['eg2sustain']['label']       = 'Env. Gen. 2 Sustain'
    # params['eg2release']['label']       = 'Env. Gen. 2 Release'
    # params['eg2velo']['label']          = 'Env. Gen. 2 Velocity Sensitivity'
    # params['eg3attack']['label']        = 'Env. Gen. 3 Attack'
    # params['eg3decay']['label']         = 'Env. Gen. 3 Decay'
    # params['eg3sustain']['label']       = 'Env. Gen. 3 Sustain'
    # params['eg3release']['label']       = 'Env. Gen. 3 Release'
    # params['eg3velo']['label']          = 'Env. Gen. 3 Velocity Sensitivity'
    # params['lfo1wavea']['label']        = 'LFO 1 Wave A'
    # params['lfo1waveb']['label']        = 'LFO 1 Wave B'
    # params['lfo1freq']['label']         = 'LFO 1 Frequency'
    # params['lfo2wavea']['label']        = 'LFO 2 Wave A'
    # params['lfo2waveb']['label']        = 'LFO 2 Wave B'
    # params['lfo2freq']['label']         = 'LFO 2 Wave Frequency'
    # params['osc1wave']['label']         = 'Oscillator 1 Wave'
    # params['osc1dwgs']['label']         = 'DWGS Type'
    # params['osc2wave']['label']         = 'Oscillator 2 Wave'
    # params['fx1']['label']              = 'Effect 1'
    # params['fx2']['label']              = 'Effect 2'
    # params['vp1src']['label']           = 'V. Patch 1 Source'
    # params['vp2src']['label']           = 'V. Patch 2 Source'
    # params['vp3src']['label']           = 'V. Patch 3 Source'
    # params['vp4src']['label']           = 'V. Patch 4 Source'
    # params['vp5src']['label']           = 'V. Patch 5 Source'
    # params['vp6src']['label']           = 'V. Patch 6 Source'
    # params['vp1dst']['label']           = 'V. Patch 1 Destination'
    # params['vp2dst']['label']           = 'V. Patch 2 Destination'
    # params['vp3dst']['label']           = 'V. Patch 3 Destination'
    # params['vp4dst']['label']           = 'V. Patch 4 Destination'
    # params['vp5dst']['label']           = 'V. Patch 5 Destination'
    # params['vp6dst']['label']           = 'V. Patch 6 Destination'
    # params['vp1int']['label']           = 'V. Patch 1 Intensity'
    # params['vp2int']['label']           = 'V. Patch 2 Intensity'
    # params['vp3int']['label']           = 'V. Patch 3 Intensity'
    # params['vp4int']['label']           = 'V. Patch 4 Intensity'
    # params['vp5int']['label']           = 'V. Patch 5 Intensity'
    # params['vp6int']['label']           = 'V. Patch 6 Intensity'
    # params['osc1lfo1mod']['label']      = 'Oscillator 1 LFO1 Mod '
    #
    # params['name']['input']             = 'field'
    # params['voicemode']['input']        = 'checkbox'
    # params['octave']['input']           = 'slider'
    # params['splitkey']['input']         = 'slider'
    # params['unisonsw']['input']         = 'checkbox'
    # params['unisondetune']['input']     = 'slider'
    # params['unisonspread']['input']     = 'slider'
    # params['analog']['input']           = 'slider'
    # params['pitchbendrange']['input']   = 'slider'
    # params['voiceassign']['input']      = 'checkbox'
    # params['vibratointensity']['input'] = 'slider'
    # params['timb1osc1level']['input']   = 'slider'
    # params['timb1osc2level']['input']   = 'slider'
    # params['noiselevel']['input']       = 'slider'
    # params['filter2tnr']['input']       = 'checkbox'
    # params['filter1balance']['input']   = 'slider'
    # params['filter1cutoff']['input']    = 'slider'
    # params['filter1res']['input']       = 'slider'
    # params['filter1eg1int']['input']    = 'slider'
    # params['filter1velsens']['input']   = 'slider'
    # params['filter2cutoff']['input']    = 'slider'
    # params['filter2res']['input']       = 'slider'
    # params['filter2eg1int']['input']    = 'slider'
    # params['filter2velsens']['input']   = 'slider'
    # params['waveshapea']['input']       = 'checkbox'
    # params['waveshapeb']['input']       = 'checkbox'
    # params['waveshapedepth']['input']   = 'slider'
    # params['punch']['input']            = 'slider'
    # params['eg1attack']['input']        = 'slider'
    # params['eg1decay']['input']         = 'slider'
    # params['eg1sustain']['input']       = 'slider'
    # params['eg1release']['input']       = 'slider'
    # params['eg1velo']['input']          = 'slider'
    # params['eg2attack']['input']        = 'slider'
    # params['eg2decay']['input']         = 'slider'
    # params['eg2sustain']['input']       = 'slider'
    # params['eg2release']['input']       = 'slider'
    # params['eg2velo']['input']          = 'slider'
    # params['eg3attack']['input']        = 'slider'
    # params['eg3decay']['input']         = 'slider'
    # params['eg3sustain']['input']       = 'slider'
    # params['eg3release']['input']       = 'slider'
    # params['eg3velo']['input']          = 'slider'
    # params['lfo1wavea']['input']        = 'checkbox'
    # params['lfo1waveb']['input']        = 'checkbox'
    # params['lfo1freq']['input']         = 'slider'
    # params['lfo2wavea']['input']        = 'checkbox'
    # params['lfo2waveb']['input']        = 'checkbox'
    # params['lfo2freq']['input']         = 'slider'
    # params['osc1wave']['input']         = 'checkbox'
    # params['osc1dwgs']['input']         = 'checkbox'
    # params['osc2wave']['input']         = 'checkbox'
    # params['fx1']['input']              = 'checkbox'
    # params['fx2']['input']              = 'checkbox'
    # params['vp1src']['input']           = 'checkbox'
    # params['vp2src']['input']           = 'checkbox'
    # params['vp3src']['input']           = 'checkbox'
    # params['vp4src']['input']           = 'checkbox'
    # params['vp5src']['input']           = 'checkbox'
    # params['vp6src']['input']           = 'checkbox'
    # params['vp1dst']['input']           = 'checkbox'
    # params['vp2dst']['input']           = 'checkbox'
    # params['vp3dst']['input']           = 'checkbox'
    # params['vp4dst']['input']           = 'checkbox'
    # params['vp5dst']['input']           = 'checkbox'
    # params['vp6dst']['input']           = 'checkbox'
    # params['vp1int']['input']           = 'slider'
    # params['vp2int']['input']           = 'slider'
    # params['vp3int']['input']           = 'slider'
    # params['vp4int']['input']           = 'slider'
    # params['vp5int']['input']           = 'slider'
    # params['vp6int']['input']           = 'slider'
    # params['osc1lfo1mod']['input']      = 'slider'
    #
    # params['voicemode']['checks']        = ['Single', 'Layer', 'Split', 'Multi']
    # params['unisonsw']['highchecks']     = ['On', 'Off']
    # params['unisonsw']['lowchecks']      = ['2', '3', '4']
    # params['voiceassign']['checks']      = ['Mono 1', 'Mono 2', 'Poly']
    # params['filter2tnr']['highchecks']   = ['LPF', 'HPF', 'BPF', 'Comb']
    # params['filter2tnr']['lowchecks']    = ['Single', 'Serial', 'Parallel', 'Individual']
    # params['waveshapea']['highchecks']   = ['Pre-Filter 1', 'Pre-Amp']
    # params['waveshapea']['lowchecks']    = ['Off', 'Drive', 'Decimator']
    # params['waveshapeb']['checks']       = ['HardClip', 'OctSaw', 'MultiTri', 'MultiSin', 'SubOsc Saw', 'SubOsc Tri', 'SubOsc Squ', 'SubOsc Sin', 'Pickup', 'Level Boost']
    # params['lfo1wavea']['checks']        = ['Saw', 'Square', 'Triangle', 'S&H']
    # params['lfo1waveb']['checks']        = ['Wave', 'Random']
    # params['lfo2wavea']['checks']        = ['Saw', 'Square', 'Triangle', 'S&H']
    # params['lfo2waveb']['checks']        = ['Wave', 'Random']
    # params['osc1wave']['lowchecks']      = ['Saw', 'Pulse', 'Triangle', 'Sine', 'Formant', 'Noise', 'DWGS']
    # params['osc1wave']['highchecks']     = ['Waveform', 'Cross', 'Unison', 'VPM']
    # params['osc2wave']['lowchecks']      = ['Saw', 'Square', 'Triangle' ,'Sine']
    # params['osc2wave']['highchecks']     = ['None', 'Ring','Sync','Ring & Sync']
    # params['osc1dwgs']['checks']         = []
    # params['fx1']['checks']              = []
    # params['fx2']['checks']              = []
    # params['vp1src']['checks']           = ['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel']
    # params['vp2src']['checks']           = ['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel']
    # params['vp3src']['checks']           = ['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel']
    # params['vp4src']['checks']           = ['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel']
    # params['vp5src']['checks']           = ['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel']
    # params['vp6src']['checks']           = ['EG1', 'EG2', 'EG3', 'LFO1', 'LFO2', 'Velocity', 'Pitch Bend', 'Mod Wheel']
    #
    # params['vp1dst']['checks']           = ['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level',
    #                                         'Noise Level', 'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance',
    #                                         'Filter 2 Cutoff', 'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency',
    #                                         'LFO2 Frequency']
    #
    # params['vp2dst']['checks']           = ['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level',
    #                                         'Noise Level', 'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance',
    #                                         'Filter 2 Cutoff', 'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency',
    #                                         'LFO2 Frequency']
    #
    # params['vp3dst']['checks']           = ['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level',
    #                                         'Noise Level', 'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance',
    #                                         'Filter 2 Cutoff', 'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency',
    #                                         'LFO2 Frequency']
    #
    # params['vp4dst']['checks']           = ['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level',
    #                                         'Noise Level', 'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance',
    #                                         'Filter 2 Cutoff', 'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency',
    #                                         'LFO2 Frequency']
    #
    # params['vp5dst']['checks']           = ['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level',
    #                                         'Noise Level', 'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance',
    #                                         'Filter 2 Cutoff', 'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency',
    #                                         'LFO2 Frequency']
    #
    # params['vp6dst']['checks']           = ['Pitch', 'Osc 2 Tune', 'Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level',
    #                                         'Noise Level', 'Filter 1 Balance', 'Filter 1 Cutoff', 'Filter 1 Resonance',
    #                                         'Filter 2 Cutoff', 'Waveshape Depth', 'Amp Level', 'Panpot', 'LFO1 Frequency',
    #                                         'LFO2 Frequency']
    #
    #
    # params['name']['location'] = 32
    # params['name']['options'] = ['Testing']
    # params['voicemode']['location'] = 49
    # params['voicemode']['options'] = range(0, 0xFF, 0x40)
    # params['octave']['location'] = 53
    # params['octave']['options'] = range(5, 12)
    # params['splitkey']['location'] = 87
    # params['splitkey']['options'] = range(0x00, 0x80)
    # params['unisonsw']['location'] = 88
    # params['unisonsw']['options'] = None
    # params['unisonsw']['highnibbles'] = [0x70, 0xF0]
    # params['unisonsw']['lownibbles'] = range(0x0, 0x03)
    # params['unisondetune']['location'] = 89
    # params['unisondetune']['options'] = range(0x00, 0x63)
    # params['unisonspread']['location'] = 90
    # params['unisonspread']['options'] = range(0x00, 0x80)
    # params['pitchbendrange']['location'] = 91
    # params['pitchbendrange']['options'] = range(0x34, 0x4D)
    # params['voiceassign']['location'] = 102
    # params['voiceassign']['options'] = [0x30, 0x70, 0xF0]
    # params['vibratointensity']['location'] = 107
    # params['vibratointensity']['options'] = range(0x00, 0x80)
    # params['osc1wave']['location'] = 118
    # params['osc1wave']['options'] = None
    # params['osc1wave']['highnibbles'] = range(0x80, 0xC0, 0x10)
    # params['osc1wave']['lownibbles'] = range(0x0, 0x07)
    # params['osc1dwgs']['location'] = 121
    # params['osc1dwgs']['options'] = range(0x0, 0x40)
    # # params['waveform']['location'] = 119
    # # params['waveform']['options'] = range(0x00, 0x80)
    # params['osc1lfo1mod']['location'] = 120
    # params['osc1lfo1mod']['options'] = range(0x00, 0x80)
    # params['osc2wave']['location'] = 123
    # params['osc2wave']['options'] = None
    # params['osc2wave']['highnibbles'] = range(0x00, 0x40, 0x10)
    # params['osc2wave']['lownibbles'] = range(0x0, 0x04)
    # params['analog']['location'] = 114
    # params['analog']['options'] = range(0x00, 0x20)
    # params['timb1osc1level']['location'] = 126
    # params['timb1osc1level']['options'] = range(0x00, 0x80)
    # params['timb1osc2level']['location'] = 127
    # params['timb1osc2level']['options'] = range(0x00, 0x80)
    # params['noiselevel']['location'] = 128
    # params['noiselevel']['options'] = range(0x00, 0x80)
    #
    # params['noiselevel']['location'] = 128
    # params['filter2tnr']['location'] = 129
    # params['filter1balance']['location'] = 130
    # params['filter1cutoff']['location'] = 131
    # params['filter1res']['location'] = 132
    # params['filter1eg1int']['location'] = 133
    # params['filter1velsens']['location'] = 135
    # params['filter2cutoff']['location'] = 136
    # params['filter2res']['location'] = 137
    # params['filter2eg1int']['location'] = 138
    # params['filter2velsens']['location'] = 140
    # params['waveshapea']['location'] = 142
    # params['waveshapeb']['location'] = 143
    # params['waveshapedepth']['location'] = 144
    # params['punch']['location'] = 147
    # params['eg1attack']['location'] = 148
    # params['eg1decay']['location'] = 149
    # params['eg1sustain']['location'] = 150
    # params['eg1release']['location'] = 151
    # params['eg1velo']['location'] = 153
    # params['eg2attack']['location'] = 156
    # params['eg2decay']['location'] = 157
    # params['eg2sustain']['location'] = 158
    # params['eg2release']['location'] = 159
    # params['eg2velo']['location'] = 161
    # params['eg3attack']['location'] = 164
    # params['eg3decay']['location'] = 165
    # params['eg3sustain']['location'] = 166
    # params['eg3release']['location'] = 167
    # params['eg3velo']['location'] = 169
    # params['lfo1wavea']['location'] = 172
    # params['lfo1waveb']['location'] = 173
    # params['lfo1freq']['location'] = 174
    # params['lfo2wavea']['location'] = 177
    # params['lfo2waveb']['location'] = 178
    # params['lfo2freq']['location'] = 179
    # params['fx1']['location'] = 200
    # params['fx2']['location'] = 224
    # params['fx1']['options'] = range(0x80, 0x9D)
    # params['fx2']['options'] = range(0x80, 0x9D)
    #
    # params['vp1src']['location'] = 182
    # params['vp1src']['options'] = range(0x00, 0x08)
    # params['vp2src']['location'] = 185
    # params['vp2src']['options'] = range(0x00, 0x08)
    # params['vp3src']['location'] = 188
    # params['vp3src']['options'] = range(0x00, 0x08)
    # params['vp4src']['location'] = 191
    # params['vp4src']['options'] = range(0x00, 0x08)
    # params['vp5src']['location'] = 194
    # params['vp5src']['options'] = range(0x00, 0x08)
    # params['vp6src']['location'] = 197
    # params['vp6src']['options'] = range(0x00, 0x08)
    # params['vp1dst']['location'] = 183
    # params['vp1dst']['options'] = range(0x00, 0x08)
    # params['vp2dst']['location'] = 186
    # params['vp2dst']['options'] = range(0x00, 0x08)
    # params['vp3dst']['location'] = 189
    # params['vp3dst']['options'] = range(0x00, 0x08)
    # params['vp4dst']['location'] = 192
    # params['vp4dst']['options'] = range(0x00, 0x08)
    # params['vp5dst']['location'] = 195
    # params['vp5dst']['options'] = range(0x00, 0x08)
    # params['vp6dst']['location'] = 198
    # params['vp6dst']['options'] = range(0x00, 0x08)
    # params['vp1int']['location'] = 184
    # params['vp1int']['options'] = range(0x00, 0x80)
    # params['vp2int']['location'] = 187
    # params['vp2int']['options'] = range(0x00, 0x80)
    # params['vp3int']['location'] = 190
    # params['vp3int']['options'] = range(0x00, 0x80)
    # params['vp4int']['location'] = 193
    # params['vp4int']['options'] = range(0x00, 0x80)
    # params['vp5int']['location'] = 196
    # params['vp5int']['options'] = range(0x00, 0x80)
    # params['vp6int']['location'] = 199
    # params['vp6int']['options'] = range(0x00, 0x80)
    #
    # params['noiselevel']['options'] = range(0x00, 0x10)
    # params['filter2tnr']['options'] = None
    # params['filter2tnr']['highnibbles'] = range(0x40, 0x80, 0x10)
    # params['filter2tnr']['lownibbles'] = range(0x0C, 0x10)
    # params['filter1balance']['options'] = range(0x00, 0x80)
    # params['filter1cutoff']['options'] = range(0x00, 0x80)
    # params['filter1res']['options'] = range(0x00, 0x80)
    # params['filter1eg1int']['options'] = range(0x00, 0x80)
    # params['filter1velsens']['options'] = range(0x00, 0x80)
    # params['filter2cutoff']['options'] = range(0x00, 0x80)
    # params['filter2res']['options'] = range(0x00, 0x80)
    # params['filter2eg1int']['options'] = range(0x00, 0x80)
    # params['filter2velsens']['options'] = range(0x00, 0x80)
    # params['waveshapea']['options'] = None #[0x00, 0x01, 0x02, 0x10, 0x11, 0x12]
    # params['waveshapea']['highnibbles'] = [0x00,0x10]
    # params['waveshapea']['lownibbles'] = range(0x00, 0x03)
    # params['waveshapeb']['options'] = range(0x00, 0x0B)
    # params['waveshapedepth']['options'] = range(0x00, 0x80)
    # params['punch']['options'] = range(0x00, 0x80)
    # params['eg1attack']['options'] = range(0x00, 0x30)
    # params['eg1decay']['options'] = range(0x00, 0x80)
    # params['eg1sustain']['options'] = range(0x00, 0x80)
    # params['eg1release']['options'] = range(0x00, 0x80)
    # params['eg1velo']['options'] = range(0x00, 0x80)
    # params['eg2attack']['options'] = range(0x00, 0x80)
    # params['eg2decay']['options'] = range(0x00, 0x80)
    # params['eg2sustain']['options'] = range(0x00, 0x80)
    # params['eg2release']['options'] = range(0x00, 0x80)
    # params['eg2velo']['options'] = range(0x00, 0x80)
    # params['eg3attack']['options'] = range(0x00, 0x80)
    # params['eg3decay']['options'] = range(0x00, 0x80)
    # params['eg3sustain']['options'] = range(0x00, 0x80)
    # params['eg3release']['options'] = range(0x00, 0x80)
    # params['eg3velo']['options'] = range(0x00, 0x80)
    # params['lfo1wavea']['options'] = range(0x00, 0x04)
    # params['lfo1waveb']['options'] = [0x40, 0x7F]
    # params['lfo1freq']['options'] = range(0x00, 0x80)
    # params['lfo2wavea']['options'] = range(0x00, 0x04)
    # params['lfo2waveb']['options'] = [0x40, 0x7F]
    # params['lfo2freq']['options'] = range(0x00, 0x80)

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
