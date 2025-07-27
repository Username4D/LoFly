from scipy.io import wavfile
import vita
import numpy
import os
SAMPLE_RATE = 44_100

bpm = 120.0
note_dur = 1.0
render_dur = 1.0
pitch = 36  # integer
velocity = 0.7  # [0.0 to 1.0]

synth = vita.Synth()
# The initial preset is loaded by default.
synth2 = vita.Synth()
synth2.set_bpm(bpm)
synth.set_bpm(bpm)

# Let's make a custom modulation using
# the available modulation sources and destinations.
# These lists are constant.
roots = os.path.dirname(os.path.abspath(__file__))
# "lfo_1" is a potential source,
# and "filter_1_cutoff" is a potential destination.
assert synth.connect_modulation("lfo_1", "filter_1_cutoff")
synth2.load_preset(os.path.join(roots, 'audio/zero.vital'))

controls = synth.get_controls()
controls["modulation_1_amount"].set(1.0)
controls["filter_1_on"].set(1.0)
val = controls["filter_1_on"].value()
controls["lfo_1_tempo"].set(vita.constants.SyncedFrequency.k1_16)

# Use normalized parameter control (0-1 range, VST-style)
controls["filter_1_cutoff"].set_normalized(0.5)  # Set knob to 50%


# Get parameter details and display text
info = synth.get_control_details("delay_style")


# Render audio to numpy array shaped (2, NUM_SAMPLES)
audio2 = synth.render(pitch, velocity, note_dur, render_dur)
audio3 = synth2.render(1,1,1,1)
audio = synth.render(pitch+12, 0, 1,1)                    
out = numpy.hstack([audio,audio3, audio2])
wavfile.write("generated_preset.wav", SAMPLE_RATE, out.T)

# Dump current state to JSON text
preset_path = "generated_preset.vital"

json_text = synth.to_json()

with open(preset_path, "w") as f:    
    f.write(json_text)

# Load JSON text
with open(preset_path, "r") as f:
    json_text = f.read()

assert synth.load_json(json_text)

# Or load directly from file
assert synth.load_preset(preset_path)

# Load the initial preset, which also clears modulations
synth.load_init_preset()
# Or just clear modulations.
synth.clear_modulations()