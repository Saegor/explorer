#!/usr/bin/env python3

from math import log2
import curses
import numpy
import pyaudio
import rtmidi

#from scipy import interpolate #


def main(stdscr):

    curses.curs_set(False)
    stdscr.nodelay(True)

    # audio in
    audio_format = pyaudio.paInt16
    rate = 48000
    device = 7
    chunk = 2048
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format = audio_format,
        channels = 1,
        rate = rate,
        input = True,
#        input_device_index = device,
        frames_per_buffer = chunk
    )

    # midi out
    midiout = rtmidi.MidiOut()
    midiout.open_port(1)

    note_byte = -1

    width = pyaudio.get_sample_size(audio_format)
    freqs = numpy.fft.fftfreq(chunk * width)

    run = True
    while run:

        # draw + input routine
        stdscr.refresh()
        ch = stdscr.getch()
        stdscr.erase()

        if ch == ord('q') :
            run = False

        # fft
        buffer_data = stream.read(chunk, exception_on_overflow = False)
        data = numpy.frombuffer(buffer_data, dtype = numpy.int16)
        fft_data = numpy.fft.fft(data)
        idx = numpy.argmax(numpy.abs(fft_data))
        freq_adim = freqs[idx]
        freq = abs(freq_adim * rate)

        stdscr.addstr(1, 2, 'FREQ ' + str(freq))

        # store last note
        last_note_byte = note_byte
        note_byte = -1

        # freq to midi
        if freq > 0:
            note_float = (12 * log2(freq) - 36.376)
            stdscr.addstr(2, 2, 'MIDI ' + str(note_float))

            # midi float to midi byte
            if note_float > 48:
                note_byte = int(round(note_float))
                step = note_byte % 12
                stdscr.addstr(3, 2, 'STEP ' + str(step))

        # play/stop midi notes
        if note_byte != last_note_byte:
            # note_off
            if last_note_byte != -1:
                midiout.send_message([0x80, last_note_byte, 0])
            # note_on
            if note_byte != -1:
                midiout.send_message([0x90, note_byte, 64])

    stream.close()
    audio.terminate()

curses.wrapper(main)
