from scipy.io import wavfile
import vita
import random
import numpy
import os, os.path
import cfg # Use the cfg.py file to configure LoFly generation
import print_agent # Used to store all CLI printing stuff

SAMPLE_RATE = 44_100

print_agent.opening()

bpm = 80.0
note_dur = 1.0
render_dur = 4.0
pitch = 36  # integer
velocity = 0.7  # [0.0 to 1.0]

roots = os.path.dirname(os.path.abspath(__file__))

keys = vita.Synth()
keys_presets = os.listdir(os.path.join(roots, 'audio/keys'))
keys_preset = os.path.join(os.path.join(roots, 'audio/keys'), random.choice(keys_presets))
keys.load_preset(keys_preset)
keys.set_bpm(bpm)

lead = vita.Synth()
lead_presets = os.listdir(os.path.join(roots, 'audio/leads'))
lead_preset = os.path.join(os.path.join(roots, 'audio/leads'), random.choice(lead_presets))
lead.load_preset(lead_preset)
lead.set_bpm(bpm)

bass = vita.Synth()
bass_presets = os.listdir(os.path.join(roots, 'audio/basses'))
bass_preset = os.path.join(os.path.join(roots, 'audio/basses'), random.choice(bass_presets))
bass.load_preset(bass_preset)
bass.set_bpm(bpm)

pad = vita.Synth()
pad_presets = os.listdir(os.path.join(roots, 'audio/pads'))
pad_preset = os.path.join(os.path.join(roots, 'audio/pads'), random.choice(pad_presets))
pad.load_preset(pad_preset)
pad.set_bpm(bpm)

void = vita.Synth()
void.load_preset(os.path.join(roots, 'audio/zero.vital'))

if len(keys_presets) != 0 and len(lead_presets) != 0 and len(bass_presets) != 0 and len(pad_presets) != 0:
    print_agent.loaded_presets(keys_preset, lead_preset, bass_preset, pad_preset)
else:
    print('ERROR - MISSING PRESETS: Please add atleast one Preset for every Instrument type(keys, leads, basses, pads)')
    os._exit(0)

pad.load_preset(os.path.join(roots, 'audio/pads/synth.vital'))

def generate_midi():
    root_note = random.randint(0, 11)
    scale_type = random.randint(0,1) # currently only implementation for generic major/minor
    print_agent.scale(scale_type)
    global notes
    notes = numpy.array([])
    match scale_type:
        case 0: #Major
            notes = [0,2,4,5,7,9,11]
        case 1: #Minor
            notes = [0,2,3,5,7,8,10]
    
    notes = numpy.add(notes, root_note)
    notes = numpy.append(notes, numpy.add(notes, 12))
    notes = numpy.append(notes, numpy.add(notes, 24))
    bass_notes = [random.randint(0,6),random.randint(0,6),random.randint(0,6),random.randint(0,6)]
    bass_notes_out = [notes[bass_notes[0]],notes[bass_notes[1]],notes[bass_notes[2]],notes[bass_notes[3]]]

    def create_chord(note):
        chord_type = random.randint(0,1)
        chord = []
        match chord_type:
            case 0:
                chord = [note, note + 2 + 12, note + 4]
            case 1:
                chord = [note, note + 2 + 12, note + 4, note + 6]
        return chord
    
    chords = [create_chord(bass_notes[0]),create_chord(bass_notes[1]),create_chord(bass_notes[2]),create_chord(bass_notes[3])]

    def key_chord(chord):
        if len(chord) == 4:
            return [notes[chord[0]],notes[chord[1]],notes[chord[2]],notes[chord[3]]]
        else:
            return [notes[chord[0]],notes[chord[1]],notes[chord[2]]]
    
    chords_out = [key_chord(chords[0]),key_chord(chords[1]),key_chord(chords[2]),key_chord(chords[3])]

    global midi_chords
    midi_chords = chords_out
    global midi_bassline
    midi_bassline = bass_notes_out
    print('- Composed Track            -')

