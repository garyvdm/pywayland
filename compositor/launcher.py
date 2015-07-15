from ._ffi_launcher import ffi, lib
import fcntl
import os
import signal
import sys

TTY_MAJOR = lib.TTY_MAJOR

KDGKBMODE = lib.KDGKBMODE
KDSKBMODE = lib.KDSKBMODE
KDSETMODE = lib.KDSETMODE
KDGETMODE = lib.KDGETMODE

K_OFF = lib.K_OFF
KD_GRAPHICS = lib.KD_GRAPHICS

VT_SETMODE = lib.VT_SETMODE
VT_AUTO = bytes(bytearray([lib.VT_AUTO]))
VT_PROCESS = bytes(bytearray([lib.VT_PROCESS]))
VT_ACKACQ = bytes(bytearray([lib.VT_ACKACQ]))

VT_RELDISP = lib.VT_RELDISP


def _mkhandler(self, func):
    return lambda n, s: func(self, n, s)


class Launcher(object):
    def __init__(self):
        self.tty = None

        self._kbmode = None
        self._mode = None

    def __enter__(self):
        self.setup()

    def __exit__(self, exception_type, exception_value, traceback):
        self.finalize()

    def handle_chld(self, signum, stack):
        _, status = os.wait()
        print('Server exited with status {:d}'.format(os.WEXITSTATUS(status)), file=sys.stderr)
        # TODO: figure out how to run/kill the launcher... asyncio event loop maybe? or wayland event loop?

    def handle_usr1(self, signum, stack):
        # TODO: send deactivate...
        fnctl.ioctl(self.tty, VT_RELDISP, 1);

    def handle_usr2(self, signum, stack):
        fnctl.ioctl(self.tty, VT_RELDISP, VT_ACKACQ)
        # TODO: send activate...

    def setup(self, tty=None):
        if tty is None:
            tty = sys.stdin.fileno()

        self.setup_signals()
        self.setup_tty(tty)

    def finalize(self):
        self.finalize_signals()
        self.finalize_tty()

    def setup_signals(self):
        signal.signal(signal.SIGCHLD, _mkhandler(self, Launcher.handle_chld))

    def finalize_signals(self):
        pass

    def setup_tty(self, tty):
        stat = os.fstat(tty)

        if os.major(stat.st_rdev) != TTY_MAJOR or os.minor(stat.st_rdev) == 0:
            raise RuntimeError("qtile-launch must be run from a virtual terminal")
        self.tty = tty

        buf = bytearray(1)

        if fcntl.ioctl(tty, KDGKBMODE, buf):
            raise RuntimeError("failed to get KDGKBMODE")

        if fcntl.ioctl(tty, KDSKBMODE, K_OFF):
            raise RuntimeError("failed to set K_OFF keyboard mode")
        self._kbmode = buf[0]

        if fcntl.ioctl(tty, KDGETMODE, buf):
            raise RuntimeError("failed to get text/graphics mode")

        if fcntl.ioctl(tty, KDSETMODE, KD_GRAPHICS):
            raise RuntimeError("unable to set KD_GRAPHICS on tty")
        self._mode = buf[0]

        mode = ffi.new('struct vt_mode *')
        mode.mode = VT_PROCESS
        mode.relsig = signal.SIGUSR1
        mode.acqsig = signal.SIGUSR2
        if fcntl.ioctl(tty, VT_SETMODE, bytes(ffi.buffer(mode))) == -1:
            raise RuntimeError("unable to set VT mode")

    def finalize_tty(self):
        # reset VT mode
        mode = ffi.new('struct vt_mode *')
        mode.mode = VT_AUTO
        if fcntl.ioctl(self.tty, VT_SETMODE, bytes(ffi.buffer(mode))) == -1:
            print("Failed to reset VT mode", file=sys.stderr)

        # reset keyboard
        if self._kbmode is not None and fcntl.ioctl(self.tty, KDSKBMODE, self._kbmode):
            print("Failed to reset keyboard mode", file=sys.stderr)
        self._kbmode = None

        # reset graphics
        if self._mode is not None and fcntl.ioctl(self.tty, KDSETMODE, self._mode):
            print("Failed to reset graphics", file=sys.stderr)
        self._mode = None

        self.tty = None
