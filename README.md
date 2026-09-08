# Korg R3 Randomizer
A Python utility to generate random patches for the Korg R3 Synthesizer
## Getting started
Clone or download this repository.
Run r3.pyw
## Use
### Basic
The simplest case is to randomize all available parameters within all of their possibile settings. To do this, simply click the Randomize button. A .r3l file will be generated that can be loaded into the R3 Sound Editor software.
### Custom
All available parameters can have the limits of their settings reconfigured. Do this by moving sliders to limit the range of parameters like Bend Range and Octave, or by enabling and disabling checkboxes associated with parameters like Voice Mode. With the Randomize button, "Slider" parameters will only be randomly selected between the minimum and maximum sliders, and "Checkbox" parameters will only be selected from the enabled options.

### Saving and loading settings
Once you've configured the sliders and checkboxes the way you like, use File > Save Settings to write them to a JSON file (`r3_settings.json` by default). Use File > Load Settings to bring a saved configuration back. If `r3_settings.json` exists in the folder you ran the app from, it's loaded automatically on startup.

### Templates
The Templates menu loads a set of built-in presets (bundled under `templates/`) that bias the randomizer toward a particular kind of sound, instead of every parameter being wide open:

Roughly ordered mellow to extreme:

- **Keys** — melodic and relatively in-tune. Polyphonic, no unison detune, clean tonal oscillator waveforms, gentle effects (compressor, EQ, reverb, chorus, ensemble, delay), and modulation routing kept away from pitch so patches stay playable instead of drifting out of tune.
- **Brass** — big-band/soul horn stabs. Dual-oscillator section richness, a fast filter "blat" driven by strong velocity sensitivity, real vibrato, and a tight early-reflections room instead of a wash of reverb.
- **Funk Clav** — percussive electric-clav/keys. Fast bandpass filter envelope for that classic "quack," near-zero sustain, and a Wah/Comp/Drive/Phaser chain lifted straight from the funk keys playbook.
- **Supersaw Lead** — trance/EDM lead. Unison pushed to its max voice count, detune, and spread for the "wall of saws," plus chorus/ensemble/delay/reverb/flanger for maximum width.
- **Pad / Ambient** — lush, slow-evolving textures. Layered unison for width, slow filter/amp attacks, long releases, gentle low-resonance filtering, and spatial effects (reverb, early reflections, chorus, ensemble, modulation delay, vibrato).
- **Vaporwave** — lo-fi, detuned, nostalgic. Analog Tuning maxed for that wavery pitch drift, a muffled/warm cutoff, and a tape echo/chorus/ensemble/reverb/decimator chain for the washed-out chorused-tape sound.
- **Bass** — deep, punchy, monophonic low end. Mono voice assign, low register, a strong filter envelope for pluck/wobble character, a tight amp envelope, and shaping effects (compressor, EQ, distortion, tube preamp, decimator).
- **Reese Growl** — jungle/DnB/dubstep sub-bass. Heavily detuned unison saws (the classic Reese technique), forced waveshaping distortion, and filter/decimator/ring-mod grit.
- **Acid 303** — Chicago acid squelch. Mono, resonance pushed near self-oscillation, and a huge filter envelope intensity — that's the whole trick behind the "squelch."
- **Techno Stab** — rave/techno chord stab. Filter envelope sweeping bright-to-dark, near-zero sustain so it's a hit rather than a pad, and drive/flanger/phaser/delay/reverb for that dated-but-glorious rave processing.
- **Percussion / FX Hits** — short one-shot transients: drum hits, zaps, foley-style sound design. Near-zero sustain, strong transient punch, wide oscillator/filter variety, dramatic effects (pitch shifter, grain shifter, ring modulator, decimator, gate, flanger), and pitch modulation left wide open for classic "zap" pitch-drops.
- **Chiptune** — 8-bit game-console bleeps. High register, pure pulse/saw/triangle waves, no analog drift, the Decimator waveshape type for authentic bitcrush, and stepped LFOs for that classic chip arpeggio feel.
- **Drone** — slow, infinite, evolving texture. Maxed-out attack/sustain/release so notes swell in and never really leave, with LFOs crawling so movement happens over minutes, not seconds.
- **Industrial** — crunchy, grinding, noisy sound design. Thick detuned unison, aggressive oscillator cross/ring/sync modulation, harsh filter types pushed toward self-oscillation, forced distortion, harsh effects (distortion, decimator, ring modulator, tube preamp, grain shifter, flanger), and deep, unrestricted modulation (pitch chaos included).
- **Horror Drone** — dissonant, unsettling, cinematic dread. Like Drone, but pushed toward unease instead of lushness: harsher detune for real dissonant beating, inharmonic/vocal-ish oscillator waves, unstable vibrato, jerky sample-and-hold modulation, and pitch left open to drift.
- **Noise Wall** — maximal harsh noise, power-electronics territory. Every parameter that has a "harsh" direction is pushed there: max unison/detune/drift/noise, filters screaming at the edge of self-oscillation, forced heavy distortion, and envelopes that snap to full volume and just stay there — a wall, not a note.

Picking a template just loads its settings into the GUI like any other saved file — you can still fine-tune sliders and checkboxes afterward before hitting Randomize. Since a template only constrains parameters it has an opinion about, anything it doesn't mention keeps its current (or default) range.

Templates are generated by `tools/build_templates.py`, which defines each preset using the same human-readable option names shown in the GUI (e.g. `'Saw'`, `'LPF'`, `'Single'`) rather than raw byte values, and checks them against the real parameter definitions before writing the JSON. To tweak a template, edit its entry in that script and re-run `python3 tools/build_templates.py`.

The 29 Effect checkbox options are named after the official Korg R3 Effect Guide (S.Comp, Distort, Reverb, S.Chorus, and so on — see `r3patch.py`'s `fx_type_names` for the full list and the reasoning behind the mapping). The guide documents 30 selectable effect types, one more than the 29 raw values available to the `fx1`/`fx2` byte field in the patch format, so the mapping (which of the 30 gets left out) is inferred from the count matching up rather than read off Korg's raw MIDI implementation chart. It's easy to spot-check: pick a single effect, randomize, and confirm the name in the actual R3 Sound Editor. If it's off by one, flag it and the mapping (and templates) can be corrected in one place.

The DWGS (`DWGS 0`-`63`) checkbox options are still numbered rather than named — we don't have a source for the R3's DWGS waveform list, so `osc1dwgs` is left unconstrained in every template.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

