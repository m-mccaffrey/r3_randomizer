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
    checklist('fx1', ['S.Comp (Stereo Compressor)', 'S.2BndEQ (Stereo 2Band EQ)',
                       'Reverb', 'S.Chorus (Stereo Chorus)', 'Ensemble', 'S.Delay (Stereo Delay)']),
    checklist('fx2', ['S.Comp (Stereo Compressor)', 'S.2BndEQ (Stereo 2Band EQ)',
                       'Reverb', 'S.Chorus (Stereo Chorus)', 'Ensemble', 'S.Delay (Stereo Delay)']),
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
    checklist('fx1', ['Distort (Distortion)', 'S.Dcmtr (Stereo Decimator)', 'S.RingMd (Stereo Ring Modulator)',
                       'Tube Sim (Tube PreAmp Simulator)', 'GrainSft (Grain Shifter)',
                       'S.Flangr (Stereo Flanger/Comb Filter)']),
    checklist('fx2', ['Distort (Distortion)', 'S.Dcmtr (Stereo Decimator)', 'S.RingMd (Stereo Ring Modulator)',
                       'Tube Sim (Tube PreAmp Simulator)', 'GrainSft (Grain Shifter)',
                       'S.Flangr (Stereo Flanger/Comb Filter)']),
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
    checklist('fx1', ['Reverb', 'EarlyRef (Early Reflections)', 'S.Chorus (Stereo Chorus)',
                       'Ensemble', 'S.ModDly (Stereo Modulation Delay)', 'S.Vibart (Stereo Vibrato)']),
    checklist('fx2', ['Reverb', 'EarlyRef (Early Reflections)', 'S.Chorus (Stereo Chorus)',
                       'Ensemble', 'S.ModDly (Stereo Modulation Delay)', 'S.Vibart (Stereo Vibrato)']),
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
    checklist('fx1', ['S.Comp (Stereo Compressor)', 'S.2BndEQ (Stereo 2Band EQ)', 'Distort (Distortion)',
                       'Tube Sim (Tube PreAmp Simulator)', 'S.Dcmtr (Stereo Decimator)']),
    checklist('fx2', ['S.Comp (Stereo Compressor)', 'S.2BndEQ (Stereo 2Band EQ)', 'Distort (Distortion)',
                       'Tube Sim (Tube PreAmp Simulator)', 'S.Dcmtr (Stereo Decimator)']),
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
    checklist('fx1', ['PitchSft (Pitch Shifter)', 'GrainSft (Grain Shifter)', 'S.RingMd (Stereo Ring Modulator)',
                       'S.Dcmtr (Stereo Decimator)', 'S.Gate (Stereo Gate)',
                       'S.Flangr (Stereo Flanger/Comb Filter)']),
    checklist('fx2', ['PitchSft (Pitch Shifter)', 'GrainSft (Grain Shifter)', 'S.RingMd (Stereo Ring Modulator)',
                       'S.Dcmtr (Stereo Decimator)', 'S.Gate (Stereo Gate)',
                       'S.Flangr (Stereo Flanger/Comb Filter)']),
] + [
    slider(f'vp{n}int', 40, 127) for n in range(1, 7)
])


