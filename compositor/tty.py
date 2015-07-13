import fcntl
import os
import sys

TTY_MAJOR = 4

KDGKBMODE = 0x4b44
KDSKBMODE = 0x4b45
KDSETMODE = 0x4b3a
K_OFF = 0x04
KD_TEXT = 0x00
KD_GRAPHICS = 0x01


class TTY(object):
    def __init__(self):
        self._prev_mode = None

        tty = sys.stdin.fileno()
        buf = os.fstat(tty)

        if os.major(buf.st_rdev) != TTY_MAJOR or os.minor(buf.st_rdev) == 0:
            raise RuntimeError("qtile-launch must be run from a virtual terminal")

        self.tty = tty

    def setup(self):
        buf = bytearray(1)
        fcntl.ioctl(self.tty, KDGKBMODE, buf)

        if fcntl.ioctl(self.tty, KDSKBMODE, K_OFF):
            with open('/home/sean/log', 'a') as f:
                f.write('failed set kb\n')
            raise RuntimeError("failed to set K_OFF keyboard mode")
        self._prev_mode = buf[0]

        if fcntl.ioctl(self.tty, KDSETMODE, KD_GRAPHICS):
            with open('/home/sean/log', 'a') as f:
                f.write('failed set graphics\n')
            raise RuntimeError("unable to set KD_GRAPHICS on tty")

    def finalize(self):
        # reset keyboard
        if self._prev_mode and fcntl.ioctl(self.tty, KDSKBMODE, self._prev_mode):
            with open('/home/sean/log', 'a') as f:
                f.write('failed reset keyboard\n')
            print("Failed to reset keyboard mode", file=sys.stderr)
        self._prev_mode = None

        # reset graphics
        if fcntl.ioctl(self.tty, KDSETMODE, KD_TEXT):
            with open('/home/sean/log', 'a') as f:
                f.write('failed reset graphics\n')
