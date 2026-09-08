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

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