# "Brass": big-band/soul horn stabs. Poly, dual-oscillator for section
# richness, a fast filter "blat" driven by strong velocity sensitivity
# (the core of an expressive brass patch), and vibrato that only shows up
# at the LFO's own rate rather than being baked into the pitch. Space
# comes from a tight early-reflections room rather than a wash of reverb.
BRASS = build([
    checklist('voicemode', ['Single', 'Layer']),
    slider('octave', 7, 9),
    nibble('unisonsw', high_labels=['Off'], low_labels=['2']),
    slider('unisondetune', 0, 10),
    slider('unisonspread', 0, 30),
    checklist('voiceassign', ['Poly']),
    slider('vibratointensity', 20, 70),
    slider('analog', 0, 10),
    slider('timb1osc1level', 100, 127),
    slider('timb1osc2level', 60, 127),
    slider('noiselevel', 0, 3),
    nibble('osc1wave', high_labels=['Waveform'], low_labels=['Saw', 'Pulse']),
    nibble('osc2wave', high_labels=['None', 'Sync'], low_labels=['Saw', 'Square']),
    nibble('filter2tnr', high_labels=['LPF'], low_labels=['Single']),
    slider('filter1balance', 40, 100),
    slider('filter1cutoff', 70, 127),
    slider('filter1res', 0, 40),
    slider('filter1eg1int', 40, 100),
    slider('filter1velsens', 40, 110),
    slider('filter2cutoff', 70, 127),
    slider('filter2res', 0, 40),
    slider('filter2eg1int', 40, 100),
    nibble('waveshapea', high_labels=['Pre-Filter 1'], low_labels=['Off', 'Drive']),
    checklist('waveshapeb', ['HardClip', 'Level Boost']),
    slider('waveshapedepth', 0, 40),
    slider('punch', 60, 127),
    slider('eg1attack', 0, 10),
    slider('eg1decay', 20, 70),
    slider('eg1sustain', 40, 100),
    slider('eg1release', 10, 50),
    slider('eg1velo', 50, 127),
    slider('eg2attack', 0, 8),
    slider('eg2decay', 20, 70),
    slider('eg2sustain', 60, 110),
    slider('eg2release', 15, 60),
    slider('eg2velo', 60, 127),
    checklist('lfo1wavea', ['Triangle']),
    checklist('lfo1waveb', ['Wave']),
    slider('lfo1freq', 30, 70),
    checklist('lfo2wavea', ['Triangle']),
    checklist('lfo2waveb', ['Wave']),
    slider('lfo2freq', 20, 60),
    checklist('fx1', ['S.Comp (Stereo Compressor)', 'S.2BndEQ (Stereo 2Band EQ)',
                       'EarlyRef (Early Reflections)', 'S.Chorus (Stereo Chorus)', 'Reverb']),
    checklist('fx2', ['S.Comp (Stereo Compressor)', 'S.2BndEQ (Stereo 2Band EQ)',
                       'EarlyRef (Early Reflections)', 'S.Chorus (Stereo Chorus)', 'Reverb']),
] + [
    checklist(f'vp{n}dst', ['Osc 1 Ctrl 1', 'Filter 1 Balance', 'Filter 1 Cutoff'])
    for n in range(1, 7)
] + [
    slider(f'vp{n}int', 0, 40) for n in range(1, 7)
])


# "Funk Clav": percussive, plucky electric-clav/keys with an auto-wah
# filter character - fast bandpass envelope "quack," near-zero sustain,
# and a Wah/Comp/Drive/Phaser chain that's the classic funk keys signal
# path. "Pickup" waveshape type is a literal nod to a clav's pickup.
FUNKCLAV = build([
    checklist('voicemode', ['Single']),
    slider('octave', 7, 9),
    nibble('unisonsw', high_labels=['Off'], low_labels=['2']),
    slider('unisondetune', 0, 5),
    slider('unisonspread', 0, 20),
    checklist('voiceassign', ['Poly']),
    slider('vibratointensity', 0, 10),
    slider('analog', 0, 8),
    slider('timb1osc1level', 100, 127),
    slider('timb1osc2level', 30, 90),
    slider('noiselevel', 0, 3),
    nibble('osc1wave', high_labels=['Waveform'], low_labels=['Saw', 'Pulse']),
    nibble('osc2wave', high_labels=['None', 'Ring'], low_labels=['Saw', 'Square']),
    nibble('filter2tnr', high_labels=['BPF', 'LPF'], low_labels=['Single']),
    slider('filter1cutoff', 30, 90),
    slider('filter1res', 40, 100),
    slider('filter1eg1int', 70, 127),
    slider('filter1velsens', 50, 127),
    slider('filter2cutoff', 30, 90),
    slider('filter2res', 40, 100),
    slider('filter2eg1int', 70, 127),
    nibble('waveshapea', high_labels=['Pre-Filter 1'], low_labels=['Off', 'Drive']),
    checklist('waveshapeb', ['HardClip', 'Pickup']),
    slider('waveshapedepth', 0, 50),
    slider('punch', 80, 127),
    slider('eg1attack', 0, 3),
    slider('eg1decay', 10, 50),
    slider('eg1sustain', 0, 30),
    slider('eg1release', 0, 25),
    slider('eg1velo', 60, 127),
    slider('eg2attack', 0, 2),
    slider('eg2decay', 10, 60),
    slider('eg2sustain', 0, 40),
    slider('eg2release', 0, 30),
    slider('eg2velo', 70, 127),
    checklist('lfo1wavea', ['Square']),
    slider('lfo1freq', 0, 40),
    checklist('fx1', ['S.Wah (Stereo Wah)', 'S.Comp (Stereo Compressor)', 'Distort (Distortion)',
                       'S.Phaser (Stereo Phaser)']),
    checklist('fx2', ['S.Wah (Stereo Wah)', 'S.Comp (Stereo Compressor)', 'Distort (Distortion)',
                       'S.Phaser (Stereo Phaser)']),
] + [
    checklist(f'vp{n}dst', ['Filter 1 Balance', 'Filter 1 Cutoff', 'Osc 1 Ctrl 1'])
    for n in range(1, 7)
] + [
    slider(f'vp{n}int', 20, 70) for n in range(1, 7)
])


