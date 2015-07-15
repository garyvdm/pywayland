from cffi import FFI
import fcntl
import os
import signal
import sys

TTY_MAJOR = 4

KDGKBMODE = 0x4b44
KDSKBMODE = 0x4b45
KDSETMODE = 0x4b3a
KDGETMODE = 0x4b3b

K_OFF = 0x04
KD_GRAPHICS = 0x01

VT_SETMODE = 0x5602
VT_AUTO = b'\x00'
VT_PROCESS = b'\x01'

ffi = FFI()
ffi.cdef("""
struct vt_mode {
    char mode;          /* vt mode */
    char waitv;         /* if set, hang on writes if not active */
    short relsig;       /* signal to raise on release req */
    short acqsig;       /* signal to raise on acquisition */
    short frsig;        /* unused (set to 0) */
};
""")


def handle_chld(signum, frame):
    pass


def handle_usr1(signum, frame):
    pass


def handle_usr2(signum, frame):
    pass


class Launcher(object):
    def __init__(self):
        self.tty = None

        self._kbmode = None
        self._mode = None

    def __enter__(self):
        self.setup()

    def __exit__(self, exception_type, exception_value, traceback):
        self.finalize()

    def setup(self, tty=None):
        if tty is None:
            tty = sys.stdin.fileno()

        self.setup_signals()
        self.setup_tty(tty)

    def finalize(self):
        self.finalize_signals()
        self.finalize_tty()

    def setup_signals(self):
        signal.signal(signal.SIGCHLD, handle_chld)

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