def render_stems():
    # render pad stem
    print('- Rendering Stems           -')
    def render_multinote(inp, predelay): 
        out = pad.render(inp[0] + 36, velocity, 4, 8)
        voidstart = void.render(0,0,1,predelay * 4)
        voidend = void.render(0,0,1, 16 - predelay * 4)
        for n in range(1, len(inp)):
            i = inp[n]
            out = numpy.concatenate((out, pad.render(i + 36, velocity, 4, 8))) 
            voidstart = numpy.concatenate([voidstart, void.render(0,0,1,predelay * 4),])
            voidend = numpy.concatenate([voidend, void.render(0,0,1, 16 - predelay * 4)])
        if len(inp) == 3:
            out = numpy.concatenate((out, void.render(0 + 36, velocity, 4, 8))) 
            voidstart = numpy.concatenate([voidstart, void.render(0,0,1,predelay * 4),])
            voidend = numpy.concatenate([voidend, void.render(0,0,1, 16 - predelay * 4)])
        return numpy.hstack([voidstart, out, voidend])
    audio_pad = numpy.add(numpy.add(render_multinote(midi_chords[0], 0), render_multinote(midi_chords[1], 1)), numpy.add(render_multinote(midi_chords[2], 2), render_multinote(midi_chords[3], 3)))
    audio_pad *= cfg.pad_volume
    wavfile.write('stems_pad.wav', SAMPLE_RATE, audio_pad.T)
    print('')
    print('Pad: completed')
    # render bass stem

    def render_bass(inp):
        def get_bass(n, d):
            return numpy.hstack((void.render(1,1,0,4 * d), bass.render(n + 24,100,4,8), void.render(1,1,4, 16 - d * 4)))
        return numpy.add(numpy.add(get_bass(inp[0], 0), get_bass(inp[1], 1)), numpy.add(get_bass(inp[2], 2), get_bass(inp[3], 3)))

    audio_bass = render_bass(midi_bassline)
    audio_bass *= cfg.bass_volume

    wavfile.write('stems_bass.wav', SAMPLE_RATE, audio_bass.T)

    audio_bass = numpy.vstack((void.render(1,1,0,24), audio_bass))
    audio_bass = numpy.vstack((void.render(1,1,0,24), audio_bass))
    audio_bass = numpy.vstack((void.render(1,1,0,24), audio_bass))
    print('Bass: completed')
    # render keys stem

    def render_multinote(inp, predelay): 
        out = keys.render(inp[0] + 24, velocity, 4, 8)
        
        voidend = void.render(0,0,1, 16 - predelay * 4)
        for n in range(1, len(inp)):
            start = random.uniform(0, cfg.max_random_start_time)
            i = inp[n]
            out = numpy.concatenate((out, keys.render(i + 24, velocity, 4, 8))) 
            voidstart = numpy.concatenate([voidstart, void.render(0,0,1,predelay * 4 + start),])
            voidend = numpy.concatenate([voidend, void.render(0,0,1, 16 - predelay * 4 - start)])
        if len(inp) == 3:
            out = numpy.concatenate((out, void.render(0 + 24, velocity, 4, 8))) 
            voidstart = numpy.concatenate([voidstart, void.render(0,0,1,predelay * 4),])
            voidend = numpy.concatenate([voidend, void.render(0,0,1, 16 - predelay * 4)])
        return numpy.hstack([voidstart, out, voidend])
    audio_keys = numpy.add(numpy.add(render_multinote(midi_chords[0], 0), render_multinote(midi_chords[1], 1)), numpy.add(render_multinote(midi_chords[2], 2), render_multinote(midi_chords[3], 3)))
    audio_keys *= cfg.keys_volume
    wavfile.write('stems_keys.wav', SAMPLE_RATE, audio_keys.T)
    print('Keys: completed')
    def render_lead(inp):
        def get_lead(n, d):
            return numpy.hstack((void.render(1,1,0,4 * d), lead.render(n + 48,100,4,8), void.render(1,1,4, 16 - d * 4)))
        return numpy.add(numpy.add(get_lead(inp[0], 0), get_lead(inp[1], 1)), numpy.add(get_lead(inp[2], 2), get_lead(inp[3], 3)))

    audio_lead = render_lead(midi_bassline)
    audio_lead *= cfg.lead_volume
    audio_lead = numpy.vstack((void.render(1,1,0,24), audio_lead))
    audio_lead = numpy.vstack((void.render(1,1,0,24), audio_lead))
    audio_lead = numpy.vstack((void.render(1,1,0,24), audio_lead))

    wavfile.write('stems_lead.wav', SAMPLE_RATE, audio_lead.T)
    print('Lead: completed')

    audio_full = numpy.add(audio_bass, audio_lead)
    audio_full = numpy.add(audio_full, audio_keys)
    audio_full = numpy.add(audio_full, audio_pad)
    wavfile.write("full.wav", SAMPLE_RATE, audio_full.T)
    print('Merged: completed')
generate_midi()


render_stems()

print_agent.exit()
