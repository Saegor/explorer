#!/usr/bin/env python3

import time
import curses
import rtmidi


class Step():

    status = 'off'
    timer = 0

    def __init__(self, step):
        self.glyph = hex(step)[2:].upper()


def main(stdscr):

    curses.curs_set(False)
    stdscr.nodelay(True)

    # colors
    for i in range(8):
        curses.init_pair(8 if i == 0 else i, i, 0)

    # midi in
    midiin = rtmidi.MidiIn(name = 'Analyser')
    midiin.open_virtual_port('Virtual 0')

    # list of notes
    book = []
    for step in range(12):
        book.append(Step(step))

    # loop
    run = True
    while run:

        # draw + input routine
        stdscr.refresh()
        key_pressed = stdscr.getch()
        stdscr.erase()

        time.sleep(.004)
        msg = midiin.get_message()

        if msg:
            (status, note, vel), delta = msg
            step = book[note % 12]

            # note_off
            if  status == 0x80:
                step.status = 'release'
                step.timer = 256

            # note_on
            elif  status == 0x90:
                step.status = 'on'


        # matrix
        for y in range(8):
            for x in range(12):

                step = book[(x * 7 - y * 4) % 12]

                if step.status == 'on':
                    color = curses.color_pair(3) | curses.A_BOLD

                elif step.status == 'release':
                    color = curses.color_pair(3)

                elif step.glyph in ("0", "2", "4", "5", "7", "9", "B"):
                    color = curses.color_pair(7)

                else:
                    color = curses.color_pair(8) | curses.A_BOLD

                stdscr.addstr(4 + 2 * y, 8 + 4 * x, step.glyph, color)

        # auto release
        for step in book:
            if step.status == 'release':
                step.timer -= 1
                if step.timer < 0:
                    step.status = 'off'

        # quit if 'q' pressed
        if key_pressed == ord('q'):
            run = False

    del midiin

curses.wrapper(main)