# "Supersaw Lead": trance/EDM lead. Unison pushed to its max voice count
# and detune/spread for the classic "wall of saws," bright cutoff, and a
# chorus/ensemble/delay/reverb/flanger chain for maximum width - the
# opposite design goal from Keys, which deliberately avoids all of this.
SUPERSAWLEAD = build([
    checklist('voicemode', ['Single', 'Layer']),
    slider('octave', 8, 10),
    nibble('unisonsw', high_labels=['On'], low_labels=['3', '4']),
    slider('unisondetune', 50, 98),
    slider('unisonspread', 90, 127),
    checklist('voiceassign', ['Poly']),
    slider('vibratointensity', 0, 30),
    slider('analog', 5, 20),
    slider('timb1osc1level', 110, 127),
    slider('timb1osc2level', 80, 127),
    slider('noiselevel', 0, 3),
    nibble('osc1wave', high_labels=['Waveform'], low_labels=['Saw']),
    nibble('osc2wave', high_labels=['None', 'Sync'], low_labels=['Saw']),
    nibble('filter2tnr', high_labels=['LPF'], low_labels=['Single']),
    slider('filter1cutoff', 80, 127),
    slider('filter1res', 10, 60),
    slider('filter1eg1int', 20, 80),
    slider('filter1velsens', 30, 100),
    slider('filter2cutoff', 80, 127),
    slider('filter2res', 10, 60),
    nibble('waveshapea', high_labels=['Pre-Filter 1'], low_labels=['Off']),
    checklist('waveshapeb', ['HardClip', 'Level Boost']),
    slider('waveshapedepth', 0, 30),
    slider('punch', 50, 110),
    slider('eg1attack', 0, 10),
    slider('eg1decay', 20, 47),
    slider('eg1sustain', 60, 127),
    slider('eg1release', 30, 127),
    slider('eg2attack', 0, 8),
    slider('eg2decay', 20, 90),
    slider('eg2sustain', 70, 127),
    slider('eg2release', 30, 100),
    checklist('lfo1wavea', ['Triangle']),
    slider('lfo1freq', 10, 50),
    checklist('fx1', ['S.Chorus (Stereo Chorus)', 'Ensemble', 'S.Delay (Stereo Delay)',
                       'Reverb', 'S.Flangr (Stereo Flanger/Comb Filter)']),
    checklist('fx2', ['S.Chorus (Stereo Chorus)', 'Ensemble', 'S.Delay (Stereo Delay)',
                       'Reverb', 'S.Flangr (Stereo Flanger/Comb Filter)']),
] + [
    checklist(f'vp{n}dst', ['Filter 1 Cutoff', 'Osc 1 Level', 'Osc 2 Level'])
    for n in range(1, 7)
] + [
    slider(f'vp{n}int', 0, 40) for n in range(1, 7)
])


# "Acid 303": Chicago acid squelch. Mono, single-oscillator-dominant like
# the real TB-303, resonance pushed near self-oscillation, and a huge
# filter envelope intensity - that's the whole trick behind the "squelch."
# Low sustain lets the filter decay do the sweeping instead of holding.
ACID303 = build([
    checklist('voicemode', ['Single']),
    slider('octave', 6, 8),
    nibble('unisonsw', high_labels=['Off'], low_labels=['2']),
    slider('unisondetune', 0, 5),
    slider('unisonspread', 0, 20),
    checklist('voiceassign', ['Mono 1', 'Mono 2']),
    slider('vibratointensity', 0, 5),
    slider('analog', 0, 15),
    slider('timb1osc1level', 110, 127),
    slider('timb1osc2level', 0, 30),
    slider('noiselevel', 0, 2),
    nibble('osc1wave', high_labels=['Waveform'], low_labels=['Saw', 'Pulse']),
    nibble('osc2wave', high_labels=['None'], low_labels=['Saw']),
    nibble('filter2tnr', high_labels=['LPF'], low_labels=['Single']),
    slider('filter1cutoff', 10, 70),
    slider('filter1res', 80, 127),
    slider('filter1eg1int', 90, 127),
    slider('filter1velsens', 30, 100),
    slider('filter2cutoff', 10, 70),
    slider('filter2res', 80, 127),
    slider('filter2eg1int', 90, 127),
    nibble('waveshapea', high_labels=['Pre-Filter 1'], low_labels=['Off', 'Drive']),
    checklist('waveshapeb', ['HardClip']),
    slider('waveshapedepth', 0, 50),
    slider('punch', 60, 127),
    slider('eg1attack', 0, 3),
    slider('eg1decay', 20, 47),
    slider('eg1sustain', 0, 40),
    slider('eg1release', 0, 30),
    slider('eg1velo', 30, 100),
    slider('eg2attack', 0, 3),
    slider('eg2decay', 20, 100),
    slider('eg2sustain', 40, 100),
    slider('eg2release', 0, 30),
    checklist('lfo1wavea', ['Square']),
    slider('lfo1freq', 0, 30),
    checklist('fx1', ['Distort (Distortion)', 'S.Dcmtr (Stereo Decimator)',
                       'S.Flangr (Stereo Flanger/Comb Filter)', 'Tube Sim (Tube PreAmp Simulator)']),
    checklist('fx2', ['Distort (Distortion)', 'S.Dcmtr (Stereo Decimator)',
                       'S.Flangr (Stereo Flanger/Comb Filter)', 'Tube Sim (Tube PreAmp Simulator)']),
] + [
    checklist(f'vp{n}dst', ['Filter 1 Cutoff', 'Filter 1 Balance'])
    for n in range(1, 7)
] + [
    slider(f'vp{n}int', 20, 80) for n in range(1, 7)
])


