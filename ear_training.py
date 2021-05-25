import random as r
import pyaudio
import numpy as np

FREQ_TABLE = {}
with open('freq_table.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        note, freq, _ = line.split()
        if len(note) > 3:
            note = note.split('/')[1]
        FREQ_TABLE[note] = float(freq)

interval_to_name = {
    0: "Same/Octave",
    1: "Minor 2nd",
    2: "Major 2nd",
    3: "Minor 3rd",
    4: "Major 3rd",
    5: "Perfect 4th",
    6: "Tritone",
    7: "Perfect 5th",
    8: "Minor 6th",
    9: "Major 6th",
    10: "Minor 7th",
    11: "Major 7th",
}
# r.seed(1)


def play_notes(low, high, wholetone=False, remove_C=False, freq_list=list(FREQ_TABLE.items())):
    # initialize audio stuff
    p = pyaudio.PyAudio()
    volume = 0.5  # range [0.0, 1.0]
    fs = 44100  # sampling rate, Hz, must be integer
    duration = 5.0  # in seconds, may be float

    if remove_C:
        freq_list = [(k, v) for k,v in FREQ_TABLE.items() if 'C' not in k]
    if wholetone:
        freq_list = [freq_list[i] for i in range(len(freq_list)) if i % 2 == (r.random() < 1)]

    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    while True:
        key, frequency = r.choice(freq_list)
        if frequency < low or frequency > high:
            continue

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        # generate samples, note conversion to float32 array
        samples = (np.sin(2 * np.pi * np.arange(fs * duration) * frequency / fs)).astype(np.float32)

        # play. May repeat with different volume values (if done interactively)
        stream.write(volume * samples)
        print(key)
        for i in range(2):
            stream.write(0 * samples)

    # End audio stuff
    stream.stop_stream()
    stream.close()
    p.terminate()


def play_interval(low, high, from_note='', freq_list=list(FREQ_TABLE.items()),
                  low_first=False, max_interval=12, min_interval=-1, together=False):
    # initialize audio stuff
    p = pyaudio.PyAudio()
    volume = 0.5  # range [0.0, 1.0]
    fs = 44100  # sampling rate, Hz, must be integer
    duration = 4.0  # in seconds, may be float

    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    while True:
        if from_note:
            first_key = from_note
            first_frequency = FREQ_TABLE[first_key]
        else:
            first_key, first_frequency = r.choice(freq_list)
        second_key, second_frequency = r.choice(freq_list)
        # Get indices
        first_index = freq_list.index((first_key, first_frequency))
        second_index = freq_list.index((second_key, second_frequency))
        diff = abs(second_index-first_index)
        # Make sure it's in specified range
        if first_frequency < low or first_frequency > high or second_frequency < low or second_frequency > high:
            continue
        # Make sure the low note is first if needed
        if low_first and second_index <= first_index:
            continue
        # Make sure the interval is within limits
        if diff > max_interval or diff < min_interval:
            continue

        samples_1 = (np.sin(2 * np.pi * np.arange(fs * duration) * first_frequency / fs)).astype(np.float32)
        samples_2 = (np.sin(2 * np.pi * np.arange(fs * duration) * second_frequency / fs)).astype(np.float32)
        print(first_key)
        print(second_key)
        print('\n\n\n')
        print(interval_to_name[diff%12])
        # play. May repeat with different volume values (if done interactively)
        if together:
            stream.write(volume * (samples_1+0.7*samples_2))
            stream.write(volume * (samples_1+0.7*samples_2))
        else:
            stream.write(volume * samples_1)
            stream.write(volume * samples_2)


        # Silence
        for i in range(4):
            stream.write(0 * samples_1)

    # End audio stuff
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == '__main__':

    flats = [(k, v) for k, v in FREQ_TABLE.items() if 'b' in k]
    # to learn intervals for relative pitch
    # play_interval(250, 700, from_note='G4', low_first=True, max_interval=4, min_interval=1)
    # play_interval(250, 700, low_first=True, max_interval=4, min_interval=1)
    # play_interval(250, 700, from_note='D4', low_first=True, max_interval=7, min_interval=4)
    # play_interval(250, 700, low_first=True, max_interval=7, min_interval=4)
    # play_interval(250, 700, from_note='G4', low_first=True, min_interval=7, max_interval=9)
    # play_interval(250, 700, low_first=True, min_interval=7, max_interval=9)
    # play_interval(250, 750, from_note='G4', low_first=True, min_interval=8)
    # play_interval(250, 750, low_first=True, min_interval=8)

    # play_interval(250, 750, from_note='G4', low_first=True)
    # play_interval(250, 700, low_first=True)

    # play_interval(250, 700, from_note='Eb4', low_first=True, min_interval=9, max_interval=11)
    # play_interval(250, 700, from_note='Eb4', low_first=True, min_interval=7, max_interval=9)
    # play_interval(250, 700, from_note='C4', low_first=True, min_interval=5, max_interval=9)
    # play_interval(250, 700, from_note='Eb4', low_first=True, min_interval=5, max_interval=7)
    play_interval(250, 700, from_note='C4')
    # play_interval(250, 700, low_first=True)
    #
    # to memorize specific notes for perfect pitch
    # play_notes(250, 700)
