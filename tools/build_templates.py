"""
Generates the preset files under templates/*.json.

Presets are defined below using the human-readable option names shown in
the GUI (e.g. 'Saw', 'LPF', 'Single') rather than raw byte/nibble values,
and are resolved against the real Patch parameter definitions in
r3patch.py. That resolution is checked at generation time: an unknown
label or an out-of-range slider bound raises immediately instead of
silently producing a bad preset.

To change a template, edit its list of entries below and re-run:
    python3 tools/build_templates.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r3patch import Patch

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')

patch = Patch(-1)
params = {p.index: p for p in patch.parameters}


def slider(index, lo, hi):
    p = params[index]
    assert p.control == 'slider', index
    full_lo, full_hi = min(p.options), max(p.options)
    assert full_lo <= lo <= hi <= full_hi, (index, lo, hi, full_lo, full_hi)
    return index, {'type': 'slider', 'min': lo, 'max': hi}


def checklist(index, labels):
    p = params[index]
    assert p.control == 'checkbox' and p.options != [''], index
    values = [p.options[p.checks.index(label)] for label in labels]
    return index, {'type': 'checklist', 'options': values}


def nibble(index, high_labels=None, low_labels=None):
    p = params[index]
    assert p.control == 'checkbox' and p.options == [''], index
    result = {'type': 'nibble'}
    result['highnibbles'] = (list(p.highnibbles) if high_labels is None else
                              [p.highnibbles[p.highchecks.index(l)] for l in high_labels])
    result['lownibbles'] = (list(p.lownibbles) if low_labels is None else
                             [p.lownibbles[p.lowchecks.index(l)] for l in low_labels])
    return index, result


def build(entries):
    return dict(entries)


# "Keys": melodic, playable, relatively in-tune patches. Polyphonic, no
# unison detune, clean tonal oscillator waveforms, moderate/bright but
# non-screaming filter, envelopes shaped for a struck/held note, and
# Virtual Patch destinations restricted away from Pitch/Osc 2 Tune so
# random modulation routing can't detune the patch.
KEYS = build([
    checklist('voicemode', ['Single', 'Layer']),
    slider('octave', 7, 9),
    nibble('unisonsw', high_labels=['Off'], low_labels=['2']),
    slider('unisondetune', 0, 5),
    slider('unisonspread', 0, 20),
    checklist('voiceassign', ['Poly']),
    slider('vibratointensity', 0, 30),
    slider('analog', 0, 8),
    slider('timb1osc1level', 90, 127),
    slider('timb1osc2level', 40, 110),
    slider('noiselevel', 0, 2),
    nibble('osc1wave', high_labels=['Waveform'], low_labels=['Saw', 'Pulse', 'Triangle', 'Sine']),
    nibble('osc2wave', high_labels=['None'], low_labels=['Saw', 'Triangle', 'Sine']),
    nibble('filter2tnr', high_labels=['LPF'], low_labels=['Single']),
    slider('filter1balance', 40, 100),
    slider('filter1cutoff', 55, 115),
    slider('filter1res', 0, 45),
    slider('filter1eg1int', 0, 60),
    slider('filter1velsens', 20, 90),
    slider('filter2cutoff', 60, 127),
    slider('filter2res', 0, 40),
    slider('filter2eg1int', 0, 50),
    slider('filter2velsens', 20, 90),
    nibble('waveshapea', high_labels=['Pre-Filter 1'], low_labels=['Off']),
    checklist('waveshapeb', ['HardClip']),
    slider('waveshapedepth', 0, 5),
    slider('punch', 20, 70),
    slider('eg1attack', 0, 15),
    slider('eg1decay', 20, 80),
    slider('eg1sustain', 50, 127),
    slider('eg1release', 10, 60),
    slider('eg1velo', 30, 100),
    slider('eg2attack', 0, 10),
    slider('eg2decay', 20, 90),
    slider('eg2sustain', 70, 127),
    slider('eg2release', 15, 70),
    slider('eg2velo', 50, 120),
    checklist('lfo1wavea', ['Triangle']),
    checklist('lfo1waveb', ['Wave']),
    slider('lfo1freq', 20, 60),
    checklist('lfo2wavea', ['Triangle']),
    checklist('lfo2waveb', ['Wave']),
    slider('lfo2freq', 10, 50),
] + [
    checklist(f'vp{n}dst', ['Osc 1 Ctrl 1', 'Osc 1 Level', 'Osc 2 Level', 'Noise Level',
                            'Filter 1 Balance', 'Filter 1 Cutoff'])
    for n in range(1, 7)
] + [
    slider(f'vp{n}int', 0, 30) for n in range(1, 7)
])


# "Industrial": crunchy, grinding, noisy sound design. Thick detuned
# unison, aggressive oscillator mod types (Cross/Unison/VPM) and ring/sync
# on osc 2, harsh filter types (HPF/BPF/Comb) pushed near self-oscillation,
# forced waveshaping distortion, fast/chaotic LFOs, and deep, unrestricted
# Virtual Patch modulation (including Pitch) since pitch chaos is part of
# the aesthetic here rather than something to avoid.
INDUSTRIAL = build([
    checklist('voicemode', ['Single', 'Layer', 'Multi']),
    slider('octave', 5, 11),
    nibble('unisonsw', high_labels=['On'], low_labels=['3', '4']),
    slider('unisondetune', 40, 98),
    slider('unisonspread', 60, 127),
    slider('vibratointensity', 40, 127),
    slider('analog', 15, 31),
    slider('timb1osc1level', 80, 127),
    slider('timb1osc2level', 80, 127),
    slider('noiselevel', 6, 15),
    nibble('osc1wave', high_labels=['Cross', 'Unison', 'VPM'],
           low_labels=['Saw', 'Pulse', 'Formant', 'Noise', 'DWGS']),
    nibble('osc2wave', high_labels=['Ring', 'Sync', 'Ring & Sync'], low_labels=['Saw', 'Square']),
    nibble('filter2tnr', high_labels=['HPF', 'BPF', 'Comb'], low_labels=['Serial', 'Parallel']),
    slider('filter1cutoff', 10, 90),
    slider('filter1res', 90, 127),
    slider('filter1eg1int', 60, 127),
    slider('filter2cutoff', 10, 100),
    slider('filter2res', 90, 127),
    slider('filter2eg1int', 60, 127),
    nibble('waveshapea', high_labels=['Pre-Filter 1', 'Pre-Amp'], low_labels=['Drive', 'Decimator']),
    checklist('waveshapeb', ['HardClip', 'OctSaw', 'SubOsc Squ', 'Level Boost']),
    slider('waveshapedepth', 70, 127),
    slider('punch', 60, 127),
    slider('eg1attack', 0, 30),
    slider('eg2attack', 0, 40),
    slider('eg2sustain', 20, 127),
    checklist('lfo1wavea', ['Square', 'S&H']),
    checklist('lfo1waveb', ['Random']),
    slider('lfo1freq', 60, 127),
    checklist('lfo2wavea', ['Square', 'S&H']),
    checklist('lfo2waveb', ['Random']),
    slider('lfo2freq', 60, 127),
] + [
    slider(f'vp{n}int', 60, 127) for n in range(1, 7)
])


# "Pad / Ambient": lush, slow-evolving, sustained textures. Layered/thick
# unison for width, slow filter+amp attacks (the defining pad trait), long
# releases, gentle low-resonance filtering, and slow LFOs. Virtual Patch
# destinations stay off Pitch/Osc 2 Tune so long sustained chords stay in
# tune, and modulation depth is kept subtle.
PAD = build([
    checklist('voicemode', ['Layer', 'Multi']),
    slider('octave', 6, 9),
    nibble('unisonsw', high_labels=['On'], low_labels=['2', '3', '4']),
    slider('unisondetune', 15, 45),
    slider('unisonspread', 70, 127),
    checklist('voiceassign', ['Poly']),
    slider('vibratointensity', 0, 25),
    slider('analog', 5, 20),
    slider('timb1osc1level', 70, 127),
    slider('timb1osc2level', 70, 127),
    slider('noiselevel', 0, 5),
    nibble('osc1wave', high_labels=['Waveform'], low_labels=['Saw', 'Triangle', 'Sine', 'Formant']),
    nibble('osc2wave', high_labels=['None'], low_labels=['Saw', 'Triangle', 'Sine']),
    nibble('filter2tnr', high_labels=['LPF'], low_labels=['Single', 'Parallel']),
    slider('filter1balance', 40, 100),
    slider('filter1cutoff', 30, 90),
    slider('filter1res', 0, 35),
    slider('filter1eg1int', 0, 40),
    slider('filter1velsens', 0, 50),
    slider('filter2cutoff', 30, 100),
    slider('filter2res', 0, 35),
    slider('filter2eg1int', 0, 40),
    nibble('waveshapea', high_labels=['Pre-Filter 1'], low_labels=['Off']),
    checklist('waveshapeb', ['HardClip']),
    slider('waveshapedepth', 0, 5),
    slider('punch', 0, 30),
    slider('eg1attack', 35, 47),
    slider('eg1decay', 40, 127),
    slider('eg1sustain', 70, 127),
    slider('eg1release', 60, 127),
    slider('eg1velo', 0, 40),
    slider('eg2attack', 50, 127),
    slider('eg2decay', 40, 127),
    slider('eg2sustain', 90, 127),
    slider('eg2release', 70, 127),
    slider('eg2velo', 0, 40),
    checklist('lfo1wavea', ['Triangle']),
    checklist('lfo1waveb', ['Wave']),
    slider('lfo1freq', 0, 25),
    checklist('lfo2wavea', ['Triangle']),
    checklist('lfo2waveb', ['Wave']),
    slider('lfo2freq', 0, 20),
] + [
    checklist(f'vp{n}dst', ['Osc 1 Level', 'Osc 2 Level', 'Filter 1 Balance', 'Filter 1 Cutoff'])
    for n in range(1, 7)
] + [
    slider(f'vp{n}int', 0, 40) for n in range(1, 7)
])


# "Bass": deep, punchy, monophonic low end. Mono voice assign, low octave
# register, dark-ish cutoff with a strong filter envelope for pluck/wub
# character, tight amp envelope (no lingering sustain/release), and
# Virtual Patch destinations limited to filter/osc-ctrl targets for wobble
# without detuning the fundamental.
BASS = build([
    checklist('voicemode', ['Single']),
    slider('octave', 5, 7),
    nibble('unisonsw', high_labels=['On', 'Off'], low_labels=['2']),
    slider('unisondetune', 0, 15),
    slider('unisonspread', 0, 40),
    checklist('voiceassign', ['Mono 1', 'Mono 2']),
    slider('vibratointensity', 0, 10),
    slider('analog', 0, 10),
    slider('timb1osc1level', 100, 127),
    slider('timb1osc2level', 0, 90),
    slider('noiselevel', 0, 3),
    nibble('osc1wave', high_labels=['Waveform'], low_labels=['Saw', 'Pulse', 'Triangle', 'Sine']),
    nibble('osc2wave', high_labels=['None', 'Sync'], low_labels=['Saw', 'Square']),
    nibble('filter2tnr', high_labels=['LPF'], low_labels=['Single']),
    slider('filter1balance', 40, 100),
    slider('filter1cutoff', 10, 70),
    slider('filter1res', 20, 90),
    slider('filter1eg1int', 40, 127),
    slider('filter1velsens', 30, 100),
    slider('filter2cutoff', 10, 70),
    slider('filter2res', 20, 90),
    slider('filter2eg1int', 40, 127),
    nibble('waveshapea', high_labels=['Pre-Filter 1'], low_labels=['Off', 'Drive']),
    checklist('waveshapeb', ['HardClip', 'SubOsc Saw', 'SubOsc Squ']),
    slider('waveshapedepth', 0, 60),
    slider('punch', 60, 127),
    slider('eg1attack', 0, 10),
    slider('eg1decay', 10, 80),
    slider('eg1sustain', 0, 70),
    slider('eg1release', 0, 40),
    slider('eg1velo', 40, 127),
    slider('eg2attack', 0, 5),
    slider('eg2decay', 10, 90),
    slider('eg2sustain', 40, 127),
    slider('eg2release', 0, 40),
    slider('eg2velo', 50, 127),
    checklist('lfo1wavea', ['Triangle', 'Square']),
    checklist('lfo1waveb', ['Wave']),
    slider('lfo1freq', 0, 40),
    checklist('lfo2wavea', ['Triangle']),
    checklist('lfo2waveb', ['Wave']),
    slider('lfo2freq', 0, 40),
] + [
    checklist(f'vp{n}dst', ['Osc 1 Ctrl 1', 'Filter 1 Balance', 'Filter 1 Cutoff'])
    for n in range(1, 7)
] + [
    slider(f'vp{n}int', 0, 60) for n in range(1, 7)
])


# "Percussion / FX Hits": short one-shot transients - drum hits, zaps,
# foley-style sound design. Near-zero sustain on both envelopes (the
# opposite of Pad), strong punch/transient, wide-open oscillator/filter
# variety since every hit is meant to be a distinct sound, and Virtual
# Patch destinations deliberately left unrestricted (Pitch included) since
# a pitch-drop is a classic "zap" characteristic here.
PERCUSSION = build([
    checklist('voicemode', ['Single']),
    slider('octave', 5, 11),
    nibble('unisonsw', high_labels=['Off'], low_labels=['2']),
    slider('unisondetune', 0, 10),
    slider('unisonspread', 0, 50),
    slider('timb1osc1level', 80, 127),
    slider('noiselevel', 0, 15),
    nibble('osc1wave', high_labels=['Waveform', 'Cross', 'VPM'],
           low_labels=['Saw', 'Pulse', 'Formant', 'Noise', 'DWGS']),
    nibble('osc2wave', high_labels=['None', 'Ring', 'Sync'],
           low_labels=['Saw', 'Square', 'Triangle', 'Sine']),
    nibble('filter2tnr', high_labels=['LPF', 'HPF', 'BPF'], low_labels=['Single', 'Individual']),
    slider('filter1cutoff', 20, 127),
    slider('filter1res', 0, 110),
    slider('filter1eg1int', 60, 127),
    slider('filter2cutoff', 20, 127),
    slider('filter2res', 0, 110),
    slider('filter2eg1int', 60, 127),
    nibble('waveshapea', high_labels=['Pre-Filter 1', 'Pre-Amp'], low_labels=['Off', 'Drive', 'Decimator']),
    slider('waveshapedepth', 0, 100),
    slider('punch', 80, 127),
    slider('eg1attack', 0, 5),
    slider('eg1decay', 0, 50),
    slider('eg1sustain', 0, 20),
    slider('eg1release', 0, 30),
    slider('eg2attack', 0, 3),
    slider('eg2decay', 0, 50),
    slider('eg2sustain', 0, 10),
    slider('eg2release', 0, 30),
    slider('eg3attack', 0, 30),
    slider('eg3decay', 0, 60),
    slider('eg3sustain', 0, 20),
    slider('eg3release', 0, 30),
    slider('lfo1freq', 60, 127),
    slider('lfo2freq', 60, 127),
] + [
    slider(f'vp{n}int', 40, 127) for n in range(1, 7)
])


TEMPLATES = {
    'keys.json': KEYS,
    'industrial.json': INDUSTRIAL,
    'pad.json': PAD,
    'bass.json': BASS,
    'percussion.json': PERCUSSION,
}


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    for filename, data in TEMPLATES.items():
        path = os.path.join(OUT_DIR, filename)
        with open(path, 'w') as fh:
            json.dump(data, fh, indent=2, sort_keys=True)
        print(f'{filename}: {len(data)} parameters constrained')