# "Reese Growl": jungle/DnB/dubstep sub-bass. Heavily detuned unison saws
# (the classic Reese technique), narrower stereo spread than Supersaw
# Lead since a growl bass wants low-end mono power not width, forced
# waveshaping distortion, and a fast-ish LFO for wobble movement.
REESEGROWL = build([
    checklist('voicemode', ['Single', 'Layer']),
    slider('octave', 5, 7),
    nibble('unisonsw', high_labels=['On'], low_labels=['3', '4']),
    slider('unisondetune', 60, 98),
    slider('unisonspread', 20, 70),
    checklist('voiceassign', ['Mono 1', 'Mono 2']),
    slider('vibratointensity', 0, 15),
    slider('analog', 10, 25),
    slider('timb1osc1level', 110, 127),
    slider('timb1osc2level', 90, 127),
    slider('noiselevel', 0, 5),
    nibble('osc1wave', high_labels=['Waveform', 'Cross'], low_labels=['Saw']),
    nibble('osc2wave', high_labels=['None', 'Ring'], low_labels=['Saw', 'Square']),
    nibble('filter2tnr', high_labels=['LPF', 'BPF'], low_labels=['Single', 'Serial']),
    slider('filter1cutoff', 10, 60),
    slider('filter1res', 40, 110),
    slider('filter1eg1int', 40, 110),
    slider('filter1velsens', 20, 90),
    slider('filter2cutoff', 10, 60),
    slider('filter2res', 40, 110),
    slider('filter2eg1int', 40, 110),
    nibble('waveshapea', high_labels=['Pre-Filter 1', 'Pre-Amp'], low_labels=['Drive', 'Decimator']),
    checklist('waveshapeb', ['HardClip', 'SubOsc Saw', 'SubOsc Squ', 'Level Boost']),
    slider('waveshapedepth', 50, 127),
    slider('punch', 60, 127),
    slider('eg1attack', 0, 15),
    slider('eg1decay', 10, 47),
    slider('eg1sustain', 30, 110),
    slider('eg1release', 0, 50),
    slider('eg2attack', 0, 8),
    slider('eg2decay', 10, 90),
    slider('eg2sustain', 50, 127),
    slider('eg2release', 0, 40),
    checklist('lfo1wavea', ['Square', 'S&H']),
    slider('lfo1freq', 20, 90),
    checklist('fx1', ['Distort (Distortion)', 'S.Dcmtr (Stereo Decimator)',
                       'Tube Sim (Tube PreAmp Simulator)', 'S.RingMd (Stereo Ring Modulator)']),
    checklist('fx2', ['Distort (Distortion)', 'S.Dcmtr (Stereo Decimator)',
                       'Tube Sim (Tube PreAmp Simulator)', 'S.RingMd (Stereo Ring Modulator)']),
] + [
    checklist(f'vp{n}dst', ['Filter 1 Cutoff', 'Filter 1 Balance', 'Osc 1 Ctrl 1'])
    for n in range(1, 7)
] + [
    slider(f'vp{n}int', 40, 110) for n in range(1, 7)
])


