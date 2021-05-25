import random as r
import pyaudio
import numpy as np

FREQ_TABLE = {}
with open('freq_table.txt','r') as f:
    lines = f.readlines()
    for line in lines:
        note, freq, _ = line.split()
        if len(note) > 3:
            note = note.split('/')[1]
        FREQ_TABLE[note] = float(freq)

# r.seed(1)

KEYS = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
MAJOR_SCALE = ('Major', [0, 2, 4, 5, 7, 9, 11])
MINOR_SCALE = ('Minor', [0, 2, 3, 5, 7, 8, 10])
SEVEN_CHORD = ('7 Chord', [0, 2, 4, 6])

SCALES = [MAJOR_SCALE, MINOR_SCALE]


def get_notes_in_key(key='C', scale=MAJOR_SCALE):
    all_notes = list(FREQ_TABLE.keys())
    all_notes_no_num = [note[:-1] for note in all_notes]
    first_position = all_notes_no_num.index(key)
    degrees = scale[1]
    notes_in_key = []
    i = 0
    while True:
        for degree in degrees:
            index = first_position + degree + i
            if index < len(all_notes):
                notes_in_key.append(all_notes[index])
            else:
                return notes_in_key
        i += 12


def generate_melody_notes(number_of_notes):
    # add first note
    notes_in_melody = [r.sample(notes_in_key[20:40], 1)[0]]
    for i in range(number_of_notes - 1):
        last_node_index = notes_in_key.index(notes_in_melody[i])
        new_note = r.sample(notes_in_key[max(last_node_index - 5, 0):min(last_node_index + 5, len(notes_in_key))], 1)[0]
        notes_in_melody.append(new_note)
    return notes_in_melody


def play_melody(notes_to_play, positions):
    # initialize audio stuff
    p = pyaudio.PyAudio()
    volume = 0.5  # range [0.0, 1.0]
    fs = 44100  # sampling rate, Hz, must be integer
    duration = 1.0  # in seconds, may be float
    frequency = 440

    i = 0
    note_num = 0
    while i < 16:
        if i in positions:
            note_to_play = notes_to_play[note_num]
            frequency = FREQ_TABLE[note_to_play]
            volume = 0.5
            note_num += 1
        else:
            volume = 0
        # for paFloat32 sample values must be in range [-1.0, 1.0]
        # generate samples, note conversion to float32 array
        samples = (np.sin(2 * np.pi * np.arange(fs * duration) * frequency / fs)).astype(np.float32)

        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=fs,
                        output=True)

        # play. May repeat with different volume values (if done interactively)
        stream.write(volume * samples)
        i += 1

    # End audio stuff
    stream.stop_stream()
    stream.close()
    p.terminate()


def play_chords(chords_to_play, positions):
    # initialize audio stuff
    p = pyaudio.PyAudio()
    volume = 0.5  # range [0.0, 1.0]
    fs = 44100  # sampling rate, Hz, must be integer
    duration = 1.0  # in seconds, may be float
    frequency = 440

    i = 0
    note_num = 0
    while i < 16:
        if i in positions:
            chord_to_play = chords_to_play[note_num]
            frequencies = [FREQ_TABLE[note] for note in chord_to_play]
            volume = 0.5
            note_num += 1
        else:
            volume = 0
        # for paFloat32 sample values must be in range [-1.0, 1.0]
        # generate samples, note conversion to float32 array
        samples = sum([(np.sin(2 * np.pi * np.arange(fs * duration) * frequency / fs)).astype(np.float32)
                       for frequency in frequencies])

        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=fs,
                        output=True)

        # play. May repeat with different volume values (if done interactively)
        stream.write(volume * samples)
        i += 1

    # End audio stuff
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == '__main__':
    # Generate notes

    key = r.sample(KEYS, 1)[0]
    scale = r.sample(SCALES, 1)[0]

    # Pick number of notes in melody
    number_of_notes = r.randint(5, 16)
    # Pick location of notes
    note_position_range = range(16)
    note_positions = sorted(r.sample(note_position_range, number_of_notes))

    # Get all notes in the key from the frequency table, return a new table
    notes_in_key = get_notes_in_key(key, scale)

    # generate melody
    notes_in_melody = generate_melody_notes(number_of_notes)

    print('Key:', key, scale)
    print(notes_in_melody)
    print(note_positions)


    play_melody(notes_in_melody, note_positions)