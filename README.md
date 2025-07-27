# LoFly

Randomly generated LoFi samples using Python and the Vital Synthesizer

This Project is still in the works

## Overview:

This Project offers a command-line tool for creating randomly generated lofi samples. It does this by choosing random presets for the Vital synth and running them through randomly generated melodies, rendering and merging the results to a sample. The tool is configurable using the cfg.py file. Presets can/should be added by the user, but a few presets come with the tool

## Requirements

- vita: python bindings for vital 
- numpy: maths
- pydub: merging wav files
- scipy.io: writing wav files

## Config

The config file currently can customize the leveling of the different stems and some randomization options, but is still a big wip

## Bugs

There currently is a Problem merging the Full version and one error that can arise during randomisation