# "Chiptune": 8-bit game-console bleeps. High register, pure pulse/saw/
# triangle waves (no analog drift - chips don't wander), the Decimator
# waveshape type for authentic bitcrush, and stepped Square/S&H LFOs for
# that classic chip arpeggio/vibrato feel.
CHIPTUNE = build([
    checklist('voicemode', ['Single']),
    slider('octave', 8, 11),
    nibble('unisonsw', high_labels=['Off'], low_labels=['2']),
    slider('unisondetune', 0, 3),
    slider('unisonspread', 0, 10),
    checklist('voiceassign', ['Mono 1', 'Mono 2', 'Poly']),
    slider('vibratointensity', 0, 20),
    slider('analog', 0, 3),
    slider('timb1osc1level', 110, 127),
    slider('timb1osc2level', 0, 60),
    slider('noiselevel', 0, 15),
    nibble('osc1wave', high_labels=['Waveform'], low_labels=['Pulse', 'Saw', 'Triangle']),
    nibble('osc2wave', high_labels=['None'], low_labels=['Square', 'Triangle']),
    nibble('filter2tnr', high_labels=['LPF'], low_labels=['Single']),
    slider('filter1cutoff', 60, 127),
    slider('filter1res', 0, 30),
    slider('filter1eg1int', 0, 40),
    slider('filter2cutoff', 60, 127),
    slider('filter2res', 0, 30),
    nibble('waveshapea', high_labels=['Pre-Filter 1'], low_labels=['Off', 'Decimator']),
    checklist('waveshapeb', ['HardClip']),
    slider('waveshapedepth', 40, 127),
    slider('punch', 60, 127),
    slider('eg1attack', 0, 2),
    slider('eg1decay', 0, 40),
    slider('eg1sustain', 0, 127),
    slider('eg1release', 0, 20),
    slider('eg2attack', 0, 2),
    slider('eg2decay', 0, 40),
    slider('eg2sustain', 0, 127),
    slider('eg2release', 0, 20),
    checklist('lfo1wavea', ['Square', 'S&H']),
    slider('lfo1freq', 40, 127),
    checklist('fx1', ['S.Dcmtr (Stereo Decimator)', 'S.Gate (Stereo Gate)', 'S.Comp (Stereo Compressor)']),
    checklist('fx2', ['S.Dcmtr (Stereo Decimator)', 'S.Gate (Stereo Gate)', 'S.Comp (Stereo Compressor)']),
] + [
    checklist(f'vp{n}dst', ['Osc 1 Level', 'Osc 2 Level', 'Noise Level', 'Filter 1 Cutoff'])
    for n in range(1, 7)
] + [
    slider(f'vp{n}int', 20, 90) for n in range(1, 7)
])


# "Vaporwave": lo-fi, detuned, nostalgic. Analog Tuning maxed out for the
# characteristic wavery pitch drift, a muffled/warm cutoff instead of a
# bright one, slow envelopes, and a TapeEcho/Chorus/Ensemble/Reverb/
# Decimator chain - the quintessential washed-out, chorused-tape sound.
VAPORWAVE = build([
    checklist('voicemode', ['Layer', 'Multi']),
    slider('octave', 6, 9),
    nibble('unisonsw', high_labels=['On'], low_labels=['2', '3']),
    slider('unisondetune', 20, 60),
    slider('unisonspread', 60, 127),
    checklist('voiceassign', ['Poly']),
    slider('vibratointensity', 10, 50),
    slider('analog', 15, 31),
    slider('timb1osc1level', 70, 127),
    slider('timb1osc2level', 70, 127),
    slider('noiselevel', 0, 8),
    nibble('osc1wave', high_labels=['Waveform'], low_labels=['Saw', 'Triangle', 'Sine']),
    nibble('osc2wave', high_labels=['None'], low_labels=['Saw', 'Triangle', 'Sine']),
    nibble('filter2tnr', high_labels=['LPF'], low_labels=['Single', 'Parallel']),
    slider('filter1cutoff', 30, 90),
    slider('filter1res', 0, 40),
    slider('filter1eg1int', 0, 40),
    slider('filter2cutoff', 30, 90),
    nibble('waveshapea', high_labels=['Pre-Filter 1'], low_labels=['Off']),
    checklist('waveshapeb', ['HardClip']),
    slider('waveshapedepth', 0, 20),
    slider('punch', 0, 30),
    slider('eg1attack', 10, 47),
    slider('eg1decay', 30, 127),
    slider('eg1sustain', 60, 127),
    slider('eg1release', 50, 127),
    slider('eg2attack', 20, 127),
    slider('eg2decay', 30, 127),
    slider('eg2sustain', 70, 127),
    slider('eg2release', 60, 127),
    checklist('lfo1wavea', ['Triangle', 'S&H']),
    slider('lfo1freq', 0, 15),
    checklist('fx1', ['TapeEcho', 'S.Chorus (Stereo Chorus)', 'Ensemble', 'Reverb',
                       'S.Dcmtr (Stereo Decimator)']),
    checklist('fx2', ['TapeEcho', 'S.Chorus (Stereo Chorus)', 'Ensemble', 'Reverb',
                       'S.Dcmtr (Stereo Decimator)']),
] + [
    checklist(f'vp{n}dst', ['Osc 1 Level', 'Osc 2 Level', 'Filter 1 Cutoff'])
    for n in range(1, 7)
] + [
    slider(f'vp{n}int', 0, 50) for n in range(1, 7)
])


# "Drone": slow, infinite, evolving texture. Maxed-out attack/sustain/
# release on both envelopes so notes swell in and never really leave, and
# LFOs crawling at 0-10 so movement happens over minutes, not seconds.
# Deliberately near-zero punch/filter-envelope intensity: a drone isn't
# "played" percussively, it just continuously is.
DRONE = build([
    checklist('voicemode', ['Layer', 'Multi']),
    slider('octave', 5, 9),
    nibble('unisonsw', high_labels=['On'], low_labels=['3', '4']),
    slider('unisondetune', 30, 98),
    slider('unisonspread', 80, 127),
    slider('vibratointensity', 0, 40),
    slider('analog', 10, 31),
    slider('timb1osc1level', 70, 127),
    slider('timb1osc2level', 70, 127),
    slider('noiselevel', 0, 10),
    nibble('osc1wave', high_labels=['Waveform', 'Unison'], low_labels=['Saw', 'Triangle', 'Sine', 'Formant']),
    nibble('osc2wave', high_labels=['None', 'Ring'], low_labels=['Saw', 'Triangle', 'Sine']),
    nibble('filter2tnr', high_labels=['LPF', 'BPF'], low_labels=['Single', 'Parallel']),
    slider('filter1cutoff', 10, 80),
    slider('filter1res', 0, 60),
    slider('filter1eg1int', 0, 30),
    slider('filter2cutoff', 10, 80),
    slider('filter2res', 0, 60),
    nibble('waveshapea', high_labels=['Pre-Filter 1'], low_labels=['Off', 'Drive']),
    checklist('waveshapeb', ['HardClip']),
    slider('waveshapedepth', 0, 40),
    slider('punch', 0, 10),
    slider('eg1attack', 40, 47),
    slider('eg1decay', 100, 127),
    slider('eg1sustain', 110, 127),
    slider('eg1release', 110, 127),
    slider('eg2attack', 100, 127),
    slider('eg2decay', 100, 127),
    slider('eg2sustain', 120, 127),
    slider('eg2release', 110, 127),
    checklist('lfo1wavea', ['Triangle', 'S&H']),
    slider('lfo1freq', 0, 10),
    checklist('lfo2wavea', ['Triangle']),
    slider('lfo2freq', 0, 10),
    checklist('fx1', ['Reverb', 'EarlyRef (Early Reflections)', 'S.ModDly (Stereo Modulation Delay)',
                       'S.Vibart (Stereo Vibrato)', 'Ensemble']),
    checklist('fx2', ['Reverb', 'EarlyRef (Early Reflections)', 'S.ModDly (Stereo Modulation Delay)',
                       'S.Vibart (Stereo Vibrato)', 'Ensemble']),
] + [
    checklist(f'vp{n}dst', ['Osc 1 Level', 'Osc 2 Level', 'Filter 1 Cutoff', 'Filter 1 Balance'])
    for n in range(1, 7)
] + [
    slider(f'vp{n}int', 0, 60) for n in range(1, 7)
])


# "Horror Drone": dissonant, unsettling, cinematic dread. Like Drone, but
# every choice pushed toward unease instead of lushness: harsher detune
# for real dissonant beating, inharmonic osc mod types (Cross/Unison/VPM)
# and vocal-ish Formant/Noise/DWGS waves, unstable vibrato, jerky S&H
# modulation, and Virtual Patch destinations deliberately left
# unrestricted - including Pitch, since unstable pitch drift is the point.
HORRORDRONE = build([
    checklist('voicemode', ['Layer', 'Multi', 'Split']),
    slider('octave', 5, 11),
    nibble('unisonsw', high_labels=['On'], low_labels=['3', '4']),
    slider('unisondetune', 60, 98),
    slider('unisonspread', 60, 127),
    slider('vibratointensity', 40, 127),
    slider('analog', 20, 31),
    slider('timb1osc1level', 70, 127),
    slider('timb1osc2level', 70, 127),
    slider('noiselevel', 5, 15),
    nibble('osc1wave', high_labels=['Cross', 'Unison', 'VPM'], low_labels=['Formant', 'Noise', 'DWGS']),
    nibble('osc2wave', high_labels=['Ring', 'Sync'], low_labels=['Saw', 'Sine']),
    nibble('filter2tnr', high_labels=['HPF', 'BPF', 'Comb'], low_labels=['Serial', 'Parallel']),
    slider('filter1cutoff', 10, 70),
    slider('filter1res', 50, 120),
    slider('filter1eg1int', 20, 100),
    slider('filter2cutoff', 10, 70),
    slider('filter2res', 50, 120),
    nibble('waveshapea', high_labels=['Pre-Filter 1', 'Pre-Amp'], low_labels=['Drive']),
    checklist('waveshapeb', ['HardClip', 'MultiSin']),
    slider('waveshapedepth', 30, 100),
    slider('punch', 0, 30),
    slider('eg1attack', 30, 47),
    slider('eg1decay', 60, 127),
    slider('eg1sustain', 80, 127),
    slider('eg1release', 90, 127),
    slider('eg2attack', 60, 127),
    slider('eg2decay', 60, 127),
    slider('eg2sustain', 90, 127),
    slider('eg2release', 90, 127),
    checklist('lfo1wavea', ['S&H', 'Square']),
    slider('lfo1freq', 0, 30),
    checklist('lfo2wavea', ['S&H']),
    slider('lfo2freq', 0, 30),
    checklist('fx1', ['S.RingMd (Stereo Ring Modulator)', 'Reverb', 'S.Phaser (Stereo Phaser)',
                       'EarlyRef (Early Reflections)', 'S.Vibart (Stereo Vibrato)']),
    checklist('fx2', ['S.RingMd (Stereo Ring Modulator)', 'Reverb', 'S.Phaser (Stereo Phaser)',
                       'EarlyRef (Early Reflections)', 'S.Vibart (Stereo Vibrato)']),
] + [
    slider(f'vp{n}int', 40, 120) for n in range(1, 7)
])


# "Techno Stab": rave/techno chord stab. Layered, detuned unison for
# density, filter envelope sweeping down from bright to dark (the classic
# stab shape), near-zero sustain so it's a hit rather than a pad, and a
# drive/flanger/phaser/delay/reverb chain for that dated-but-glorious
# rave-stab processing.
TECHNOSTAB = build([
    checklist('voicemode', ['Layer', 'Multi']),
    slider('octave', 7, 9),
    nibble('unisonsw', high_labels=['On'], low_labels=['2', '3']),
    slider('unisondetune', 30, 70),
    slider('unisonspread', 50, 110),
    checklist('voiceassign', ['Poly']),
    slider('vibratointensity', 0, 20),
    slider('analog', 5, 20),
    slider('timb1osc1level', 100, 127),
    slider('timb1osc2level', 80, 127),
    slider('noiselevel', 0, 5),
    nibble('osc1wave', high_labels=['Waveform', 'Cross'], low_labels=['Saw', 'Pulse']),
    nibble('osc2wave', high_labels=['None', 'Sync'], low_labels=['Saw', 'Square']),
    nibble('filter2tnr', high_labels=['LPF', 'BPF'], low_labels=['Single', 'Serial']),
    slider('filter1cutoff', 60, 127),
    slider('filter1res', 40, 110),
    slider('filter1eg1int', 60, 127),
    slider('filter1velsens', 40, 110),
    slider('filter2cutoff', 60, 127),
    slider('filter2res', 40, 110),
    slider('filter2eg1int', 60, 127),
    nibble('waveshapea', high_labels=['Pre-Filter 1'], low_labels=['Off', 'Drive']),
    checklist('waveshapeb', ['HardClip', 'Level Boost']),
    slider('waveshapedepth', 20, 80),
    slider('punch', 90, 127),
    slider('eg1attack', 0, 2),
    slider('eg1decay', 20, 47),
    slider('eg1sustain', 0, 40),
    slider('eg1release', 0, 30),
    slider('eg1velo', 50, 127),
    slider('eg2attack', 0, 2),
    slider('eg2decay', 20, 90),
    slider('eg2sustain', 0, 50),
    slider('eg2release', 0, 30),
    checklist('lfo1wavea', ['Triangle']),
    slider('lfo1freq', 20, 70),
    checklist('fx1', ['Distort (Distortion)', 'S.Flangr (Stereo Flanger/Comb Filter)',
                       'S.Phaser (Stereo Phaser)', 'S.Delay (Stereo Delay)', 'Reverb']),
    checklist('fx2', ['Distort (Distortion)', 'S.Flangr (Stereo Flanger/Comb Filter)',
                       'S.Phaser (Stereo Phaser)', 'S.Delay (Stereo Delay)', 'Reverb']),
] + [
    checklist(f'vp{n}dst', ['Filter 1 Cutoff', 'Filter 1 Balance', 'Osc 1 Level'])
    for n in range(1, 7)
] + [
    slider(f'vp{n}int', 20, 80) for n in range(1, 7)
])


# "Noise Wall": maximal harsh noise, Pharmakon/power-electronics
# territory. Every parameter that has a "harsh" direction is pushed
# there: max unison voices and detune, max analog drift, max noise
# level, inharmonic/ring-modulated oscillators, filters screaming at the
# edge of self-oscillation, forced heavy distortion, and envelopes that
# snap to full volume and just stay there - a wall, not a note. Virtual
# Patch routing (including destination and source) is left completely
# open, same as Industrial, because unpredictable chaos is the aesthetic.
NOISEWALL = build([
    checklist('voicemode', ['Layer', 'Multi']),
    slider('octave', 5, 11),
    nibble('unisonsw', high_labels=['On'], low_labels=['4']),
    slider('unisondetune', 80, 98),
    slider('unisonspread', 100, 127),
    slider('vibratointensity', 100, 127),
    slider('analog', 25, 31),
    slider('timb1osc1level', 115, 127),
    slider('timb1osc2level', 115, 127),
    slider('noiselevel', 10, 15),
    nibble('osc1wave', high_labels=['Cross', 'Unison', 'VPM'], low_labels=['Noise', 'Formant', 'DWGS']),
    nibble('osc2wave', high_labels=['Ring', 'Sync', 'Ring & Sync'], low_labels=['Saw', 'Square']),
    nibble('filter2tnr', high_labels=['HPF', 'BPF', 'Comb'], low_labels=['Parallel', 'Individual']),
    slider('filter1cutoff', 0, 127),
    slider('filter1res', 110, 127),
    slider('filter1eg1int', 100, 127),
    slider('filter2cutoff', 0, 127),
    slider('filter2res', 110, 127),
    slider('filter2eg1int', 100, 127),
    nibble('waveshapea', high_labels=['Pre-Filter 1', 'Pre-Amp'], low_labels=['Drive', 'Decimator']),
    checklist('waveshapeb', ['HardClip', 'Level Boost', 'MultiSin', 'SubOsc Squ']),
    slider('waveshapedepth', 110, 127),
    slider('punch', 110, 127),
    slider('eg1attack', 0, 47),
    slider('eg1decay', 100, 127),
    slider('eg1sustain', 110, 127),
    slider('eg1release', 100, 127),
    slider('eg2attack', 0, 10),
    slider('eg2decay', 100, 127),
    slider('eg2sustain', 110, 127),
    slider('eg2release', 100, 127),
    checklist('lfo1wavea', ['S&H', 'Square']),
    slider('lfo1freq', 100, 127),
    checklist('lfo2wavea', ['S&H']),
    slider('lfo2freq', 100, 127),
    checklist('fx1', ['Distort (Distortion)', 'S.Dcmtr (Stereo Decimator)', 'S.RingMd (Stereo Ring Modulator)',
                       'Tube Sim (Tube PreAmp Simulator)', 'GrainSft (Grain Shifter)']),
    checklist('fx2', ['Distort (Distortion)', 'S.Dcmtr (Stereo Decimator)', 'S.RingMd (Stereo Ring Modulator)',
                       'Tube Sim (Tube PreAmp Simulator)', 'GrainSft (Grain Shifter)']),
] + [
    slider(f'vp{n}int', 100, 127) for n in range(1, 7)
])


TEMPLATES = {
    'keys.json': KEYS,
    'industrial.json': INDUSTRIAL,
    'pad.json': PAD,
    'bass.json': BASS,
    'percussion.json': PERCUSSION,
    'brass.json': BRASS,
    'funkclav.json': FUNKCLAV,
    'supersawlead.json': SUPERSAWLEAD,
    'acid303.json': ACID303,
    'reesegrowl.json': REESEGROWL,
    'chiptune.json': CHIPTUNE,
    'vaporwave.json': VAPORWAVE,
    'drone.json': DRONE,
    'horrordrone.json': HORRORDRONE,
    'technostab.json': TECHNOSTAB,
    'noisewall.json': NOISEWALL,
}


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    for filename, data in TEMPLATES.items():
        path = os.path.join(OUT_DIR, filename)
        with open(path, 'w') as fh:
            json.dump(data, fh, indent=2, sort_keys=True)
        print(f'{filename}: {len(data)} parameters constrained')
